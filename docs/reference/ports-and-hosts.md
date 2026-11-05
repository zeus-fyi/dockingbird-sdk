---
title: Ports and hosts
summary: Every port and route Dockingbird opens or expects, on which interface, with the timeouts of each and the hosts an egress preset reaches.
audience: team-admin
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Ports and hosts

This page lists each port and route Dockingbird opens or expects, the interface it is on, and the hosts an egress mode reaches. [Networking](../guides/networking.md) explains the three routes.

## Ports the control plane and the agents open

| Port or route | Interface | Opened by | Reached by | Guide |
|---|---|---|---|---|
| TCP 4222 (`NATS_PORT`), the fleet hub | published by Docker on the control plane computer's loopback only | `cp init` | member computers, once you serve the port to your private network | [Tailscale](../guides/tailscale.md) |
| TCP 9464 (`METRICS_PORT`), `/metrics` of one agent | inside that agent's container network; no port of the computer reaches it | the agent's container | nothing outside the container; `fleet scrape` prints the same lines | [metrics](../guides/metrics.md) |
| `FLEET_SCHED_METRICS_PORT`, the admitter's `/metrics` | the org pointer's database host | `fleet admitter` | your Prometheus | [metrics](../guides/metrics.md) |
| ssh to a host | the host's ssh port, as your own ssh configuration reaches it | your own ssh | `fleet hosts set --ssh`, `fleet agents`, `fleet attach` | [hosts](../guides/hosts.md) |
| `gcloud compute ssh` to a VM | whatever your gcloud uses; with no external IP it uses IAP TCP tunneling | your own gcloud | `fleet hosts set --gcloud` | [other networks](../guides/other-networks.md) |
| the fleet database, PostgreSQL | the `host` and `port` of `org.toml` | your PostgreSQL | every fleet scheduler command, each host's worker, the admitter | [team fleet](../guides/team-fleet.md) |

## Timeouts and sizes of the routes

| Bound | Value | Applies to |
|---|---|---|
| `FLEET_SSH_CONNECT_TIMEOUT_S` | 15 s | the ssh connect of a host read |
| `FLEET_PROBE_COMMAND_TIMEOUT_S` | 20 s | each read of `fleet agents --host` and `fleet probe` |
| `FLEET_PROBE_TIMEOUT_S` | 60 s | a whole `fleet probe` |
| `FLEET_HOME_READ_TIMEOUT_S` | 30 s | each read of `fleet read-home` and `fleet scrape` |
| `FLEET_DB_CONNECT_TIMEOUT_S` | 5 s | a fleet scheduler command's connection to the fleet database; a failure ends 69 |
| `NATS_REQUEST_TIMEOUT_S` | 30 s | a fleet call's wait for its answer |
| `AGENT_PERIODIC_RPC_TIMEOUT_S` | 10 s | an agent's own fleet inbox read and heartbeat |
| `NATS_PING_INTERVAL_S`, `NATS_PING_MAX` | 40 s in all | a member finds a silent control plane, then reconnects by itself |
| `NATS_MAX_CONNECTIONS` | 1024 | connections to the hub: one per member and one for the control plane |
| `NODE_BUNDLE_MAX_BYTES` | 4096 bytes | a bundle, decoded |
| `ARTIFACT_MAX_BYTES` | 1048576 bytes | a fleet attachment |
| `HOST_LABEL_MAX_CHARS` | 8 | a computer's label in the fleet |

## What an egress mode reaches

| Mode | Reaches |
|---|---|
| `full` | every host, from the agent's own network with NAT out and no proxy; the default |
| `allowlist` | its tool's own hosts (the model API and the sign-in), the hosts of its presets, and the hosts of its config's `allow`, through a proxy container, on every port of an admitted host |
| `models` | its tool's own hosts alone |
| `none` | nothing; no network at all, the model API included |

## Hosts of the presets

| Preset | Hosts |
|---|---|
| `github` | `github.com`, `api.github.com`, `codeload.github.com`, `*.githubusercontent.com` |
| `registries` | the package registries of the ecosystems GitHub's recommended allowlist names: npm and Yarn, PyPI, crates.io, the Go module proxy and checksum database, RubyGems, Maven Central and the Gradle plugin portal, NuGet, Packagist and pub.dev, and Hex |

## Entries of allow

| Entry of `allow` | Reaches |
|---|---|
| `docs.python.org` | that host, on every port |
| `*.corp.example` | every name under that domain |
| `registries` or `github` | the hosts of the preset |
| an internationalized name (an `xn--` label) | refused when the config is read |

## What the proxy answers

| Answer | Meaning |
|---|---|
| `407` | the host is not in the list, or its address is not public, or the request names an upstream proxy of its own |
| `502`, `504`, `500` | the host is in the list, and its name does not resolve or it does not answer |

## Addresses the proxy refuses

| Address | Answer, listed or not |
|---|---|
| the computer, your LAN, `host.docker.internal`, Docker's own ranges, another agent's address | `407` |

## Docker version

| Needs | Value |
|---|---|
| a proxy mode (`models`, `allowlist`) | Docker Engine 28 or later |

## Hosts the computer itself reaches

| Host | For |
|---|---|
| `license.zeus.fyi` over HTTPS | installing and updating Dockingbird from the release index |
| the pinned public base images' registries | the first build of Dockingbird's image, pulled without your login; Dockingbird pushes nothing |

## When it fails

- [`FLEET_HOSTS_NOT_REACHED`](../troubleshooting.md#fleet_hosts_not_reached): a host route did not answer.
- [`NATS_SERVER_UNAVAILABLE`](../troubleshooting.md#nats_server_unavailable): the hub did not answer.
- [`EGRESS_PROXY_FAILED`](../troubleshooting.md#egress_proxy_failed): the proxy of a `models` or `allowlist` start did not come up.
- [`START_NETWORK_POOLS_FULL`](../troubleshooting.md#start_network_pools_full): Docker has no address range left.
