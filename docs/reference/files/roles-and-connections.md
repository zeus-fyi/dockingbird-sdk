---
title: Role and connection files
summary: The keys of a library role file and the library's index.toml, a service connection file with its argument keys, and a subagent block.
audience: team-admin
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../../llms.txt).

# Role and connection files

A role library holds the settings a swarm role reuses, and a service connection file says what a brokered program runs and what an agent may choose. Both live in your repository's `.dockingbird/` folder. [The swarm definition reference](swarm-definition.md) shows how a role names a library file, and [the cookbook on role libraries](../../../examples/swarm-from-a-role-library/README.md) uses both.

## Library role file

`.dockingbird/roles/NAME.toml` is a role a definition names with `use = "NAME"`, and `use = "dockingbird/NAME"` names the shipped file of that name. Paths in it are relative to `.dockingbird/roles/`. `{{name}}` expands in its string values and its texts, a parameter of the definition or a built-in such as `{{swarm}}`, whether or not the definition declares `[params]`.

| Key | Type | Meaning |
|---|---|---|
| `name` | slug | optional; when given, the file's own name, else `use-name` |
| `harness` | `claude` or `codex` | the tool the agents run |
| `model`, `effort` | string | the role's model and effort; the shipped roles name neither, so the project file or your organisation's store gives them |
| `brief` | path | the Markdown file of the first task |
| `instructions` | path | text added after Dockingbird's rules and the project's, never in place of them |
| `connections` | list of names | the home's connections its agents are granted at start |
| `subagents` | table | one helper kind, `[subagents.NAME]`; a role takes one kind at most |
| `workspace`, `egress`, `allow`, `env` | as in a config | session settings |
| `context` | `kept` or `fresh` | one conversation for every delivery, or a new one for each task delivery |
| `tools` | as in a config | A config takes `bus` (messages and files, the default), `default` (claims and commits) or `full` (both); a swarm role takes `bus`, `full` or a list that keeps every bus tool |
| `harness_config` | a path, or a table by harness | the harness's own settings file, relative to `.dockingbird/roles/`; never expanded |
| `needs` | cpus, memory, pids | the role's resource reservation |
| `compact_at` | `500000`, `500k` or `auto` | the point at which the agent's context compacts |
| `session_hours` | integer, 1 to 168 | how long each agent may run |
| `skills` | table of `path` and `into` | skills its agents' tool lists as its own, as a config's `[skills]` takes them; each `path` is from the top of the swarm's source, not from `.dockingbird/roles/`; see [skills.md](../../guides/skills.md) |
| `[fallback]`, `[fallback.on]` | tables | the tool its agents move to after a failed turn, and each error class's rule, as a config's `[fallback]` takes them; see [app-config.md](app-config.md#keys-of-fallback) |

A `[[role]]` entry that uses the file replaces each key it gives. `needs` and each `[subagents.NAME]` table merge field by field instead, the entry's field winning. An entry's `skills` or `fallback` replaces the file's whole table.

| Not allowed in a library file | Why |
|---|---|
| `use`, `count`, `min`, `max`, `send_to`, `reviews`, `tests`, `kind`, `args` | they belong to a swarm's own `[[role]]` |
| `system_prompt`, `append_system_prompt`, `developer_instructions`, `rules` | they would change a layer Dockingbird injects, so they are refused (`fixed-prompt`) |

## The library's index

`.dockingbird/roles/index.toml` lists the library's roles and the names a role is looked up by. `dockingbird init` installs the shipped one.

```toml
roles = ["coordinator", "implementer", "reviewer", "tester", "reader", "hands"]

[defaults]
reviews = "reviewer"
tests = "tester"
otherwise = "implementer"
```

| Key | Meaning |
|---|---|
| `roles` | the library's roles; `init` writes one `[roles.NAME]` table into `.dockingbird/project.toml` for each |
| `[defaults]` `reviews` | the name a role that reviews and names no `kind` looks its model and effort up by |
| `[defaults]` `tests` | the same for a role that tests |
| `[defaults]` `otherwise` | the same for every other role |

The shipped index is read first, and the project's replaces each key it gives. An empty value in the project's `[defaults]` gives no name for that kind of role, so such a role needs a model and an effort from another source. A `use` reads the role's file by its name, whether or not `roles` lists it.

## Subagent block

`[subagents.NAME]` is one helper that the role's harness runs, with its own settings. A role holds one such table at most (`one-subagent-kind`).

| Key | Type | Meaning |
|---|---|---|
| `instructions` | path | required; the helper's own text; the first line is the helper's description |
| `model` | string | the helper's model; left out, the role's own |
| `effort` | string | the helper's effort; left out, the tool's default |
| `max` | integer, 0 to 20 | how many helpers run at once; `0` denies the helper tool; left out, the tool's own cap |
| `tools` | list of tool names | the tool's own tools the helper may use; left out, the role's |

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
