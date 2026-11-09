---
title: Two Macs over ssh
summary: Add a second Mac as a host over ssh, fix its PATH and Docker socket, read its agents and attach to one.
audience: daily
commands:
  - fleet hosts set --ssh
  - fleet hosts
  - fleet agents --host
  - fleet attach
  - fleet hosts rename
  - fleet hosts forget
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Two Macs, over ssh

You work on one Mac, and another Mac, `lab`, runs agents of its own. Once this Mac knows how to reach `lab`, the fleet commands show `lab`'s homes and agents beside this Mac's own, `local`. The [GUI](../../docs/guides/gui.md) lists the hosts in its sidebar and adds, renames or forgets one. [Hosts](../../docs/guides/hosts.md) is the guide behind this example.

## Before you start

- Dockingbird is installed and set up on both Macs ([One Mac, day one](../one-mac/README.md)).
- This Mac's ssh reaches `lab` with no question asked: `ssh lab.example true` returns at once. Dockingbird runs your own ssh, with your own configuration and keys, and never copies or forwards a key.
- `lab` has Remote Login on (System Settings, General, Sharing).

Try what Dockingbird will run first.

```bash
ssh lab.example docker version
```

Done: Docker's client and server versions.

## Add `lab`

```bash
dockingbird fleet hosts set lab --ssh lab.example
```

`set` reaches `lab` and reads its Docker and its Dockingbird homes as `dockingbird fleet agents --host lab` does. Once that read succeeded, it saves the host, then prints what it read and says so. The last line is the done line (`FLEET_HOSTS_SET`).

```text
lab: 2 agents running in 1 home
...
lab: ssh lab.example, saved in ~/.local/share/dockingbird/hosts.toml.
```

When it can't read `lab`, it saves nothing and says what to try. The usual cause on a Mac: a login over ssh has a shorter `PATH` than a terminal, without the folder of Docker Desktop's `docker`. Give the commands run there a `PATH` that holds it.

```bash
dockingbird fleet hosts set lab --ssh lab.example --path /Applications/Docker.app/Contents/Resources/bin:/usr/bin:/bin
```

Done: `lab: ssh lab.example, updated in ~/.local/share/dockingbird/hosts.toml.` when the first attempt had saved the host, else the `saved in` line. The command writes [this file's](hosts.toml) table.

```toml
[[host]]
name = "lab"
ssh = "lab.example"
path = "/Applications/Docker.app/Contents/Resources/bin:/usr/bin:/bin"
```

`path` names Docker Desktop's folder, then the system's. When `lab`'s Docker answers on a socket other than the default one, `--docker-host URL` sets the `docker_host` key: the `DOCKER_HOST` value the commands run with there, `unix://` followed by the socket's path. Docker Desktop keeps its socket inside the login's own home folder, under `.docker/run/`, unless its settings allow the default socket. `docker context inspect`, run on `lab`, prints the one it uses.

## Every day

```bash
dockingbird fleet hosts                # the hosts this Mac reaches
dockingbird fleet agents --host lab    # lab's homes and agents
dockingbird fleet agents               # this Mac's, local
```

The three commands print these first lines, in order, and the last two add a row for every home and every agent (`FLEET_HOSTS_ROW`, `FLEET_HOST_ROW`).

```text
lab: ssh lab.example
lab: 2 agents running in 1 home
local: 5 agents running in 3 homes
```

To open a terminal agent of `lab` on this Mac, take its full container id from the JSON listing and attach. The attach prints its done line, and Ctrl-] then Ctrl-\ leaves the agent running.

```bash
dockingbird --json fleet agents --host lab
dockingbird fleet attach --host lab --container ID
```

```text
Opening NAME on lab. Ctrl-] then Ctrl-\ leaves it running.
```

Rename the host, or remove it from the file, with the next two commands. The page on [the hosts file](../../docs/reference/files/hosts-file.md) lists every key and rule of the file.

```bash
dockingbird fleet hosts rename lab bench
dockingbird fleet hosts forget bench
```

## When it fails

| Message id | What happened |
|---|---|
| [`FLEET_HOSTS_NOT_REACHED`](../../docs/troubleshooting.md#fleet_hosts_not_reached) | `set` could not read `lab` and saved nothing; the message gives `ssh lab.example docker version` to try, and `--path` and `--docker-host` when Docker is there but the login does not find it |
| [`FLEET_HOST_NOT_READ`](../../docs/troubleshooting.md#fleet_host_not_read) | `fleet agents --host lab` could not read `lab` |
| [`FLEET_HOST_UNKNOWN`](../../docs/troubleshooting.md#fleet_host_unknown) | the `--host` name is not in the file; `fleet hosts` lists the names |
| [`FLEET_HOSTS_FILE_INVALID`](../../docs/troubleshooting.md#fleet_hosts_file_invalid) | a value in `hosts.toml` breaks a rule |
| [`FLEET_HOSTS_IN_USE`](../../docs/troubleshooting.md#fleet_hosts_in_use) | the host is in a fleet pool; drain and remove it there before `rename` or `forget` |
| [`FLEET_ATTACH_BAD_CONTAINER`](../../docs/troubleshooting.md#fleet_attach_bad_container) | `--container` is not a full container id; exit 2 |
| [`FLEET_ATTACH_GONE`](../../docs/troubleshooting.md#fleet_attach_gone) | the agent ended after the list was read |
