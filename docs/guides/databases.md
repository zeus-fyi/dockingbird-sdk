---
title: Give agents a database
summary: Connect a PostgreSQL database so agents query it, and write to it through a broker, without ever seeing its address or password.
audience: daily
commands:
  - connect --database
  - connect --to-role
  - connect --revoke
  - connections
  - disconnect
---

# Give agents a database

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

An agent that needs rows from PostgreSQL asks Dockingbird for one statement, and Dockingbird runs it with the password it keeps. The agent gets a name and a file of results. This page connects a database read-only, then adds brokered writes, grants and revokes. The model behind it is on [connections.md](connections.md).

## Before you start

- Dockingbird is set up. `dockingbird status` must not print "Dockingbird isn't set up yet."
- The server is PostgreSQL. No other engine works yet.
- Docker can reach the server. On Docker Desktop your Mac is `host.docker.internal`. On a plain Linux Engine, name the Docker bridge's address, let the server listen on it with `listen_addresses`, and admit it in `pg_hba.conf`.
- The server allows no prepared transactions. `SHOW max_prepared_transactions;` must print 0, which is PostgreSQL's default.
- A database user for agents exists. Step 1 makes it.

## Steps

1. Make a role that cannot write. Dockingbird opens the database itself before it says done, and refuses a role that can write, owns a table, owns the database, or may call `pg_logical_emit_message`. That function writes to the server's log in a way a rollback does not undo, and every role may call it by default. The revoke below is the cost of that check, and it is needed once for each database.

   ```sql
   CREATE ROLE reader LOGIN;
   GRANT CONNECT ON DATABASE app TO reader;
   GRANT USAGE ON SCHEMA public TO reader;
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;
   REVOKE EXECUTE ON FUNCTION
     pg_catalog.pg_logical_emit_message(boolean, text, text, boolean),
     pg_catalog.pg_logical_emit_message(boolean, text, bytea, boolean)
   FROM PUBLIC;
   ```

   On PostgreSQL 16 and earlier the function has no fourth parameter, so name its two forms without it. Where the `dblink` extension is installed, every role may call it. The check then refuses every role of that database until one of these runs, with `dblink`'s schema on the search path.

   ```sql
   REVOKE EXECUTE ON FUNCTION
     dblink(text), dblink(text, text), dblink(text, boolean), dblink(text, text, boolean),
     dblink_exec(text), dblink_exec(text, text), dblink_exec(text, boolean), dblink_exec(text, text, boolean),
     dblink_connect(text), dblink_connect(text, text)
   FROM PUBLIC;
   -- or: DROP EXTENSION dblink;
   ```

   If the server asks for a password for the role, give the role one, such as `ALTER ROLE reader PASSWORD 'a long password';`, and add `--password` in step 2.

2. Connect the database. The URL holds the role, the server's host name in lowercase, a port (5432 when left out) and the database name, and nothing else. A password, a query or a fragment in the URL is refused before anything is saved. `--password` asks for the role's password on your terminal, hidden, and keeps it inside Dockingbird, never in a file of yours. Without a terminal it reads the password from what you pipe in.

   ```bash
   dockingbird connect app-db --database postgres://reader@host.docker.internal:5432/app --password
   ```

   The step is done when the command asks for the password and then prints these lines.

   ```text
   Password for reader (hidden):
   Connected app-db: host.docker.internal:5432/app as reader, read-only, checked from Dockingbird.
   Agents of a config that names it query it through Dockingbird;
   none sees the database.
   A config that names it: connections = ["app-db"]
   ```

3. Name the connection in a config you add. A config of a repo cannot name it.

   ```toml
   command = "analyst"
   connections = ["app-db"]
   tools = "default"
   ```

   ```bash
   dockingbird config add analyst.toml
   ```

   The four tools that use a connection, `bus_connections`, `bus_request`, `bus_request_status` and `bus_request_cancel`, sit in the `default` and `full` sets and not in `bus`, which is what `tools` holds when you leave it out. A config that names `app-db` with no `tools` line gives its agents no tool to query. `default` and `full` also hold `bus_claim` and its kin, so a config with `workspace = "scratch"` cannot use either: `config add` refuses it with [`CONFIG_INVALID_FILE`](../troubleshooting.md#config_invalid_file) at `tools`. Leave `workspace` at its default, `repo`. [The agent tools page](../reference/agent-tools.md) lists each set, and [How a secret is brokered](connections.md#how-a-secret-is-brokered) follows a request through the broker.

   An agent of that config sends one SQL statement that returns rows and reads the rows as a file of JSON lines in its log folder. It never sees the database, its address or the password. A statement that writes, changes the transaction or runs past its time limit fails and changes nothing, and the database's own words are never shown. Dockingbird checks the role again before every query.

4. Let the broker write. Register the database for writes with `--writes`, under its own name and with a role that may write. The check then proves the server alone, because the role is meant to write.

   ```bash
   dockingbird connect scores-db --database postgres://scorer@host.docker.internal:5432/app --password --writes
   ```

   The step is done when the command prints these lines.

   ```text
   Connected scores-db: host.docker.internal:5432/app as scorer, which may write, checked from Dockingbird.
   Agents of a config that names it query and change it through Dockingbird;
   none sees the database.
   A config that names it: connections = ["scores-db"]
   ```

   An agent writes with a `bus_request` of kind `db.execute`, which carries three fields.

   | Field | What it holds |
   |---|---|
   | `sql` | one statement |
   | `arguments` | the values its `%(name)s` placeholders bind, each a whole number or a text, and `{}` for none |
   | `rows` | optional, the most rows it wants back |

   The broker runs the statement on its own connection in one read-write transaction, under the statement timeout and the row and byte limits of a query. It commits when the statement succeeds and rolls back on any refusal. A role that writes is refused `db.query` with the reason `role-can-write`, so agents of such a connection read with `db.execute` too.

5. Give the database to a running agent for a while, or to a swarm role. Without these, only the agents of an added config that names the connection get it. Add `--to AGENT --until ISO` to the connect command to give it to a running agent as well, and use `--to-role` to lift a role's denial and grant the role's running agents.

   ```bash
   dockingbird connect app-db --database postgres://reader@host.docker.internal:5432/app --password --to analyst-1 --until 2026-12-01T00:00:00+00:00
   dockingbird connect scores-db --to-role grader --until 2026-12-01T00:00:00+00:00
   ```

   The second command is done when it prints this line, where the count is the role's running agents.

   ```text
   scores-db: granted to role grader until 2026-12-01T00:00:00+00:00, 2 running agents
   ```

   A swarm role that uses the grant needs `tools = "full"`, or a list that holds the four tools above and every `bus` tool. A role left at `bus` holds none of them.

6. Take the database back. A role revoke stops every running agent of the role at its next request, with no restart, and keeps it from agents of the role that start later. `--swarm KEY` narrows it to one swarm. A disconnect removes the connection and the password it kept, for everyone.

   ```bash
   dockingbird connect scores-db --revoke --role grader
   dockingbird disconnect scores-db
   ```

   The revoke prints this line, and the disconnect prints `Disconnected scores-db.`

   ```text
   scores-db: denied to role grader
   ```

   While a connection exists, `dockingbird connections app-db` shows what its agents may do with it, by this line.

   ```text
   Query host.docker.internal:5432/app as reader, read-only
   ```

## The service file keys that touch a database

A service connection, a program of yours that agents may run, can take a database's credential without the agent holding any grant on it. The other keys of the file are on [mcp-and-services.md](mcp-and-services.md).

| Key | What it does |
|---|---|
| `uses` | names one database connection, such as `uses = ["scores"]`; each run gets `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER` and, when the role has one, `PGPASSWORD` |
| `[call]` | names a Python function in the checkout with `python`, `module` and `function`, in place of `argv` |
| `[arguments.NAME]` | declares one argument with `type` `int`, `choice` or `text`, bounded by `minimum` and `maximum`, `choices` or `max_chars` |

## When it fails

- [`CONNECT_DATABASE_INVALID`](../troubleshooting.md#connect_database_invalid) rejects a URL that is not `postgres://ROLE@HOST:PORT/DATABASE`. A password, a query or a fragment in it is the usual cause.
- [`CONNECT_DATABASE_REFUSED`](../troubleshooting.md#connect_database_refused) means the check found a role that can write, a server that allows prepared transactions, or a missing revoke. Dockingbird removed the connection and kept nothing.
- [`CONNECT_DATABASE_PASSWORD_SHORT`](../troubleshooting.md#connect_database_password_short) means the password you typed was empty. Run the command again and type it.
- [`CONNECTION_CONFIG_CHANGED`](../troubleshooting.md#connection_config_changed) appears when the name already exists with other settings. Disconnect it first.
- [`CONNECTION_INVALID_UNTIL`](../troubleshooting.md#connection_invalid_until) rejects an `--until` time that is past or has no timezone.
- [`CONNECT_ROLE_NONE`](../troubleshooting.md#connect_role_none) says the denial was lifted but no agent of that role runs, so nothing was granted. The exit status is 0.
- [`CONNECTION_UNKNOWN_CONNECTION`](../troubleshooting.md#connection_unknown_connection) stops a start whose config names a connection that is not enabled. `dockingbird connections` lists the enabled ones.
