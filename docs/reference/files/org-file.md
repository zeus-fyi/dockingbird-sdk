---
title: org.toml and the password file
summary: The keys of org.toml, the file that names your organisation's store, and the ~/.pgpass line that holds each role's password.
audience: team-admin
commands:
  - dockingbird org login
  - dockingbird org status
  - dockingbird org logout
  - dockingbird org create
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../../llms.txt).

# org.toml and the password file

`org.toml` names the organisation's store, a PostgreSQL database, and the role each kind of command connects as.
It holds no secret: each role's password is a line of `~/.pgpass`, PostgreSQL's own password file, which `psql` reads too.

## Where the files are

| File | Path | Written by | Rules |
|---|---|---|---|
| `org.toml` | `~/.config/dockingbird/org.toml`, or `$XDG_CONFIG_HOME/dockingbird/org.toml` when `XDG_CONFIG_HOME` is a path from `/` | `dockingbird org login` and `dockingbird org logout` only | a regular file of yours, mode 0600, in a folder of mode 0700; never read through a link |
| `~/.pgpass` | your home folder, or the file `PGPASSFILE` names | `dockingbird org login`, or by hand | a file of yours that no one else can read (`chmod 600`); a file anyone else can read is refused, and no refusal shows a password |

## Keys of org.toml

```toml
version = 1

[org]
host = "db.example.net"
port = 5433
database = "dockingbird_fleet"
project = "example-app"

[org.roles]
user = "fleet_admin"
worker = "fleet_worker_lab"
admitter = "fleet_admin"
```

| Key | Values | Default | What it holds |
|---|---|---|---|
| `version` | `1` | required | the file's format; any other number is refused |
| `[org] host` | text | required | the address the hosts reach the fleet database at |
| `[org] port` | 1 to 65535 | PostgreSQL's default | the database's port |
| `[org] database` | text | `dockingbird_fleet` | the database's name |
| `[org] project` | project slug | none | the project the owner's own leases count against |
| `[org.roles] user` | PostgreSQL role | none | the role for your own commands: `fleet_admin` for the owner, your own login role for every other person, their coordinators and runners included |
| `[org.roles] worker` | PostgreSQL role | none | the role for `dockingbird fleet worker` |
| `[org.roles] admitter` | PostgreSQL role | none | the role for `dockingbird fleet admitter` |

Any other key, a missing required key, a value of the wrong type or another `version` is refused, and the refusal names the key and never a value.

## The password line

`~/.pgpass` holds one line for each role, in PostgreSQL's own format, and `psql` reads the same line.

```text
db.example.net:5433:dockingbird_fleet:fleet_admin:PASSWORD
```

| Part | Meaning |
|---|---|
| `HOST:PORT:DATABASE:ROLE:PASSWORD` | the order of the five fields, with the role's password in place of `PASSWORD` |
| `dockingbird org login` | asks for the password without echo, or reads it whole from standard input with `--password-stdin`; a password is never a word of the command line |

## What the files decide

| Case | Result |
|---|---|
| no org login on this computer | the command ends 78 and names `dockingbird org login HOST --as user --role ROLE` |
| a kind of command with no role in `org.toml`, or a role with no line in `~/.pgpass` | the command ends 78 and names the login to run |
| the database does not answer within 5 seconds, or ends the work for a passing reason (restarting, too many connections) | the command names the database's host, the role tried and the connection's own words, and ends 69 |
| the database turns the login down (wrong password, a role or database it lacks) or answers with an error code once connected | the command is refused with that role and the words or the code, and ends 78 |
| an access rule that does not list this computer | the refusal comes before the password is asked, so it reads as no answer, with the database's own words on the line |
| one login | one login serves every Dockingbird home of that user on the computer |

## The older fleet.toml

Before `org.toml`, a fleet database login lived in a `fleet.toml` in your Dockingbird home.

| Case | Result |
|---|---|
| no `org.toml`, and a `fleet.toml` without a `password` | the command still reads `fleet.toml` |
| a `fleet.toml` that holds a `password` | the command connects nothing, names the file and the line that moves it, and ends 78 |
| `dockingbird org login --from-fleet-toml --as KIND` | moves the login into `org.toml` and `~/.pgpass`, then takes the password out of the file after a yes; `--yes` answers it where there is no terminal |
| both files | `org.toml` is read and a line says `fleet.toml` is not |

| Key | Default | What it holds |
|---|---|---|
| `host` | required | where the fleet database answers |
| `role` | required | `fleet_submitter_PROJECT`, `fleet_worker_HOST` or `fleet_admin` |
| `port` | 5432 | the database's port |
| `database` | `dockingbird_fleet` | the database's name |
| `project` | none | in the admin's file only: the project the admin's leases count against |
| `password` | refused | a file that holds one stops the command with exit 78 |

## Commands that write these files

| Command | What it does |
|---|---|
| `dockingbird org login HOST[:PORT] --as user\|worker\|admitter --role ROLE` | writes both files; `--database NAME`, `--project SLUG`, `--password-stdin` and `--replace` (sign in to another store in place of this one) adjust it |
| `dockingbird org status` | shows the login and connects once as `user` |
| `dockingbird org logout [--as KIND]` | takes the login away, or one kind's |

## Related

| Page | What it holds |
|---|---|
| [commands.md](../commands.md) | every `org` action |
| [exit-codes.md](../integration/exit-codes.md) | the statuses 69, 77 and 78 |
| [team-fleet.md](../../guides/team-fleet.md) | the steps that build the store |
