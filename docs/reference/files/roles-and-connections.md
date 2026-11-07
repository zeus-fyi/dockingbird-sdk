---
title: Role and connection files
summary: The keys of a library role file, a service connection file with its argument keys, and a subagent block.
audience: team-admin
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../../llms.txt).

# Role and connection files

A role library holds the settings a swarm role reuses, and a service connection file says what a brokered program runs and what an agent may choose. Both live in your repository's `.dockingbird/` folder. [The swarm definition reference](swarm-definition.md) shows how a role names a library file, and [the cookbook on role libraries](../../../examples/swarm-from-a-role-library/README.md) uses both.

## Library role file

`.dockingbird/roles/NAME.toml` is a role a definition names with `use = "NAME"`. Paths in it are relative to `.dockingbird/roles/`.

| Key | Type | Meaning |
|---|---|---|
| `harness` | `claude` or `codex` | the tool the agents run |
| `model`, `effort` | string | the role's model and effort |
| `brief` | path | the Markdown file of the first task; `{{name}}` expands a parameter of the definition |
| `instructions` | path | text added after Dockingbird's rules and the project's, never in place of them |
| `connections` | list of names | the home's connections its agents are granted at start |
| `subagents` | tables | helper kinds, one `[subagents.NAME]` each |
| `workspace`, `egress`, `allow`, `env` | as in a config | session settings |
| `tools` | as in a config | A config takes `bus` (messages and files, the default), `default` (claims and commits) or `full` (both); a swarm role takes `bus`, `full` or a list that keeps every bus tool |
| `needs` | cpus, memory, pids | the role's resource reservation |
| `compact_at` | `500000`, `500k` or `auto` | the point at which the agent's context compacts |
| `session_hours` | integer, 1 to 168 | how long each agent may run |
| `skills` | table of `path` and `into` | skills its agents' tool lists as its own, as a config's `[skills]` takes them; each `path` is from the top of the swarm's source, not from `.dockingbird/roles/`; see [skills.md](../../guides/skills.md) |

| Not allowed in a library file | Why |
|---|---|
| `use`, `count`, `min`, `max`, `send_to`, `reviews`, `tests`, `kind`, `args` | they belong to a swarm's own `[[role]]` |
| `system_prompt`, `append_system_prompt`, `developer_instructions` | the fixed prompt keys are refused |

## Subagent block

`[subagents.NAME]` is one helper that the role's harness runs, with its own settings.

| Key | Type | Meaning |
|---|---|---|
| `instructions` | path | the helper's own text; the first line is the helper's description |
| `model`, `effort` | string | the helper's model and effort |
| `max` | integer | how many helpers run at once |

## Service connection file

`.dockingbird/connections/NAME.toml` is registered with `dockingbird connect NAME --service FILE`. The file must be yours, readable by you alone, not a link and not inside `DOCKINGBIRD_HOME`. `connect` checks every key, that `argv` uses each argument the file declares, and that the checkout is at its commit. It runs nothing.

| Key | Type | Meaning |
|---|---|---|
| `program` | absolute path | the program that runs, with `argv` |
| `checkout` | absolute path | the program's checkout; give it with `commit` or give neither |
| `commit` | string | the commit the checkout must be at; `serve` refuses to run once the checkout moved |
| `timeout_s` | integer | the most seconds one run may take, then it is stopped |
| `argv` | list of words | the program's words; `{output}` stands once for the output folder and each `{NAME}` for an argument |
| `uses` | list with one name | a database connection of the home whose credential each run gets as `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER` and `PGPASSWORD`, never in a file, a log or an agent |
| `[call]` | table | in place of `argv`, a Python function in the checkout |
| `[call]` `python` | path | the interpreter, relative to the checkout |
| `[call]` `module` | string | the module that holds the function |
| `[call]` `function` | string | the function; it is called with the checked arguments as keyword arguments, and its return value, as JSON, is the run's `result.json` |

## Argument keys

Each argument the agent may choose is a table `[arguments.NAME]`, or an inline table under `[arguments]`.

| Key | Used by | Meaning |
|---|---|---|
| `type` | all | `int`, `text` or `choice` |
| `minimum` | `int` | the lowest whole number allowed |
| `maximum` | `int` | the highest whole number allowed |
| `choices` | `choice` | the list of words the agent may pick |
| `max_chars` | `text` | the longest text allowed |

A `text` argument reaches the program as the agent typed it. A program that reads one as a path or a command name gives the agent that reach, so declare `choice` or `int` where the program takes a path, a name or a mode.

## How a run behaves

| Item | Rule |
|---|---|
| process | the program alone, never through a shell, in its checkout |
| environment | `PATH`, your `HOME`, `LANG=C.UTF-8`, a `TMPDIR` of its own and `DOCKINGBIRD_SERVICE_OUTPUT`, the output folder's path |
| timeout | past `timeout_s` it gets `SIGTERM`, then `SIGKILL` 10 seconds later |
| output | the output folder is the result, with `stdout.txt` and `stderr.txt`, at most 64 MiB and 10,000 entries, links left out |
| where it lands | in the asking agent's log folder under `log/connections/<job>/` |
| who runs it | `dockingbird serve NAME`, as you, one request at a time, oldest first |
