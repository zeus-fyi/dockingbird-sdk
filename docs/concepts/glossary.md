---
title: Glossary
summary: One short entry for each word the Dockingbird docs use for a part of the product, with a link to the page that explains it.
audience: first-day
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

The entries below are in the order a new user meets them: one computer first, then messages, then teams, then licensing. Each entry says what the word names in two sentences and links to the page that explains it.

## home

A home is the folder `DOCKINGBIRD_HOME`, `~/.local/share/dockingbird` by default, with the containers, volumes and image that belong to it. `dockingbird --home NAME` runs a command in a second home on the same computer.

Explained in [Architecture](architecture.md).

## agent

An agent is one Claude Code or Codex process that runs in its own container with its own copy of a branch. Dockingbird names agents `claude-1`, `codex-1` and so on, or by the name you give with `--as`.

Explained in [Agents and the bus](agents-and-the-bus.md).

## the bus

The bus is the message system you and your agents use to pass tasks, questions, answers and files. The commands `send`, `inbox`, `read`, `wait` and `results` move messages on it.

Explained in [Agents and the bus](agents-and-the-bus.md).

## turn

A turn is the work an agent does between one message and its report. After each turn an agent on the bus sends you a status message such as `turn 3`, at priority P3.

Explained in [Agents and the bus](agents-and-the-bus.md).

## delivery

A delivery is one message waiting in an inbox, yours or an agent's. `dockingbird inbox claude-2` lists the deliveries waiting for that agent, and `dockingbird read ID` reads one.

Explained in [Agents and the bus](agents-and-the-bus.md).

## question row

A question row is one line of `dockingbird questions`, a question an agent asks you. It keeps its row number until you answer it with `dockingbird answer ROW`.

Explained in [Agents and the bus](agents-and-the-bus.md).

## config

A config is a small TOML file that adds a command of your own, such as `dockingbird review`, which runs Claude Code or Codex with settings you chose. It lives in the `.dockingbird/` folder of a repo or is copied in with `dockingbird config add`.

Explained in [Your own commands](../guides/your-own-commands.md).

## skill

A skill is a folder holding a `SKILL.md` and the files it uses, named by its folder, which an agent's tool lists as its own. A config's `[skills]` table, `--skills` on a start and `dockingbird set NAME --skills` give an agent skills.

Explained in [Give agents skills](../guides/skills.md).

## fallback tool

A fallback tool is the other tool, Claude Code or Codex, that a bus agent moves to with its conversation when a rule of its `[fallback]` table says so. The same table sets which failed turns are tried again and which are reported.

Explained in [Your own commands](../guides/your-own-commands.md#a-fallback-tool).

## connection

A connection is a named grant of one outside thing: a GitHub branch, a folder, a database, a service, an MCP server or a browser. Dockingbird holds the secret, and the agent only asks for the thing by its name.

Explained in [Security model](security-model.md).

## host

A host is a computer your `dockingbird` command reaches, named in `hosts.toml` by an ssh destination or a Compute Engine VM. This computer is always the host called `local`.

Explained in [Fleet and hosts](fleet-and-hosts.md).

## pool

The pool is the set of hosts the fleet scheduler may place swarms on, kept in your organisation's PostgreSQL store. Each pool host has cores, memory, a rank and an agent cap.

Explained in [Fleet scheduler](fleet-scheduler.md).

## swarm

A swarm is a team of agents started together from one definition file, with a count for each role. `dockingbird fleet submit` queues it.

Explained in [Swarms and roles](swarms-and-roles.md).

## role

A role is one kind of agent in a swarm definition, such as a reviewer, a tester or a builder. It names the tool, the model, the effort, the count, a brief and the roles its agents may message.

Explained in [Swarms and roles](swarms-and-roles.md).

## role library

A role library is a folder of role files, `.dockingbird/roles/`, that a swarm's role names with `use` and overrides key by key. Dockingbird ships six roles, which `dockingbird init` copies there.

Explained in [Swarms and roles](swarms-and-roles.md).

## parameter

A parameter is a value a swarm definition declares in `[params]` and writes as `{{name}}`, given at submit with `--set` or `--values`. The built-ins, such as `{{swarm}}` and `{{branch}}`, need no declaration.

Explained in [Swarm definition file](../reference/files/swarm-definition.md#parameters).

## workload

A workload is what the fleet scheduler queues: a swarm or a lease. It has an id, a priority from P0 to P3 and an age.

Explained in [Swarms and roles](swarms-and-roles.md).

## control plane

The control plane is a Dockingbird home of its own that other computers join with `node join`. Once a computer has joined, its agents get a fleet inbox and can message agents on other computers.

Explained in [Control plane](control-plane.md).

## seat

A seat is one person's share of a license. One seat may link up to three computers.

Explained in [Licensing model](licensing-model.md).

## computer

A computer, for licensing, is one machine linked to a seat by `dockingbird license activate`. A second home on the same computer shares its link, and agents, containers and repos are never counted.

Explained in [Licensing model](licensing-model.md).

## lease

A lease is a claim on a host's cores and memory that a command holds while it runs, made with `dockingbird fleet run`. The scheduler waits for a host with room, then runs the command there.

Explained in [Fleet scheduler](fleet-scheduler.md).

## admitter

The admitter is the long-running `dockingbird fleet admitter` command that decides which host each queued workload goes to. It runs on one machine of the pool that stays awake.

Explained in [Fleet and hosts](fleet-and-hosts.md).

## worker

A worker is the long-running `dockingbird fleet worker --host NAME` command, one for each machine of the pool. It reports the machine's load every 30 seconds and starts and watches the agents placed there.

Explained in [Fleet and hosts](fleet-and-hosts.md).

## egress mode

An egress mode sets how far an agent's network reaches. The four modes are `full`, `allowlist`, `models` and `none`.

Explained in [Security model](security-model.md).

## kept copy

A kept copy is the copy of your branch that an agent leaves behind when it stops with work not yet shared. `dockingbird claude --as NAME` picks it up, and `dockingbird clean` asks before it removes one.

Explained in [Sync model](sync-model.md).
