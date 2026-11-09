---
title: Connections
summary: A connection lets agents use a GitHub repo, a folder, a database, a program, an MCP server or a browser while the secret stays with Dockingbird; this page lists every connect option, how a request is brokered, and how access ends.
audience: daily
commands:
  - connect
  - connect --config
  - connect --to
  - connect --revoke
  - connect --to-role
  - connections
  - connections --release
  - revoke
  - disconnect
  - serve
  - serve --once
  - serve --unit
  - watch
---

# Connections

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

A connection hands an agent one thing of yours, such as a branch, a folder or a database, and keeps the key or password inside Dockingbird. This page lists the seven kinds, every `connect` option, how a request reaches the thing without the agent holding the secret, and the commands that grant, list, revoke and serve a connection.

## What a connection is

You record a connection once with `dockingbird connect NAME`. The name is lowercase letters, digits and hyphens, at most 63 characters. Dockingbird keeps whatever opens the thing: a copy of an ssh key, a database password, a vault passphrase. The agent never sees it. For a repo, a database, a program, a browser or a sign-in, the agent asks Dockingbird for one action through `bus_request`, such as a fetch, a query or a run. Dockingbird does it and sends back the result. A folder and an MCP server need no request: the folder is a mount, and the server's tools sit in the agent's harness.

A config lists the connections its agents may use, as `connections = ["github"]`. Only a config you added with `dockingbird config add` may do that. A repo's own config that names a connection is refused when it starts, with [`START_PROJECT_CONNECTIONS`](../troubleshooting.md#start_project_connections), and the refusal names the step to add it instead. Each start of an added config's command grants its connections to that agent's session for at most its `session_hours`. A name you have not recorded, or have disabled, stops the start.

A home holds at most 500 enabled connections. `connect` of a new name past that refuses with [`CONNECTION_TOO_MANY`](../troubleshooting.md#connection_too_many) and saves nothing. `dockingbird disconnect NAME` frees a place.

## How a secret is brokered

The agent holds a grant and no secret. Four parts keep it that way: where the secret lives, who checks each request, what comes back, and how access ends.

### Where the secret lives

`connect` writes two records. The registration, which names the repo, the branch, the server or the program and holds no secret, is a file in `connections/` of your Dockingbird home, readable by you alone. The secret goes to the coordinator, the one container that holds every credential of the home. A GitHub key copy, a database password and a vault passphrase live in the coordinator's store, in a Docker volume that no agent mounts.

A secret you type or point at reaches the coordinator through a container's standard input. It never appears in an argument, a container environment, `docker inspect`, a log or a file on your Mac. The coordinator has no network, except ssh to the hosts of your GitHub connections through a relay. The page [security-model.md](../concepts/security-model.md) shows the rest of the boundary.

Four kinds keep no secret: a folder, a service without `uses`, a browser and an MCP server. What they give is reach, and the limits below name it.

| Kind | What Dockingbird keeps | Where |
|---|---|---|
| GitHub repo | a copy of the key your ssh uses for GitHub, without its passphrase, or none with `--agent` | the coordinator's store, removed by `disconnect` and `clean --all` |
| Database | the role's password, when you give `--password` | the coordinator's store |
| Vault | the gopass store's passphrase; the store itself stays under `vaults/` in your home | the coordinator's store |
| Service | nothing; the program stays on your Mac | none |
| Folder | nothing; the path is recorded | none |
| Browser | nothing | none |
| MCP server | the server's URL; a server that needs a key is not served | none |

### Who checks each request

Dockingbird grants a connection to one session, at its start, from an added config or a swarm role. The grant is bound to that session and expires at its `session_hours` or when its credential ends. The agent lists its grants with `bus_connections`, which shows each grant's id, operations and resource aliases, and never a credential or a path of your Mac.

To use one, the agent calls `bus_request` with the grant id, the connection id, an operation and a resource alias, and polls `bus_request_status`. `bus_request_cancel` withdraws a request that has not started, and a started effect cannot be undone. The coordinator admits each request once and checks the live grant again when it dispatches the job. A change at the broker therefore takes effect on the agent's next request, with no restart. A refused request answers one of `CREDENTIAL_GRANT_REVOKED`, `CREDENTIAL_GRANT_EXPIRED`, `CREDENTIAL_CONNECTION_DISABLED`, `CREDENTIAL_CATALOG_CHANGED` or `CREDENTIAL_ROLE_DENIED`.

The tools are part of the agent's tool set. `bus_connections`, `bus_request`, `bus_request_status` and `bus_request_cancel` sit in the `default` and `full` sets and not in `bus`, which is a config's default. A config that names a GitHub, database or service connection therefore needs `tools = "default"` or `tools = "full"`, and a swarm role needs `full` or a list that holds those four tools beside every bus tool. A browser of this Mac, lent through `connect --browser`, needs `full`, since only `full` holds the browser tools without a `browser` key. A folder and an MCP server need no tool. [The agent tools page](../reference/agent-tools.md) lists the sets and each tool's arguments.

The agent's text never reaches a command line, a URL or a branch name. It names a grant, an operation and an alias. The remote, the host, the port and the branch come from the registration you made.

| Operation | Connection | What the agent sends | What it receives |
|---|---|---|---|
| `git.fetch` | GitHub repo | the alias, and optionally `have`, a commit it holds | a bundle file in its log folder, with the head, the ref, the sha256 and the size; the last 2 bundles of a session are kept |
| `git.push` | GitHub repo | the alias | the published head; Dockingbird pushes the shared branch's head, never the agent's working copy, and needs a fetch of that connection first |
| `db.query` | database | one SQL statement that returns rows, its `arguments` and `rows` | a JSON-lines file in its log folder |
| `db.execute` | database added with `--writes` | one statement, its `arguments` and `rows` | the rows the statement returns, in the same file form |
| `service.run` | service | the arguments the service file declares | a folder under `log/connections/<job>/` |
| `browser.control` | browser | the browser tools of the harness | the page, and the screenshots the tools return |
| `login.fill`, `login.totp` | vault | the `browser_login` tool's login name and page address | the page the sign-in reached, or a refusal in words |
| `folder.read`, `mcp.use` | folder, MCP server | nothing; the mount and the harness's own client are the use | files at `/dockingbird/folders/NAME`, or the server's tools |

A session keeps its last 8 query results and service folders. Older ones are removed from its log folder.

### What the agent can and cannot read

The agent can read the result of each request, the names of its grants, the words of each refusal and, for a folder, the files you mounted. It cannot read the key, the password, the passphrase, a database's address, the path of a key file, or another agent's grants. A message, a payload or an artifact it sends through the bus is refused with `SECRET_DETECTED` when it holds a value Dockingbird keeps, and the refusal never repeats the value.

A few limits stay with you.

- A service's program runs as you on your Mac. With `uses`, its run gets a database credential in its environment, so the program sees it. The agent never does.
- A browser in your own profile lets the agent act as you on every site you are signed in to. Dockingbird restricts nothing it does on a website.
- Whatever you type or paste into a browser you `watch` is visible to the agent.
- A GitHub key copy can reach every repo your GitHub account reaches. A job is still bound to the one repo and branch you connected, but the key is not. A deploy key made for one repo limits that, and [github.md](github.md) covers it.

The operator guide's "Checking an agent's log for a value Dockingbird holds" shows how to ask the coordinator whether a log holds a kept value, without printing it.

### How access ends

| Action | Effect |
|---|---|
| `dockingbird revoke NAME --to AGENT` | that agent's new and waiting requests are refused; a request already running finishes |
| `dockingbird disconnect NAME` | new grants and requests stop for everyone, and Dockingbird's copy of the key is deleted; your own key files stay |
| `dockingbird connect NAME --revoke --role ROLE` | every running agent of the role loses it at its next request, and an agent of the role that starts later never gets it |
| the grant's expiry | the session's `session_hours`, or the `--until` time of a grant you made, ends it |
| `dockingbird clean --all` | removes the volumes, so every stored secret goes, and keeps your `vaults` folder |

Revoking does not undo what a finished request did, such as a push or a statement that committed.

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

A browser connection lends Chrome, Firefox or Safari of this Mac to one agent at a time, with your logins if you choose your own profile, and only while you serve it. An added config with `browser = "chrome"` instead gets a Chrome of Dockingbird's own in a container, with no connection, none of your logins and nothing on your Mac. Its network follows the agent's egress setting, and a swarm role cannot have one. An agent's own browser in a container: see [agent-browser.md](agent-browser.md).

A vault connection points at a gopass store. Dockingbird types the stored password and one-time code into the browser, and the agent sees neither. The agent can sign in through a Chrome you lend with `serve`, or through the container browser of its own. The page [secrets-vault.md](secrets-vault.md) shows the store.

## Every connect option

`dockingbird connect` takes exactly one form per run. Two forms at once end with [`CONNECT_ARGUMENTS_REQUIRED`](../troubleshooting.md#connect_arguments_required) and exit 2. Each option below that needs another one ends with `OPTION_NEEDS_OPTION` when it stands alone. The last column marks the options that `dockingbird connect -h` does not list.

| Option | Needs | Meaning | In `connect -h` |
|---|---|---|---|
| `NAME` | every form but `--config` | the connection's name, lowercase letters, digits and hyphens | yes |
| `--github OWNER/REPO` | a git checkout | connects the repo and the branch you are on, with a copy of your ssh key | yes |
| `--key PATH` | `--github` | a key file to copy instead of the one your ssh uses, such as a deploy key; not with `--agent` | yes |
| `--agent` | `--github` | uses your Mac's ssh-agent through Docker Desktop and copies no key | yes |
| `--branch BRANCH` | `--github` | another branch to copy; yours is copied first if it is not named | yes |
| `--known-hosts PATH` | `--github` | host keys to trust instead of GitHub's own pinned keys | yes |
| `--folder PATH` | none | connects a folder of this computer, read-only for agents | yes |
| `--database URL` | none | connects a PostgreSQL database, `postgres://ROLE@HOST:PORT/DATABASE` | yes |
| `--password` | `--database` | asks for the role's password on your terminal, hidden, or reads it from a pipe | yes |
| `--writes` | `--database` | registers the database for writes through the broker with `db.execute` | no |
| `--service FILE` | none | registers a program of this computer from a TOML file | yes |
| `--mcp URL` | none | registers a streamable-HTTP MCP server for swarm roles | no |
| `--browser BROWSER` | none | `chrome`, `firefox` or `safari` of this Mac | yes |
| `--vault gopass` | at least one `--login` | connects a gopass store under `vaults/` of your home | yes |
| `--store NAME` | `--vault` | the store's folder under `vaults/`, when it is not the connection's name | in the `--vault` line |
| `--login ALIAS ORIGIN USERNAME` | `--vault` | one sign-in, as three words; repeat for each login | yes |
| `--totp ALIAS` | `--vault` | marks a login whose entry also holds a time-based code; repeat | in the `--login` line |
| `--code-origin ALIAS ORIGIN` | `--vault`, a `--totp` login | the origin of the page that asks that login's code, when it is not the login's own site; once per login | no |
| `--reveal ALIAS TEXT` | `--vault`, a `--totp` login | the visible text of a control the typist clicks to show the code field; repeat in click order, at most 4 per login, 1 to 64 characters each | no |
| `--config FILE` | none | registers a reviewed JSON catalog, described in [the role and connection files reference](../reference/files/roles-and-connections.md#connection-catalog-file) | yes |
| `--to AGENT` | `--until` | grants the connection to that running agent too; not with `--folder` | yes |
| `--until ISO` | `--to` or `--to-role` | the grant's expiry, a future time with a timezone such as `2026-12-01T00:00:00+00:00` | yes |
| `--revoke` | `--role` | denies the connection to a swarm role | no |
| `--role ROLE` | `--revoke` | the role whose agents the denial covers | no |
| `--to-role ROLE` | `--until` | lifts the role's denial and grants the connection to its running agents | no |
| `--swarm KEY` | `--role` or `--to-role` | limits a role denial or grant to one swarm | no |

The other commands take little. `dockingbird connections [NAME]` lists connections, or shows one in full. `dockingbird connections --release` takes no name. `dockingbird revoke NAME --to AGENT` needs both words. `dockingbird disconnect NAME` takes the name only. `serve` and `watch` take the options in the steps below.

## Before you start

- Dockingbird is set up. `dockingbird status` must not print "Dockingbird isn't set up yet."; `dockingbird login claude` does the set-up from any folder.
- A GitHub connection runs inside a git checkout, on the branch the agents work on. Every other kind runs from any folder.
- A folder connection needs the folder under a path Docker Desktop shares, which its Settings > Resources > File sharing lists.

## Steps

1. Record a folder of this computer. Dockingbird refuses a link, the root of the disk and its own folder.

   ```bash
   dockingbird connect notes --folder ../notes
   ```

   The step is done when the command prints these lines. The message id is [`CONNECT_FOLDER_DONE`](../troubleshooting.md#connect_folder_done).

   ```text
   Connected notes: agents of a config that names it read it, read-only unless
   the config gives them write access, at /dockingbird/folders/notes.
   On this Mac it is <path>.
   Reads there aren't logged; the grant is.
   A config that names it: connections = ["notes"]
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

   With no connection recorded, `connections` prints [`CONNECTION_LIST_EMPTY`](../troubleshooting.md#connection_list_empty) and exits 0.

5. Take a connection from one agent, or from everyone. A revoke refuses that agent's new and waiting requests, and an agent already running finishes. A disconnect stops new grants and deletes Dockingbird's copy of any key. Your own key files stay.

   ```bash
   dockingbird revoke notes --to analyst-1
   dockingbird disconnect notes
   ```

   A folder cannot be taken from a running agent, so for a folder both commands stop the agent and name the command that continues it. The revoke prints these lines, with the id [`CONNECTION_REVOKE_STOPPED`](../troubleshooting.md#connection_revoke_stopped).

   ```text
   Revoked analyst-1's access to notes and stopped analyst-1: a folder can't be
   taken away from a running agent.
   Continue it: dockingbird analyst --as analyst-1
   ```

   For any other kind, `revoke` prints `Revoked analyst-1's access to NAME.` ([`CONNECTION_REVOKE_DONE`](../troubleshooting.md#connection_revoke_done)) and `disconnect` prints `Disconnected NAME.` ([`CONNECTION_DISCONNECT_DONE`](../troubleshooting.md#connection_disconnect_done)). A `disconnect` that stops agents for a folder prints [`CONNECTION_DISCONNECT_STOPPED`](../troubleshooting.md#connection_disconnect_stopped).

6. Serve a service or a browser as yourself. Until this runs in a terminal, `dockingbird status` shows the agent's request as waiting. A vault has no `serve` of its own: Dockingbird types its sign-ins while you serve the browser it is lent.

   ```bash
   dockingbird serve convert
   ```

   The step is done when the command prints this line ([`SERVE_READY`](../troubleshooting.md#serve_ready)). The page [mcp-and-services.md](mcp-and-services.md) covers `serve --all` and `serve --unit`, which keep serving with no terminal open.

   ```text
   Serving convert: agents' requests to it run here, as you, one at a time.
   Ctrl-C stops it.
   ```

   `dockingbird serve convert --once` runs the request that waits now, if there is one, and stops.

7. Watch the browser of an agent whose config says `browser = "chrome"`. The command prints a `vnc://127.0.0.1` address and the browser's own password, then opens Screen Sharing. The agent can read anything you type there. An agent's own browser in a container: see [agent-browser.md](agent-browser.md).

   ```bash
   dockingbird watch surf-1
   ```

   The step is done when the command prints these lines ([`WATCH_OPEN`](../troubleshooting.md#watch_open) and [`WATCH_PASSWORD`](../troubleshooting.md#watch_password)). Close the viewer or press Ctrl-C to stop. `--no-open` prints the address and opens no viewer.

   ```text
   Opening surf-1's browser, vnc://127.0.0.1:<port>, in your VNC viewer.
   Anything you type or paste into this browser is visible to the agent surf-1,
   which reads the page. Sign in to nothing you would not hand it.
   VNC password: <the browser's own password>
   ```

## Grant a connection to one agent

`--to AGENT --until ISO` registers a connection and grants it to a running agent in one command. `AGENT` is the active agent's name. The time needs a timezone. A folder takes neither option, because a folder reaches an agent only as a mount at its start.

```bash
dockingbird connect app-db --database postgres://reader@host.docker.internal:5432/app --password --to review-1 --until 2026-12-01T00:00:00+00:00
```

The command prints the kind's own done line, then `Connected app-db to review-1 until <time>.` ([`CONNECTION_CONNECT_DONE`](../troubleshooting.md#connection_connect_done)). A connect without `--to` prints only the done line.

## Register a reviewed catalog

`dockingbird connect --config FILE` registers a JSON catalog you reviewed. `NAME` may follow it, and then must equal the catalog's `name`. The file must be a regular file of yours that only you can read, with no link in its path, and on a Mac `/tmp` is `/private/tmp`. Without `--to`, the command prints `Saved NAME.` ([`CONNECTED_REGISTERED`](../troubleshooting.md#connected_registered)), grants the connection to no one, and a config you add may name it. With `--to AGENT --until ISO` it grants the connection to that agent, as above. The catalog's keys are in [the role and connection files reference](../reference/files/roles-and-connections.md#connection-catalog-file).

A catalog that differs from the connection already recorded under that name is refused with [`CONNECTION_CONFIG_CHANGED`](../troubleshooting.md#connection_config_changed). Disconnect the name first. A catalog Dockingbird cannot read ends with [`CONNECTION_INVALID_CONFIG`](../troubleshooting.md#connection_invalid_config), and the line names the field to fix and never its value.

## Grants to a swarm role

A swarm role can also hold or lose a connection. A role lists the connections its agents get in its `connections` key, in a `[[role]]` entry or in a library role file. Each agent of the role gets them at its start. `fleet submit` refuses a name the submitting home has not recorded, and a placed home that lacks one holds the swarm with [`FLEET_NO_CONNECTION`](../troubleshooting.md#fleet_no_connection): connect it there, then run `fleet release ID`. The reference page [roles-and-connections.md](../reference/files/roles-and-connections.md) lists the key.

```bash
dockingbird connect scores --revoke --role grader
dockingbird connect scores --to-role grader --until 2026-12-01T00:00:00+00:00
```

The first command stops every running agent of the role from using `scores` at its next request, with no restart. It also keeps the connection from any agent of the role that starts later, and `fleet why` shows that start as `denied_by_role`. The second command lifts that denial and grants the connection to the role's running agents until the time you give. Add `--swarm KEY` to narrow either one to a single swarm. Without it, a denial covers every swarm of the home that has a role of that name, now and later.

The first command prints `scores: denied to role grader` ([`CONNECT_ROLE_DENIED`](../troubleshooting.md#connect_role_denied)); with `--swarm` the line adds `of swarm KEY`. The second prints `scores: granted to role grader until <time>, <n> running agents` ([`CONNECT_ROLE_GRANTED`](../troubleshooting.md#connect_role_granted)), or `scores: no running agent of role grader` ([`CONNECT_ROLE_NONE`](../troubleshooting.md#connect_role_none)) when none runs; an agent of the role that starts later gets the connection as its config names it. A role form with `--to` is refused with `OPTIONS_NOT_BOTH`.

## Release a push of unknown result

A push that ended with an unknown result blocks the next push to that repo. Check the branch on GitHub first. Then run `dockingbird connections --release`, which records that push as failed, so the next push starts with a fresh fetch.

```bash
dockingbird connections --release
```

The command prints `Released the push to <repo> whose result was unknown.` ([`CONNECTION_RELEASED`](../troubleshooting.md#connection_released)), or `No push is waiting to be released.` ([`CONNECTION_NOTHING_UNRESOLVED`](../troubleshooting.md#connection_nothing_unresolved)) and exits 0 in both cases. The page [github.md](github.md) shows the full case.

## Message ids of the connection commands

Add `--verbose` to any command and each message shows its id. The ids below are the ones these commands print on success. The failures are under "When it fails".

| Command | Id |
|---|---|
| `connect --github` | [`CONNECT_GITHUB_DONE`](../troubleshooting.md#connect_github_done) |
| `connect --database` | [`CONNECT_DATABASE_DONE`](../troubleshooting.md#connect_database_done) |
| `connect --folder` | [`CONNECT_FOLDER_DONE`](../troubleshooting.md#connect_folder_done) |
| `connect --service` | [`CONNECT_SERVICE_DONE`](../troubleshooting.md#connect_service_done) |
| `connect --browser` | [`CONNECT_BROWSER_DONE`](../troubleshooting.md#connect_browser_done) |
| `connect --vault` | [`CONNECT_VAULT_PASSPHRASE`](../troubleshooting.md#connect_vault_passphrase) asks, then [`CONNECT_VAULT_DONE`](../troubleshooting.md#connect_vault_done) |
| `connect --mcp`, `connect --config` | [`CONNECTED_REGISTERED`](../troubleshooting.md#connected_registered) |
| `connect --to AGENT --until ISO` | [`CONNECTION_CONNECT_DONE`](../troubleshooting.md#connection_connect_done) |
| `connect --revoke --role`, `connect --to-role` | [`CONNECT_ROLE_DENIED`](../troubleshooting.md#connect_role_denied), [`CONNECT_ROLE_GRANTED`](../troubleshooting.md#connect_role_granted), [`CONNECT_ROLE_NONE`](../troubleshooting.md#connect_role_none) |
| `connections` | [`CONNECTION_LIST_CONNECTION`](../troubleshooting.md#connection_list_connection), or [`CONNECTION_LIST_EMPTY`](../troubleshooting.md#connection_list_empty) |
| `connections NAME` | the kind's line ([`CONNECTION_LIST_SSH`](../troubleshooting.md#connection_list_ssh), [`CONNECTION_LIST_FOLDER`](../troubleshooting.md#connection_list_folder), [`CONNECTION_LIST_DATABASE`](../troubleshooting.md#connection_list_database), [`CONNECTION_LIST_SERVICE`](../troubleshooting.md#connection_list_service), [`CONNECTION_LIST_BROWSER`](../troubleshooting.md#connection_list_browser), [`CONNECTION_LIST_VAULT`](../troubleshooting.md#connection_list_vault)), then one [`CONNECTION_LIST_AGENT`](../troubleshooting.md#connection_list_agent) for each grant and [`CONNECTION_LIST_REQUEST`](../troubleshooting.md#connection_list_request) for each recent request |
| `connections --release` | [`CONNECTION_RELEASED`](../troubleshooting.md#connection_released) |
| `revoke` | [`CONNECTION_REVOKE_DONE`](../troubleshooting.md#connection_revoke_done), or [`CONNECTION_REVOKE_STOPPED`](../troubleshooting.md#connection_revoke_stopped) for a folder |
| `disconnect` | [`CONNECTION_DISCONNECT_DONE`](../troubleshooting.md#connection_disconnect_done), or [`CONNECTION_DISCONNECT_STOPPED`](../troubleshooting.md#connection_disconnect_stopped) for a folder |
| `serve NAME` | [`SERVE_READY`](../troubleshooting.md#serve_ready), then [`SERVE_RAN`](../troubleshooting.md#serve_ran) for each request |
| `watch NAME` | [`WATCH_OPEN`](../troubleshooting.md#watch_open), [`WATCH_PASSWORD`](../troubleshooting.md#watch_password), [`WATCH_ENDED`](../troubleshooting.md#watch_ended) |

`dockingbird status` shows `Connections` with one row for each connection ([`STATUS_CONNECTION_ROW`](../troubleshooting.md#status_connection_row)), and a request that waits for `serve` ([`STATUS_SERVICE_WAITING`](../troubleshooting.md#status_service_waiting)).

## When it fails

- [`CONNECTION_UNKNOWN_CONNECTION`](../troubleshooting.md#connection_unknown_connection): the config names a connection that `dockingbird connections` does not list, so the start stopped.
- [`CONNECTION_INVALID_NAME`](../troubleshooting.md#connection_invalid_name): the name holds a capital, a space or a character beyond letters, digits and hyphens.
- [`CONNECTION_CONFIG_CHANGED`](../troubleshooting.md#connection_config_changed): you connected an existing name again with another repo, branch or key. Run `dockingbird disconnect NAME` first.
- [`CONNECTION_UNKNOWN_AGENT`](../troubleshooting.md#connection_unknown_agent): no running agent has that name. `dockingbird status` lists the running ones.
- [`CONNECTION_UNKNOWN_GRANT`](../troubleshooting.md#connection_unknown_grant): the agent holds no unrevoked grant for that connection, so `revoke` had nothing to take.
- [`CONNECTION_INVALID_UNTIL`](../troubleshooting.md#connection_invalid_until): the `--until` time is past, or lacks a timezone such as `+00:00`.
- [`CONNECTION_TOO_MANY`](../troubleshooting.md#connection_too_many): 500 connections are enabled. Disconnect one you no longer use.
- [`CONNECTION_LIST_TOO_LARGE`](../troubleshooting.md#connection_list_too_large): the running agents hold more grants than Dockingbird lists at once. Stop agents you no longer need, or run `dockingbird update` when the home still runs a release before 0.15.12.
- [`CONNECTION_NATIVE_FAILED`](../troubleshooting.md#connection_native_failed): Dockingbird could not read or confirm the change. When it says it changed none, run the command again. Otherwise check `dockingbird connections` first.
- [`CONNECT_FOLDER_INVALID`](../troubleshooting.md#connect_folder_invalid): the path is missing, a link, the whole disk or Dockingbird's own folder.
- [`CONNECT_MCP_INVALID`](../troubleshooting.md#connect_mcp_invalid): the `--mcp` URL is not an `https` address Dockingbird accepts.
- [`WATCH_NO_BROWSER`](../troubleshooting.md#watch_no_browser): the agent has no browser running in a container. Its config asks for none, or its container stopped.
- [`START_FOLDER_MISSING`](../troubleshooting.md#start_folder_missing): the folder moved or was deleted since you connected it. Connect it again at its new path.
- [`CONNECT_ARGUMENTS_REQUIRED`](../troubleshooting.md#connect_arguments_required): `connect` got no name, or two forms at once, or `--folder` with `--to`.
- [`START_PROJECT_CONNECTIONS`](../troubleshooting.md#start_project_connections): a repo's own config names a connection. Move the file out of `.dockingbird/` and run `dockingbird config add` on it.

Related pages: [your-own-commands.md](your-own-commands.md) for configs, [delegating-tasks.md](delegating-tasks.md) for the tasks agents get, [secrets-vault.md](secrets-vault.md) for the password vault, and [../concepts/security-model.md](../concepts/security-model.md) for what agents can reach.
