---
title: A team fleet on PostgreSQL
summary: Share a pool of two hosts through an organisation store, log in with org login, run a worker on each host and the admitter on one, queue a swarm and update the pool.
audience: team-admin
commands:
  - fleet hosts set
  - org login
  - org create
  - fleet hosts add
  - fleet worker --host
  - fleet admitter
  - fleet submit
  - fleet queue
  - fleet why
  - fleet update
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# A team fleet: a pool of two hosts

A team shares a fleet pool: a PostgreSQL database that the fleet scheduler queues swarms in, and the hosts it places them on. Here the pool holds two hosts, `lab`, a Mac, and `cloud`, a Compute Engine VM. Each member submits [a swarm definition](swarm.toml) that the scheduler admits where it fits. [The team fleet guide](../../docs/guides/team-fleet.md) installs the store and its roles, and [the fleet scheduler guide](../../docs/guides/fleet-scheduler.md) runs the pool. This cookbook walks one small pool from the first login to an update.

## Before you start

- The store exists on PostgreSQL 18, and its admin has run `dockingbird org create`. The team fleet guide does this in its steps 1 to 3.
- Your login role exists, with a password the admin gave you, and you are a member of the project `example`.
- Both hosts have Docker and Dockingbird set up. Check each with `dockingbird --version`.
- This computer reaches both hosts, as [Two Macs, over ssh](../two-macs-ssh/README.md) and [a cloud VM](../cloud-vm-gcloud/README.md) show.

## 1. One name

A host has one name: the `name` of its `[[host]]` table in a member's `hosts.toml`. That is also its name in the pool, the name its worker runs under (`dockingbird fleet worker --host lab`) and the name a swarm definition places work on. Set each host in your `hosts.toml` under its pool name.

```bash
dockingbird fleet hosts set lab --ssh lab.example
dockingbird fleet hosts set cloud --gcloud cloud-1 --zone europe-west1-b --project example-project
```

Each command prints this line when the host answered and was saved.

```text
{host}: {route} {target}, saved in {path}.
```

`fleet hosts rename` and `fleet hosts forget` of a host the pool holds are refused while it is there. Drain and remove it from the pool first, then rename it in your file, then enrol it again under its new name. A rename never changes a swarm definition, which names pool hosts.

## 2. Log in to the store

Every fleet scheduler command reads this computer's org login first. The login names the store, and the role each kind of command connects as. It never holds a password. Each role's password is a line of `~/.pgpass`, the file PostgreSQL's own tools read, which must be yours alone (`chmod 600`).

```bash
dockingbird org login db.example.net:5433 --as user --role alice
dockingbird org status
```

The command asks for the password without echo, or reads it from standard input with `--password-stdin`. The step is done when you see these lines.

```text
Saved: user logs in to db.example.net:5433, database dockingbird_fleet, as alice.
Connected as alice.
```

The admin logs in as `fleet_admin`, and adds `--project example` where the admin's own leases run. A host's worker logs in with `--as worker --role fleet_worker_lab`, and the admitter's machine with `--as admitter --role fleet_admin`. A command whose kind has no login ends 78 and names the login to run. An older home may still hold a `fleet.toml` with a `password`. This release refuses it, so run `dockingbird org login --from-fleet-toml --as KIND` once to move the login to the org pointer and `~/.pgpass`.

## 3. The pool

The admin enrols each host once, with its reservable share and the gate lines its OS requires. The first step of the fleet scheduler guide names them and explains each line.

```bash
dockingbird fleet hosts add cloud --os linux --cores 60 --memory 230g --line idle_millicores=4000,8000 --line free_mib=16384,32768 --line psi_io_full=1500,1200 --power gcloud
```

`--power gcloud` lets the pool's admitter start the stopped VM when work waits on it. The step is done when `fleet queue` lists the host.

```text
cloud: {liveness}, {policy}, no sample yet
```

## 4. Services

Each host runs its worker, `dockingbird fleet worker --host cloud`. One machine of the pool that stays awake runs the admitter, `dockingbird fleet admitter`. Each runs until stopped, under the machine's own service manager: a LaunchAgent on a Mac, or a systemd user unit on Linux with `loginctl enable-linger`. Dockingbird prints no unit for these two commands, so you write each one for your service manager. It starts `installs/current/bin/dockingbird` with the command's arguments.

The step is done when the host's line in `fleet queue` stops saying `no sample yet`, because a worker publishes a sample every 30 seconds. A worker or admitter started against a store that lacks a migration refuses with `FLEET_STORE_BEHIND`. Run `dockingbird org create` as the admin first, then start it again.

## 5. A swarm

[swarm.toml](swarm.toml) places a reviewer, a tester and two builders on `lab` first, else `cloud`, in each host's home `/opt/dockingbird/homes/team-1`, on the branch `feature/example` of `example-org/example-app`. A home of the placement must already link a checkout of that repository on that branch, in a folder named `example-app`. `fleet submit` refuses a definition whose source no home of its placement has checked out. Write a brief for each role beside it, as `briefs/reviewer.md`, `briefs/tester.md` and `briefs/builder.md`. Then submit it.

```bash
dockingbird fleet submit swarm.toml
dockingbird fleet queue
```

`fleet submit` checks the definition against the pool and queues it. `fleet queue` shows each host and each workload, and `dockingbird fleet why ID` shows what holds one that waits.

```text
{id} pending, position {position}
```

## 6. Update the pool

A new release reaches a host's engine in this order: install it, update each home the worker serves, move `installs/current` to the release, then restart the host's services. `fleet update` runs that order on every pool host in rank order, or on the one host `--host` names. It is the admin's alone, and any other login ends 77.

Each pool host needs a `repoint` line in its `[[host]]` table in the `hosts.toml` of the computer you run it on. The line restarts that host's services and must return without waiting for them to stop.

```text
repoint = "launchctl kickstart -k gui/$UID/<label>"
repoint = "systemctl --user restart --no-block <unit>"
```

The first line is for a Mac and the second for Linux, so each host's table holds one of them. Before a release changes the store, the admin runs `dockingbird org create` at the new build, then `fleet update` moves the pool.

```bash
dockingbird fleet update --release V
```

The step is done when the last line prints. A step that fails stops the command with exit 1 and leaves the hosts after it as they are, so fix the cause and run the same command again.

```text
Dockingbird {release} runs on {names:and}.
```

## When it fails

Eight ids cover this cookbook. Read the one your command printed.

- [`ORG_ROLE_MISSING`](../../docs/troubleshooting.md#org_role_missing) shows that this computer has no login for the kind the command needs. Run the `org login` the message names.
- [`FLEET_DB_UNREACHABLE`](../../docs/troubleshooting.md#fleet_db_unreachable) appears when the store does not answer. The command ends 69, and a service restarts itself until the store returns.
- [`FLEET_DB_REFUSED`](../../docs/troubleshooting.md#fleet_db_refused) appears when the store turns the login down. The command ends 78, so check the role and its password.
- [`FLEET_CONFIG_PASSWORD_REFUSED`](../../docs/troubleshooting.md#fleet_config_password_refused) comes from an older `fleet.toml` that still holds a password. Run `org login --from-fleet-toml --as KIND`.
- [`FLEET_STORE_BEHIND`](../../docs/troubleshooting.md#fleet_store_behind) stops a worker or admitter whose build needs a migration the store lacks. The admin runs `org create`.
- [`FLEET_NOT_A_MEMBER`](../../docs/troubleshooting.md#fleet_not_a_member) answers a submit for a project you are not a member of. An admin runs `org members add`.
- [`FLEET_UPDATE_NO_REPOINT`](../../docs/troubleshooting.md#fleet_update_no_repoint) shows that a host has no `repoint` line, so nothing was updated.
- [`FLEET_UPDATE_NO_WORKER`](../../docs/troubleshooting.md#fleet_update_no_worker) shows that a host's worker has not reported in time. Start it, then run the update again.
