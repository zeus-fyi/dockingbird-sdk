---
title: Join a second computer to a control plane
summary: Make a control plane, join a second computer with its own bundle, read its status, remove it, and join it again after a lost home.
audience: team-admin
commands:
  - cp init
  - cp token
  - node join
  - cp status
  - cp remove
  - node leave
  - cp off
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Join a second computer to a control plane

This cookbook joins a computer named `lab` to a control plane, so agents started on `lab` get a fleet inbox beside their own. It then removes `lab` and joins it again with a new bundle, as you would after a lost home. [The control plane concept page](../../docs/concepts/control-plane.md) explains the parts, and [the team fleet guide](../../docs/guides/team-fleet.md) covers the whole install.

## Before you start

- Two computers with the same Dockingbird release. Check each with `dockingbird --version`.
- A private network between them, and the control plane computer's IPv4 address on it. This cookbook uses the placeholder `100.64.0.1`.
- No agents running in the two homes. `cp init` and `node join` are refused while agents run (`MODE_CHANGE_AGENTS_RUNNING`). Stop them with `dockingbird stop`.
- A second computer you can open a terminal on. The commands below say which home runs each one.

## 1. Make the control plane

On the control plane's home, run `cp init` with the address the other computers reach it at. Then serve the hub's port to your network. The hub listens on port 4222 of that computer, published on loopback only, until you serve it.

```bash
dockingbird cp init --hub-address 100.64.0.1
tailscale serve --bg --tcp 4222 tcp://127.0.0.1:4222
```

The second line is for a tailnet, the network the product is built against. [Other networks](../../docs/guides/other-networks.md) covers the rest. The step is done when `cp init` prints this.

```text
This home is now the fleet's control plane, at {host}:{port}.
Make a bundle for each computer that joins.
dockingbird cp token --host LABEL --platform PLATFORM
```

A home that already is the control plane prints `CP_ALREADY_INITIALIZED` and changes nothing.

## 2. Make a bundle for lab

Each computer needs a bundle of its own, and you make it on the control plane's home. Give the computer a label of one to eight lowercase letters or digits, starting with a letter. Give its platform too, macos or linux. The control plane prints the bundle as one line and keeps no copy of it, so copy it before you clear the screen.

```bash
dockingbird cp token --host lab --platform macos
dockingbird cp status
```

The step is done when `cp token` prints the three lines below and the bundle follows. Until the computer joins, `cp status` lists it as waiting to join.

```text
lab is enrolled as node {node_id} (macos).
Its bundle is the next line, shown once and not kept here.
paste it into dockingbird node join on that computer.
```

## 3. Join

Now go to the home of the computer you named lab. Run `node join`, paste the bundle and press Control-D. The command reads the bundle from standard input, because a bundle never goes on a command line. A bundle joins one computer once.

```bash
dockingbird node join
```

The step is done when it prints this.

```text
This computer joined the fleet as lab (node {node_id}).
Each agent started here from now on gets a fleet inbox.
```

## 4. Read the status

On the control plane's home, `cp status` lists each computer on one line: its label and node id, its platform, whether it joined, waits to join or was removed, its version, how many of its agents have a fleet inbox and how long ago the control plane last heard from one. With `--json`, each line also carries when the computer joined and when it was removed.

```bash
dockingbird cp status
```

The step is done when `lab` shows as joined.

```text
  lab  {node_id}  macos  joined  {version}  0 fleet inboxes
```

Start an agent on `lab` and `dockingbird status` there shows its fleet session under it. The fleet name is the label, a dash and the agent's name.

```text
fleet: lab-notes-1, heartbeat {age}, asks {n}
```

## 5. Remove lab

`cp remove` takes the computer out at once, with no precondition. It revokes its token, closes its agents' fleet inboxes and drops the computer from the hub. The agents on `lab` keep running there without the fleet.

```bash
dockingbird cp remove lab
```

The step is done when it prints this.

```text
lab (node {node_id}) is out of the fleet;
{count} fleet inboxes of its agents closed.
Its own agents keep running there without the fleet.
```

## 6. Join again after a lost home

A computer whose home was lost, or that was removed, joins again with a new bundle. Remove it, make a new bundle, leave on the computer and join with the new bundle. Run the first two commands on the control plane's home and the last two on `lab`'s home.

```bash
dockingbird cp remove lab
dockingbird cp token --host lab --platform macos
dockingbird node leave
dockingbird node join
```

On a fresh home that never joined, `node leave` prints the second line below and changes nothing. A home that is still in the fleet prints the first, and then it must have no agent that uses the fleet (`NODE_SESSIONS_LIVE`). The final `node join` prints its joined line again.

```text
This computer left the fleet.
This computer isn't a fleet member; nothing changed.
```

## 7. Turn the control plane off

`cp off` turns the control plane back into a plain home once every computer is removed. While one is in the fleet it is refused.

```bash
dockingbird cp remove lab
dockingbird cp off
```

```text
This home is a plain home again; the fleet's control plane is off.
```

After the control plane's computer restarts, the first `dockingbird cp status` on its home starts the control plane again. The members reconnect by themselves.

## When it fails

Eight ids cover these steps. Read the one your command printed.

- [`CP_ALREADY_INITIALIZED`](../../docs/troubleshooting.md#cp_already_initialized) comes from a second `cp init` on the same home. Nothing changed, and `cp status` lists the computers.
- [`MODE_CHANGE_AGENTS_RUNNING`](../../docs/troubleshooting.md#mode_change_agents_running) appears when `cp init`, `cp off`, `node join` or `node leave` meets agents that still run in the home. Run `dockingbird stop` first.
- [`NODE_ALREADY_ENROLLED`](../../docs/troubleshooting.md#node_already_enrolled) appears when a bundle joined once already. Remove the label on the control plane's home and make a new bundle.
- [`NODE_ALREADY_JOINED`](../../docs/troubleshooting.md#node_already_joined) appears on a home that is in the fleet. Leave it, then join with the new bundle.
- [`NODE_SESSIONS_LIVE`](../../docs/troubleshooting.md#node_sessions_live) blocks `node leave` while an agent on this computer still holds a fleet inbox. Stop that agent, then leave.
- [`RPC_PEER_HOST_MISMATCH`](../../docs/troubleshooting.md#rpc_peer_host_mismatch) shows that a bundle made for one computer was used on another. Leave and join again with a bundle made for this computer.
- [`NODE_VERSION_MISMATCH`](../../docs/troubleshooting.md#node_version_mismatch) shows that the computer and the control plane run different releases. Fleet messages wait until you update the one that is behind.
- [`CP_HOSTS_ENABLED`](../../docs/troubleshooting.md#cp_hosts_enabled) answers a `cp off` while a computer remains in the fleet. Run `cp remove` for each, then try again.
