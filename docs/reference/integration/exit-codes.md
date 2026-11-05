---
title: Exit codes
summary: The one table of the exit statuses a dockingbird command ends with, and what a script does on each.
audience: integrator
commands:
  - dockingbird claude
  - dockingbird codex
  - dockingbird init --check
  - dockingbird org login
  - dockingbird org create
  - dockingbird fleet submit
  - dockingbird fleet run
  - dockingbird fleet update
  - dockingbird fleet worker
  - dockingbird fleet admitter
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../../llms.txt).

# Exit codes

Every dockingbird command ends with one exit status, also called an exit code, and under `--json` the last envelope repeats it as `exit_code` ([the envelope](json.md)).
A message's id says what happened and its status says how the command ended, so a script reads both; [the catalogue](../../troubleshooting.md) lists every id.
`ok` in the envelope is `true` only when the status is 0.

| Status | Meaning | When | What a script does |
|---|---|---|---|
| 0 | done | the command did what was asked, or had nothing to do (`stop` and `clean` on a computer that is not set up) | goes on |
| 1 | a problem Dockingbird printed, with its next step | a refused start, a `sync` that could not do what was asked, `init --check` finding a file that is not the running release's, `clean` with no terminal to ask on, a `fleet update` step that failed | reads `id` and `next_step` from the envelope, runs the next step or stops, and never repeats the same command unchanged |
| 2 | usage | a word, an option or a value the command does not take: a bad `--as` name, `--home` together with `DOCKINGBIRD_HOME`, a `DOCKINGBIRD_` variable no command reads, a `fleet update` refused before it runs (a release tag that does not exist, a host with no `repoint` line) | fixes the command line, since a retry cannot succeed |
| the tool's own | `dockingbird claude` and `dockingbird codex` end with Claude Code's or Codex's status once the tool has started; 0 when the agent keeps working without a terminal; 1 when Dockingbird stopped before starting it | the tool's own run ended | treats the status as the tool's result; a tool that exits 3 gives an envelope with `"ok": false` and `"exit_code": 3` |
| 69 | the organisation's store did not answer | a fleet scheduler command whose database is down, restarting or out of connections; the message names the database's host, the role tried and the connection's own words | retries after a delay and checks the network and the database; a `fleet worker` or `fleet admitter` under a service manager exits 69 and is started again by it |
| 77 | a login the store's roles refuse for this command | `org create` by a role that is not a member of `fleet_admin`; `fleet update` by a login that is not a member; `fleet submit` or `fleet run` by a person who is not a member of the project's group, with nothing recorded | asks an admin to run `dockingbird org members add PERSON --project SLUG`, or runs the command as `fleet_admin` |
| 78 | a fleet refusal: no usable login | no org login on this computer; a kind of command with no role in `org.toml`; a role with no line in `~/.pgpass`; a login the database turns down (wrong password, a role or database it lacks) or an error code once connected; a `fleet.toml` that holds a `password` | runs the login the message names, `dockingbird org login HOST --as user --role ROLE`, then repeats the command |

A script treats exit code 78 as "log in first": it runs the `org login` line the message names and repeats the command. Exit code 77 means the login is not the admin's. Exit code 69 means the store did not answer.


`fleet run` ends with the status of the command it ran, 124 when its `--bound` interrupts the command, and 1 when no lease was taken within `--wait`.
The scheduler's login and role rules are in [the org file](../files/org-file.md) and [the team fleet guide](../../guides/team-fleet.md).

## Where the table is used

| Page | What it says about exit statuses |
|---|---|
| [json.md](json.md) | the `exit_code` key of the envelope and the streams a message uses |
| [compatibility.md](compatibility.md) | statuses 0, 1, 2, the tool's own, 69, 77 and 78 are a surface you can build on |
| [commands.md](../commands.md) | the statuses each command can end with |
| [the fleet scheduler guide](../../guides/fleet-scheduler.md) | the refusals the scheduler's commands end 77 and 78 on |
