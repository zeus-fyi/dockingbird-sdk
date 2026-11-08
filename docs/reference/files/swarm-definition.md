---
title: Swarm definition file
summary: Every top-level key and every role key of a swarm definition at schema 1, its parameters and placeholders, where a role's model and effort come from, its fallback table and the values a submit takes.
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
| `[placement]` `spread` | `true` or `false` | `false` | `true` lets the fleet place the swarm's roles on more than one host; `fleet where ID` names where each agent runs |
| `[params]` | table of parameters | none | declared parameters, at most 32, each written `{{name}}` in values and in role texts; [Parameters](#parameters) has their keys |
| `[[attachments]]` | tables with `path` and `name` | none | files attached to the swarm, sent as they are, with no placeholder expanded |

## Parameters

Each entry of `[params]` is one parameter, a table with a `type` and the keys of its type. A parameter with no `default` must get a value at every submit.

```toml
[params]
N = { type = "int", default = 2, min = 1, max = 8 }
effort = { type = "choice", default = "high", choice = ["medium", "high", "xhigh"] }
focus = { type = "text", default = "the login flow", max_chars = 80 }
```

| Type | Its keys | A value given at submit |
|---|---|---|
| `int` | `default`, `min`, `max`; each a whole number of 0 or more | a whole number within `min` and `max` |
| `choice` | `choice`, the list of words, each once; `default`, one of them | one of the words |
| `text` | `default`; `max_chars`, 1 to 120, 120 when left out | one printable line of at most `max_chars` characters, with no `"`, no `\`, no `{{` and no `}}` |

A parameter's name is at most 32 characters of letters, digits and `-`, and its letters may be upper case, as in `N`. It is never a built-in's name. A parameter may narrow the field it fills, such as a `choice` of three efforts, and never widen it: a word or a bound the field refuses is refused at the declaration (`wider`).

### Where a placeholder expands

| Place | `{{name}}` expands |
|---|---|
| a string value of a `[[role]]` entry | when the definition declares `[params]`; without `[params]`, `{{` stays as written |
| a role's `brief`, its `instructions` and its subagent's `instructions` | when the definition declares `[params]` |
| a library role's string values and texts | always |
| an attachment, a `harness_config` file | never |

A string that is one placeholder of an `int` parameter and nothing else becomes that number, so `count = "{{N}}"` is `count = 4` for `--set N=4`. A placeholder in a key is refused (`placeholder-key`). A placeholder that names no declared parameter and no built-in is refused (`undeclared`).

### Built-in parameters

The submit supplies these. A definition never declares them.

| Placeholder | Its value | Where it expands |
|---|---|---|
| `{{swarm}}` | the swarm's key | everywhere a placeholder expands |
| `{{project}}` | the project's slug | everywhere a placeholder expands |
| `{{repository}}` | `[source]` `repository`; empty for a swarm with no `[source]` | everywhere a placeholder expands |
| `{{branch}}` | `[source]` `branch`; empty for a swarm with no `[source]` | everywhere a placeholder expands |
| `{{roles}}` | one line per role: its name, its count, and its model and effort as resolved, each with its source | in a text alone, such as a brief |
| `{{params}}` | one line per declared parameter and its value | in a text alone |

In a definition that declares `[params]`, names a new role key such as `use`, or gets values at submit, no role may be named `parent`, `repo`, `scratch`, a built-in or a declared parameter (`reserved`).

## Role keys

Each `[[role]]` is one kind of agent.

| Key | Type | Default | Meaning |
|---|---|---|---|
| `name` | slug | required | the role's name |
| `harness` | `claude` or `codex` | required, or from the library role or project file | the tool the agents run |
| `model`, `effort` | string | [where they come from](#where-a-roles-model-and-effort-come-from) | override only; a role none of the sources gives one is refused |
| `count` | integer or `"{{N}}"` | required | agents of the role at the start; at most 24 per home |
| `min` | integer | the role's `count` | the fewest agents a retire leaves; the fleet admits a swarm once every role's `min` fits; a role that reviews or tests keeps at least 1 |
| `max` | integer | the role's `count` | the most agents an add reaches |
| `brief` | path | required, or from the library role | the Markdown file of the first task, read under the definition's folder |
| `reviews`, `tests` | list of role names | none | whose commits this role reviews or tests |
| `kind` | slug | `reviewer` or `tester` by `reviews` or `tests`, else `implementer`, as the role library's `index.toml` names them | a name the model and effort are looked up by |
| `use` | string | none | `"NAME"` names `.dockingbird/roles/NAME.toml`; `"dockingbird/NAME"` names a shipped role |
| `instructions` | path | none | text the agents get after Dockingbird's rules and the project's |
| `connections` | list of names | none | the home's connections the agents are granted at start; each must name an enabled connection at submit |
| `[role.subagents.<name>]` | table | none | one helper kind, at most one table per role: `instructions` (required), `model`, `effort`, `max` and `tools`, as [the subagent block](roles-and-connections.md#subagent-block) gives them |
| `send_to` | list of role names | any agent of the project | the roles the agents may message beside their parent; `[]` allows the parent alone |
| `workspace`, `egress`, `allow`, `env` | as in a config | as in a config | session settings, as [`app.toml`](app-config.md) takes them |
| `context` | `kept` or `fresh` | `kept` | as a config's `context`: one conversation for every delivery, or a new one for each task delivery |
| `tools` | `bus`, `full` or a list | as in a config | A config takes `bus` (messages and files, the default), `default` (claims and commits) or `full` (both); a swarm role takes `bus`, `full` or a list that keeps every bus tool; a list that drops a bus tool gives `refused: role[N].tools: drops a tool of the bus set` |
| `harness_config` | a path, or a table by harness | none | the harness's own settings file, the base under Dockingbird's own keys, read under the definition's folder or the library role's; never expanded |
| `compact_at` | `500000`, `500k` or `auto` | `500000` for a fleet-started agent | the point at which the agent's context compacts |
| `session_hours` | integer, 1 to 168 | 48 for a fleet-started agent | how long each agent may run |
| `needs` | cpus, memory and pids, each with `request` and `limit` | measured | the role's resource reservation |
| `args` | list from a closed set of start words | none | extra words a start takes |
| `hosts` | list of host names | the placement's hosts | the hosts of `[placement]` its agents may take, in order; the roles that publish commits (each role that reviews, and each role another reviews or tests) share one host, and in a swarm without `spread = true` every role does, else `hosts-apart` |
| `skills` | table of `path` and `into` | none | skills its agents' tool lists as its own, as a config's `[skills]` takes them: `path`, one skill or skills folder or a list of them, each a path from the top of the swarm's source; `into`, `both`, `claude` or `agents`; every start reads them from the swarm's clone, and a path the clone lacks holds the swarm (`skills_refused`) until you push the fix and run `fleet release ID`; `--set` cannot set it; see [skills.md](../../guides/skills.md) |
| `[role.fallback]`, `[role.fallback.on]` | tables | none | the tool its agents move to after a failed turn, and each error class's rule; see [A role's fallback](#a-roles-fallback) |

## Library roles

The shipped roles are `coordinator`, `implementer`, `reviewer`, `tester`, `reader` and `hands`. Each names its `harness`, `brief`, `instructions`, `workspace` and `tools`, and none names a model or an effort. `hands` carries out a coordinator's host requests with no clone of its own: `workspace = "scratch"`, a list of tools and `compact_at = "300k"`.

`dockingbird init` copies them into `.dockingbird/roles/` with the library's `index.toml`, and a copy you edited survives a later `init`. A key the entry gives replaces the library role's whole value. Two tables merge field by field instead, the entry's field winning: `needs` and each `subagents.<name>`. A `skills` or a `fallback` table the entry gives replaces the library role's whole. [The roles and connections reference](roles-and-connections.md) lists the library file's keys and `index.toml`.

## Where a role's model and effort come from

The first source that gives a value wins, separately for `model` and for `effort`.

1. A value given at submit: `--set ROLE.model=M`, `--set ROLE.effort=E`, or the role's entry in `--values FILE`.
2. The `[[role]]` entry.
3. The library role it names with `use`.
4. `[roles.<lookup name>]` of `.dockingbird/project.toml`, read only when its `harness` is the role's. An empty value there falls through.
5. Your organisation's store, the row of the lookup name and the role's harness, set by `dockingbird org roles set NAME --harness H --model M --effort E`.

A role none of them gives is refused, as `refused: role[N].model: missing`. The lookup name is the role's `kind`, else the name `index.toml` `[defaults]` gives for what the role does: `reviewer` for a role that reviews, `tester` for one that tests, `implementer` otherwise. A role that names a new key, such as `use`, `instructions`, `skills` or `send_to`, tries its own name first, then its library role's name, then those two. The first name with a row in the project file or the store gives the values.

A Claude effort is checked against `low`, `medium`, `high`, `xhigh` and `max` at submit. A Codex effort and every model word reach the tool as given, so a word the tool does not take fails at the agent's first request. [Claude Code and Codex](../../concepts/claude-code-and-codex.md#model-and-effort-per-role) recommends a model and an effort for each kind of role.

## A role's fallback

`[role.fallback]` under a `[[role]]`, or `[fallback]` in a library role file, takes the keys of a config's `[fallback]` table: `harness`, `model`, `effort`, `placement`, `retry_wait`, `retry_max` and `[role.fallback.on]`. [The app.toml reference](app-config.md#keys-of-fallback) lists each key, the error classes and the defaults.

```toml
[[role]]
name = "builder"
harness = "claude"
count = 1
brief = "briefs/builder.md"

[role.fallback]
harness = "codex"

[role.fallback.on]
refusal = "fallback"
```

This table names no `model` or `effort`, so the submit takes them from the `codex` row of the role's lookup names. Name both in the table when no row gives them.

| Rule | Refusal |
|---|---|
| each key is checked as a config's | at `role[N].fallback.<key>` |
| `harness` names the role's own tool | `fallback-same` |
| `model` or `effort` left out takes the fallback tool's row by the role's lookup names: `[roles.<name>]` of the project file when its `harness` is the fallback's, else the store's row of the name and that tool | `fallback-model` when no row gives one |
| `placement = "require-login"` and the role's `hosts` pin a host whose home is not signed in to both tools, as of its last sample | `no-login-host` at `role[N].fallback.placement` |

With `placement = "require-login"`, the fleet also holds the swarm off a host whose home is not signed in to both tools, and `fleet why ID` names the hold `no_fallback_login`. Sign in there with `dockingbird login claude` or `dockingbird login codex`. The role's config carries the table to each of its agents, which follow its rules as an agent started with that config does.

## Values at submit

| Form | Meaning |
|---|---|
| `--set KEY=VALUE` | repeatable; a parameter (`N=4`), a role's setting (`grader.count=6`), a subagent's (`grader.helper.max=4`) or a role's fallback key (`grader.fallback.harness=codex`) |
| `--values FILE` | JSON of the shape `{"params": {...}, "roles": {"ROLE": {...}}}`, a role's subagents under `subagents` and its fallback keys under `fallback` |
| precedence | a `--set` beats the file for the same key; a role's setting given at submit beats the value its entry got from a parameter |
| settable for a role | `count`, `min`, `max`, `model`, `effort`, `compact_at`, `session_hours` |
| settable for a subagent | `model`, `effort`, `max` |
| settable for a role's fallback | `harness`, `model`, `effort`, `placement`; each laid over the role's own table, or making one for a role that names none; a role whose subagent is named `fallback` keeps that subagent's meaning |
| where the values show | `fleet queue` and `fleet why` print the values a submit gave as `values: {values}`; the defaults are not shown |
| a refusal | one `refused: <field>: <rule>` line each, in a fixed order, then exit 1 |

A value's field is `set.<key>` for a `--set` and `values.<path>` for the document, such as `values.roles.grader.count`, and a parameter that gets no value is refused at `params.<name>`. These rules apply to the values themselves.

| Rule | Its words after the field |
|---|---|
| `undeclared` | names no declared parameter, built-in, role or subagent |
| `not-a-setting` | not a setting an invocation may set |
| `not-a-subagent` | names no subagent of that role |
| `twice` | named twice |
| `values-shape` | not the values document's shape: params and roles |
| `not-json` | not a JSON document |
| `range` | outside the parameter's own bounds or words |
| `missing` | missing, for a parameter with no default and no value |
