---
title: Swarms and roles
summary: What a swarm definition holds, how roles, counts and send_to shape a team, where a role's model and effort come from, how values are given at submit, and what a workload is.
audience: team-admin
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

You describe a team of agents in one TOML file, for example four builders, a reviewer and a tester. The fleet scheduler then starts that team on a host of your pool. Below are the parts of the file, the values you give at submit, and the workload that results.

## The definition

A definition is a TOML file at `schema = 1`. It names a `project`, a `priority` from P0 to P3, the `[source]` repository and branch the agents work on, and an optional `[placement]` list of hosts. Each kind of agent is one `[[role]]` table. A `key` makes the definition repeatable: a second submit with the same key answers the swarm that was queued first. Without a `key`, every submit queues a new swarm, keyed by its name and the UTC time. The [team fleet example](../../examples/team-fleet/swarm.toml) places a reviewer, a tester and two builders.

## Roles

A role is one kind of agent. It names a `harness` (`claude` or `codex`), a `count`, and a `brief`, a Markdown file that is the agent's first task. It may add `min` and `max`, the fewest agents a retire leaves and the most an add reaches. Both default to the count. A role marks its job with `reviews` or `tests`, which name the roles whose commits it checks.

The model and the effort come from the first place that gives them: a value given at submit, the role, its library role, then `[roles.<name>]` in `.dockingbird/project.toml` when its harness is the role's, then your organisation's store. A role that none of them covers is refused. The name the last two are read by is the role's `kind`, else `reviewer` when it reviews, `tester` when it tests and `implementer` otherwise, the names the library's `index.toml` gives. A role that uses a library role, or names another new key, tries its own name and its library role's name first. [The definition reference](../reference/files/swarm-definition.md#where-a-roles-model-and-effort-come-from) gives the whole order, and [the swarms guide](../guides/swarms.md#choose-each-roles-model-and-effort) recommends a model and an effort for each kind of role.

A role can take its settings from a library. `use = "<name>"` reads `.dockingbird/roles/<name>.toml` in the project. `use = "dockingbird/<name>"` reads one of the roles Dockingbird ships: `coordinator`, `implementer`, `reviewer`, `tester`, `reader` and `hands`. None of them names a model or an effort. `dockingbird init` copies those into the project, and a copy you edited survives a later `init`. Each key the swarm gives replaces the library role's, but `needs` and a subagent's table, which merge field by field.

A role can also name a fallback tool, a `[role.fallback]` table with the keys of a config's `[fallback]`. After a failed turn its agents retry, report, or move to the other tool with their conversation, as the table's rules say.

A role's `send_to` lists the roles whose agents it may message besides its parent. An empty list means the parent alone. Leaving it out lets the agent message any agent of the project. Any other send is refused with `FORBIDDEN`.

## Values at submit

A definition may declare `[params]`, each an `int`, a `choice` or a `text` with a default and bounds, and write `{{name}}` in its roles' values and texts. The submit also supplies built-ins: `{{swarm}}`, `{{project}}`, `{{repository}}` and `{{branch}}`, and in a text alone `{{roles}}` and `{{params}}`. `dockingbird fleet submit NAME --set N=4` gives one value, and `--set grader.count=6` sets a role's count. `--values FILE` takes a JSON document shaped `{"params": {...}, "roles": {"<role>": {...}}}`. A `--set` beats the file for the same key.

A submit may set a role's `count`, `min`, `max`, `model`, `effort`, `compact_at` and `session_hours`, a subagent's `model`, `effort` and `max`, and a role's fallback `harness`, `model`, `effort` and `placement`. `dockingbird fleet describe NAME` prints every parameter and settable field as JSON and connects to nothing. A submit checks every rule before it stores anything, prints each refusal as `refused: <field>: <rule>`, and exits 1. `fleet queue` and `fleet why` show the values a swarm was given.

## What a workload is

A workload is the unit the scheduler queues, and it is either a swarm or a lease. A successful submit prints `<id> pending, position <n>`, and that id names the workload in every later command. The controls `hold`, `release`, `pause`, `resume`, `cancel` and `done` take it. [The fleet scheduler](fleet-scheduler.md) explains how a workload waits and how it is admitted.

Agents the fleet starts get `--compact-at 500000` and `--session-hours 48` unless their role names its own. An agent that hands its parent a message beginning `status: done` is retired on its own word.

## What it never does

- It never stops an agent during a turn. `pause`, `cancel`, `done` and `retire` each wait for the running turn to end.
- It never queues a definition that breaks a rule. Nothing is stored when a refusal prints.
- It never starts a second swarm for a repeated `key`.
- It never places a swarm on a host whose home has no checkout of the repository, and `fleet why` names that hold `no_seed`.
- It never lets a role drop a tool of the bus set.
- It never moves one agent between its tools more often than the installation allows, once by default, so an agent never moves back and forth.

## The picture

```mermaid
flowchart LR
  vals["--set builder.count=4"] -->|"values at submit"| def["Definition: swarm.toml"]
  subgraph roles["Roles and counts, an example"]
    coord["coordinator x1"]
    build["builder x4"]
    rev["reviewer x1"]
    test["tester x1"]
  end
  def --- roles
  coord -->|"send_to"| build
  build -->|"send_to"| rev
  build -->|"send_to"| test
  def -->|"fleet submit"| wl["Workload: pending"]
  wl -->|"placed on a host"| run["Running swarm"]
  run -->|"done or cancel"| fin["Ended"]
```

Text alternative. A definition lists its roles and their counts, here one coordinator, four builders, one reviewer and one tester. The `send_to` edges show who may message whom: the coordinator reaches the builders, and the builders reach the reviewer and the tester. Values such as `--set builder.count=4` enter at submit. `fleet submit` turns the definition into a pending workload, the scheduler places it on a host, and `done` or `cancel` ends it.

## Guides that use it

| Guide | What it adds |
|---|---|
| [Swarms](../guides/swarms.md) | Writes a definition, submits it and changes a running swarm. |
| [The fleet scheduler](../guides/fleet-scheduler.md) | Follows the queue and uses the controls. |
| [Team fleet](../guides/team-fleet.md) | Installs the store, the worker and the admitter first. |
| [Swarm definition](../reference/files/swarm-definition.md) | Lists every key of a definition. |
| [Roles and connections](../reference/files/roles-and-connections.md) | Lists the keys of a library role. |
