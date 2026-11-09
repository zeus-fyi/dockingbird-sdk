---
title: Run work on the fleet pool
summary: Enrol hosts in the pool, read the queue, see why a workload waits, control it, run a check under a lease and move the pool to a release.
audience: team-admin
commands:
  - fleet hosts add --os --cores --memory --line --rank --agent-cap --power
  - fleet hosts policy --lease-headroom
  - fleet hosts drain
  - fleet hosts undrain
  - fleet hosts remove
  - fleet queue
  - fleet why
  - fleet ledger
  - fleet hold
  - fleet release
  - fleet pause
  - fleet resume
  - fleet cancel
  - fleet done
  - fleet set --priority
  - fleet run --cores --memory --bound --priority
  - fleet update --release --host
  - fleet admitter --metrics-port
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Run work on the fleet pool

This guide for teams runs the pool once [the team fleet guide](team-fleet.md) is done. You enrol hosts, read the queue and control each workload. You also run a check under a lease and move the pool to a new release. Submitting a swarm is on [the swarms guide](swarms.md), and the model behind it is on [the fleet scheduler concept page](../concepts/fleet-scheduler.md). The gate lines you set here also decide whether a direct start on a pool host is refused, which [the host load protection guide](host-load-protection.md) explains.

## Before you start

- The store and your org login exist. `dockingbird org status` ends with `Connected as {role}.` when they do.
- Each host runs a worker, and one host runs the admitter. `dockingbird fleet hosts` lists both.
- The pool commands need the `fleet_admin` role. A project's role queues and controls its own workloads only.
- The top help screen does not list `fleet`. `dockingbird fleet -h` shows every action.
- The admitter serves the pool's metrics at the org pointer's database host on port 9107. `dockingbird fleet admitter --metrics-port N` picks another port, and 0 asks for a free one. When the address is in use or not yet this computer's, the admitter says `FLEET_METRICS_UNSERVED` once and keeps admitting, tries the address again before each pass, and says `FLEET_METRICS_SERVING` once it serves.

## 1. Enrol a host

The host must already be in your `hosts.toml` under the name the pool will use. The admin enrols it with its reservable share and its gate lines. Every line its OS requires is needed. This host is a 60-core Linux VM that the admitter starts when work waits for it.

```bash
dockingbird fleet hosts add cloud --os linux --cores 60 --memory 230g --line idle_millicores=4000,8000 --line free_mib=16384,32768 --line psi_io_full=1500,1200 --agent-cap 10 --rank 2 --power gcloud
dockingbird fleet queue --host cloud
```

A line is `FIGURE=BOUND,CLEAR`. `--agent-cap N` is the most agents one home on the host runs, 24 at most, which is also the default. `--lease-headroom CORES,SIZE` keeps room for leases, `--no-swarms` keeps swarms off the host, and `--rank N` sets its place in the order, 1 first. The host's line appears once its worker has published a sample, and says `no sample yet` before that. The same lines guard every agent start on the host, yours included: a start is refused while one reads red, as [the host load protection guide](host-load-protection.md) says.

```text
cloud: {liveness}, {policy}, sample {age} old
  cores: {reserved_millicores} of {millicores} millicores reserved, {foreign_millicores} foreign
  memory: {reserved_mib} of {mib} MiB reserved, {foreign_mib} foreign
  lines: {lines}
```

## 2. Change, drain and remove a host

`policy` changes whether a host takes swarms, its rank, its agent cap, its lines and its lease headroom. `--lease-headroom CORES,SIZE` is the part of the host's share that swarms may not reserve into, so a check run finds room. A headroom above the share is refused, as `hosts add` refuses it. A free-disk line is given once the host's sample shows the figure, because a line on a figure the sample lacks is red. Drain keeps new work off a host, undrain lets it back, and remove takes it out of the pool. Remove is refused while a workload is reserved on the host or pinned to it.

```bash
dockingbird fleet hosts policy cloud --takes-swarms no
dockingbird fleet hosts policy cloud --rank 1 --line free_disk_mib=45056,90112
dockingbird fleet hosts policy cloud --lease-headroom 4,16g
dockingbird fleet hosts drain cloud
dockingbird fleet hosts undrain cloud
dockingbird fleet hosts remove cloud
```

`policy` prints the host's new policy. The other three print `{host} {liveness}`, which reads `draining` after a drain and `removed` after a removal.

```text
cloud: {policy}, agent cap {cap}, lines {lines}
```

## 3. Read the queue

`fleet queue` shows the pool, then each workload not yet ended, in the order the scheduler admits them. A host line gives its sample's age, the cores and memory reserved against what it may reserve, the load the fleet did not start, and its gate lines with their colours. A workload line gives its project, kind, priority, state, age and what it needs, then where it is or what holds it.

```bash
dockingbird fleet queue
dockingbird fleet queue --metrics
```

`--metrics` prints the queue's numbers in the Prometheus text format instead. It takes neither `--json` nor `--host`. An empty pool prints this line.

```text
The pool has no host and the queue no workload.
```

## 4. See why a workload waits

`fleet why ID` names, for each host, the first thing that keeps a waiting workload off it, with the figures. For a running swarm it names the agents still waiting to start and what holds them. `fleet ledger ID` lists a swarm's commits, newest first, with who approved each and the test result. When a hold on many hosts is too long for the store's 4096-byte record, `fleet why` says how many hosts the record left out.

```bash
dockingbird fleet why ID
dockingbird fleet ledger ID
```

```text
cloud: {hold}, {figure} {reading}, bound {line_bound}
{sha} by {author}: approved by {reviewer} at {approved_at}; tested {result} by {tester} at {tested_at}
```

A swarm held for a missing checkout names the home and the host, and ends `fleet release ID` as the next step. Link the checkout, then release it. A release starts a new attempt that first fetches and fast-forwards the worker's own clone, so a fix you pushed reaches it.

A swarm with a role whose `[role.fallback]` says `placement = "require-login"` is held off each host whose home is not signed in to the role's tool and its fallback tool, as of the host's last sample, and `fleet why ID` names the hold `no_fallback_login`. Sign in in that home with `dockingbird login claude` or `dockingbird login codex`. Each pass of the admitter judges the hold again.

## 5. Control a workload

Each control takes the workload's id. `hold` keeps a waiting workload out of every pass until `release`. `pause`, `resume`, `cancel` and `done` act on a running team, and each agent stops after its running turn, never during it. `set` changes a priority in any state but an ended one and keeps the workload's age.

```bash
dockingbird fleet hold ID --reason "wait for the release branch"
dockingbird fleet release ID
dockingbird fleet pause ID
dockingbird fleet resume ID
dockingbird fleet cancel ID
dockingbird fleet done ID
dockingbird fleet set ID --priority P0
```

Each control prints the state it entered and the agents still working. `set` prints the new priority.

```text
{id} {state}; still working: {names}
{id} priority P0
```

A lease takes `cancel` only. An agent that is idle after it was asked to stop or retire, and has not stopped 10 minutes later, is stopped by name once, and the worker logs one warning line. An agent with a turn running, or whose status is unread, is never stopped this way. `done` ends a running team after each agent's turn. It is refused for a swarm that was admitted or interrupted before any agent started, and `cancel` applies there.

## 6. Run a check under a lease

A lease reserves cores and memory for one command. `fleet run` records the lease, waits for a host to take it, then runs the command here in a process group of its own, with `FLEET_LEASE_CORES` and `FLEET_LEASE_HOST` in its environment. The lease ends with the command.

```bash
dockingbird fleet run --cores 4 --memory 8g --bound 30m -- make test
dockingbird fleet run --cores 2 --memory 4g --bound 20m --hosts cloud --wait 10m --kind picker --exclusive -- make lint
dockingbird fleet run --cores 4 --memory 8g --bound 30m --priority P1 -- make test
```

The command's own exit status is the result. At the bound the command is interrupted, stopped 15 seconds later, and `fleet run` ends 124. `fleet cancel ID` of a running lease interrupts it the same way. A lease not taken within `--wait`, 30 minutes by default, is given up and ends 1. `--priority P` records the lease with that priority, P0 to P3, the words of `fleet set`, and a lease without it is P2. While it waits, `fleet run` reads its lease every 5 seconds, so a one-minute check starts within seconds of its admission. An agent start inside a lease the host runs is counted by the start guard and never refused by it. Durations name their unit, such as `90s`, `20m` or `2h`, up to a day.

On Linux the command runs inside a transient scope of your own systemd user manager, so its cores and memory are the lease's. On a Mac nothing bounds the command, and a lease there counts cores only. When the store does not answer, `fleet run` runs the command without a lease and says so on one line. When the store turns the login down, it ends 78 and runs nothing. The owner's role has no project of its own, so its leases count against the `--project` of its `org login`.

```text
fleet: no answer from the database at {host} for {role} within {seconds} s: {error}; running without a lease
```

## Update the pool

`fleet update` moves every pool host to one release, in rank order, or the one host `--host` names. It is the admin's alone: any other login ends 77. The release is the one `--release` names, else this program's own. Run it from a computer whose `hosts.toml` has a `repoint` line for each host.

```bash
dockingbird fleet update --release 0.15.3
dockingbird fleet update --release 0.15.3 --host cloud
```

Before anything runs, each host needs a live worker and a `repoint` line, or no host changes and the command ends 2. A host whose worker already runs the release is skipped. Then, host by host, the release is installed, each home the worker serves is updated from it, `installs/current` moves and the services restart, and the command waits for the worker to report the release. Each step is printed as it starts. The waits are bounded: the install 15 minutes, a home's update about an hour, each link move and restart 40 seconds, and the worker's report 10 minutes.

```text
cloud: installing Dockingbird 0.15.3 ...
cloud: updating {home} to Dockingbird 0.15.3 ...
cloud: moving its Dockingbird services to 0.15.3 and restarting them ...
cloud: waiting for its worker to run Dockingbird 0.15.3 (at most {bound}) ...
Dockingbird 0.15.3 runs on cloud.
```

A step that fails stops the command with exit 1 and names the host. The hosts after it stay as they are and the hosts done stay done, so fix the cause and run the same command again. A host's homes finish moving on their own, and `dockingbird --home NAME status` shows how far each got.

## When it fails

### Queue, controls and hosts

These ids come from the queue, the controls and host changes. Each line says what the id means and what to do.

- [`FLEET_NOT_FOUND`](../troubleshooting.md#fleet_not_found) means your role sees no such workload or host. `fleet queue` lists what it does see.
- [`FLEET_NOT_NOW`](../troubleshooting.md#fleet_not_now) means the control does not apply in the workload's present state. The line names the states where it does.
- [`FLEET_HOST_STILL_HAS`](../troubleshooting.md#fleet_host_still_has) blocks `hosts remove` while a workload is reserved on the host or pinned to it. Cancel it or let it end.
- [`FLEET_REFUSED`](../troubleshooting.md#fleet_refused) means a value broke a rule, such as a gate line or an agent cap. Fix the value and run the command again.
- [`FLEET_OPTION_NEEDED`](../troubleshooting.md#fleet_option_needed) means an option is missing. `hosts add` needs `--os`, `--cores`, `--memory` and `--line`.
- [`FLEET_NOT_PERMITTED`](../troubleshooting.md#fleet_not_permitted) means your role may not change hosts, lines or policies. Only the owner may.
- [`FLEET_NOT_A_MEMBER`](../troubleshooting.md#fleet_not_a_member) means you are not a member of the project. An admin runs `org members add`.
- [`FLEET_NO_CHECKOUT`](../troubleshooting.md#fleet_no_checkout) holds a swarm whose home links no usable checkout. Fix the link, then run `fleet release ID`.

### Leases and updates

The rest come from leases, `fleet run`, the admitter's metrics and `fleet update`. Each line says what the id means and what to do.

- [`FLEET_LEASE_CANCEL_ONLY`](../troubleshooting.md#fleet_lease_cancel_only) says a lease takes `cancel` and no other control.
- [`FLEET_DONE_NEVER_STARTED`](../troubleshooting.md#fleet_done_never_started) says no agent of the swarm ever started, so `cancel` applies in place of `done`.
- [`FLEET_METRICS_UNSERVED`](../troubleshooting.md#fleet_metrics_unserved) says the admitter could not open its metrics address. Admission goes on. Free the port or wait for the address, and nothing needs a restart. [`FLEET_METRICS_SERVING`](../troubleshooting.md#fleet_metrics_serving) says it opened it.
- [`FLEET_RUN_NOT_ADMITTED`](../troubleshooting.md#fleet_run_not_admitted) means no host took the lease within `--wait`. The line names what held each host off.
- [`FLEET_RUN_NO_LEASE`](../troubleshooting.md#fleet_run_no_lease) means the store did not answer, so the command ran with no lease at all.
- [`FLEET_LEASE_NO_PROJECT`](../troubleshooting.md#fleet_lease_no_project) means the owner's login names no project. Log in again with `--project`.
- [`FLEET_UPDATE_NO_REPOINT`](../troubleshooting.md#fleet_update_no_repoint) means a host has no `repoint` line, so no host was updated.
- [`FLEET_UPDATE_NO_WORKER`](../troubleshooting.md#fleet_update_no_worker) means a host's worker has not reported in time. Start it, then go on.
- [`FLEET_UPDATE_NO_RELEASE`](../troubleshooting.md#fleet_update_no_release) means the source lists no such release. The command ends 2.
- [`FLEET_UPDATE_SOURCE_UNREAD`](../troubleshooting.md#fleet_update_source_unread) means git here cannot read the source. Check the network, then run it again.
- [`FLEET_UPDATE_HOST_FAILED`](../troubleshooting.md#fleet_update_host_failed) means a step failed on one host. Fix the cause and run the same command again.
- [`FLEET_UPDATE_HOST_TIMEOUT`](../troubleshooting.md#fleet_update_host_timeout) means a worker did not run the release in time. Run the command again once it does.
