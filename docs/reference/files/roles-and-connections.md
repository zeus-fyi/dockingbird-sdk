---
title: Role and connection files
summary: The keys of a library role file and the library's index.toml, a service connection file with its argument keys, a reviewed connection catalog, and a subagent block.
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
| `connections` | list of names | the home's connections its agents are granted at start; `fleet submit` refuses a name the home has not recorded (`no-connection`), and an MCP server connection in the list gives the role's agents that server's tools; a role that asks for a repo, a database or a service needs the tools `bus_connections`, `bus_request`, `bus_request_status` and `bus_request_cancel`, which `full` holds and `bus` does not |
| `subagents` | table | one helper kind, `[subagents.NAME]`; a role takes one kind at most |
| `workspace`, `egress`, `allow`, `env` | as in a config | session settings |
| `context` | `kept` or `fresh` | one conversation for every delivery, or a new one for each task delivery |
| `tools` | as in a config | A config takes `bus` (messages and files, the default), `default` (claims and commits) or `full` (both); a swarm role takes `bus`, `full` or a list that keeps every bus tool |
| `harness_config` | a path, or a table by harness | the harness's own settings file, relative to `.dockingbird/roles/`; never expanded |
| `needs` | cpus, memory, pids | the role's resource reservation |
| `compact_at` | `500000`, `500k` or `auto` | the point at which the agent's context compacts; the shipped roles name `300k` for `coordinator` and `hands` and `500k` for the other four |
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
| `timeout_s` | integer, 1 to 86,400 | the most seconds one run may take, then it is stopped; the home's own cap of 7,200 seconds by default applies as well |
| `argv` | list of words, at most 64 | the program's words, each at most 1,024 characters; `{output}` stands once for the output folder and each `{NAME}` for an argument, and every declared argument must be used |
| `arguments` | at most 16 tables | the arguments an agent may fill in, each `[arguments.NAME]` below |
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

## Connection catalog file

`dockingbird connect --config FILE` registers a JSON catalog you reviewed. The file is one object. It must be a regular file of yours that only you can read, with no link in its path. Every other form of `connect` builds the same object itself, so a file you write follows the same keys. Dockingbird refuses an unknown key and never prints its value ([`CONNECTION_INVALID_CONFIG`](../../troubleshooting.md#connection_invalid_config)). A name that is already connected with a different catalog is refused until you disconnect it ([`CONNECTION_CONFIG_CHANGED`](../../troubleshooting.md#connection_config_changed)).

| Key | Type | Meaning |
|---|---|---|
| `connection_id` | UUID version 4 | optional; Dockingbird makes one at the first registration |
| `name` | slug | the connection's name, at most 63 characters; a `NAME` after `--config` must equal it |
| `revision` | integer, 1 or more | optional, default 1 |
| `resources` | list, not empty | what the connection reaches; each `alias` is unique |

Each resource holds three keys.

| Key | Type | Meaning |
|---|---|---|
| `alias` | slug | the name an agent uses for this resource |
| `operations` | list, not empty, no repeats | the operations the resource allows, from its kind's set below |
| `configuration` | object | the resource's settings; its `kind` key names the kind |

| `kind` | Operations | Keys of `configuration` |
|---|---|---|
| `ssh` | `git.fetch`, `git.push` | `repository_id` (UUID version 4), `remote` (`git@HOST:OWNER/REPO.git`, or `ssh://git@HOST[:PORT]/OWNER/REPO.git`), `branch`, `identity` (`file`, the default, or `agent`), `identity_file` (an absolute path, required for `file`, absent for `agent`), `known_hosts` (an absolute path), `host` (default `github.com`), `port` (default 22) |
| `folder` | `folder.read` | `path`, the folder's real path on this computer |
| `postgres` | `db.query`, and `db.execute` when `writes` is true | `host`, `port` (default 5432), `database`, `role`, `password` (true when Dockingbird holds the role's password), `writes` (default false) |
| `service` | `service.run` | `program`, `checkout`, `commit`, `argv` or `call`, `uses`, `timeout_s` as in the service file above, and `arguments`, a list of objects that each hold `name`, `type` and the argument keys below |
| `browser` | `browser.control` | `browser`: `chrome`, `firefox` or `safari` |
| `vault` | `login.fill`, `login.totp` | `manager` (`gopass`), `store`, `logins` |
| `mcp` | `mcp.use` | `url` |

An `ssh` resource with the default host and port needs no `known_hosts`, since Dockingbird pins GitHub's host keys. Any other host or port needs one. The host in `remote` must agree with `host` and `port`. Each entry of a vault's `logins` holds `alias`, `origin`, `username`, `totp` (default false), and, only with `totp`, `code_origin` and `reveal`, a list of at most 4 control texts of 1 to 64 characters. The password and the code stay in the store, so no key of a catalog is a secret. The catalog also accepts the kinds `gcp`, `aws`, `azure`, `digitalocean` and `api`. This page does not cover them.

## How a grant reaches an agent

| Item | Rule |
|---|---|
| who grants | each start of an added config's command, or of a swarm role, grants the connections it names to that session |
| expiry | the session's opening plus its `session_hours`, never past its credential |
| `connect NAME --to AGENT --until ISO` | grants one running agent as well, with the expiry you give |
| `connect NAME --revoke --role ROLE` | a standing denial of the connection to the role, of one swarm with `--swarm KEY`, until `--to-role ROLE --until ISO` lifts it |
| a repo's own config | cannot name a connection; only a config you added can |
| what the agent lists | `bus_connections` gives its grants' ids, operations and aliases, never a credential or a host path |

