---
title: A host behind a bastion
summary: Reach a host that only a bastion reaches with a ProxyJump entry, add it with fleet hosts set, and fix its PATH.
audience: team-admin
commands:
  - fleet hosts set --ssh
  - fleet agents
  - fleet attach
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# A host behind a bastion

You end with a host that only a bastion can reach, listed by `dockingbird fleet hosts` and read by `dockingbird fleet agents --host lab`. The example uses the bastion `bastion.lab.example` and the host `lab-1.internal.example`. The guide on [other networks](../../docs/guides/other-networks.md) explains the pieces.

## Before you start

| You need | Check |
|---|---|
| Dockingbird set up on the host, with Docker running | `ssh lab-1.internal.example docker version` works from the bastion |
| your ssh reaching the bastion with no question, so the key sits in your ssh agent | `ssh ops@bastion.lab.example true` returns at once |
| the bastion reaching the host's ssh | the same check, run from the bastion |

## Steps

### 1. Write the ssh entries

Add two entries to `~/.ssh/config`. OpenSSH reads `ProxyJump` as one or more jump hosts in the form `[user@]host[:port]`, visited in order. The step is done when the file saves.

```text
Host bastion
  HostName bastion.lab.example
  User ops

Host lab
  HostName lab-1.internal.example
  ProxyJump bastion
```

### 2. Reach the host through the bastion

This command succeeds when it returns at once and prints nothing.

```bash
ssh lab true
```

### 3. Run the command Dockingbird runs

Dockingbird reads a host with this exact kind of call. It prints Docker's client and server versions when the route and the login's `PATH` are right. If it says `docker` is missing, do step 5 first.

```bash
ssh lab docker version
```

### 4. Add the host

Give Dockingbird the entry's name as the destination. It saves nothing until a read of the host has worked, then prints the rows it read and the last line below.

```bash
dockingbird fleet hosts set lab --ssh lab
```

```text
lab: 2 agents running in 1 home
...
lab: ssh lab, saved in ~/.local/share/dockingbird/hosts.toml.
```

The command writes this table.

```toml
[[host]]
name = "lab"
ssh = "lab"
```

### 5. Fix the PATH if the read fails

A login over ssh sometimes has a shorter search path than a terminal, and `docker` is not on it. Ask the host where `docker` lives, then pass those folders to `set` as the `path` key. The second command prints a last line that ends `updated in` followed by the file's path. `--docker-host URL` sets `DOCKER_HOST` the same way, for a socket that is not the default one.

```bash
ssh lab 'command -v docker'
dockingbird fleet hosts set lab --ssh lab --path /usr/local/bin:/usr/bin:/bin
```

### 6. Read the host's agents

The first command prints `lab: ssh lab`. The second prints `lab: 2 agents running in 1 home`, then a row for each home and each agent.

```bash
dockingbird fleet hosts
dockingbird fleet agents --host lab
```

### 7. Attach to one agent

Take the agent's container id from the JSON listing, then attach. The attach prints `Opening NAME on lab.` and tells you that Ctrl-] then Ctrl-\ leaves the agent running.

```bash
dockingbird --json fleet agents --host lab
dockingbird fleet attach --host lab --container ID
```

## When it fails

| Message id | What happened |
|---|---|
| [`FLEET_HOSTS_NOT_REACHED`](../../docs/troubleshooting.md#fleet_hosts_not_reached) | the read through the bastion failed and nothing was saved; the message gives `ssh lab docker version` to try, and `--path` when the login's `PATH` lacks `docker` |
| [`FLEET_HOST_NOT_READ`](../../docs/troubleshooting.md#fleet_host_not_read) | the agents listing could not read the host |
| [`FLEET_HOST_UNKNOWN`](../../docs/troubleshooting.md#fleet_host_unknown) | the `--host` name is not in the file; `fleet hosts` lists the names |
| [`FLEET_HOSTS_FILE_INVALID`](../../docs/troubleshooting.md#fleet_hosts_file_invalid) | a value in `hosts.toml` breaks a rule, such as a space in `ssh` |
| [`FLEET_ATTACH_BAD_CONTAINER`](../../docs/troubleshooting.md#fleet_attach_bad_container) | the value is not a full container id; exit 2 |
| [`FLEET_ATTACH_GONE`](../../docs/troubleshooting.md#fleet_attach_gone) | the agent ended after the list was read |
