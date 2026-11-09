---
title: Choose a topology
summary: Pick one computer, two computers over ssh, a cloud VM or a team pool, and see which pages and examples each needs.
audience: team-admin
commands:
  - dockingbird fleet hosts set
  - dockingbird fleet agents
  - dockingbird org login
  - dockingbird fleet submit
  - dockingbird cp init
  - dockingbird node join
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Choose a topology

This page helps you pick where your agents run, from one Mac to a team pool. It names the pages and the example each choice needs.
Every choice starts with the one-computer set-up, so finish [first run](first-run.md) first.

## Before you start

- `dockingbird claude` has started an agent on this computer. [First run](first-run.md) shows the lines that prove it.
- You know how many computers should run agents, and whether one person or a team uses them.

## The four choices

| Choice | Use it when | What you add | Example | Pages |
|---|---|---|---|---|
| One computer | One person, one Mac | Nothing | [One Mac](../../examples/one-mac/README.md) | [Quickstart](../quickstart.md), [daily loop](../guides/daily-loop.md) |
| Two computers over ssh | You have a second Mac or Linux host you reach with ssh | A host, with `dockingbird fleet hosts set NAME --ssh DEST` | [Two Macs](../../examples/two-macs-ssh/README.md) | [Hosts](../guides/hosts.md), [hosts file](../reference/files/hosts-file.md) |
| A cloud VM | The second computer is a Compute Engine VM | A host, with `dockingbird fleet hosts set NAME --gcloud VM --zone ZONE --project PROJECT` | [Cloud VM](../../examples/cloud-vm-gcloud/README.md) | [Cloud VMs](../guides/cloud-vms.md), [hosts](../guides/hosts.md) |
| A team pool | Several people share hosts and a queue of swarms | A PostgreSQL 18 store, an org login, a worker on each host | [Team fleet](../../examples/team-fleet/README.md) | [Team fleet](../guides/team-fleet.md), [control plane setup](../guides/control-plane-setup.md), [fleet scheduler](../guides/fleet-scheduler.md), [swarms](../guides/swarms.md) |

The license does not depend on the topology: one seat is one person with up to three computers.
[Activate](activate.md) explains seats.

## 1. One computer

Install, activate, make the repo ready and run `dockingbird claude`.
Every agent runs in its own container on this computer, and its work reaches you only as commits through `dockingbird sync`.
Nothing else is needed, and this setup is the base of the other three.

Done when `dockingbird status` lists your agents.

## 2. Two computers over ssh

You keep working on your first computer, and agents also run on a second one.
The second computer needs Docker, and your own ssh must reach it without asking.
A Mac whose login does not find Docker Desktop's `docker` needs `--path PATH`, and Docker Desktop's socket needs `--docker-host URL`.
A Linux host is added the same way, with Docker Engine there.

`dockingbird fleet hosts set NAME --ssh DEST` first reads the host over your ssh. It writes the host into `hosts.toml` only when that read works.
`dockingbird fleet agents --host NAME` then lists the agents running there.

Done when `fleet hosts set` prints this line, where the host's rows follow.

```text
{host}: {route} {target}, saved in {path}.
```

If the host cannot be read, the command saves nothing and prints the ssh check to try first.

## 3. A cloud VM

A Compute Engine VM is added through your own `gcloud compute ssh`, with `--gcloud VM --zone ZONE --project PROJECT`.
Another cloud's VM is a host over ssh, so it follows choice 2.
Start a stopped VM first, because `fleet hosts set` cannot read it.
The VM needs the same things as any host: arm64, Docker Engine with buildx, uv and git.

Done when `fleet hosts set` prints its "saved in" line, as in choice 2.

## 4. A team pool

A pool shares hosts across people.
It queues swarms and starts each where it fits.
It needs a PostgreSQL 18 store that your organisation runs. It also needs one admin, and a login for each host's worker and for each person.
Each computer logs in once with `dockingbird org login HOST:PORT --as user --role ROLE`, and `dockingbird fleet submit` queues a swarm.

Computers can also join a control plane, so agents on different computers can message each other. The control plane is a home of its own, made with `dockingbird cp init`.
Each joining computer runs `dockingbird node join` with a bundle the control plane makes for it. You run the control plane and its hub yourself, and [Run your own control plane](../guides/control-plane-setup.md) walks through it.

A store that Zeusfyi hosts for you is not yet available.
[Team fleet](../guides/team-fleet.md) installs the store and both features, in order.

Done when `dockingbird org login` ends 0 on a computer, and `dockingbird org status` checks the login.

## When it fails

- A host that ssh, gcloud or Docker cannot reach ends `fleet hosts set` with [`FLEET_HOSTS_NOT_REACHED`](../troubleshooting.md#fleet_hosts_not_reached). Nothing is saved, and the message prints the command to try by hand.
- A `hosts.toml` that cannot be read gives [`FLEET_HOSTS_FILE_INVALID`](../troubleshooting.md#fleet_hosts_file_invalid). The message names the line to fix.
- `fleet agents --host NAME` with a name the file lacks gives [`FLEET_HOST_UNKNOWN`](../troubleshooting.md#fleet_host_unknown), plus the `set` command that adds it.
- A fleet command on a computer with no org login gives [`ORG_NOT_CONFIGURED`](../troubleshooting.md#org_not_configured). Run `dockingbird org login HOST --as user --role ROLE`.
- Logging in as the wrong kind for a command gives [`ORG_ROLE_MISSING`](../troubleshooting.md#org_role_missing). The message prints the login that command needs.
