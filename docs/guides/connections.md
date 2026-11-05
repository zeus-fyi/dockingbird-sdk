---
title: Connections
summary: A connection lets agents use a GitHub repo, a folder, a database, a program, an MCP server or a browser while the secret stays with Dockingbird.
audience: daily
commands:
  - connect
  - connections
  - revoke
  - disconnect
  - serve
  - serve --unit
  - watch
---

# Connections

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

A connection hands an agent one thing of yours, such as a branch, a folder or a database, and keeps the key or password inside Dockingbird. Below are the seven kinds, each linked to its page, and the commands that record, list, revoke and serve a connection.

## What a connection is

You record a connection once with `dockingbird connect NAME`. The name is lowercase letters, digits and hyphens. Dockingbird keeps whatever opens the thing: a copy of an ssh key, a database password, a vault passphrase. The agent never sees it. When an agent needs the thing, it asks Dockingbird for one action through `bus_request`, such as a fetch, a query or a run. Dockingbird does it and sends back the result.

A config lists the connections its agents may use, as `connections = ["github"]`. Only a config you added with `dockingbird config add` may do that. A repo's own config that names a connection is refused when it starts, and the refusal names the step to add it instead. Each start of an added config's command grants its connections to that agent's session for at most its `session_hours`. A name you have not recorded, or have disabled, stops the start.

## The seven kinds

| Kind | Command | What the agent gets | Page |
|---|---|---|---|
| GitHub repo | `connect NAME --github OWNER/REPO` | a fetch and a push of one branch | [github.md](github.md) |
| Folder | `connect NAME --folder PATH` | a folder of this computer, read-only unless the config says `write` | this page |
| Database | `connect NAME --database URL` | one SQL statement at a time, and its rows | [databases.md](databases.md) |
| Service | `connect NAME --service FILE` | a run of your program with arguments you allow | [mcp-and-services.md](mcp-and-services.md) |
| MCP server | `connect NAME --mcp URL` | the server's tools inside the agent's harness | [mcp-and-services.md](mcp-and-services.md) |
| Browser | `connect NAME --browser chrome` | Chrome, Firefox or Safari of this Mac, lent while you serve it | [mcp-and-services.md](mcp-and-services.md) |
| Vault | `connect NAME --vault gopass` | a sign-in that Dockingbird types into the lent browser | [secrets-vault.md](secrets-vault.md) |

A GitHub connection copies your ssh key, without its passphrase, into Dockingbird's own volume, or uses your Mac's ssh-agent. Agents fetch and push the one branch you connected and never hold the key. The page [github.md](github.md) covers deploy keys, grants and a push that stopped midway.

A folder connection mounts one folder of this computer at `/dockingbird/folders/NAME` from the agent's next start. The agent reads there and cannot write, rename or delete unless its config holds a `[folders]` table with `NAME = "write"`. Reads are not logged, the grant is. The details follow in the steps below.

A database connection is PostgreSQL only. Dockingbird keeps the role's password and opens the database itself, so the agent sends a statement and reads rows from a file. A role that can write is refused unless you register the database with `--writes`. The page [databases.md](databases.md) has the role's SQL and the write path.

A service connection names a program of yours in a TOML file. The program runs on this computer, as you, only while `dockingbird serve NAME` runs, with the arguments the file allows. The page [mcp-and-services.md](mcp-and-services.md) shows the file.

An MCP server connection registers a streamable-HTTP server by URL for the roles of a swarm that list its name. Each of their agents gets the server's tools beside Dockingbird's own at every start.

A browser connection lends Chrome, Firefox or Safari of this Mac to one agent at a time. An added config with `browser = "chrome"` instead gets a Chrome of Dockingbird's own in a container, with no connection and nothing on your Mac.

A vault connection points at a gopass store. Dockingbird types the stored password and one-time code into the lent browser, and the agent sees neither. The page [secrets-vault.md](secrets-vault.md) shows the store.

## Before you start

- Dockingbird is set up. `dockingbird status` must not print "Dockingbird isn't set up yet."; `dockingbird login claude` does the set-up from any folder.
- A GitHub connection runs inside a git checkout, on the branch the agents work on. Every other kind runs from any folder.
- A folder connection needs the folder under a path Docker Desktop shares, which its Settings > Resources > File sharing lists.

## Steps

1. Record a folder of this computer. Dockingbird refuses a link, the root of the disk and its own folder.

   ```bash
   dockingbird connect notes --folder ../notes
   ```

   The step is done when the command prints these lines.

   ```text
   Connected notes: agents of a config that names it read it, read-only unless
   the config gives them write access, at /dockingbird/folders/notes.
   ```

2. Write a config that names it. In this file the agents get write access to the folder and work in an empty scratch folder.

   ```toml
   command = "analyst"
   workspace = "scratch"
   connections = ["notes"]

   [folders]
   notes = "write"
   ```

3. Add the config, then start its command. Dockingbird locks nothing in a folder, so when two agents hold write access to it, the last write wins.

   ```bash
   dockingbird config add analyst.toml
   dockingbird start --command analyst "Read /dockingbird/folders/notes and write analysis.md there."
   ```

   The step is done when the two commands print these lines.

   ```text
   Registered analyst: dockingbird analyst "task" (connections: notes)
   analyst-1 started in a scratch folder.
   ```

4. List your connections. Bare `connections` prints each enabled name. Give it a name and it adds the permitted operations, each agent's grant and expiry, and the newest requests.

   ```bash
   dockingbird connections
   dockingbird connections notes
   ```

   The second command is done when it prints the folder's line, then one `Agent:` line for each agent granted it.

   ```text
   Read-only: <path>
   Agent: analyst-1; <state>; until <time>
   ```

5. Take a connection from one agent, or from everyone. A revoke refuses that agent's new and waiting requests, and an agent already running finishes. A disconnect stops new grants and deletes Dockingbird's copy of any key. Your own key files stay.

   ```bash
   dockingbird revoke notes --to analyst-1
   dockingbird disconnect notes
   ```

   A folder cannot be taken from a running agent, so for a folder both commands stop the agent and name the command that continues it. The revoke prints these lines.

   ```text
   Revoked analyst-1's access to notes and stopped analyst-1: a folder can't be
   taken away from a running agent.
   Continue it: dockingbird analyst --as analyst-1
   ```

   For any other kind, `revoke` prints `Revoked analyst-1's access to NAME.` and `disconnect` prints `Disconnected NAME.`

6. Serve a service, a browser or a vault as yourself. Until this runs in a terminal, `dockingbird status` shows the agent's request as waiting.

   ```bash
   dockingbird serve convert
   ```

   The step is done when the command prints this line. The page [mcp-and-services.md](mcp-and-services.md) covers `serve --all` and `serve --unit`, which keep serving with no terminal open.

   ```text
   Serving convert: agents' requests to it run here, as you, one at a time.
   Ctrl-C stops it.
   ```

7. Watch the browser of an agent whose config says `browser = "chrome"`. The command prints a `vnc://127.0.0.1` address and the browser's own password, then opens Screen Sharing. The agent can read anything you type there.

   ```bash
   dockingbird watch surf-1
   ```

   The step is done when the command prints these lines. Close the viewer or press Ctrl-C to stop.

   ```text
   Opening surf-1's browser, vnc://127.0.0.1:<port>, in your VNC viewer.
   Anything you type or paste into this browser is visible to the agent surf-1,
   which reads the page. Sign in to nothing you would not hand it.
   VNC password: <the browser's own password>
   ```

## Grants to a swarm role

Dockingbird also grants and denies a connection by the role of a swarm, for the agents of one swarm or all of them.

```bash
dockingbird connect scores --revoke --role grader
dockingbird connect scores --to-role grader --until 2026-12-01T00:00:00+00:00
```

The first command stops every running agent of the role from using `scores` at its next request, with no restart. It also keeps the connection from any agent of the role that starts later. The second lifts that denial and grants the connection to the role's running agents until the time you give. Add `--swarm KEY` to narrow either one to a single swarm. Done when they print `scores: denied to role grader` and `scores: granted to role grader until <time>, <n> running agents`.

## When it fails

- [`CONNECTION_UNKNOWN_CONNECTION`](../troubleshooting.md#connection_unknown_connection): the config names a connection that `dockingbird connections` does not list, so the start stopped.
- [`CONNECTION_INVALID_NAME`](../troubleshooting.md#connection_invalid_name): the name holds a capital, a space or a character beyond letters, digits and hyphens.
- [`CONNECTION_CONFIG_CHANGED`](../troubleshooting.md#connection_config_changed): you connected an existing name again with another repo, branch or key. Run `dockingbird disconnect NAME` first.
- [`CONNECTION_UNKNOWN_AGENT`](../troubleshooting.md#connection_unknown_agent): no running agent has that name. `dockingbird status` lists the running ones.
- [`CONNECTION_UNKNOWN_GRANT`](../troubleshooting.md#connection_unknown_grant): the agent holds no unrevoked grant for that connection, so `revoke` had nothing to take.
- [`CONNECTION_INVALID_UNTIL`](../troubleshooting.md#connection_invalid_until): the `--until` time is past, or lacks a timezone such as `+00:00`.
- [`CONNECT_FOLDER_INVALID`](../troubleshooting.md#connect_folder_invalid): the path is missing, a link, the whole disk or Dockingbird's own folder.
- [`WATCH_NO_BROWSER`](../troubleshooting.md#watch_no_browser): the agent has no browser running in a container. Its config asks for none, or its container stopped.
- [`START_FOLDER_MISSING`](../troubleshooting.md#start_folder_missing): the folder moved or was deleted since you connected it. Connect it again at its new path.
- [`CONNECT_ARGUMENTS_REQUIRED`](../troubleshooting.md#connect_arguments_required): `connect` got no name, or two kinds at once.
- [`CONFIG_INVALID_FILE`](../troubleshooting.md#config_invalid_file): a repo's own config names a connection. Move the file out of `.dockingbird/` and run `dockingbird config add` on it.

Related pages: [your-own-commands.md](your-own-commands.md) for configs, [delegating-tasks.md](delegating-tasks.md) for the tasks agents get, and [../concepts/security-model.md](../concepts/security-model.md) for what agents can reach.
