---
title: Swarm definition file
summary: Every top-level key and every role key of a swarm definition at schema 1, with its type, default and meaning.
audience: team-admin
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../../llms.txt).

# Swarm definition file

A swarm definition is a TOML file, `swarm.toml`, at `schema = 1`. Keep it at `.dockingbird/swarms/NAME/swarm.toml` and submit it by name with `dockingbird fleet submit NAME`, or give a folder or a file path. [The swarms guide](../../guides/swarms.md) writes and submits one. `fleet describe NAME` prints every parameter and settable field as JSON.

## Top-level keys

| Key | Type | Default | Meaning |
|---|---|---|---|
| `schema` | integer | required, `1` | the definition's version |
| `project` | string | required, or given by `--project` | the project's slug |
| `key` | string | `NAME` and the UTC time as `YYYYMMDDhhmmss`, or `--key` | a repeat of a key answers the swarm queued first |
| `priority` | `P0`, `P1`, `P2` or `P3` | required | the queue priority |
| `[source]` `repository` | string | required unless every role has `workspace = "scratch"` | the repository the agents work on, such as `example-org/example-app` |
| `[source]` `branch` | string | required with `repository` | the branch they work on |
| `[placement]` `hosts` | list of host names | every pool host that takes swarms, in pool rank order | the hosts to try, in order of preference |
| `[placement]` `home.<host>` | string | a home that fixes nothing: one with a checkout of the repository first, then the fewest running agents, then by path | the host's home, by the name its worker publishes or by its folder path |
| `[params]` | table of parameters | none | declared parameters, each a table with `type` (`int`, `choice` or `text`), `default`, and `min` and `max` for an `int` or `choice` for a `choice`; written `{{name}}` in values and in role texts |
| `[[attachments]]` | tables with `path` and `name` | none | files attached to the swarm |

## Role keys

Each `[[role]]` is one kind of agent.

| Key | Type | Default | Meaning |
|---|---|---|---|
| `name` | slug | required | the role's name |
| `harness` | `claude` or `codex` | required, or from the library role or project file | the tool the agents run |
| `model`, `effort` | string | the role, else its library role, else `[roles.<kind>]` of `.dockingbird/project.toml` when its harness matches, else the org store | override only; a role none of these gives one is refused |
| `count` | integer or `"{{N}}"` | required | agents of the role at the start; at most 24 per home |
| `min` | integer | the role's `count` | the fewest agents a retire leaves; the fleet admits a swarm once every role's `min` fits |
| `max` | integer | the role's `count` | the most agents an add reaches |
| `brief` | path | required, or from the library role | the Markdown file of the first task, read under the definition's folder |
| `reviews`, `tests` | list of role names | none | whose commits this role reviews or tests |
| `kind` | slug | `reviewer` or `tester` by `reviews` or `tests`, else `implementer` | selects the model and effort rows |
| `use` | string | none | `"NAME"` names `.dockingbird/roles/NAME.toml`; `"dockingbird/NAME"` names a shipped role |
| `instructions` | path | none | text the agents get after Dockingbird's rules and the project's |
| `connections` | list of names | none | the home's connections the agents are granted at start; each must name an enabled connection at submit |
| `[role.subagents.<name>]` | table | none | one helper kind: `instructions` (required), `model`, `effort`, `max`, `tools` |
| `send_to` | list of role names | any agent of the project | the roles the agents may message beside their parent; `[]` allows the parent alone |
| `workspace`, `egress`, `allow`, `env` | as in a config | as in a config | session settings, as [`app.toml`](app-config.md) takes them |
| `tools` | `bus`, `full` or a list | as in a config | must keep every bus tool, else `refused: role[N].tools: drops a tool of the bus set` |
| `compact_at` | `500000`, `500k` or `auto` | `500000` for a fleet-started agent | the point at which the agent's context compacts |
| `session_hours` | integer, 1 to 168 | 48 for a fleet-started agent | how long each agent may run |
| `needs` | cpus, memory and pids, each with `request` and `limit` | measured | the role's resource reservation |
| `args` | list from a closed set of start words | none | extra words a start takes |

The shipped roles are `coordinator`, `implementer`, `reviewer`, `tester` and `reader`. `dockingbird init` copies them into `.dockingbird/roles/` with the library's `index.toml`, and a copy you edited survives a later `init`. A key the entry gives replaces the library role's, and a subagent's table is merged field by field. [The roles and connections reference](roles-and-connections.md) lists the library file's keys.

## Values at submit

| Form | Meaning |
|---|---|
| `--set KEY=VALUE` | repeatable; a parameter (`N=4`), a role's setting (`grader.count=6`) or a subagent's (`grader.helper.max=4`) |
| `--values FILE` | JSON of the shape `{"params": {...}, "roles": {"ROLE": {...}}}`, a role's subagents under `subagents` |
| precedence | a `--set` beats the file for the same key |
| settable for a role | `count`, `min`, `max`, `model`, `effort`, `compact_at`, `session_hours` |
| settable for a subagent | `model`, `effort`, `max` |
| a refusal | one `refused: <field>: <rule>` line each, in a fixed order, then exit 1 |
