---
title: A fleet on a tailnet
summary: Make one home the control plane at its tailnet address, serve its hub port, grant a tagged VM access, and join each computer once.
audience: team-admin
commands:
  - cp init --hub-address
  - tailscale serve
  - cp token
  - node join
  - cp status
  - cp remove
  - node leave
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# A fleet on a tailnet

You end with a control plane on one computer and a second computer joined to it over your tailnet, so that an agent on the second computer has a fleet inbox. The example joins a Linux VM labelled `lab`, tagged `tag:lab`, to a control plane on the computer that your policy calls `control-plane.example`. The [Tailscale guide](../../docs/guides/tailscale.md) explains each step in more depth.

## Before you start

| You need | Check |
|---|---|
| Dockingbird on both computers | `dockingbird --version` prints a version on each |
| both computers on your tailnet | `tailscale ip -4` prints one IPv4 address on each |
| no agent running in the control plane's home or the joining home | `dockingbird stop` prints `Nothing is running. Dockingbird is off.` |
| edit rights on your tailnet's policy, with `tag:lab` in its `tagOwners` section | the policy file opens and saves |

## Steps

### 1. Read the control plane's tailnet address

Run this on the control plane's computer. It prints one IPv4 address, which the steps below call `<ipv4>`.

```bash
tailscale ip -4
```

### 2. Make the home the control plane

On the control plane's home, run `cp init` with that address. It is done when it prints these lines.

```bash
dockingbird cp init --hub-address <ipv4>
```

```text
This home is now the fleet's control plane, at <ipv4>:4222.
Make a bundle for each computer that joins:
dockingbird cp token --host LABEL --platform PLATFORM
```

### 3. Serve the hub's port to the tailnet

Docker publishes the hub's port on the control plane's loopback only. On that computer, forward the tailnet's port 4222 to it. The command is done when it returns with no error. Tailscale's page quotes no output line for it, so the join in step 6 is the real proof.

```bash
tailscale serve --bg --tcp 4222 tcp://127.0.0.1:4222
```

### 4. Grant the tag access

Your own devices on the tailnet need no grant, but a VM under a tag does. Add this line to your tailnet's policy, and the step is done when the policy saves.

```json
{"src": ["tag:lab"], "dst": ["control-plane.example"], "ip": ["tcp:4222"]}
```

### 5. Make a bundle for the VM

On the control plane's home, pick a label for the VM: one to eight lowercase letters and digits, starting with a letter. The command prints three lines and then the bundle on a line of its own. Copy the bundle now, since it is shown once and kept nowhere on the control plane.

```bash
dockingbird cp token --host lab --platform linux
```

```text
lab is enrolled as node NODE_ID (linux).
Its bundle is the next line, shown once and not kept here:
paste it into dockingbird node join on that computer.
```

### 6. Join from the VM

On the VM's home, run node join and paste the bundle from step 5. Joining has worked when two lines come back. They name the label `lab` and the node id the control plane gave the VM. They also say that each agent started from now on gets a fleet inbox.

```bash
dockingbird node join
```

```text
This computer joined the fleet as lab (node NODE_ID).
Each agent started here from now on gets a fleet inbox.
```

### 7. List the computers

Back on the control plane's home, read the fleet. The step is done when the VM has a row with its node id, its platform, its state, its version and its fleet inboxes. If the output says that no computer has joined the fleet yet, no bundle was made or every computer was removed.

```bash
dockingbird cp status
```

### 8. Start an agent on the VM

Start an agent on the VM with claude inside any repository, then run status. The agent's entry gains a fleet line. It holds the label `lab`, a dash, the agent's name, a heartbeat age and a count of open questions. The words `fleet: not open` instead mean the control plane has not opened the session yet.

```bash
dockingbird status
```

```text
fleet: lab-NAME, heartbeat AGE, asks N
```

## Take a computer out and bring it back

On the control plane's home, `cp remove` disables the computer, revokes its token and ends its agents' fleet sessions. On the computer, `node leave` removes its credential. To join again, make a new bundle and join with it.

```bash
dockingbird cp remove lab
dockingbird cp token --host lab --platform linux
dockingbird node leave
dockingbird node join
```

The removal prints these lines.

```text
lab (node NODE_ID) is out of the fleet;
N fleet inboxes of its agents closed.
Its own agents keep running there without the fleet.
```

Leaving prints `This computer left the fleet.` and then says the agents keep running, with their fleet inboxes gone. When every computer is removed, `dockingbird cp off` prints that this home is a plain home again.

## When it fails

| Message id | What happened |
|---|---|
| [`MODE_CHANGE_AGENTS_RUNNING`](../../docs/troubleshooting.md#mode_change_agents_running) | agents run in the home; run `dockingbird stop`, then the command again |
| [`CP_ALREADY_INITIALIZED`](../../docs/troubleshooting.md#cp_already_initialized) | the home is already the control plane; nothing changed |
| [`NATS_SERVER_UNAVAILABLE`](../../docs/troubleshooting.md#nats_server_unavailable) | the hub did not answer in time; run the command again |
| [`NODE_ALREADY_ENROLLED`](../../docs/troubleshooting.md#node_already_enrolled) | the control plane already used that bundle; run `cp remove`, then `cp token` |
| [`NODE_ALREADY_JOINED`](../../docs/troubleshooting.md#node_already_joined) | the home is in the fleet; run `node leave` first |
| [`RPC_PEER_HOST_MISMATCH`](../../docs/troubleshooting.md#rpc_peer_host_mismatch) | the bundle was made for another computer |
| [`FLEET_SESSION_NOT_OPENED`](../../docs/troubleshooting.md#fleet_session_not_opened) | the agent has no fleet inbox yet; check the serve line and the grant |
| [`NODE_VERSION_MISMATCH`](../../docs/troubleshooting.md#node_version_mismatch) | the versions differ; update the control plane's home first, then each member |
| [`NODE_SESSIONS_LIVE`](../../docs/troubleshooting.md#node_sessions_live) | `node leave` found agents that still use the fleet; stop them first |
| [`CP_HOSTS_ENABLED`](../../docs/troubleshooting.md#cp_hosts_enabled) | `cp off` found computers still in the fleet; remove each one first |
