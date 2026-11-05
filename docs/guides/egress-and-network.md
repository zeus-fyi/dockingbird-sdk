---
title: Egress and what agents can reach
summary: Choose how far an agent reaches on the network, with four egress modes, an allowlist, and what a blocked host sees.
audience: daily
commands:
  - egress
  - claude --egress
  - start --egress
---

# Egress and what agents can reach

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

Egress is how far an agent's network reaches, and Dockingbird's own default is `full`, which has no limit at all. Below you pick a mode for new agents, for one start and for one config. You also see what a blocked host looks like from inside the agent, and what an allowlist still leaves open.

## The four modes

| Mode | What the agent reaches | How |
|---|---|---|
| `allowlist` | its tool's own hosts (the model API and the sign-in), the hosts of its presets, and the hosts of the config's `allow` | through a proxy container of its own, and nothing else |
| `models` | its tool's own hosts alone | through the same proxy |
| `none` | nothing, not even the model's API | no network at all |
| `full` | the whole internet | the agent's own network with NAT out, and no proxy |

Under `full`, a hijacked agent can send out the repo it works on, and its own Docker sign-in or key, to any host. `allowlist` closes that: with the registries and GitHub allowed, installing dependencies and reading GitHub's content still work, while sending something out needs a credential the agent does not hold.

| Preset | Hosts it covers |
|---|---|
| `registries` | the package registries of the ecosystems GitHub's recommended allowlist names: npm and Yarn, PyPI, crates.io, the Go module proxy and checksum database, RubyGems, Maven Central and the Gradle plugin portal, NuGet, Packagist, pub.dev and Hex |
| `github` | `github.com`, `api.github.com`, `codeload.github.com` and `*.githubusercontent.com` |

## Before you start

- Docker Engine 28 or later runs for `allowlist` and `models`. `docker version` prints the Engine's version, and an older one needs a Docker Desktop update first. The mode `full` works on any version.
- About 30 Docker networks fit in Docker's default address pools, shared by every Docker network on the computer. A start with no range left is refused.

Dockingbird checks no Engine version. Engine 27 refuses the agent's network with Docker's own error, shown as `EGRESS_PROXY_FAILED`. Engine 26 or older ignores the isolated-gateway option, so the agent's internal network keeps an address on the Docker host, and the agent can reach what listens there. Update Docker Desktop first.

## Steps

1. See what new agents get. The output also says whether a file named `egress.toml` in Dockingbird's folder sets it, or it is Dockingbird's own default.

   ```bash
   dockingbird egress
   ```

   The step is done when the command prints one of these two forms.

   ```text
   Egress for new agents: full.
   Nothing is set: this is Dockingbird's own default.
   ```

2. Set the default for new agents on this Mac. An allowlist given no entries takes the two presets. One given entries is exactly those entries plus the tool's own hosts, so name both presets again to keep them. An entry is a host like docs.python.org, a wildcard like *.corp.example for every name under it, or a preset.

   ```bash
   dockingbird egress allowlist --allow registries --allow github --allow docs.python.org
   ```

   Agents already running keep what they started with. The step is done when the command prints these lines, with your list in the brackets.

   ```text
   Egress for new agents is now allowlist (<the allow list>).
   Agents already running keep theirs.
   ```

3. Change one start. The flag exists on `claude`, `codex` and `start`. An agent you pick up again keeps the mode of its last start.

   ```bash
   dockingbird claude --egress models
   dockingbird start --egress none "Summarise the README"
   ```

   A config can set the same thing with the keys `egress` and `allow`, and a start flag cannot override them. Configs are covered on [your-own-commands.md](your-own-commands.md).

   ```toml
   command = "review"
   egress = "allowlist"
   allow = ["registries", "github", "docs.python.org"]
   ```

4. Remove the setting, so new agents get Dockingbird's own default again.

   ```bash
   dockingbird egress --reset
   ```

   The step is done when the command prints these lines.

   ```text
   Egress for new agents is Dockingbird's own default: full.
   Agents already running keep theirs.
   ```

## What a blocked host sees

A host outside the list gets the proxy's `407` and a message that names Dockingbird and the way out, so a tool fails with its own proxy-refused error and not a timeout.

```text
Dockingbird's egress proxy refuses with 407 a host that is not in the allow list or whose address is not public, and a request that names an upstream proxy of its own: allow a public host with allow in the config, or start with --egress full. A host in the list whose name does not resolve, or that does not answer, gets 502, 504 or 500 instead.
```

An allowed host whose name does not resolve gets the proxy's `502`, as the lookup would fail anywhere. TLS is never opened. The proxy tunnels the connection, sees the host name and the port and nothing inside, and the tool's own certificate check runs against the real server.

In `allowlist` and `models`, a tool that ignores the proxy fails and does not get around it. The agent's network has no route out, no gateway and no IPv6. Its only resolver, Docker's, answers the names of containers on that network and no outside name. A connection to an IP address, to an IPv6 literal, or any other traffic such as UDP, QUIC or ping, has no route or is refused at the proxy.

## What the list does not limit

- An entry names a host, not a port. An admitted host is open on every port, and a host you allow is a host the agent can post to. Allow only hosts you would let it send the repo to.
- A `*.` entry admits every name under the domain, and the proxy's lookup of the name the agent picks reaches that domain's own nameservers.
- An internationalized name, with an `xn--` label, is not admitted yet. An `allow` entry holding one is refused when the config is read.
- The proxy refuses every address that is not public, whether or not the name is allowed. A connection to your Mac, your LAN, `host.docker.internal`, Docker's own ranges or another agent's address gets the same `407`. A name in the list that resolves to one of them is refused too. `--egress full` is the way to reach them.
- Under `full` there is no proxy, so an agent's own browser reaches this Mac's loopback services through `host.docker.internal`. A browser agent that must not reach them uses `allowlist` or `models`.
- Behind a proxy that every connection must use, only `--egress full` works.
- A project config in a checkout you marked untrusted can only narrow egress, with `none`, `models` or a list the default already covers. Anything wider is refused, and the step is `dockingbird trust`.

Your claude.ai connectors never load in an agent. The image's managed settings turn them off in every mode, `--egress full` included, and a repo's or an agent's own settings cannot turn them back on. An agent gets a document by `send --file` or an artifact, never through your accounts.

The agents' own networks are separate. Each agent gets a network named `dockingbird-net-<name>` that no other agent joins. Under `allowlist` and `models` its proxy, `dockingbird-proxy-<name>`, sits on that network and on the shared `dockingbird-out` bridge. Under `none` there is no network.

## When it fails

- A start that prints [`EGRESS_PROXY_FAILED`](../troubleshooting.md#egress_proxy_failed) found the proxy of a `models` or `allowlist` agent dead or silent. The start removed everything it made. Run it again.
- Docker has no address range left when you see [`START_NETWORK_POOLS_FULL`](../troubleshooting.md#start_network_pools_full). List the networks with `docker network ls`, free them with `docker network prune`, or add pools through Docker's `default-address-pools` setting.
- [`EGRESS_FILE_INVALID`](../troubleshooting.md#egress_file_invalid) blocks every new agent while `egress.toml` is unreadable. Repair the file, or delete it with `dockingbird egress --reset`.
- An `--allow` entry that is no host, wildcard name or preset draws [`EGRESS_ENTRY_INVALID`](../troubleshooting.md#egress_entry_invalid).
- An untrusted checkout whose config asks for more than the default allows stops with [`START_EGRESS_UNTRUSTED`](../troubleshooting.md#start_egress_untrusted). Narrow the entry, or run `dockingbird trust`.
- [`START_CONFIG_FIXED`](../troubleshooting.md#start_config_fixed) says the `--egress` you typed disagrees with the `egress` in the config file. Drop the flag or edit the file.
- [`BROWSER_STORE_NO_EGRESS`](../troubleshooting.md#browser_store_no_egress) refuses egress `none` for a config that installs Web Store extensions, since Chrome downloads them from Google.
