---
title: hosts.toml
summary: Every key of hosts.toml, the file that names the other computers you reach, and the commands that write it.
audience: team-admin
commands:
  - dockingbird fleet hosts set
  - dockingbird fleet hosts rename
  - dockingbird fleet hosts forget
  - dockingbird fleet agents
  - dockingbird fleet attach
  - dockingbird fleet update
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../../llms.txt).

# `hosts.toml`: the other computers you reach

The hosts file lists the other computers you reach from this one, so the fleet commands that take a host name can read their agents and open their screens.
With no file there are no other hosts, which is not an error, and a command that writes the file makes it.

| Fact | Detail |
|---|---|
| path | `~/.local/share/dockingbird/hosts.toml`, or `hosts.toml` in the folder `DOCKINGBIRD_HOME` names |
| commands that read it | `fleet agents --host NAME` reads the agents on a listed computer, and `fleet attach --host NAME` opens one of their screens |
| this computer | never an entry, because it is `local` in every fleet line and `fleet agents` always reads it; a pool host is the one exception, written with `local = true` |

## The three commands that write it

```bash
dockingbird fleet hosts set NAME --ssh DEST [--path PATH] [--docker-host URL]
dockingbird fleet hosts set NAME --gcloud VM --zone ZONE --project PROJECT
dockingbird fleet hosts rename OLD NEW
dockingbird fleet hosts forget NAME
```

- `set` reaches the host over its route and reads its Docker and its Dockingbird homes exactly as
  `dockingbird fleet agents --host NAME` does; only once that read succeeded does it write the host's `[[host]]`
  table, then it prints the host's rows and says so:
  `lab: ssh lab.example, saved in ~/.local/share/dockingbird/hosts.toml.` (`FLEET_HOSTS_SET`). For a name the file
  already has it says `updated in` (`FLEET_HOSTS_UPDATED`): the route keys are replaced, and the host's
  `[[host.home]]` tables and its place in the file are kept. When the host can't be read, nothing is saved, and the
  message says what to try first: `ssh DEST docker version`, or `gcloud compute ssh VM -- docker version`.
- `rename OLD NEW` renames a host, its `[[host.home]]` tables kept. Swarm definitions and pool records that name
  `OLD` are not changed.
- `forget NAME` removes a host and its `[[host.home]]` tables.

`set` and `rename` refuse a name that is not a host name and the name `local`, this computer's own; `rename` and
`forget` refuse a name the file lacks, and `rename` a new name the file already has. A command that writes the file
holds its lock, so two at once never lose each other's change; while another one is writing, it says so and changes
nothing. With `--json`, each line is an envelope ([the envelope](../integration/json.md)).

You may still write the file by hand. A write by Dockingbird keeps every table and their order, and leaves the file
readable by you alone (0600), but loses a hand-written file's comments and the order of keys inside a table.

## One name

| Rule | What it means |
|---|---|
| a host has one name | its `name` here is what `--host` takes and the rows say, its name in the fleet pool when it is in one, and the name a swarm definition places work on |
| renaming a pooled host | on a computer whose Dockingbird home holds a `fleet.toml`, `rename` and `forget` of a host the pool holds are refused (`FLEET_HOSTS_IN_USE`); drain and remove it from the pool first, then rename it here, then enrol it again under its new name |

## `[[host]]`: one per computer

Each `[[host]]` has a `name` and one route: `ssh`, or `gcloud` with `zone` and `project`; this computer as a pool host has `local = true` instead.

| Key | Route | What it holds |
|---|---|---|
| `name` | both | the host's name: lowercase letters, digits and dashes, at most 56 characters, one per file, never `local` |
| `ssh` | ssh | a destination your own ssh reaches: `lab.example`, `user@lab.example`, or a `Host` of your ssh configuration |
| `path` | ssh | the `PATH` the commands run with there, for a login whose own `PATH` lacks Docker's `docker` |
| `docker_host` | ssh | the `DOCKER_HOST` the commands run with there, for a Docker whose socket is not the default one |
| `gcloud` | gcloud | a Compute Engine VM's instance name, reached through your own `gcloud compute ssh` |
| `zone` | gcloud | the instance's zone |
| `project` | gcloud | the instance's project |
| `gcloud_program` | gcloud | this computer's `gcloud`, as an absolute path, when it is neither on your `PATH` nor in the Google Cloud SDK's usual places; written by hand, and kept by a `set` that keeps the gcloud route |
| `repoint` | any | your own command that restarts the host's Dockingbird services, its worker and the admitter where it runs; `dockingbird fleet update` runs it over the host's route after it moves the host to a release |
| `login_push` | ssh, gcloud | a list of the tools whose login this computer's fleet worker copies to the host: `["codex"]`, the one word it takes; see `login_push` below |
| `local` | none | `true` for this computer when it is a pool host, written with neither `ssh` nor `gcloud`; its lines run here under `sh`, and `fleet hosts` shows it as `this computer` |

## `[[host.home]]` and `[[home]]`: a home's own program

| Table | Names |
|---|---|
| `[[host.home]]`, after a host's keys | one of that host's Dockingbird homes |
| `[[home]]`, at the top level | a home of this computer |

You write both by hand, and `set` keeps them.
A table names its home by `path` or by `name`, and `program` is the home's own `dockingbird`, which a send to one of its agents with no screen runs there.

| Key | What it holds |
|---|---|
| `path` | the home's folder, an absolute path; the worker identifies the home by its real path |
| `name` | a home `homes/NAME` of the worker's user, in place of `path`; its `program` is that home's own program file unless the table names one |
| `program` | the home's own `dockingbird`, an absolute path |
| `clones` | optional, an absolute folder where a fleet worker keeps one clone per repository and branch it starts swarms from |

```toml
[[host]]
name = "lab"
ssh = "lab.example"

[[host.home]]
path = "/opt/dockingbird/homes/team-1"
program = "/opt/dockingbird/bin/dockingbird"
```

## `repoint`: the restart line `fleet update` runs

`dockingbird fleet update` needs a `repoint` line in each pool host's `[[host]]` table.
Dockingbird runs the line exactly as you wrote it, over the host's route, and composes no restart command of its own.
It must return without waiting for the services to stop, because a restart that takes longer than the call's 40 seconds reads as failed.

```toml
[[host]]
name = "lab"
ssh = "lab.example"
repoint = "systemctl --user restart --no-block UNIT"
```

On Linux `UNIT` is the systemd user unit of the worker. On a Mac the line is `launchctl kickstart -k gui/$UID/LABEL`, with the label of the worker's launchd unit in place of `LABEL`.
A Dockingbird older than the release that reads `repoint` and `local` refuses the whole file with `FLEET_HOSTS_FILE_INVALID` until it is updated, so write both keys on a computer that runs the newer release.

## `login_push`: a Codex login for a pool host

A pool host with no Codex login of its own, such as a cloud VM, cannot run Codex agents. `login_push = ["codex"]` on its `[[host]]` table in the `hosts.toml` of a fleet worker's home gives it one: the worker copies the Codex login of the computer it runs on.

```toml
[[host]]
name = "lab"
ssh = "lab.example"
login_push = ["codex"]
```

- The worker reads `~/.codex/auth.json` on its own computer. Within 30 seconds of each change (`FLEET_LOGIN_PUSH_INTERVAL_S`), it writes a copy over the host's route as `~/.codex/auth.json` of the user that route signs in as, mode 0600. Every home on the host then uses that copy as the computer's own login.
- The copy has no refresh token. It works until its access token expires, and only a new Codex sign-in on the worker's computer, or Codex there renewing the token, gives the host a new one.
- `dockingbird status` shows when the pushed Codex copy expires, and an expired copy is refused. [sign-in-and-api-keys.md](../../guides/sign-in-and-api-keys.md) says how to renew it.
- A host that already holds a Codex login of its own keeps it. The worker never writes over it and logs that once.
- When the login on the worker's computer is gone, the worker removes the copy from the host.
- `set` keeps the key and has no option for it. Write it by hand.

`codex` is the only word the key takes, because Claude reaches a pool host through its gateway and a Claude login is never copied. The key is refused on a `local = true` entry, which is this computer.

To stop the copy, take these steps in order. A new login on the worker's computer does not revoke a copy already pushed, which works until its token expires.

1. Remove `login_push` from the worker's `hosts.toml` and restart the worker.
2. Delete `~/.codex/auth.json` on the host.
3. Run `dockingbird logout codex` in each of the host's homes.

A Dockingbird older than v0.15.5 does not know the key and refuses the whole file with `FLEET_HOSTS_FILE_INVALID`, so write it on a computer that runs the newer release.

## The rules

Dockingbird reads the file before every fleet command that uses it and refuses one that breaks a rule.
The refusal names the rule's place, such as `host[2].ssh` numbered from 1, and never a value (`FLEET_HOSTS_FILE_INVALID`).
Every value reaches a command as one word, so the rules refuse a value that could be read as an option or split in two.

| Applies to | Rule |
|---|---|
| the file | TOML of at most 1 MiB, a regular file of yours (not a link), holding `[[host]]` and `[[home]]` tables alone, each with no key but its own |
| a `[[host]]` | a `name` and exactly one of `ssh` and `gcloud`, or `local = true` with neither; `gcloud` with both `zone` and `project`; `ssh` with none of `zone`, `project` and `gcloud_program`; every value text |
| `ssh` | not empty, no leading `-`, no whitespace |
| `gcloud`, `zone`, `project` | not empty, no leading `-`, lowercase letters, digits, `-`, `.` and `:` alone |
| `login_push` | a list of one or two texts, none twice, each `codex`, and never on a `local = true` entry |
| `path` | not empty |
| `docker_host` | not empty, no whitespace |
| `gcloud_program`, and each home's `path`, `program` and `clones` | an absolute path |
| every value | no character that is not printable |
