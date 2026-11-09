---
title: A swarm from a role library
summary: Submit a coordinator and four graders built from library roles, with helpers, values at submit and scores written through the broker.
audience: team-admin
commands:
  - fleet describe
  - fleet submit --set
  - fleet submit --values
  - fleet add
  - fleet retire
  - connect
  - serve
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# A swarm from a role library

This cookbook queues a swarm that takes its roles from a library and its sizes, models and efforts from each submit. A coordinator comes from Dockingbird's shipped roles. Four graders come from the project's own `grader` role. Each grader takes ideas from a database, researches each one on the web with an MCP server and its own `helper` subagents, scores it, and writes the score back through the broker. The agents never hold the database password.

It shows five things.

- A role written once as a library file with its texts, `.dockingbird/roles/grader.toml`, and used by name with `use = "grader"`. The coordinator is the shipped library's, `use = "dockingbird/coordinator"`.
- Declared parameters, `[params]`: `N`, `x`, `y`, `batch`, `effort` and `model`. They bind to roles' fields and to the words of the grader's brief.
- Values per role and per subagent at submit, as `--set` lines or as a values document, [graders.json](graders.json).
- Who may message whom with `send_to`. A grader reaches the coordinator and its parent, never another grader.
- Connections a role names: an MCP server, a database the broker writes through, and two Python functions the broker runs with the database's credential in their environment.

## Before you start

- The pool and your org login work, as [the team fleet guide](../../docs/guides/team-fleet.md) sets up. `dockingbird org status` ends with `Connected as {role}.`
- A home of the pool links a checkout of your repository. [The swarms guide](../../docs/guides/swarms.md) lists this as a prerequisite.
- A PostgreSQL database named `ideas` with the tables the brief names, and a role `grader` for it.
- The two functions, `insert_score` and `next_ideas`, exist in a checkout at the commit the connection files name.

`project = "example"` and the source `example-org/example-app` in the definition are placeholders. Copy the `.dockingbird/` folder into your repository's own, and write your project and repository in their place.

## The files

| File | What it holds |
|---|---|
| `.dockingbird/swarms/graders/swarm.toml` | the definition: the parameters, the `coord` role and the `grader` role |
| `.dockingbird/roles/grader.toml` | the grader role: harness, texts, tools, connections and the `helper` subagent |
| `.dockingbird/roles/grader/brief.md` | the grader's first task, the loop; `N`, `x`, `y` and `batch` expand in it |
| `.dockingbird/roles/grader/rules.md` | the grader's rules, added after Dockingbird's own and the project's |
| `.dockingbird/roles/grader/helper.md` | the helper's prompt; its first line is its description |
| `.dockingbird/connections/insert-score.toml` | the brokered write: the `insert_score` function and its arguments |
| `.dockingbird/connections/next-ideas.toml` | the brokered read: the `next_ideas` function and its argument |
| `graders.json` | a values document for `--values` |

[The role and connection reference](../../docs/reference/files/roles-and-connections.md) lists every key of the role and connection files. Both connection files give each argument its bounds with `minimum` and `maximum`.

## 1. Register the connections

Register the four connections once for each pool home. No file holds a secret. The database's password is asked for without echo and kept by the broker.

```bash
dockingbird connect search --mcp https://search.example/mcp
dockingbird connect scores --database postgres://grader@db.example.net:5433/ideas --password --writes
dockingbird connect insert-score --service .dockingbird/connections/insert-score.toml
dockingbird connect next-ideas --service .dockingbird/connections/next-ideas.toml
```

`--writes` lets a grader write through the broker with `db.execute`, a statement the broker runs on its own connection. The two services are the same write and read as your own code. The two forms are alternatives granted together to show both. For least privilege, leave `scores` off the role and keep the two services. The step is done when each command prints its connected line. The database one reads as the first line below, and each service as the second.

```text
Connected scores: {target} as {value}, which may write, checked from Dockingbird.
Connected insert-score: agents of a config that names it run {path} here, as you,
with the arguments it declares, when you run dockingbird serve insert-score.
```

## 2. Serve the two services

A service runs only while `serve` runs. `serve --all` serves every service and browser connection of the home in one process. `serve --unit` prints the unit that keeps it running under the machine's service manager, a launchd property list on a Mac and a systemd user unit on Linux. It installs nothing, so a swarm's brokered commands run with no terminal open once you install the unit.

```bash
dockingbird serve --all
dockingbird serve --unit
```

The step is done when `serve` for a service prints its ready line. `serve --all` with no service or browser connection ends 1 and says `Nothing to serve: this home has no service or browser connection.`

```text
Serving insert-score: agents' requests to it run here, as you, one at a time.
Ctrl-C stops it.
```

## 3. Describe what a submit takes

```bash
dockingbird fleet describe graders
```

It prints, as JSON, every parameter and every role's settable field with its type, its bounds or words, its default and where the default comes from. It connects to nothing, and its defaults alone are a values document that `--values` takes. The step is done when the document prints.

## 4. Submit the swarm

The first submit gives values per role and per subagent as `--set` lines.

```bash
dockingbird fleet submit graders \
  --set coord.model=MODEL --set coord.effort=xhigh \
  --set grader.count=4 --set grader.model=MODEL --set grader.effort=xhigh \
  --set grader.helper.model=MODEL --set grader.helper.effort=xhigh --set grader.helper.max=4
```

Write a model word of the role's tool in place of each `MODEL`. [Claude Code and Codex](../../docs/concepts/claude-code-and-codex.md#model-and-effort-per-role) names a model for each kind of role, and `xhigh` is the coordinator's recommended effort.

The second reads the counts, the efforts and the helpers' cap from a file. It names no model, so each role takes its model from `[roles.NAME]` of the project file, else from your organisation's store: `coord` by its name, then `coordinator`, the shipped role it uses.

```bash
dockingbird fleet submit graders --values graders.json
```

The third takes the definition's defaults through its own parameters, `N` graders, `y` helpers each, `effort` and `model`.

```bash
dockingbird fleet submit graders
```

`--set N=4 --set y=4 --set effort=xhigh --set model=MODEL` sets the parameters in place of the roles' fields. A `--set` beats the file's value for the same key. The definition has no `key`, so each submit queues a new swarm named `graders-` and the UTC time. `--key K` names one, and a repeated `--key K` answers the swarm it queued first. Each submit is done when it prints this line.

```text
{id} pending, position {position}
```

## 5. Scale it while it runs

Add two graders, then retire one. Each stays within the role's `min` and `max`, and a retire waits for the agent's running turn to end.

```bash
dockingbird fleet add ID grader --count 2
dockingbird fleet retire ID NAME
```

To start larger, set `--set grader.count=6 --set grader.max=12` at the submit. Both commands print their result line.

```text
{id} running: added {names}; each starts once its host has room
{id} running: {name} retires at the first tick that finds it idle
with no question open and no request it has not taken yet; a tick
that finds it working or with either refuses the ask, and the
next fleet retire says so
```

## 6. Revoke and give back a connection

This stops every grader's next call to `insert-score` at once, with no restart. It keeps the connection from graders that start later until you lift it.

```bash
dockingbird connect insert-score --revoke --role grader
dockingbird connect insert-score --to-role grader --until ISO
```

```text
insert-score: denied to role grader
insert-score: granted to role grader until {until}, {count} running agents
```

## The note on x

Dockingbird runs one harness session per container, so `x`, the main agents in one grader's container, can only be 1. The definition pins it with its own bounds. More graders is `N`.

## When it fails

These ids come from the submit, the connections and `serve`. Each line says what the id means and what to do.

- [`FLEET_REFUSED`](../../docs/troubleshooting.md#fleet_refused) names a field of the definition and the rule it breaks, one line for each rule. Fix them all, then submit again.
- [`FLEET_NO_CONNECTION`](../../docs/troubleshooting.md#fleet_no_connection) holds the swarm because its home lacks a connection a role lists. Connect it there, then run `fleet release ID`.
- [`CONNECT_SERVICE_INVALID`](../../docs/troubleshooting.md#connect_service_invalid) means a service file has a key or a value that Dockingbird refuses. Nothing was saved.
- [`CONNECT_SERVICE_CHECKOUT_MOVED`](../../docs/troubleshooting.md#connect_service_checkout_moved) means the checkout is not at the commit the file names. Check that commit out, or name the commit it is at.
- [`CONNECT_MCP_INVALID`](../../docs/troubleshooting.md#connect_mcp_invalid) means the MCP address is not an `https` address of the allowed form. The command ends 2.
- [`SERVE_CHECKOUT_MOVED`](../../docs/troubleshooting.md#serve_checkout_moved) means the checkout moved after the connection was made, so nothing ran.
- [`FLEET_RETIRE_REFUSED`](../../docs/troubleshooting.md#fleet_retire_refused) means the swarm is not running, the agent is unknown, or the role is at its `min`.
