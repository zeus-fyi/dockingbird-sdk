# `hosts.toml`: the other computers you reach

`hosts.toml`, in your Dockingbird home (`~/.local/share/dockingbird/hosts.toml`, unless `DOCKINGBIRD_HOME` names
another folder), names the other computers whose agents `dockingbird fleet agents --host NAME` reads and
`dockingbird fleet attach --host NAME` opens, and that the GUI shows beside this computer's. This computer itself is
never an entry: it is `local` in every fleet line, and `fleet agents` always reads it. With no file, there are no other
hosts, and that is no error.

## The three commands that write it

```
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
nothing. With `--json`, each line is an envelope ([the envelope](json.md)).

You may still write the file by hand. A write by Dockingbird keeps every table and their order, and leaves the file
readable by you alone (0600), but loses a hand-written file's comments and the order of keys inside a table.

## One name

A host has one name: its `name` here, what `--host` takes and the rows say, which is also its name in the fleet pool
when it is in one, and the name a swarm definition places work on. On a computer whose Dockingbird home holds a
`fleet.toml`, `rename` and `forget` of a host the pool holds are refused (`FLEET_HOSTS_IN_USE`): drain and remove it
from the pool first, then rename it here, then enrol it again under its new name.

## `[[host]]`: one per computer

Each `[[host]]` has a `name` and one route: `ssh`, or `gcloud` with `zone` and `project`.

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

## `[[host.home]]` and `[[home]]`: a home's own program

A `[[host.home]]` table after a host's keys names one of that host's Dockingbird homes; a top-level `[[home]]` table
names a home of this computer. Each has two keys, both absolute paths: `path`, the home's folder, and `program`, that
home's own `dockingbird`, which a send to one of its agents with no screen runs there. They are written by hand; `set`
keeps them.

```toml
[[host]]
name = "lab"
ssh = "lab.example"

[[host.home]]
path = "/opt/dockingbird/homes/team-1"
program = "/opt/dockingbird/bin/dockingbird"
```

## The rules

Dockingbird reads the file before every fleet command that uses it and refuses one that breaks a rule, naming the rule's
place (`host[2].ssh`, numbered from 1) and never a value (`FLEET_HOSTS_FILE_INVALID`). Every value reaches a command as
one word, so the rules refuse a value that could be read as an option or split in two:

- the file: TOML of at most 1 MiB, a regular file of yours (not a link), holding `[[host]]` and `[[home]]` tables
  alone, each with no key but its own;
- a `[[host]]`: a `name` and exactly one of `ssh` and `gcloud`; `gcloud` with both `zone` and `project`; `ssh` with
  none of `zone`, `project` and `gcloud_program`; every value text;
- `ssh`: not empty, no leading `-`, no whitespace;
- `gcloud`, `zone` and `project`: not empty, no leading `-`, lowercase letters, digits, `-`, `.` and `:` alone;
- `path`: not empty; `docker_host`: not empty, no whitespace;
- `gcloud_program`, and each home's `path` and `program`: an absolute path;
- no value holds a character that is not printable.
