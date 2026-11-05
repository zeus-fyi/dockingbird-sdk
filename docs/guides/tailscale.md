---
title: Tailscale
summary: Use a tailnet as the fleet's network, with the hub address, the serve line, the grant for a tagged VM and MagicDNS names for ssh.
audience: team-admin
commands:
  - cp init --hub-address
  - cp token
  - node join
  - cp status
  - fleet hosts set --ssh
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Tailscale

This page puts the fleet on a tailnet. The control plane's tailnet address becomes the hub address, `tailscale serve` puts the hub's port on the tailnet, a grant lets a tagged VM reach it, and MagicDNS names reach each host over ssh. Dockingbird publishes no port to the internet for any of this. Its hub port is on loopback until you serve it.

## Before you start

- Every computer of the fleet is a device of your tailnet. Check on each with `tailscale ip -4`, which prints the device's IPv4 address.
- Dockingbird is installed on each computer. Check with `dockingbird --version`.
- No agent runs in the home that becomes the control plane, or in a home that joins. `cp init` and `node join` refuse with `MODE_CHANGE_AGENTS_RUNNING` until `dockingbird stop` has stopped them.
- MagicDNS is on, if you want to type host names. Tailnets created on or after October 20, 2022 have it on by default.
- For a member in a cloud under a tag, the tag exists in your tailnet policy. Tags are defined by their owners in the `tagOwners` section.

## Find the control plane's tailnet address

Run this on the computer that holds the control plane's home.

```bash
tailscale ip -4
```

It prints that device's IPv4 address, and no IPv6 address. The steps below call it `<ipv4>`. In a policy, the name `control-plane.example` stands for the same device.

## Make the home the control plane

```bash
dockingbird cp init --hub-address <ipv4>
```

```text
This home is now the fleet's control plane, at <ipv4>:4222.
Make a bundle for each computer that joins:
dockingbird cp token --host LABEL --platform PLATFORM
```

That output is `CP_INITIALIZED`. The home keeps the control plane's key beside the hub's address. Run `cp init` on a home that is already the control plane, and it changes nothing and prints `CP_ALREADY_INITIALIZED`.

## Serve the hub's port to the tailnet

The hub listens on port 4222 of the control plane's computer, and Docker publishes that port on the computer's loopback only. This line, run on that computer, forwards the tailnet's port 4222 to it.

```bash
tailscale serve --bg --tcp 4222 tcp://127.0.0.1:4222
```

Tailscale describes `--bg` as running the command as a background process and `--tcp=<port>` as a raw TCP forwarder on that port. Tailscale's page does not quote an output line for it, so the proof is the join below. Frames between computers are as private as the tailnet.

## Let a tagged member reach the hub

A member that is your own device on the tailnet needs no grant. A member that is not your device, such as a VM in a cloud under a tag, needs this grant in your tailnet's policy, with its tag and the control plane's device in place of the placeholders.

```json
{"src": ["tag:lab"], "dst": ["control-plane.example"], "ip": ["tcp:4222"]}
```

Tailscale grants deny by default. A grant has a source, a destination and an `ip` field that names a protocol and a port, so this one admits devices tagged `lab` to TCP port 4222 of the control plane's device, and to no other port. Adding a tag to a device removes its associated user, so a tagged VM needs a grant of its own. [Cloud VMs](cloud-vms.md) lists the conditions a cloud member meets.

## Add each computer

On the control plane's home, make one bundle for each computer. The label is one to eight lowercase letters and digits, starting with a letter.

```bash
dockingbird cp token --host lab --platform linux
```

```text
lab is enrolled as node NODE_ID (linux).
Its bundle is the next line, shown once and not kept here:
paste it into dockingbird node join on that computer.
```

The control plane keeps only the computer's public key and its token's digest, never the bundle. A bundle joins once and decodes to at most 4096 bytes. On that computer's home, run `node join` and paste the bundle in, since the command reads standard input.

```bash
dockingbird node join
```

```text
This computer joined the fleet as lab (node NODE_ID).
Each agent started here from now on gets a fleet inbox.
```

Those two outputs are `CP_TOKEN_ISSUED` and `NODE_JOINED`. Back on the control plane's home, list the computers.

```bash
dockingbird cp status
```

Each computer gets one row. The row holds its label, node id and platform, then whether it joined, is waiting to join or was removed. It ends with the computer's version, its fleet inboxes and how long ago the control plane last heard from one of them. If you see `No computer has joined the fleet yet.` (`CP_STATUS_EMPTY`), no bundle was made or every computer was removed.

## Reach hosts by MagicDNS name

MagicDNS gives each device a fully qualified name made of its machine name and your tailnet's DNS name, and adds search domains so the machine name alone reaches it. Tailscale's own example is `ssh username@monitoring`. Dockingbird takes the same destination.

```bash
dockingbird fleet hosts set lab --ssh lab
```

```text
lab: ssh lab, saved in ~/.local/share/dockingbird/hosts.toml.
```

That is `FLEET_HOSTS_SET`. The destination is any word your own ssh reaches without asking, with no whitespace and no leading dash. Dockingbird copies no key, so the name only has to reach a host your own ssh accepts.

## Use Tailscale SSH instead of keys

Tailscale SSH lets the tailnet itself decide who may open an ssh connection. People are known by their tailnet identity, so no key has to sit on the host. To switch it on, run the command below on the host.

```bash
tailscale up --ssh
```

After that, your policy needs two entries. The first lets the source reach the destination on port 22. The second is an ssh rule with an action, and the action is either `accept` or `check`. Accept lets in anyone already signed in to the tailnet. Check asks people to sign in again once per check period, which is 12 hours unless you change it.

A prompt would stop Dockingbird, because its ssh must reach the host without asking. Choose accept for the user that runs Dockingbird. If your policy says check, open a terminal, run `ssh lab true`, sign in, and add the host before the period ends.

## After a restart and an update

After the control plane's computer restarts, the first `dockingbird cp status` on its home starts the control plane and its hub again, and every member's fleet-link reconnects by itself. To update, run `dockingbird update` on the control plane's home first, then on each member. A member that is behind has its fleet frames refused with `NODE_VERSION_MISMATCH` until the versions match, and its agents keep working on their own home.

To join a computer again after a lost home or a removal, run `dockingbird cp remove lab` and `dockingbird cp token --host lab --platform linux` on the control plane's home, then `dockingbird node leave` and `dockingbird node join` on the computer.

## When it fails

- [`CP_ALREADY_INITIALIZED`](../troubleshooting.md#cp_already_initialized): the home is already the control plane, so nothing changed. `cp status` lists the computers it holds.
- [`MODE_CHANGE_AGENTS_RUNNING`](../troubleshooting.md#mode_change_agents_running): agents still run in the home. Stop them with `dockingbird stop`, then try again.
- [`NATS_SERVER_UNAVAILABLE`](../troubleshooting.md#nats_server_unavailable): the hub took too long to answer. Everything else on the home works, so run the command again.
- [`NODE_ALREADY_ENROLLED`](../troubleshooting.md#node_already_enrolled): the control plane already used this bundle. Run `cp remove`, then `cp token` to get a new bundle.
- [`NODE_ALREADY_JOINED`](../troubleshooting.md#node_already_joined): the home is in the fleet already, so run `node leave` before you join again.
- [`RPC_PEER_HOST_MISMATCH`](../troubleshooting.md#rpc_peer_host_mismatch): you pasted a bundle made for another computer. Leave the fleet, then join with the bundle made for this one.
- [`FLEET_SESSION_NOT_OPENED`](../troubleshooting.md#fleet_session_not_opened): the control plane did not open an agent's fleet inbox. The agent works as usual. Check the serve line and the grant.
- [`NODE_VERSION_MISMATCH`](../troubleshooting.md#node_version_mismatch): the member and the control plane run different versions, so fleet messages wait. Update whichever is behind.
- [`NODE_SESSIONS_LIVE`](../troubleshooting.md#node_sessions_live): `node leave` found agents that still use the fleet. Stop them first.
- [`FLEET_HOSTS_NOT_REACHED`](../troubleshooting.md#fleet_hosts_not_reached): the host route failed. Run `ssh lab docker version` yourself to see why.

The cookbook for [a fleet on a tailnet](../../examples/fleet-on-a-tailnet/README.md) runs these steps in order, and [networking](networking.md) names the three routes.

## Sources

| Topic | Tailscale's page |
|---|---|
| MagicDNS names | https://tailscale.com/docs/features/magicdns |
| `tailscale ip` | https://tailscale.com/docs/reference/tailscale-cli |
| `tailscale serve` | https://tailscale.com/docs/reference/tailscale-cli/serve |
| Tailscale SSH | https://tailscale.com/docs/features/tailscale-ssh |
| Grants | https://tailscale.com/docs/features/access-control/grants |
| Tags | https://tailscale.com/docs/features/tags |
