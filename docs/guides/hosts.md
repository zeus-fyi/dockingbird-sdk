---
title: Hosts
summary: Add a second computer or a cloud VM as a host, read every agent on every host, attach to one, and read one Mac's load.
audience: daily
commands:
  - fleet hosts set
  - fleet hosts rename
  - fleet hosts forget
  - fleet hosts
  - fleet agents
  - fleet attach
  - fleet probe
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Hosts

This page adds a second computer to your Dockingbird, over ssh or through gcloud. It then reads the agents that run there and opens one of them in your terminal. A host is a computer with Dockingbird homes of its own. Your own computer never needs an entry in the file, because every fleet line already calls it `local`.

## Before you start

- Dockingbird is installed and set up on the host, as on this computer. Check on the host with `dockingbird --version`.
- Docker answers on the host. Check from here with `ssh lab.example docker version`, or for a Compute Engine VM with `gcloud compute ssh cloud-1 --zone europe-west1-b --project example-project -- docker version`.
- Your own ssh reaches the host without asking a question. Check with `ssh lab.example true`, which returns at once. Dockingbird runs your own ssh with your own configuration and agent, and never copies a key. A host that does not answer within 15 seconds is not reached.
- A cloud VM that is stopped must be started first. A stopped VM cannot be read.
- Networking, if the host is not on your LAN: [networking](networking.md), [Tailscale](tailscale.md), [other networks](other-networks.md).

## Add a host over ssh

```bash
dockingbird fleet hosts set lab --ssh lab.example
```

The command reaches the host and reads its Docker and its Dockingbird homes. That is the same read the agents listing makes, and it starts and changes nothing on the host. Only after the read succeeds does the command write the host into your hosts file and print the rows it read. The last line is the done line.

```text
lab: 2 agents running in 1 home
...
lab: ssh lab.example, saved in ~/.local/share/dockingbird/hosts.toml.
```

That last line is message `FLEET_HOSTS_SET`. Run the command again with a name the file already holds, and it replaces the route while it keeps the host's home tables and its place in the file. The done line then ends with the words `updated in`, which is `FLEET_HOSTS_UPDATED`. A name is lowercase letters, digits and dashes, at most 56 characters, and never `local`.

## Add a Compute Engine VM through gcloud

```bash
dockingbird fleet hosts set cloud --gcloud cloud-1 --zone europe-west1-b --project example-project
```

Dockingbird reaches the VM through your own gcloud. It uses the one on your search path, or else the one the Google Cloud SDK installs. When yours lives somewhere else, write its absolute path into the host's table by hand, under the key `gcloud_program`. A VM of another cloud is a host over ssh instead. The done line has the same shape as the ssh one.

```text
cloud: gcloud cloud-1, saved in ~/.local/share/dockingbird/hosts.toml.
```

The guide on [cloud VMs](cloud-vms.md) covers the VM itself.

## Fix a host that cannot be read

When the read fails, nothing is saved. The command ends 1 and prints the command to try yourself first. Run that command, fix what it shows, then run `set` again.

| What ssh or Docker shows | Fix | Then |
|---|---|---|
| `docker` is not found over ssh, while it works in a terminal on the host | give the commands a `PATH` with the folder that holds `docker` | add `--path PATH` |
| Docker Desktop's socket is not the default one | give the commands that socket as `DOCKER_HOST` | add `--docker-host unix://SOCKET` |
| the host does not answer | start the host, check the route | run `set` again |

On a Mac, the folder is usually Docker Desktop's.

```bash
dockingbird fleet hosts set lab --ssh lab.example --path /Applications/Docker.app/Contents/Resources/bin:/usr/bin:/bin
```

`--path` writes the `path` key and `--docker-host` writes the `docker_host` key. Both apply only to the ssh route. `--home HOME` adds a table for one of the host's homes by name, without checking that it exists.

## Read the hosts and their agents

```bash
dockingbird fleet hosts
dockingbird fleet agents --host lab
dockingbird fleet agents
```

The first command prints one line per host in the file, in the file's order (`FLEET_HOSTS_ROW`).

```text
lab: ssh lab.example
cloud: gcloud cloud-1
```

The agents listing covers every Dockingbird agent on one computer, in every home and on every version. It reads Docker alone, runs no Dockingbird command in those homes, and changes nothing. Without a host option it reads this computer, so a fresh install shows `local` with nothing written in any file. A host that cannot be read ends with exit 1 and the line `Couldn't read NAME`, then the cause (`FLEET_HOST_NOT_READ`). Each read gets at most 20 seconds.

| Line | What it shows |
|---|---|
| `lab: 2 agents running in 1 home` | the first line: how many agents in how many homes (`FLEET_HOST_ROW`) |
| a home row | the home's folder, its version, whether it is running, how many agents run in it (`FLEET_HOME_ROW`) |
| an agent row | the name, `bus` or `terminal`, `screen` or `no screen`, and its state (`FLEET_AGENT_ROW`) |
| a swarm row | how many agents of a swarm run and wait, with its project, priority and state (`FLEET_SWARM_ROW`) |

| State | Meaning |
|---|---|
| `working` | its home's coordinator reports it at work |
| `idle` | its home's coordinator reports it idle |
| `asks` with a number | it waits for that many questions to be answered |
| `unknown` with a reason | `no-coordinator`, `timeout`, `refused`, `unexpected-shape`, `not-read` or `no-session` |

A script reads the same rows with `--json`, one envelope per line, and each agent's full container id is in them. In that output the `host` of a row of this computer is `null`.

## Attach to an agent

```bash
dockingbird --json fleet agents --host lab
dockingbird fleet attach --host lab --container ID
```

The first command lists every agent as JSON, with the full container id of each, 64 letters and digits. The second opens one agent in your terminal, so it needs a real terminal, and it prints its done line before it hands you the agent's screen.

```text
Opening claude-1 on lab. Ctrl-] then Ctrl-\ leaves it running.
```

That line is `FLEET_ATTACHING`. Some agents have no screen. You then see the agent's log as it grows, and each line you type and send with Enter reaches the agent as a message (`FLEET_FOLLOWING`). Press Ctrl-C to close that view. The agent keeps working either way.

Messages to an agent with no screen are sent by its home's own `dockingbird send`. The hosts file must therefore name that program for the home, and [the hosts file](../reference/files/hosts-file.md) shows how. On another host, the log may end with a line from ssh itself, `Connection to NAME closed.`

## Rename or forget a host

```bash
dockingbird fleet hosts rename lab bench
dockingbird fleet hosts forget bench
```

```text
lab is now bench in ~/.local/share/dockingbird/hosts.toml.
bench is forgotten: its entry is removed from ~/.local/share/dockingbird/hosts.toml.
```

The first line is `FLEET_HOSTS_RENAMED`, with a second line saying that swarm definitions and pool records that name `lab` are not changed. The second is `FLEET_HOSTS_FORGOTTEN`. Both change only the file, and nothing on the host. A host that the fleet pool holds is refused with `FLEET_HOSTS_IN_USE`: drain it and remove it there first (`dockingbird fleet hosts drain NAME`, then `dockingbird fleet hosts remove NAME`), then rename it here, then enrol it again under its new name. A host has one name across your file, the pool and swarm definitions ([fleet scheduler](fleet-scheduler.md)).

## Read one Mac's load

```bash
dockingbird fleet probe
```

`fleet probe` reads this Mac and its Docker once and prints a line per figure: cores, memory, load against the load line, CPU, swap, GPU, Docker's VM, containers, networks, then each kind of process with its CPU, memory and count. It first prints `This Mac:` with the cores and memory. It shows numbers and kinds only, never a program's name. With `--json` it prints one line holding every container of every home. `--disk` also reads Docker's disk use, which is slow on a large image store.

It starts, stops and changes nothing, gives each read at most 20 seconds and the whole run 60, and ends 0 with whatever it read. A part it could not read says `unread`, and the screen ends `Not read: ...` (`FLEET_PROBE_UNREAD`). It runs on a Mac only. On Linux it ends 1 with `The fleet probe reads macOS only` (`FLEET_PROBE_NOT_MACOS`), and it reads this computer, never a host. To read a Mac host, run it on that Mac.

The GUI lists the hosts in its sidebar and adds, renames and forgets one with the same commands. See [the GUI](gui.md#3-what-the-window-shows).

## When it fails

Each message id below links to its entry in the catalogue.

- [`FLEET_HOSTS_NOT_REACHED`](../troubleshooting.md#fleet_hosts_not_reached) means `set` could not read the host. It saved nothing, and the message prints the command to try yourself.
- [`FLEET_HOST_NOT_READ`](../troubleshooting.md#fleet_host_not_read) means the agents listing could not read the host, or `local`. The line ends with the error that ssh, gcloud or Docker printed.
- [`FLEET_HOST_UNKNOWN`](../troubleshooting.md#fleet_host_unknown) means the `--host` name is not in the file. `fleet hosts` lists the names, and the message prints the `set` line that adds it.
- [`FLEET_HOSTS_ROUTE_NEEDED`](../troubleshooting.md#fleet_hosts_route_needed) means `set` got no route, or got both. Give `--ssh DEST`, or `--gcloud VM` with `--zone` and `--project`. It exits 2.
- [`FLEET_HOSTS_NAME_INVALID`](../troubleshooting.md#fleet_hosts_name_invalid) means the name is not lowercase letters, digits and dashes. It exits 2, and nothing was read or written.
- [`FLEET_HOSTS_LOCAL_FIXED`](../troubleshooting.md#fleet_hosts_local_fixed) means no host may take the name `local`, which every computer uses for itself. It exits 2.
- [`FLEET_HOSTS_NAME_TAKEN`](../troubleshooting.md#fleet_hosts_name_taken) means `rename` asked for a name the file already holds. It exits 2.
- [`FLEET_HOSTS_IN_USE`](../troubleshooting.md#fleet_hosts_in_use) means the fleet pool still lists the host, so `rename` and `forget` wait until you drain and remove it there.
- [`FLEET_HOSTS_BUSY`](../troubleshooting.md#fleet_hosts_busy) means another command was writing the file at that moment. Run yours again.
- [`FLEET_HOSTS_FILE_INVALID`](../troubleshooting.md#fleet_hosts_file_invalid) means the file breaks a rule. The message names the key and never a value, and no host is read until you fix it.
- [`FLEET_ROWS_SKIPPED`](../troubleshooting.md#fleet_rows_skipped) means some rows of the host's Docker listing could not be read. The rest is shown.
- [`FLEET_ATTACH_NO_CONTAINER`](../troubleshooting.md#fleet_attach_no_container) means `attach` got no `--container`. It exits 2.
- [`FLEET_ATTACH_BAD_CONTAINER`](../troubleshooting.md#fleet_attach_bad_container) means the value is not a full container id. It exits 2.
- [`FLEET_ATTACH_NOT_A_TERMINAL`](../troubleshooting.md#fleet_attach_not_a_terminal) means the input or output went to a file or a pipe. Run it in a terminal.
- [`FLEET_ATTACH_GONE`](../troubleshooting.md#fleet_attach_gone) means the agent ended after the list was read. Nothing was opened.
- [`FLEET_ATTACH_FAILED`](../troubleshooting.md#fleet_attach_failed) means Docker, ssh, gcloud or the home's own `dockingbird` would not start. The line ends with the system's words.
- [`FLEET_PROBE_NOT_MACOS`](../troubleshooting.md#fleet_probe_not_macos) means the probe ran on a computer that is not a Mac. It exits 1.
- [`FLEET_PROBE_NO_SYSCTL`](../troubleshooting.md#fleet_probe_no_sysctl) means the probe could not read this Mac's cores, so it stopped. It exits 1.

Every key of `hosts.toml` is in [the hosts file](../reference/files/hosts-file.md). Two worked examples are [two Macs over ssh](../../examples/two-macs-ssh/README.md) and [a cloud VM over gcloud](../../examples/cloud-vm-gcloud/README.md).
