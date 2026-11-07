---
title: Swarm definition file
summary: Every top-level key and every role key of a swarm definition at schema 1, with its type, default and meaning.
audience: team-admin
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../../llms.txt).

# Swarm definition file

A swarm definition is a TOML file, `swarm.toml`, at `schema = 1`. Keep it at `.dockingbird/swarms/NAME/swarm.toml` and submit it by name with `dockingbird fleet submit NAME`, or give a folder or a file path. [The swarms guide](../../guides/swarms.md) writes and submits one. `fleet describe NAME` prints every parameter and settable field as JSON. [The swarm parameters guide](../../guides/swarm-parameters.md) declares parameters and submits one definition many times with its values changed.

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
| `[params]` | table of parameters | none | declared parameters, at most 32, each named by a slug of at most 32 characters; each is a table with `type` (`int`, `choice` or `text`), an optional `default`, and `min` and `max` for an `int`, `choice` (a list of words) for a `choice`, or `max_chars` (1 to 120, 120 when left out) for a `text`; written `{{name}}` in values and in role texts, as [Placeholders](#placeholders) says |
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
| `[role.subagents.<name>]` | table | none | one helper kind: `instructions` (required), `model`, `effort`, `max`, `tools` (accepted by the product; the guide names model, effort, instructions and max) |
| `send_to` | list of role names | any agent of the project | the roles the agents may message beside their parent; `[]` allows the parent alone |
| `workspace`, `egress`, `allow`, `env` | as in a config | as in a config | session settings, as [`app.toml`](app-config.md) takes them |
| `tools` | `bus`, `full` or a list | as in a config | A config takes `bus` (messages and files, the default), `default` (claims and commits) or `full` (both); a swarm role takes `bus`, `full` or a list that keeps every bus tool; a list that drops a bus tool gives `refused: role[N].tools: drops a tool of the bus set` |
| `compact_at` | `500000`, `500k` or `auto` | `500000` for a fleet-started agent | the point at which the agent's context compacts |
| `session_hours` | integer, 1 to 168 | 48 for a fleet-started agent | how long each agent may run |
| `context` | `kept` or `fresh` | `kept` | `fresh` starts each task delivery of every agent of the role in a new conversation, under the same rules and settings; the entry's key wins over its library role's, and another word is refused at `role[N].context` |
| `needs` | cpus, memory and pids, each with `request` and `limit` | measured | the role's resource reservation |
| `args` | list from a closed set of start words | none | extra words a start takes |

The shipped roles are `coordinator`, `implementer`, `reviewer`, `tester` and `reader`. `dockingbird init` copies them into `.dockingbird/roles/` with the library's `index.toml`, and a copy you edited survives a later `init`. A key the entry gives replaces the library role's, and a subagent's table is merged field by field. [The roles and connections reference](roles-and-connections.md) lists the library file's keys.

## Placeholders

A placeholder is `{{name}}` in a string value. The rules are these.

| Rule | Meaning |
|---|---|
| where it works | any string value of `swarm.toml`, the text files a role or subagent names (`brief`, `instructions`), and a library role's string values and texts |
| where it does not | a key (`a placeholder in a key`), `[attachments]`, and Dockingbird's own injected layers |
| when it expands | when the definition declares `[params]`; a `{{` in a definition with none passes through untouched, and a library role's files always expand |
| how it expands | in one pass at submit; each `{{name}}` becomes the value as text, and the result is never scanned again |
| an `int` parameter | a string that is exactly one placeholder becomes an integer, so `count = "{{N}}"` becomes `count = 4` |
| built-ins | `{{swarm}}`, `{{project}}`, `{{repository}}`, `{{branch}}`, and in text files only `{{roles}}` and `{{params}}`; a declared parameter may not take one of these names |
| a name nothing declares | refused as `names no declared parameter, built-in, role or subagent` at the field |
| a wrong type | a parameter of another type than the field takes, such as a `text` in `count`, is refused |
| a wider range | a parameter may narrow a field's range or words and never widen them, so `wider than the field it binds to` is refused at `params.<name>.<key>` |

## Values at submit

| Form | Meaning |
|---|---|
| `--set KEY=VALUE` | repeatable; a parameter (`N=4`), a role's setting (`grader.count=6`) or a subagent's (`grader.helper.max=4`); split at the first `=`, and the value is read by the field it lands in |
| `--values FILE` | JSON of the shape `{"params": {...}, "roles": {"ROLE": {...}}}`, a role's subagents under `subagents`; both members are optional |
| precedence | a `--set` beats the file for the same key; a role or subagent setting of the invocation beats the definition's value, whatever gave that value, so `--set grader.count=8` beside `--set N=4` runs eight |
| the same key twice | two `--set` options with one key are refused at `set.<key>` as `named twice` |
| settable for a role | `count`, `min`, `max`, `model`, `effort`, `compact_at`, `session_hours` |
| settable for a subagent | `model`, `effort`, `max` |
| any other key | a role's `connections`, `tools`, `egress`, `env`, `workspace`, `send_to` and text files are the files' alone; a `--set` on one is refused as `not a setting an invocation may set` |
| what is recorded | the values given, after normalization into the JSON shape, never the defaults; `fleet queue` and `fleet why` print them |
| a refusal | one `refused: <place>: <rule>` line each, in a fixed order, then exit 1; the place is `params.N.default`, `role[2].count`, `set.<key>` or `values.<path>`, counted from 1 |

[The swarm parameters guide](../../guides/swarm-parameters.md) shows each form with a worked definition.
