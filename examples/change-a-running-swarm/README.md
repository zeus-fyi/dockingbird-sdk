---
title: Change a running swarm
summary: Add two agents of a role to a running swarm, retire one, and prune the agents' copies after the branch is merged.
audience: team-admin
commands:
  - fleet queue
  - fleet add
  - fleet retire
  - fleet ledger
  - fleet done
  - fleet prune
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Change a running swarm

This cookbook resizes a swarm that is already running. You add two builders, retire one, and delete the agents' kept copies once the work is merged. Each change waits for an agent's running turn to end and never interrupts it. [The swarms guide](../../docs/guides/swarms.md) explains each command, and [the swarm definition reference](../../docs/reference/files/swarm-definition.md) names the `min` and `max` that bound them.

## Before you start

- A swarm is running. `dockingbird fleet queue` lists it as `running`, with its id, which the steps below call `ID`.
- Your role queues and controls the swarm's project, or you are the admin.
- The role you add to has room under its `max`, and the role you retire from stays at or above its `min`. A role that names neither keeps its `count` for both.

## 1. Find the swarm and its agents

`fleet queue` lists each workload not yet ended. Under a swarm it names the agents still working and the agents waiting to start. Note the id of the swarm and the name of the agent you will retire.

```bash
dockingbird fleet queue
```

The step is done when you can read the swarm's line and its agents. The first line below is the swarm's.

```text
{id} {project} {kind} {priority} running on {host}, {age} old, needs {need_millicores} millicores, {need_mib} MiB, {agents} agents
```

## 2. Add two agents of a role

`fleet add` starts more agents of a role, up to its `max`, under the role's next names. The reason stays with the change. Each new agent starts once its host has room for it, is briefed with the roster, and every other agent is told the new roster.

```bash
dockingbird fleet add ID builder --count 2 --reason "two more tasks arrived"
```

The step is done when this line prints. The new agents appear in `fleet queue` as waiting to start, then as working.

```text
{id} running: added {names}; each starts once its host has room
```

An agent that waits shows what holds it, and `fleet why ID` names it host by host.

## 3. Retire one agent

`fleet retire` takes one agent out at the first tick of its host's worker that finds it idle, and gives its share back to the pool. An agent that never started retires at once. A tick that finds the agent working, asking or waiting, or with a question open or a request it has not taken yet, refuses the ask, records the refusal and sends the agent nothing. A request the agent already took holds nothing. Run the command again once the agent is idle.

```bash
dockingbird fleet retire ID build-3 --reason "its task is merged"
```

The step is done when this line prints. A `still working` form names the agents that have not stopped.

```text
{id} running: {name} retires at the first tick that finds it idle
with no question open and no request it has not taken yet; a tick
that finds it working or with either refuses the ask, and the
next fleet retire says so
```

Retire is refused before anything changes when the swarm is not running, has no such agent, or the role is at its `min`. A role with `min = 0` can be emptied if it neither reviews nor tests.

## 4. Finish and find the tested head

When the work is merged, end the swarm. `fleet done` stops each agent after its running turn. `fleet ledger` lists the commits, newest first, with who approved each and its test result. Take the sha of the head that was tested.

```bash
dockingbird fleet done ID
dockingbird fleet ledger ID
```

```text
{id} {state}
{sha} by {author}: approved by {reviewer} at {approved_at}; tested {result} by {tester} at {tested_at}
```

## 5. Prune after the merge

Prune deletes the agents' kept copies. It applies to a swarm that is done or cancelled. Prove the head is merged in your own checkout first, because the scheduler never checks it.

```bash
git merge-base --is-ancestor SHA origin/main
dockingbird fleet prune ID --merged SHA
```

The first command ends 0 when the sha is in `origin/main`. The step is done when the prune is queued.

```text
Queued the prune of {id} as job {job_id}.
Its host's worker deletes each of its agents whose container has stopped.
```

The host's worker deletes only agents whose container has stopped, never a running one. A commit an agent made and never published goes with its copy.

## When it fails

Six ids belong to the three changes. Read the one your command printed.

- [`FLEET_RETIRE_REFUSED`](../../docs/troubleshooting.md#fleet_retire_refused) comes from `retire`, and from `replace`, when the swarm is not running, the agent is unknown, or the role would fall below its `min`. Check the names with `fleet queue`.
- [`FLEET_NOT_NOW`](../../docs/troubleshooting.md#fleet_not_now) appears when a control does not apply to the workload's present state, such as `done` on a swarm that is not running. The line lists the states it does apply to.
- [`FLEET_DONE_NEVER_STARTED`](../../docs/troubleshooting.md#fleet_done_never_started) shows that no agent of the swarm ever started, so there is no team to end. Run `fleet cancel ID` in its place.
- [`FLEET_PRUNE_REFUSED`](../../docs/troubleshooting.md#fleet_prune_refused) appears when `--merged` is not a full commit id, or when the workload is not a swarm that is done or cancelled.
- [`FLEET_NOT_FOUND`](../../docs/troubleshooting.md#fleet_not_found) shows that your role sees no such workload, since a workload of another project reads as unknown to you.
- [`FLEET_NOT_A_MEMBER`](../../docs/troubleshooting.md#fleet_not_a_member) answers a command for a project you do not belong to. An admin runs `org members add` for you.
