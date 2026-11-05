---
title: Restrict what agents can reach
summary: Limit new agents to their tool's hosts, the package registries and two hosts of your own, and see what a blocked request looks like.
audience: daily
commands:
  - egress
  - egress allowlist --allow
  - claude --egress
  - egress --reset
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Restrict what agents can reach

By default an agent can reach any host on the internet. This cookbook sets the default for new agents to an allowlist: the tool's own hosts, the package registries and two hosts of your own, `docs.python.org` and `packages.lab.example`. It then shows what the agent sees when it asks for any other host. Each step ends with the line the product prints when the step worked.

## Before you start

- Dockingbird is set up. `dockingbird --version` prints a version.
- Docker Engine is version 28 or later. Docker Desktop updated to a current release has it. A proxy mode on an older Engine fails at the agent's start (`EGRESS_PROXY_FAILED`), or on Engine 26 and older leaves the agent's network with an address on the Docker host. `full` works on any.
- You know the hosts the agent needs. This cookbook uses `docs.python.org` and `packages.lab.example`.

## 1. See what new agents get now

```bash
dockingbird egress
```

The step is done when the product prints the mode.

```text
Egress for new agents: full.
Nothing is set: this is Dockingbird's own default.
```

Message id `EGRESS_SHOWN`. `full` means no limit: a hijacked agent can send the repo it works on and its own sign-in to any host.

## 2. Set the allowlist

```bash
dockingbird egress allowlist --allow registries --allow docs.python.org --allow packages.lab.example
```

`registries` is a preset: the package registries of npm and Yarn, PyPI, crates.io, the Go module proxy, RubyGems, Maven Central, NuGet, Packagist, pub.dev and Hex. The other preset is `github`. The entries you name are the whole list, besides the tool's own hosts, so add `--allow github` if you want it too. A `*.lab.example` entry admits every name under that domain. The step is done when the product prints this line.

```text
Egress for new agents is now allowlist (registries, docs.python.org, packages.lab.example).
Agents already running keep theirs.
```

Message id `EGRESS_SET`. Agents already running keep what they started with.

## 3. Start an agent

```bash
dockingbird claude
```

The agent gets the default you set in step 2, through a proxy container of its own. To try one start with another mode, `dockingbird claude --egress models` reaches the tool's hosts alone, and `--egress none` has no network at all, the model API included. `dockingbird status` shows the mode when it differs from the default for new agents. The step is done when the agent starts as it usually does.

```text
To leave it working, close this window.
```

## 4. See a blocked request

Ask the agent to fetch `https://blocked.lab.example`, which is not on the list, with a tool of its choice. The proxy answers 407 and a message that names Dockingbird. The tool then fails with its own proxy-refused error, quickly, and not with a timeout.

```text
Dockingbird's egress proxy refuses with 407 a host that is not in the allow list or whose address is not public, and a request that names an upstream proxy of its own: allow a public host with allow in the config, or start with --egress full.
```

The step is done when that message appears in the agent. Three details help when you read it. A listed host whose name does not resolve gets a 502, as the lookup would fail anywhere. A listed host is open on every port, and the agent can post to it, so list only hosts you would let it send the repo to. A name that resolves to a private address is refused even when listed, so `host.docker.internal`, your network and other agents stay out of reach. The proxy sees the host name and the port, never what is inside the TLS connection.

## 5. Go back to the default

```bash
dockingbird egress --reset
```

The step is done when the product prints this line.

```text
Egress for new agents is Dockingbird's own default: full.
Agents already running keep theirs.
```

Message id `EGRESS_RESET`. See [egress and network](../../docs/guides/egress-and-network.md) for a config's `egress` and `allow` keys and for a proxy.

## When it fails

- An `--allow` entry such as `https://docs.python.org` is a URL and no host name, so [`EGRESS_ENTRY_INVALID`](../../docs/troubleshooting.md#egress_entry_invalid) names it by its position among your `--allow` options. Write `docs.python.org`.
- A hand edit of `egress.toml` that breaks its grammar gives [`EGRESS_FILE_INVALID`](../../docs/troubleshooting.md#egress_file_invalid), and no new agent starts. `dockingbird egress --reset` removes the file.
- A proxy that does not answer in time gives [`EGRESS_PROXY_FAILED`](../../docs/troubleshooting.md#egress_proxy_failed), with the proxy's last lines. Nothing was started, so run the command again.
- About 30 networks fit in Docker's default address pools. When they are used up, a start prints [`START_NETWORK_POOLS_FULL`](../../docs/troubleshooting.md#start_network_pools_full) with `docker network ls` and `docker network prune`.
