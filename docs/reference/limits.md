---
title: Limits
summary: The bounds on sessions, files, names, licenses and fleet calls that the Dockingbird guide states, one row each with its figure.
audience: daily
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Limits

This page lists the bounds the Dockingbird guide gives a figure for, one row for each bound.
A row holds the figure, what it limits and the page that explains it.
Where a config or a flag changes a bound, the row says which one, and a bound without a figure in the guide has no row.

## Agents and sessions

| Bound | Figure | What it limits | Explained in |
|---|---|---|---|
| Session of a bus agent | 12 hours by default, 1 to 168 | how long an agent runs before it ends itself; set with `--session-hours` or `[limits] session_hours` | [app-config.md](files/app-config.md) |
| Turn deadline | none | a turn runs until it ends, unless a config sets `[limits] turn_minutes` (at least 1) | [app-config.md](files/app-config.md) |
| Idle stop | 30 minutes | Dockingbird turns itself off after this long with no agent; the next command turns it back on | [daily-loop.md](../guides/daily-loop.md) |
| Agent numbers | 9999 per tool or command | past it a start without `--as` starts nothing and exits 1 | [delegating-tasks.md](../guides/delegating-tasks.md) |
| Container limits | none unless set | `--cpus`, `--memory` and `[limits] cpus` and `memory` set them | [commands.md](commands.md) |
| Sign-in retries | 3 | a Claude turn that Anthropic refused for its sign-in is tried again after 30, 60 and 120 seconds | [sign-in-and-api-keys.md](../guides/sign-in-and-api-keys.md) |
| Rule retries in a row | 3 by default, 1 to 100 | the retries of one delivery under a `[fallback]` rule; set with `retry_max` | [app-config.md](files/app-config.md#keys-of-fallback) |
| Wait before a rule retry | 5 minutes by default, 1 second to 24 hours | set with `[fallback]` `retry_wait` | [app-config.md](files/app-config.md#keys-of-fallback) |
| Usage-limit retries | after 1, 5 and 15 minutes, then every 30 minutes, until 24 hours after the first failure | a `usage_limit` failure under a `[fallback]` rule; `retry_wait` and `retry_max` do not apply | [app-config.md](files/app-config.md#keys-of-fallback) |
| Moves to the fallback tool | 1 per agent by default | an agent never moves back and forth between its tools | [your-own-commands.md](../guides/your-own-commands.md#a-fallback-tool) |
| Fallback pick-ups | 3 per agent | the pick-ups the fallback watcher on this computer runs for an agent before `status` names the command | [your-own-commands.md](../guides/your-own-commands.md#a-fallback-tool) |
| `fleet probe` | 20 seconds per read, 60 seconds in all | a read of this Mac and its Docker | [hosts.md](../guides/hosts.md) |

## Files and sizes

| Bound | Figure | What it limits | Explained in |
|---|---|---|---|
| Rules text of one agent | 64 KB | Dockingbird's rules plus the project's rules file; a longer text stops the start | [trust-and-repo-settings.md](../guides/trust-and-repo-settings.md) |
| `--agent-md` and `--claude-md` file | 1 MB | a regular UTF-8 text file with no Dockingbird credential in it, else nothing starts | [commands.md](commands.md) |
| Entries of one `skills.path` or `--skills` | 16 | the skill folders or skills folders one config's `[skills]` or one `--skills` names | [skills.md](../guides/skills.md) |
| Skills of one agent | 32 | a config's and a start's together | [skills.md](../guides/skills.md) |
| Files of one skill | 64 | the files under one skill folder | [skills.md](../guides/skills.md) |
| Depth of a skill's file | 8 path parts | how deep a file may sit under its skill folder | [skills.md](../guides/skills.md) |
| One skill file | 1 MiB | one file of a skill | [skills.md](../guides/skills.md) |
| One agent's skills | 4 MiB | all its skills together, as Dockingbird records them | [skills.md](../guides/skills.md) |
| Codex's skills listing | 10,000 tokens | the `skills.max_context_tokens` Dockingbird sets for a Codex agent with skills | [skills.md](../guides/skills.md) |
| `hosts.toml` | 1 MiB | a regular file of yours; a larger one is refused | [hosts-file.md](files/hosts-file.md) |
| Host name | 56 characters | lowercase letters, digits and dashes, one per file, never `local` | [hosts-file.md](files/hosts-file.md) |
| Service program output | 64 MiB and 10,000 entries | what a program you connected as a service may write to its output folder | [connections.md](../guides/connections.md) |
| First image build | about 1 GB, about 5 minutes | the download of the first `dockingbird claude`, once | [first-run.md](../getting-started/first-run.md) |
| Ubuntu package pool | 441 MB | the folder the first build fills, once per snapshot | [first-run.md](../getting-started/first-run.md) |

## Swarm definitions

| Bound | Figure | What it limits | Explained in |
|---|---|---|---|
| Definition file | 64 KiB | one `swarm.toml` | [swarm-definition.md](files/swarm-definition.md) |
| Brief or instructions file | 1 MiB | one text a role names | [swarm-definition.md](files/swarm-definition.md) |
| Parameters | 32 | the entries of one definition's `[params]` | [swarm-definition.md](files/swarm-definition.md#parameters) |
| Parameter name | 32 characters | letters, digits and `-` | [swarm-definition.md](files/swarm-definition.md#parameters) |
| `text` parameter value | 120 characters, or the parameter's `max_chars` | one printable line | [swarm-definition.md](files/swarm-definition.md#parameters) |
| Agents of a swarm at its start | 24 | the roles' counts together, and each role's `count` and `max` | [swarm-definition.md](files/swarm-definition.md#role-keys) |
| Helpers at once | 20 | a role's subagent `max` | [roles-and-connections.md](files/roles-and-connections.md#subagent-block) |

## License

| Bound | Figure | What it limits | Explained in |
|---|---|---|---|
| Computers per seat | 3 | one seat is one person with up to three computers; a second home on one computer shares its computer | [licensing.md](../guides/licensing.md) |
| Activations list | 80 computers | `license activations` shows the 80 seen longest ago and says how many more there are | [licensing.md](../guides/licensing.md) |
| Unreleased computer | 90 days | a computer never released stops counting by itself after this long | [licensing.md](../guides/licensing.md) |
| Check-in | once a day | a start whose last check-in is older checks in first; a failed check-in never stops the start | [licensing.md](../guides/licensing.md) |

## Fleet and control plane

| Bound | Figure | What it limits | Explained in |
|---|---|---|---|
| Computer label | 8 characters | lowercase letters and digits, starting with a letter, in `cp token --host LABEL` | [team-fleet.md](../guides/team-fleet.md) |
| Agent name on a joined home | 63 characters less the label and its dash | a longer name is refused with `FLEET_NAME_TOO_LONG` | [team-fleet.md](../guides/team-fleet.md) |
| Control plane overview | 100 fleet sessions | `status` on the control plane and `cp status` list this many and say `truncated` past it | [team-fleet.md](../guides/team-fleet.md) |
| Join bundle | 4096 bytes | what `node join` decodes | [team-fleet.md](../guides/team-fleet.md) |
| Fleet call | 30 seconds | how long a call waits for its answer | [team-fleet.md](../guides/team-fleet.md) |
| Agent's fleet inbox | 10 seconds | a read or heartbeat from an agent's own fleet inbox | [team-fleet.md](../guides/team-fleet.md) |
| Silent control plane | 40 seconds | a member finds a silent control plane within this time, then reconnects by itself | [team-fleet.md](../guides/team-fleet.md) |
| Messages waiting for one fleet agent | 200 | messages to a fleet agent whose home is asleep, held on the control plane's store | [team-fleet.md](../guides/team-fleet.md) |
| Hub connections | 1024 | one for each member and one for the control plane | [team-fleet.md](../guides/team-fleet.md) |
| Store connection | 5 seconds | how long each fleet scheduler command waits for the database; then it ends 69 | [exit-codes.md](integration/exit-codes.md) |
| `fleet run` wait | 30 minutes by default | `--wait`; a lease not taken by then is given up and the command ends 1 | [fleet-scheduler.md](../guides/fleet-scheduler.md) |
| `fleet run` bound | at most one day | `--bound`; at the bound the command is interrupted and `fleet run` ends 124 | [fleet-scheduler.md](../guides/fleet-scheduler.md) |
| `fleet read-home` | 200 agents and rows, 30 seconds per home | the rest is counted | [hosts.md](../guides/hosts.md) |
| ssh to a host | 15 seconds | a host that does not answer in this time is not reached | [hosts.md](../guides/hosts.md) |

## Tools and tool calls

| Bound | Figure | What it limits | Explained in |
|---|---|---|---|
| First tool download | 15 minutes | how long a start waits for a first download of Claude Code or Codex, or for a version you pinned | [updates.md](../guides/updates.md) |
| `agent_wait` | 1 to 45 seconds | the `timeout_s` of the MCP tool | [mcp.md](integration/mcp.md) |
| Docker waking | 2 minutes | how long a command waits for Docker to answer after a sleep, then it says Docker is answering slowly | [daily-loop.md](../guides/daily-loop.md) |
