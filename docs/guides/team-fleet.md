---
title: Install a team fleet
summary: Install the PostgreSQL store, the roles, the worker and admitter services and the control plane that let a team share hosts and message across computers.
audience: team-admin
commands:
  - org login
  - org create
  - org status
  - org projects
  - org roles
  - org people
  - org members
  - fleet worker --host
  - fleet admitter
  - start --as fleet-link
  - cp init --hub-address
  - cp token --host --platform
  - node join
  - node leave
  - cp status
  - cp status --json
  - cp remove
  - cp off
  - status
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Install a team fleet

Two features come together on a team. The [fleet scheduler](../concepts/fleet-scheduler.md) shares a pool of hosts and queues swarms on it. The [control plane](../concepts/control-plane.md) joins computers, so an agent on one can write to an agent on another. After the last step your pool takes swarms, and every joined computer's agents can reach each other. Run the pool afterwards with [the fleet scheduler guide](fleet-scheduler.md).

## Before you start

- A PostgreSQL 18 server that the hosts reach over a private network. Check it with `psql --version` on the server.
- Two or more computers with Docker and Dockingbird set up. Check each with `dockingbird --version`.
- Each pool host reachable from the admin's computer. Check with `dockingbird fleet hosts`, set up as in [Hosts](hosts.md).
- For the control plane, a private network between the computers, such as [Tailscale](tailscale.md).

## 1. Make the store

As the cluster's superuser, make the admin role and the database. A role with `CREATEROLE` makes and grants the fleet's groups itself, so nothing more is asked of the superuser.

```bash
psql -c 'CREATE ROLE fleet_admin LOGIN CREATEROLE;'
psql -c 'CREATE DATABASE dockingbird_fleet OWNER fleet_admin;'
psql -c '\password fleet_admin'
```

The roles log in over TCP with passwords. Set `listen_addresses` in `postgresql.conf` to the loopback address and the address your hosts use, then restart PostgreSQL. Add `host` lines for `dockingbird_fleet` to `pg_hba.conf`, from both addresses, with the method `scram-sha-256`, then reload it. Psql confirms the first two commands with `CREATE ROLE` and `CREATE DATABASE`.

## 2. Log in as the admin and make the schemas

Log in on the computer you will run the admin commands from. The login asks for the password without showing it. It writes the org pointer, `org.toml`, and a line of `~/.pgpass`, the password file that PostgreSQL's own tools read. That file must be yours alone (`chmod 600`).

```bash
dockingbird org login db.example.net:5433 --as user --role fleet_admin
dockingbird org status
dockingbird org create
```

The three commands print these lines. A second `org create` says `The org store is already at version {version}: nothing changed.`

```text
Saved: user logs in to db.example.net:5433, database dockingbird_fleet, as fleet_admin.
Connected as fleet_admin.
The org store is ready, at version {version}.
```

`org create` makes the `fleet`, `org` and `work` schemas and the groups `fleet_submitter` and `fleet_worker`. A login outside `fleet_admin` is refused with exit 77. [The store reference](../reference/files/fleet-store.md) describes the schemas and the upgrade of a store an earlier build made.

## 3. Add logins, projects and members

Each worker host gets a login role, and so does each person. Make them in `psql -d dockingbird_fleet` as `fleet_admin`, and quote a name that holds a dash. Then give each a password with `\password "alice"`, which sends only the hash.

```sql
CREATE ROLE "fleet_worker_lab" LOGIN;
GRANT fleet_worker TO "fleet_worker_lab";
INSERT INTO fleet.role_host (role_name, host) VALUES ('fleet_worker_lab', 'lab');
CREATE ROLE "alice" LOGIN;
```

Record the project, the person, the membership and each role's model in the store. A person submits for a project as a member of its group, `fleet_submitter_<project>`. The admin acts for any project.

```bash
dockingbird org projects add example --name Example --url https://github.com/example-org/example-app
dockingbird org people add alice --account alice@example.net
dockingbird org members add alice --project example
dockingbird org roles set implementer --harness claude --model MODEL --effort EFFORT
```

```text
Added the project example to the org store.
Added alice, account alice@example.net, to the org store.
alice is now a member of example.
implementer with claude now runs MODEL at effort EFFORT.
```

## 4. Log in on each computer as its kind

A computer logs in once for each kind of command it runs, and one login serves every home of that user. The worker host uses the worker role, the admitter host uses the admin role, and a person uses their own role. If the database has another name, add `--database`. If the admin's leases run on that machine, add `--project`. A script sends the password on standard input with `--password-stdin`, never on the command line.

```bash
dockingbird org login db.example.net:5433 --as worker --role fleet_worker_lab
dockingbird org login db.example.net:5433 --as admitter --role fleet_admin
dockingbird org login db.example.net:5433 --as user --role alice
```

Each login prints its `Saved:` line, and `org status` lists the kind as `{kind}: {role}, password in {password_file}`. A command whose kind has no login ends 78 and names the login to run.

## 5. Link a checkout in each home

Swarm agents start in a checkout of the repository, and a home must link one first. Sign the home in once. Then, from inside the checkout, start the agent that holds the link and stop it again.

```bash
dockingbird login claude --here
dockingbird start --as fleet-link
dockingbird stop fleet-link --yes
```

Given no task, the agent waits and runs no turn, and stopping it keeps the link. Name the checkout's folder for the repository, so `example-org/example-app` lives in `example-app`. The step is done when a later `fleet submit` stops being refused with this line.

```text
refused: source: no home of the placement links a checkout of the repository, as of its host's last sample
```

## 6. Run the worker and the admitter as services

Each pool host runs one worker, `dockingbird fleet worker --host lab`. One host that stays awake runs the admitter, `dockingbird fleet admitter`. Each connects as its kind's role and runs until stopped, so each belongs under the machine's service manager. That is a LaunchAgent on a Mac, or a systemd user unit on Linux with `loginctl enable-linger` so it runs while nobody is logged in.

Dockingbird prints no unit for these two commands, because `serve --unit` covers `serve --all` only. Write each unit for your own service manager. It starts `installs/current/bin/dockingbird` under the host's data root, `~/.local/share/dockingbird/installs/`, with `fleet worker --host lab` or `fleet admitter` as arguments. Make `installs/current` a link beside the release folders. `fleet update` moves it from then on.

The worker reads the `hosts.toml` of its home. A `[[home]]` table, such as `name = "team-1"`, names each home it starts agents in. The optional `clones` key, an absolute folder such as `/srv/dockingbird/clones`, is where it keeps one clone per repository and branch.

On the computer that runs `fleet update`, each `[[host]]` table also needs a `repoint` line. It restarts that host's services and must return without waiting for them to stop. The first form is for a Mac and the second for Linux.

```text
repoint = "launchctl kickstart -k gui/$UID/<label>"
repoint = "systemctl --user restart --no-block <unit>"
```

The step is done when `fleet hosts` lists both processes. A worker started against a store that lacks a migration refuses with `FLEET_STORE_BEHIND`, so run `org create` first.

```text
lab's worker runs Dockingbird {release} (records through {schema}).
The admitter runs Dockingbird {release} (records through {schema}).
```

## 7. Make the control plane

The control plane is a home of its own. On that home, run `cp init` with the computer's IPv4 address on your tailnet, then serve the hub's port. The hub listens on port 4222, published on loopback only, so the second line shares it with the tailnet. A member that is not a device of yours, such as a cloud computer under a tag, also needs a grant in your tailnet's policy, with its tag and the control plane's device in place of these placeholders.

```bash
dockingbird cp init --hub-address 100.64.0.1
tailscale serve --bg --tcp 4222 tcp://127.0.0.1:4222
```

```text
{"src": ["tag:lab"], "dst": ["control-plane.example"], "ip": ["tcp:4222"]}
```

`cp init` prints this line. It is refused while agents run in the home (`MODE_CHANGE_AGENTS_RUNNING`).

```text
This home is now the fleet's control plane, at {host}:{port}.
```

## 8. Join each computer

Make a bundle for each computer on the control plane's home. The label is one to eight lowercase letters or digits and starts with a letter. The control plane prints the bundle once, as a single line. On the computer's own home, run `node join`, paste that line and press Control-D. Stored nowhere, a lost bundle means a new one.

```bash
dockingbird cp token --host lab --platform macos
dockingbird node join
dockingbird cp status
```

The commands print these lines, and the bundle follows the first. With `--json`, `cp status` also gives when each computer joined and when it was removed.

```text
lab is enrolled as node {node_id} (macos).
This computer joined the fleet as lab (node {node_id}).
  lab  {node_id}  macos  joined  {version}  {count} fleet inboxes, heard {ago} ago
```

From now on each `dockingbird start` on that computer opens the agent's fleet session. The `status` command shows `fleet: lab-notes-1, heartbeat {age}, asks {n}` under the agent, or `fleet: not open` or `fleet: none`. [The fleet tools reference](../reference/fleet-tools.md) lists what the agent gets.

## 9. Remove or rejoin a computer

`cp remove` takes a computer out at once, with no precondition. It revokes the token and closes its agents' fleet inboxes, and the agents keep running there. A lost home or a removed computer joins again with a new bundle. Run the first two lines on the control plane's home and the next two on the computer. Run `cp off` on the control plane's home once every computer is removed, because it is refused while one remains.

```bash
dockingbird cp remove lab
dockingbird cp token --host lab --platform macos
dockingbird node leave
dockingbird node join
dockingbird cp off
```

```text
lab (node {node_id}) is out of the fleet;
{count} fleet inboxes of its agents closed.
This computer left the fleet.
This home is a plain home again; the fleet's control plane is off.
```

After the control plane's computer restarts, the first `dockingbird cp status` on its home starts the control plane again. The members reconnect by themselves.

## 10. Update in order

Update the admin's store first with `org create`, then the control plane's home, then each member and each worker with `dockingbird update`. Until a member matches the control plane, its fleet frames are refused with `NODE_VERSION_MISMATCH` and its agents keep working without the fleet. `fleet update` moves the pool's hosts in rank order and is the admin's alone, as [the fleet scheduler guide](fleet-scheduler.md#update-the-pool) shows.

## A computer in a cloud

A cloud computer that the scheduler places swarms on may join like any other when four things hold. Its credential acts for its own home only, opening fleet sessions under its own label and reading the replies to its own inbox. The credential lives in the member home's fleet folder only, never in an agent's container, a log or a command line. `cp remove LABEL` cuts it off at once, and `node leave` on it removes the credential. Its fleet sessions expire with their hours.

A compromised member can send instructions to any agent of the fleet, including agents whose grants reach repositories. It can read what is addressed to its own agents, attachments included. It cannot read another computer's inboxes, the harness's sign-in or either database.

## Limits

| Limit | Value |
|---|---|
| a computer's label | at most 8 characters |
| an agent's name on a joined computer | at most 63 characters less the label and its dash |
| fleet sessions the overview lists | 100, then it says `truncated` in `status` and `cp status` |
| a decoded bundle | at most 4096 bytes |
| a fleet call's wait for its answer | 30 seconds |
| deliveries waiting for one asleep agent | at most 200 |
| a fleet attachment | at most 1,048,576 bytes |

## When it fails

- [`ORG_NOT_ADMIN`](../troubleshooting.md#org_not_admin) means your login is not in `fleet_admin`. The store was not changed.
- [`ORG_PGPASS_UNSAFE`](../troubleshooting.md#org_pgpass_unsafe) means `~/.pgpass` is a link or readable by others. Make it a regular file only you can read.
- [`ORG_ROLE_MISSING`](../troubleshooting.md#org_role_missing) means this computer has no login for the kind the command needs. Run the `org login` it names.
- [`FLEET_DB_UNREACHABLE`](../troubleshooting.md#fleet_db_unreachable) means the database did not answer. The command ends 69, so run it again when the server is up.
- [`FLEET_DB_REFUSED`](../troubleshooting.md#fleet_db_refused) means the database turned the login down. The command ends 78, so check the role and its password.
- [`FLEET_STORE_BEHIND`](../troubleshooting.md#fleet_store_behind) means the store lacks a migration this build needs. Run `org create`, then start the worker again.
- [`FLEET_CONFIG_PASSWORD_REFUSED`](../troubleshooting.md#fleet_config_password_refused) means an older `fleet.toml` still holds a password. Run `org login --from-fleet-toml --as KIND`.
- [`FLEET_UPDATE_NO_REPOINT`](../troubleshooting.md#fleet_update_no_repoint) means a host has no `repoint` line. Add one to its `[[host]]` table.
- [`MODE_CHANGE_AGENTS_RUNNING`](../troubleshooting.md#mode_change_agents_running) blocks `cp init`, `cp off`, `node join` and `node leave` while agents run in the home. Stop them first.
- [`CP_HOSTS_ENABLED`](../troubleshooting.md#cp_hosts_enabled) blocks `cp off` while computers remain. Run `cp remove` for each.
- [`NODE_ALREADY_ENROLLED`](../troubleshooting.md#node_already_enrolled) means a bundle was used before. Make a new one with `cp remove` and `cp token`.
- [`NODE_ALREADY_JOINED`](../troubleshooting.md#node_already_joined) means this home is in the fleet. Run `node leave`, then join with the new bundle.
- [`NODE_SESSIONS_LIVE`](../troubleshooting.md#node_sessions_live) blocks `node leave` while agents here use the fleet. Stop them.
- [`RPC_PEER_HOST_MISMATCH`](../troubleshooting.md#rpc_peer_host_mismatch) means the bundle was made for another computer. Leave, then join with this computer's own bundle.
- [`NODE_VERSION_MISMATCH`](../troubleshooting.md#node_version_mismatch) means the two ends run different releases. Update the one that is behind.
- [`FLEET_NAME_TOO_LONG`](../troubleshooting.md#fleet_name_too_long) means the label and dash push the name past 63 characters. Use a shorter name.
- [`FLEET_SESSION_NOT_OPENED`](../troubleshooting.md#fleet_session_not_opened) means the control plane did not answer at the start. The agent works here and gets its inbox later.
