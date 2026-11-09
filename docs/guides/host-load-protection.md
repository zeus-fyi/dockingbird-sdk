---
title: Host load protection
summary: Why a start is refused with HOST_AGENT_CAP or HOST_OVERLOADED, what the start guard checks, how to wait for room with start --wait, and how to read the host's load.
audience: daily
commands:
  - start --wait
  - fleet hosts add --line
  - fleet hosts policy --line
  - fleet host-history
  - fleet worker
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Host load protection

This page explains the start guard, the check that runs before Dockingbird makes an agent's container. The guard refuses a start when the home already runs 24 agents or when the host is too loaded to take another. It stops nothing that already runs. Pool hosts and their gate lines are set up in [the fleet scheduler guide](fleet-scheduler.md).

## What the guard checks

The guard runs for every start in every home of the host, whoever asks: you at a terminal, a coordinator, `agent_start` of [the MCP server](mcp-server.md), or the fleet engine. It never stops, pauses or moves a running agent. A rolling update's replacement of a stopped container is not guarded, so the guard does not refuse an update. There is no flag that skips the guard.

It makes three checks, in this order. The first refusal ends the check.

| Order | Check | Refuses with | When |
|---|---|---|---|
| 1 | The agent cap | `HOST_AGENT_CAP` | the home runs 24 agents, counting the starts the host's worker has not sampled yet |
| 2 | The age of the host's reading | `HOST_OVERLOADED`, stale form | the file `guard.json` is older than 180 seconds or does not parse |
| 3 | The host's gate lines | `HOST_OVERLOADED` | a line reads red on that reading, less what the starts not yet sampled hold |

- The cap is 24 agents per home, the default home included. A host that runs more than 24 agents needs a second home on it. Only running agents count: a stopped agent holds no slot.
- A gate line is a bound you set with `--line` in `fleet hosts add` or `fleet hosts policy`, such as `free_mib=16384,32768`. A figure the worker did not read counts as red.
- A computer outside the pool has no worker and no `guard.json`, so the cap is its one check.
- A start the fleet engine announced is counted and never refused. So is a start inside a [`fleet run`](fleet-scheduler.md#6-run-a-check-under-a-lease) lease that the host runs. Setting `DOCKINGBIRD_FLEET_LEASE` by hand grants nothing, because the guard looks the lease up in its records.

## 1. Read a refusal

Each message names what binds. This one means the home is full.

```text
The home {home} runs {count:agent|agents}, its cap of {cap},
so no agent starts there now; the host's lines were read from {path}.
Stop one there you don't need, or wait for room: dockingbird start --wait TIME
```

Message id `HOST_AGENT_CAP`. On a computer with no worker, the second line ends `unread: lines, as no fleet worker writes {path}`, which only says that the cap is the one check.

This one means a gate line is red. It names the figure, its value, the bound, and the load held for starts the worker has not sampled yet.

```text
No agent starts on this host ({host}) now: {figure} {value}, bound {line_bound},
with {provisional} held for starts its fleet worker has not sampled yet.
Stop an agent you don't need, or wait for room: dockingbird start --wait TIME
```

Message id `HOST_OVERLOADED`. This is its stale form, when the reading is too old.

```text
No agent starts on this host ({host}) until its fleet worker writes a fresh
reading; its last is {age} old.
Start the worker, then try again: {worker}
```

The command ends 1 and starts nothing.

| What the message says | What to do |
|---|---|
| `HOST_AGENT_CAP` | Stop an agent you do not need with `dockingbird stop NAME`, start in a second home, or wait for room. |
| `HOST_OVERLOADED` with a figure | Stop an agent, or wait until the line reads green. `dockingbird fleet host-history HOST` shows what the host read. |
| `HOST_OVERLOADED`, stale form | Start the worker with the command the message gives. |

A worker runs as a LaunchAgent named `com.dockingbird.fleet-worker` on a Mac and as the systemd user unit `dockingbird-fleet-worker.service` on Linux. After an update, restart the worker on the new install so it writes `guard.json` again. `dockingbird fleet update` does that for every host of the pool. The command the stale message gives is `dockingbird fleet worker --host HOST`.

## 2. Wait for room

`dockingbird start --wait TIME` makes the same decision again every 30 seconds until the host has room or the time is up. `TIME` is a whole number with its unit, `s`, `m` or `h`, up to one day.

```bash
dockingbird start --wait 30m "Fix the failing test"
```

Done when the command prints the agent's name. If the time runs out first, it ends with the last refusal.

- The wait holds no lock and makes no container, so `dockingbird stop` and a switch typed meanwhile run at once.
- A bare number such as `--wait 30` is refused with `START_WAIT_INVALID` and exit 2, and nothing starts.
- A start without `--wait` decides once, before it opens a session, so a refusal leaves no session behind and no peer hears of it.
- `dockingbird claude` and `dockingbird codex` have no `--wait`. Use `dockingbird start --harness codex --wait 30m` to wait on a Codex start.
- `agent_start` of [the MCP server](mcp-server.md) has no wait either. It refuses at once with `PROJECT_BUSY`, whose cause is `HOST_AGENT_CAP` or `HOST_OVERLOADED`, and its caller tries again.

## 3. Read the host's load

The host's worker samples the host every 30 seconds and writes the reading the guard uses to one file after each sample.

| Where | The file |
|---|---|
| Default | `~/.local/state/dockingbird/host-guard/guard.json` |
| With `XDG_STATE_HOME` set to a path from `/` | `$XDG_STATE_HOME/dockingbird/host-guard/guard.json` |

There is one file per user and host. A shell that sets `XDG_STATE_HOME` apart from the worker's service reads another file, and the cap's refusal names the path it read. Read the file for the figures behind a refusal. Do not edit it: the worker rewrites it at the next sample.

`dockingbird fleet host-history HOST [--since TIME]` prints the pool host's samples oldest first, so you can see when a figure went red. `--since` takes a time with its unit, such as `2h`. Each row gives the sample's time, the agents running on the host in every home and the part the engine started, the load Dockingbird did not start, and each figure with its value (`unread` when none was read).

```bash
dockingbird fleet host-history cloud --since 2h
```

```text
{sampled_at}: {host_agents:agent|agents}, {engine_containers} by the engine; foreign {foreign_millicores} millicores, {foreign_mib} MiB; {figures}
```

`dockingbird fleet queue` shows the same count on the host's line as `agents: {host_agents} on the host, {engine_agents} in engine homes`. The history is kept for 30 days.

## When it fails

- [`HOST_AGENT_CAP`](../troubleshooting.md#host_agent_cap) means the home runs 24 agents. Stop one, start in another home, or wait with `--wait`.
- [`HOST_OVERLOADED`](../troubleshooting.md#host_overloaded) means a gate line is red or the worker's reading is stale. Stop an agent, wait, or start the worker.
- [`START_WAIT_INVALID`](../troubleshooting.md#start_wait_invalid) means `--wait` has no unit or is longer than a day. Write `30m` or `2h`.
- `agent_start` of the MCP server answers both refusals with `PROJECT_BUSY` and the refusal's id as its cause. Its caller calls it again.
