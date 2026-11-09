---
title: Run your own control plane
summary: Make a home the control plane, run its NATS hub, serve port 4222 to your private network, join and remove computers, check the hub, back it up, upgrade it and read what fails.
audience: team-admin
commands:
  - cp init --hub-address
  - cp token --host --platform
  - node join
  - node leave
  - cp status
  - cp status --json
  - cp remove
  - cp off
  - status
  - update
  - fleet scrape
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Run your own control plane

This page sets up a control plane on a computer or VM you run. It covers the hub that the control plane runs, how members reach it, and how you check, change, upgrade and troubleshoot it. You run the control plane yourself. The hub needs no PostgreSQL store of the fleet scheduler, so a team can use the control plane alone. [The control plane concept page](../concepts/control-plane.md) explains what it is, and [the team fleet guide](team-fleet.md) installs it together with the scheduler's store.

## Before you start

- One computer or VM for the control plane, and one or more member computers. Each runs Docker and Dockingbird, set up as in [prerequisites](../getting-started/prerequisites.md). Check each with `dockingbird --version`.
- The same Dockingbird release on the control plane and on every member. A member on another release has its fleet messages refused with `NODE_VERSION_MISMATCH`.
- A private network that every member reaches the control plane's computer on, and that computer's IPv4 address on it. This page uses the placeholder `100.64.0.1`. The hub has no TLS, so keep it off the internet.
- No agent running in the home that becomes the control plane or in a home that joins. `dockingbird status` lists agents, and `dockingbird stop` stops them.

## What the control plane runs

The control plane runs one NATS server, the hub, in a container of its own. You install nothing for it. The hub is part of the Dockingbird image that `dockingbird` builds and updates, and `cp init` starts it.

| Part | What it is |
|---|---|
| Program | `nats-server` 2.15.1, installed into the image from the NATS project's release for the image's platform. The image build checks the download's SHA-256 and runs `nats-server --version` to confirm the version. |
| Container | `dockingbird-cp-relay` (a named home adds a suffix). It runs the hub and a relay that hands each frame to the control plane. Docker restarts it on failure, at most 5 times. |
| Port | TCP 4222 inside the container, published on the loopback address of the control plane's computer only. This is the one port any Dockingbird container publishes. This release has no option to change it. |
| Configuration | `hub.conf`, a JSON file in the `cp` folder of the home's state volume. Dockingbird writes it. `cp init`, `cp token` and `cp remove` each write a new one and check it with `nats-server -t` before it replaces the old one. Do not edit it. |
| Users | One user for the control plane's relay and one for each member. Each user is an NKey, a public-key identity. The default permission denies publishing and subscribing, so a member publishes on its own request subject and reads only the replies under its own inbox prefix. |
| Storage | None in the hub. JetStream, NATS's stored-message feature, is off, and the cp-relay container is read-only apart from a temporary folder. Messages, deliveries, threads and attachments are rows in the control plane home's own database. |
| TLS | None. The hub has no TLS setting. WireGuard on a tailnet encrypts each hop, so frames are as private as the network you serve the port to. |

The hub's bounds are fixed in this release.

| Bound | Value |
|---|---|
| clients at once | 1024: one for each member and one for the control plane |
| one NATS message, headers included | 16,778,240 bytes |
| one control line | 4,096 bytes |
| ping interval, unanswered pings allowed | 10 seconds, 3 |
| a fleet call's wait for its answer | 30 seconds |
| wait for the hub's first greeting after a start | 10 seconds |

## 1. Make the home the control plane

On the control plane's computer, run `cp init` with the IPv4 address that the members reach. The command accepts any IPv4 address. Members read the address from their bundle, and it stays as the first `cp init` recorded it.

A computer that also runs your agents can keep the control plane apart in a named home, with `--home NAME` before the command, such as `dockingbird --home cp cp init ...`. Every later command on the control plane then takes the same `--home NAME`.

```bash
dockingbird cp init --hub-address 100.64.0.1
```

`cp init` makes the control plane's key, writes the hub's files, starts the container and waits for the hub to answer. It prints these lines when it is done.

```text
This home is now the fleet's control plane, at 100.64.0.1:4222.
Make a bundle for each computer that joins:
dockingbird cp token --host LABEL --platform PLATFORM
```

The first line is `CP_INITIALIZED`. A home that is already the control plane prints `CP_ALREADY_INITIALIZED` and changes nothing. An earlier `cp init` that stopped part way finishes when you run it again, and the line then says the hub address the first run recorded stands.

If the hub does not answer within 10 seconds, the command goes on and prints `NATS_SERVER_UNAVAILABLE`. Run any command on the home again, as [when it fails](#when-it-fails) says.

## 2. Serve port 4222 to your private network

Docker publishes the hub on loopback, so nothing on the network reaches it yet. On a tailnet, one command on the control plane's computer shares it.

```bash
tailscale serve --bg --tcp 4222 tcp://127.0.0.1:4222
```

A member that is one of your own devices needs nothing more. A member that is not, such as a cloud VM under a tag, also needs a grant in your tailnet's policy, with its tag and the control plane's device in place of these placeholders.

```text
{"src": ["tag:lab"], "dst": ["control-plane.example"], "ip": ["tcp:4222"]}
```

[Tailscale](tailscale.md) explains both lines. Other private networks are not covered. The product publishes the port on loopback and documents one way to serve it, `tailscale serve`. [Other networks](other-networks.md) says what is and is not documented for a plain VPN, so ask through [SUPPORT.md](../../SUPPORT.md) before you serve the hub over one. Never serve it on a public address, because anyone who reaches the port can try to connect.

## 3. Check that the hub answers

A NATS server greets every client with a line that starts with `INFO `, and Dockingbird itself waits for that line. From a member computer, open the port and read the line.

```bash
nc 100.64.0.1 4222
```

The first line printed starts with `INFO {`. Press Control-C to close the connection. A connection that fails or prints nothing means the serve step or the network is wrong, so fix it before you make bundles.

## 4. Add a member

Make the bundle on the control plane's home. The label is one to eight lowercase letters or digits and starts with a letter. The platform is `macos` or `linux`. The command prints the bundle once, as a single line, and keeps no copy of it. It then starts the hub again, because the hub reads its users only at start.

```bash
dockingbird cp token --host lab --platform linux
```

```text
lab is enrolled as node {node_id} (linux).
Its bundle is the next line, shown once and not kept here:
paste it into dockingbird node join on that computer.
```

The first line is `CP_TOKEN_ISSUED`. The control plane keeps the computer's public key and a digest of its token. The bundle holds the hub address, the node id, the label, the computer's key seed and its token, and decodes to at most 4096 bytes.

On the member's own home, run `node join`, paste the bundle and press Control-D. The bundle never goes on a command line, and each bundle joins once.

```bash
dockingbird node join
```

```text
This computer joined the fleet as lab (node {node_id}).
Each agent started here from now on gets a fleet inbox.
```

That is `NODE_JOINED`. `node join` writes the member's credential under its home's `fleet` folder, starts the fleet-link container beside its coordinator and enrols the computer through the hub. When the hub is not reached, it tries again for 10 seconds, then undoes the join and stops with `NATIVE_REFUSED`.

## 5. Check that it works

On the control plane's home, list the computers.

```bash
dockingbird cp status
```

```text
  lab  {node_id}  linux  joined  {version}  0 fleet inboxes
```

A joined row means the member enrolled through the hub. Once an agent runs on the member, the row ends with its fleet inboxes and how long ago the control plane last heard from one of them. With `--json`, each row also gives when the computer joined and when it was removed. `No computer has joined the fleet yet.` (`CP_STATUS_EMPTY`) means no bundle was made or every computer was removed.

Then start an agent on the member and read its row in `dockingbird status` there.

```text
fleet: lab-notes-1, heartbeat {age}, asks {n}
```

That agent now has a fleet inbox, and it can message any other fleet agent by its fleet name. [The fleet tools reference](../reference/fleet-tools.md) lists what it gets.

## 6. Add, remove and rejoin members

Add a member with section 4 again, one bundle for each computer. A computer that already joined is refused until it leaves.

`cp remove` takes a member out at once, with no precondition. It disables the computer, revokes its token, closes its agents' fleet inboxes, removes its hub user and starts the hub again. The agents keep running on that computer without the fleet.

```bash
dockingbird cp remove lab
```

```text
lab (node {node_id}) is out of the fleet;
{count} fleet inboxes of its agents closed.
Its own agents keep running there without the fleet.
```

A removed computer, or one that lost its home, joins again with a new bundle. Run the first two commands on the control plane's home and the last two on the member's home. `node leave` is refused while an agent there still holds a fleet inbox, so stop those agents first.

```bash
dockingbird cp remove lab
dockingbird cp token --host lab --platform linux
dockingbird node leave
dockingbird node join
```

## 7. Watch the hub

The hub's own log lines and the relay's go to the cp-relay container's log, so `docker logs dockingbird-cp-relay` shows them. On a control plane's home, `dockingbird fleet scrape` also prints the relay's answered, refused and dropped requests, its requests in flight and its seconds per request, in metric families whose names start with `dockingbird_relay_`. [Metrics](metrics.md) shows how to scrape a home, and a named home takes `dockingbird --home NAME fleet scrape`.

## 8. Back up

Nothing of record lives in the hub, so losing the cp-relay container loses nothing. The next command on the control plane's home runs it again from the files on the state volume. The home's state volume, `dockingbird-state` for the default home, holds two things.

| Where | What it holds |
|---|---|
| the `cp` folder | `cp.seed`, the control plane's private key, `hub.json`, the hub's address and port, and `hub.conf` |
| the home's database | the members, the fleet sessions, the fleet's messages, deliveries, threads, attachments and questions |

Dockingbird documents no restore of this volume, and [backup and restore](backup-and-restore.md) states that a restore of a copied home is not documented until a run proves it. Protect the control plane's state volume, and keep `cp.seed` secret. A member whose home is lost joins again as section 6 shows. Ask through [SUPPORT.md](../../SUPPORT.md) before you rely on a copy of the volume.

## 9. Upgrade

The hub changes only when the image changes, so a new `nats-server` arrives with a release whose image base changed. Update in this order, as the team fleet guide does.

1. On the control plane's home, run `dockingbird update`. A cp-relay that is not the new image at the new fleet version is stopped, removed and run again, so the hub restarts. [Updates](updates.md) covers what `update` does with agents running.
2. On each member, run `dockingbird update`.

Until a member matches the control plane, its fleet messages are refused with `NODE_VERSION_MISMATCH` and its agents work without the fleet. A member that loses the hub finds out within 40 seconds, then reconnects by itself.

## 10. Change the address or turn the control plane off

The hub address is recorded once, so a second `cp init` with another address changes nothing. To move the hub, remove every member with `cp remove`, run `cp off`, then run `cp init` with the new address and make new bundles, because each bundle holds the old address. `cp off` removes the hub's files and the cp-relay container, and it is refused while agents run in the home or while a member remains (`CP_HOSTS_ENABLED`).

```bash
dockingbird cp off
```

```text
This home is a plain home again; the fleet's control plane is off.
```

After the control plane's computer restarts, the first `dockingbird cp status` on its home starts the cp-relay again, and the members reconnect by themselves.

## Limits

| Limit | Value |
|---|---|
| a computer's label | 1 to 8 lowercase letters or digits, starting with a letter |
| a decoded bundle | at most 4096 bytes |
| clients of the hub | 1024 |
| deliveries waiting for one asleep agent | at most 200 |
| a fleet attachment | at most 1,048,576 bytes |
| Docker's restarts of the cp-relay on failure | 5 |

## When it fails

Each id below is on the screen when it happens, and the catalogue has the full text.

- [`MODE_CHANGE_AGENTS_RUNNING`](../troubleshooting.md#mode_change_agents_running) blocks `cp init`, `cp off`, `node join` and `node leave` while agents run in the home. Run `dockingbird stop`.
- [`CP_ALREADY_INITIALIZED`](../troubleshooting.md#cp_already_initialized) means the home is already the control plane. Nothing changed.
- [`FLEET_MODE_NOT_RECORDED`](../troubleshooting.md#fleet_mode_not_recorded) means `config.toml` cannot take its `fleet` line. Make it a plain file of yours, then run the command the message shows.
- [`NATS_SERVER_UNAVAILABLE`](../troubleshooting.md#nats_server_unavailable) means the hub gave no greeting within 10 seconds after a command made the home ready. Everything else on the home works. Run the command again. Docker restarts the cp-relay up to 5 times, and after that the next command on the home starts it. If it keeps failing, report it.
- [`NATIVE_REFUSED`](../troubleshooting.md#native_refused) from `node join`, with the reason `RPC_SERVER_UNAVAILABLE`, means the member did not reach the hub for 10 seconds. The join is undone and the home is as before. Check the serve step and the `nc` check from section 3, then join again with the same bundle if it was not enrolled.
- [`NODE_ALREADY_ENROLLED`](../troubleshooting.md#node_already_enrolled) means the control plane already enrolled a computer with that bundle. Run `cp remove LABEL`, make a new bundle with `cp token`, and join with it.
- [`NODE_ALREADY_JOINED`](../troubleshooting.md#node_already_joined) means this home is in the fleet. Run `node leave`, then join.
- [`NODE_SESSIONS_LIVE`](../troubleshooting.md#node_sessions_live) blocks `node leave` while an agent here holds a fleet inbox. Stop that agent.
- [`RPC_PEER_HOST_MISMATCH`](../troubleshooting.md#rpc_peer_host_mismatch) means the bundle was made for another computer. Leave, then join with a bundle made for this one.
- [`NODE_VERSION_MISMATCH`](../troubleshooting.md#node_version_mismatch) and [`RPC_FRAME_INVALID`](../troubleshooting.md#rpc_frame_invalid) mean the two ends run different code. Run `dockingbird update` on the one that is behind.
- [`NODE_ROUTE_REFUSED`](../troubleshooting.md#node_route_refused) means a joined computer made a call the control plane does not allow. Dockingbird's own commands never do. Run the command again with `--verbose` and report it.
- [`FLEET_SESSION_NOT_OPENED`](../troubleshooting.md#fleet_session_not_opened) means an agent started while the control plane did not answer. The agent works as usual and gets its inbox when the control plane answers.
- [`FLEET_LINK_START_FAILED`](../troubleshooting.md#fleet_link_start_failed) means Docker refused to run the fleet-link on a member. The next command tries again.
- [`NODE_SESSION_ELSEWHERE`](../troubleshooting.md#node_session_elsewhere) means an agent with that fleet name is live on another computer. Stop it there or use another name.
- [`CP_HOSTS_ENABLED`](../troubleshooting.md#cp_hosts_enabled) blocks `cp off` while a computer remains. Run `cp remove` for each.

## Where to go next

- [The control plane](../concepts/control-plane.md), for what the fleet inbox is and what the control plane never does.
- [Install a team fleet](team-fleet.md), to add the scheduler's store and workers.
- [Tailscale](tailscale.md) and [networking](networking.md), for the network the hub's port rides on.
- [Join a computer to a control plane](../../examples/join-a-computer-to-a-control-plane/README.md), a cookbook of the join and the rejoin.
