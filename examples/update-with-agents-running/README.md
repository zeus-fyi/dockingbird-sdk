---
title: Update with agents running
summary: Update Dockingbird while agents work, watch each agent switch at its next stopping point, and finish the stragglers.
audience: daily
commands:
  - update
  - update --check
  - status
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Update with agents running

This cookbook updates Dockingbird while `claude-1` and `codex-1` work on the bus and `claude-2` sits at a terminal. The agents on the bus switch in place at their next stopping point and keep their conversations. The agent at a terminal keeps its code until its terminal closes. Each step ends with the line it prints when it worked.

## Before you start

- Dockingbird is set up and this computer is activated. `dockingbird license status` shows the license.
- Agents run. `dockingbird status` lists them, one row each.
- You know which agents are at a terminal. Those never switch by themselves, and `update` never asks them.
- Your running version is at least the first release that rolls in place. If it is older, step 5 applies.

## 1. Check that a newer release is out

```bash
dockingbird update --check
```

The step is done when the product prints this line.

```text
A newer Dockingbird is out. Get it: dockingbird update
```

## 2. Update

```bash
dockingbird update
```

The new code goes into the home's code store and Dockingbird's coordinator is replaced in the background. Your agents keep working while it restarts. If the release changes Dockingbird's records, `update` first prints `This update changes Dockingbird's records.` and `Once it takes over, it can't go back to 0.11.1.` The step is done when the product names the agents that will take the release.

```text
Dockingbird 0.11.2 is installed and takes over now.
claude-1 and codex-1 take it at their next stopping point.
```

Message id `UPDATE_ROLLING`. A command you run meanwhile waits for the coordinator's switch with `Switching Dockingbird to 0.11.2 ...`, minutes at most, and never waits for the agents. On a Mac, `update` last tries to install the GUI, which is not yet available to customers. If that fails, Dockingbird is already updated, and `update` ends with the GUI message and exit 1.

## 3. Watch the switch

```bash
dockingbird status
```

`status` says how far the roll got and what holds each agent back. The step is done when each agent is accounted for.

```text
Dockingbird 0.11.2 is taking over: claude-1 and codex-1 take it at their next stopping point.
claude-1 takes 0.11.2 at the end of its turn (asked 2 min ago).
codex-1 was asked to take 0.11.2 2 min ago and hasn't answered yet.
claude-2 on 0.11.1 keeps its own until its terminal closes.
```

Message ids `STATUS_UPDATE_ROLLING` and `STATUS_UPDATE_STRAGGLERS`. An agent switches only between two turns, never inside a turn or a tool call, and no turn is ended for it. A Claude agent whose background work still runs waits up to 30 minutes for it. An idle agent that has not answered its ask in 10 minutes is left on its old code. When an agent switches, its tool is told before its next prompt.

```text
Dockingbird updated from 0.11.1 to 0.11.2 and resumed your conversation. Continue where you were.
```

## 4. Finish the agent at a terminal

An agent at a terminal never switches. Close its terminal, or stop it, then pick it up.

```bash
dockingbird stop claude-2
dockingbird claude --as claude-2
```

The pick-up starts `claude-2` on the new code with its conversation resumed. The step is done when `dockingbird status` no longer lists `claude-2` on `0.11.1`.

## 5. Confirm that nothing waits

```bash
dockingbird update
```

Run again for the same version, `update` changes nothing. The step is done when it prints this line.

```text
Dockingbird 0.11.2 is in place, and no agent is waiting to take it.
```

Message id `UPDATE_ROLLING`. The roll waits for its stragglers up to 24 hours, then ends, and `status` names the ones still running. A later `dockingbird update` asks the bus stragglers again.

## If the running version is too old to roll

A home whose Dockingbird predates rolling updates waits once, until its agents end.

```text
Dockingbird here is too old to take 0.11.2 while agents run,
so claude-1 on 0.10.3 keeps its own until it ends.
```

Message id `UPDATE_NO_ROLL_FLOOR`. `status` says `Dockingbird 0.11.2 is installed and takes over when claude-1 on 0.10.3 ends` (`STATUS_UPDATE_STAGED`). Once the last agent ends, Dockingbird switches by itself and stays off after a `dockingbird stop` until you next use it. Later updates reach working agents at their stopping points. See [updates](../../docs/guides/updates.md).

## When it fails

- A second `dockingbird update` while the first installs gives [`UPDATE_IN_PROGRESS`](../../docs/troubleshooting.md#update_in_progress). Run it again when the first ends.
- A coordinator that does not come up gives [`UPDATE_SWITCH_FAILED`](../../docs/troubleshooting.md#update_switch_failed). The old version still runs, and `dockingbird update` shows why.
- A Dockingbird from before rolling updates prints [`UPDATE_NO_ROLL_FLOOR`](../../docs/troubleshooting.md#update_no_roll_floor) and waits for the agents to end.
- A release that changes the records prints [`UPDATE_MIGRATES`](../../docs/troubleshooting.md#update_migrates) first. After it takes over, the old version cannot run on them.
- Agents still on old code show in `status` as [`STATUS_UPDATE_STRAGGLERS`](../../docs/troubleshooting.md#status_update_stragglers), each named with its version.
