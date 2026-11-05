---
title: Give agents a database without the password
summary: Connect a PostgreSQL database for reads and brokered writes, add a service file with typed arguments, grant it to a swarm role, and revoke it.
audience: daily
commands:
  - connect --database
  - connect --service
  - connect --to-role
  - connect --revoke
  - connections
---

# Give agents a database without the password

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

Goal: agents of a `grader` role read a `scores` database and write score rows, and no agent ever sees the address or a password. You connect the database twice, once read-only and once for brokered writes. You add a program that inserts one score with arguments you bound. Then you take the access back and give it again. The guides behind each step are [databases.md](../../docs/guides/databases.md), [mcp-and-services.md](../../docs/guides/mcp-and-services.md) and [connections.md](../../docs/guides/connections.md).

## Before you start

- Dockingbird is set up. `dockingbird status` must not print "Dockingbird isn't set up yet."
- A PostgreSQL server answers at `db.example.net:5433` with a database named `scores`, and Docker can reach it. `psql -h db.example.net -p 5433 -U postgres scores -c 'select 1'` prints one row.
- The server allows no prepared transactions. `SHOW max_prepared_transactions;` prints 0.
- A table `scores` exists, owned by an administrator and not by the roles below.
- A program of yours inserts one score. It lives in a git checkout, and it reads the `PG*` variables for its connection. `git rev-parse HEAD` in that checkout prints the commit step 4 pins.
- A swarm role named `grader` lists `scores-db` in its `connections`. The swarm is described in [swarms.md](../../docs/guides/swarms.md). Steps 7 and 8 work with no running agent, and then they say so.

## Steps

1. Make the two roles. `reader` cannot write. `scorer` may insert into `scores`. The revoke is the cost of Dockingbird's check of the read-only role, and it is needed once for the database. On PostgreSQL 16 and earlier, name the function's two forms without the fourth parameter.

   ```sql
   CREATE ROLE reader LOGIN PASSWORD 'a long password';
   GRANT CONNECT ON DATABASE scores TO reader;
   GRANT USAGE ON SCHEMA public TO reader;
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;
   CREATE ROLE scorer LOGIN PASSWORD 'another long password';
   GRANT CONNECT ON DATABASE scores TO scorer;
   GRANT USAGE ON SCHEMA public TO scorer;
   GRANT SELECT, INSERT ON scores TO scorer;
   REVOKE EXECUTE ON FUNCTION
     pg_catalog.pg_logical_emit_message(boolean, text, text, boolean),
     pg_catalog.pg_logical_emit_message(boolean, text, bytea, boolean)
   FROM PUBLIC;
   ```

   The step is done when `psql` prints `CREATE ROLE` twice. If the database has the `dblink` extension, also run the `dblink` revoke on [databases.md](../../docs/guides/databases.md).

2. Connect the database read-only. Dockingbird asks for the password on your terminal, hidden, and keeps it. It then opens the database itself and checks that the role cannot write.

   ```bash
   dockingbird connect app-db --database postgres://reader@db.example.net:5433/scores --password
   ```

   The step is done when the command prints these lines.

   ```text
   Password for reader (hidden):
   Connected app-db: db.example.net:5433/scores as reader, read-only, checked from Dockingbird.
   Agents of a config that names it query it through Dockingbird;
   none sees the database.
   A config that names it: connections = ["app-db"]
   ```

3. Connect the same database for brokered writes, under its own name. Dockingbird checks the server alone, because this role is meant to write. An agent then sends `db.execute` with one statement, and the broker runs it in one read-write transaction.

   ```bash
   dockingbird connect scores-db --database postgres://scorer@db.example.net:5433/scores --password --writes
   ```

   The step is done when the command prints these lines.

   ```text
   Password for scorer (hidden):
   Connected scores-db: db.example.net:5433/scores as scorer, which may write, checked from Dockingbird.
   Agents of a config that names it query and change it through Dockingbird;
   none sees the database.
   A config that names it: connections = ["scores-db"]
   ```

4. Write the service file `insert-score.toml`. It names your program, the checkout and the commit, and it declares two arguments. The bound keys are `minimum` and `maximum`, and `max_chars` bounds a text. `uses` hands the run the credential of `scores-db`, as `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER` and `PGPASSWORD`, so the agent needs no grant on the database for this service. The file must be yours alone, not a link, and not in Dockingbird's folder.

   ```toml
   # What dockingbird serve add-score runs when an agent asks.
   program = "/path/to/scores/bin/add-score"
   checkout = "/path/to/scores"
   commit = "0123456789abcdef0123456789abcdef01234567"
   # The most seconds one run may take.
   timeout_s = 60
   # The database connection whose credential each run gets.
   uses = ["scores-db"]
   # Its words: {output} is the folder it writes its result to.
   argv = ["--score", "{score}", "--note", "{note}", "{output}"]

   # A whole number from 1 to 100.
   [arguments.score]
   type = "int"
   minimum = 1
   maximum = 100

   # Text of at most 200 characters, passed on as the agent typed it.
   [arguments.note]
   type = "text"
   max_chars = 200
   ```

   ```bash
   dockingbird connect add-score --service ./insert-score.toml
   ```

   The step is done when the command prints these lines. It runs nothing.

   ```text
   Connected add-score: agents of a config that names it run /path/to/scores/bin/add-score here, as you,
   with the arguments it declares, when you run dockingbird serve add-score.
   A config that names it: connections = ["add-score"]
   ```

5. Name the connections in a config you add. A repo's own config cannot name a connection.

   ```toml
   command = "grader"
   workspace = "scratch"
   connections = ["app-db", "scores-db", "add-score"]
   ```

   ```bash
   dockingbird config add grader.toml
   dockingbird grader "Score the three newest rows"
   ```

   The step is done when the first command prints a line that starts as follows and the second prints the start lines.

   ```text
   Registered grader: dockingbird grader "task"
   grader-1 started in a scratch folder.
   ```

6. Serve the program. The agent's request to `add-score` waits in `dockingbird status` until you run `serve` in a terminal. The run executes as you, one at a time, with five variables, and its output folder lands in the agent's log folder.

   ```bash
   dockingbird serve add-score
   ```

   The step is done when the command prints these lines.

   ```text
   Serving add-score: agents' requests to it run here, as you, one at a time.
   Ran add-score for grader-1: done in 3 s.
   ```

7. Take the database from the role. Every running agent of `grader` stops using `scores-db` at its next request, with no restart. A later start, replacement or added agent of the role is denied too. Add `--swarm KEY` to narrow it to one swarm.

   ```bash
   dockingbird connect scores-db --revoke --role grader
   dockingbird connections scores-db
   ```

   The step is done when the first command prints this line.

   ```text
   scores-db: denied to role grader
   ```

8. Give it back for a while. The command lifts the denial and grants the connection to the role's running agents until the time you give. The time is an ISO timestamp with a timezone, in the future.

   ```bash
   dockingbird connect scores-db --to-role grader --until 2026-12-01T00:00:00+00:00
   ```

   The step is done when the command prints one of these lines.

   ```text
   scores-db: granted to role grader until 2026-12-01T00:00:00+00:00, 2 running agents
   scores-db: no running agent of role grader
   ```

   With no running agent, nothing was granted, and an agent of the role that starts later gets the connection as its config names it. To remove a connection for everyone, and the password Dockingbird kept, run `dockingbird disconnect scores-db`.

## When it fails

- [`CONNECT_DATABASE_REFUSED`](../../docs/troubleshooting.md#connect_database_refused) in step 2 means the check found a role that can write, or a server that allows prepared transactions, or a missing revoke. The connection was removed. Fix the role and run the step again.
- [`CONNECT_DATABASE_INVALID`](../../docs/troubleshooting.md#connect_database_invalid) means the URL holds a password, a query or a fragment, or its parts do not match `postgres://ROLE@HOST:PORT/DATABASE`.
- [`CONNECT_SERVICE_INVALID`](../../docs/troubleshooting.md#connect_service_invalid) names the key of `insert-score.toml` to fix, and never shows its value. A key Dockingbird does not know is one cause, so spell the bounds exactly as `minimum` and `maximum`. Paths start with `/` or `~`, and the checkout is the top folder of a git checkout that has a commit.
- [`CONNECT_SERVICE_CHECKOUT_MOVED`](../../docs/troubleshooting.md#connect_service_checkout_moved) means the checkout is not at the commit the file names. Check that commit out, or write the commit it is at.
- [`SERVE_CHECKOUT_MOVED`](../../docs/troubleshooting.md#serve_checkout_moved) means the checkout moved after step 4, and nothing ran. Connect the service again.
- [`CONNECTION_UNKNOWN_CONNECTION`](../../docs/troubleshooting.md#connection_unknown_connection) stops the start in step 5 when a name in `connections` is not enabled. `dockingbird connections` lists them.
- [`CONNECTION_INVALID_UNTIL`](../../docs/troubleshooting.md#connection_invalid_until) rejects the `--until` of step 8 when it is past or has no timezone.
