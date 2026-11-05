---
title: Run a test suite under a lease
summary: Reserve cores and memory on the fleet pool for one command, wait for a host to take the lease, and run the command with the lease's size in its environment.
audience: team-admin
commands:
  - fleet run --cores --memory --bound
  - fleet queue
  - fleet why
  - fleet cancel
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Run a test suite under a lease

This cookbook runs `make test` under a lease, so several people's test runs share a host without starving each other. A lease reserves cores and memory on a pool host for one command and ends with it. [The fleet scheduler guide](../../docs/guides/fleet-scheduler.md) runs the pool, and [the scheduler concept page](../../docs/concepts/fleet-scheduler.md) explains how a lease is admitted.

## Before you start

- The pool works and this computer is one of its hosts. `dockingbird fleet queue` lists it. [The team fleet guide](../../docs/guides/team-fleet.md) sets the pool up.
- Your org login names a project for leases. The owner's login needs `--project` on `dockingbird org login`, or the command ends with `FLEET_LEASE_NO_PROJECT`.
- Your role is a member of that project, or the admin. A project's role runs and controls its own workloads only.
- A command that uses what the lease gives it. Here that is `make test`, with its parallelism read from the environment.

## 1. Run the suite under a lease

Give the lease its cores, its memory and a bound, then the command after `--`. The command runs on the computer where you typed `fleet run`, so name this computer's pool host with `--hosts` if the pool has several. `fleet run` records the lease, waits for a host to take it, reads the host's row every 30 seconds, and runs the command in a process group of its own.

```bash
dockingbird fleet run --cores 4 --memory 8g --bound 30m --hosts lab -- make test
```

The command finds its lease in two environment variables, `FLEET_LEASE_CORES` and `FLEET_LEASE_HOST`. Use them to size the test runner.

```bash
dockingbird fleet run --cores 4 --memory 8g --bound 30m --hosts lab -- sh -c 'pytest -n "$FLEET_LEASE_CORES"'
```

The step is done when the command ends. `fleet run` then ends with the command's own exit status, and the lease ends with it. A suite that passed ends 0, and a failing suite ends with its own non-zero status.

## 2. Watch the lease wait

Until a host takes the lease, your command has not started, and the terminal shows nothing. Open a second terminal. There, `fleet queue` lists the lease among the workloads with its kind, its state and the command it will run, and `fleet why ID` names the first thing that keeps the lease off each host.

```bash
dockingbird fleet queue
dockingbird fleet why ID
```

```text
{id} {project} {kind} {priority} {state}, {age} old, needs {need_millicores} millicores, {need_mib} MiB, {agents} agents
{host}: {hold}, has {have} millicores, needs {need}
```

## 3. Bound the run

At its `--bound` the command is interrupted, then stopped 15 seconds later if it has not ended, and `fleet run` ends 124. The step is done when you see this line and the exit status.

```text
lease bound reached; CMD interrupted
```

Durations name their unit, such as `90s`, `20m` or `2h`, and are at most a day.

## 4. Limit the wait

A lease that no host takes within `--wait` is given up, the command never runs and `fleet run` ends 1. The wait is 30 minutes unless you set it.

```bash
dockingbird fleet run --cores 4 --memory 8g --bound 30m --hosts lab --wait 10m -- make test
```

```text
lease not admitted within {wait}: {blocked_by}
```

`--kind picker --exclusive` also keeps a second lease of that kind off the host, so two runs of the same suite never share it.

## 5. Cancel a lease

A lease takes `cancel` and no other control. Cancelling a running lease interrupts its command the same way a bound does. Stopping `fleet run` with Control-C, or a SIGTERM from a service manager, interrupts the command's process group too, and the lease ends with it.

```bash
dockingbird fleet cancel ID
```

```text
{id} {state}
```

## What the lease bounds

| Computer | What the lease limits |
|---|---|
| Linux | the command runs inside a transient scope of your own systemd user manager whose `CPUQuota` and `MemoryMax` are the lease's; a kill at `MemoryMax` is the command's own status, 137 |
| Mac | nothing bounds the command, and a lease counts cores only |

When the store does not answer, `fleet run` says so on one line and runs the command without a lease, as checks ran before the scheduler existed. When the store turns the login down, `fleet run` ends 78 with `FLEET_DB_REFUSED` and never runs the command. A store that is down prints this line first.

```text
fleet: no answer from the database at {host} for {role} within {seconds} s: {error}; running without a lease
```

## When it fails

Seven ids belong to this page. Read the one your command printed.

- [`FLEET_RUN_NOT_ADMITTED`](../../docs/troubleshooting.md#fleet_run_not_admitted) appears when no host took the lease within `--wait`. The line names what held each host off, and the command never ran.
- [`FLEET_RUN_ENDED`](../../docs/troubleshooting.md#fleet_run_ended) appears when the lease ended before a host took it, cancelled or past its wait.
- [`FLEET_RUN_BOUND`](../../docs/troubleshooting.md#fleet_run_bound) shows that the command was still running at `--bound`, so `fleet run` ended 124.
- [`FLEET_RUN_CANCELLED`](../../docs/troubleshooting.md#fleet_run_cancelled) shows a cancel during the run. `fleet run` ends with the command's own exit status.
- [`FLEET_RUN_NO_LEASE`](../../docs/troubleshooting.md#fleet_run_no_lease) shows that the store did not answer, so the command ran with no reservation.
- [`FLEET_RUN_NO_SCOPE`](../../docs/troubleshooting.md#fleet_run_no_scope) comes up on Linux when `systemd-run` is missing. The command runs under its lease with no ceiling.
- [`FLEET_LEASE_NO_PROJECT`](../../docs/troubleshooting.md#fleet_lease_no_project) comes from the owner's login when it names no project. Log in again with `--project`.
