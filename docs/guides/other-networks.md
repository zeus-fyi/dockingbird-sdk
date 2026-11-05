---
title: Other networks
summary: Reach hosts over a bastion with ProxyJump, a WireGuard mesh or a gcloud VM with no public IP, and write each into hosts.toml.
audience: team-admin
commands:
  - fleet hosts set --ssh
  - fleet hosts set --gcloud --zone --project
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Other networks

Not every team runs a tailnet. Some reach their hosts through a bastion, over WireGuard, or in a cloud network with no public addresses. This page shows all three. Each one has the setup you do outside Dockingbird, the `fleet hosts set` line, and the table that line writes. Dockingbird runs your own ssh or gcloud, so any route those two can take works.

## Before you start

- The host runs Docker, and Dockingbird is set up on it ([hosts](hosts.md)).
- Your ssh reaches the host without a question, so every key is loaded in your ssh agent. A passphrase prompt is a question. Check with `ssh lab true`, which must return at once.
- For gcloud, the Google Cloud SDK is on this computer and signed in. Check with `gcloud compute ssh cloud-1 --zone europe-west1-b --project example-project -- true`.
- [Networking](networking.md) names the three routes and what each needs.

## A bastion with ProxyJump

A bastion is one host that your network lets you reach, and that reaches the others. `ProxyJump` in `~/.ssh/config` tells ssh to connect through it. OpenSSH describes the value as one or more jump proxies in the form `[user@]host[:port]`, separated by commas and visited in order. This entry reaches `lab-1.internal.example` through the bastion.

```text
Host bastion
  HostName bastion.lab.example
  User ops

Host lab
  HostName lab-1.internal.example
  ProxyJump bastion
```

First make ssh itself work, since Dockingbird runs exactly this.

```bash
ssh lab docker version
```

It prints Docker's client and server versions. Then give the entry's name to Dockingbird as the destination.

```bash
dockingbird fleet hosts set lab --ssh lab
```

```text
lab: ssh lab, saved in ~/.local/share/dockingbird/hosts.toml.
```

That line is `FLEET_HOSTS_SET`, and the table it writes follows.

```toml
[[host]]
name = "lab"
ssh = "lab"
```

When your terminal on the host finds `docker` and the ssh login does not, add `--path`; [hosts](hosts.md) shows the fix. The cookbook [a host behind a bastion](../../examples/host-behind-a-bastion/README.md) runs this in order.

## A WireGuard mesh

A WireGuard mesh gives each computer an address on its own interface. WireGuard's quick start adds that address with `ip address add dev wg0 ADDRESS/MASK`, makes keys with `wg genkey` and `wg pubkey`, and brings an interface up with `wg-quick`. The mesh is set up outside Dockingbird. Once the computers reach each other on it, ssh works over it like over any network.

Name the peer in `~/.ssh/config` with its WireGuard address, or use a name your DNS resolves to it.

```text
Host lab
  HostName <wireguard address of lab>
```

```bash
ssh lab docker version
dockingbird fleet hosts set lab --ssh lab
```

The done line and the table are the same as for the bastion. The host route is all this release's guide documents for a mesh. The hub route (a member joining a control plane) is documented for a tailnet only: `cp init --hub-address` is described there with a tailnet address, and the hub's port is on loopback until a forwarder you provide serves it. The guide does not say that a WireGuard address works as the hub address. Ask through [SUPPORT.md](../../SUPPORT.md) before you join computers over a mesh.

## A Compute Engine VM with no public IP

Google's documentation says that if the instance does not have an external IP address, `gcloud compute ssh` automatically uses IAP TCP tunneling. Dockingbird runs that same command, so the VM needs these on the Google side.

- A firewall rule that allows ingress from the IAP range `35.235.240.0/20` to port 22.
- The role `roles/iap.tunnelResourceAccessor` for the account that runs `gcloud`.

```bash
gcloud compute ssh cloud-1 --zone europe-west1-b --project example-project -- docker version
dockingbird fleet hosts set cloud --gcloud cloud-1 --zone europe-west1-b --project example-project
```

```text
cloud: gcloud cloud-1, saved in ~/.local/share/dockingbird/hosts.toml.
```

```toml
[[host]]
name = "cloud"
gcloud = "cloud-1"
zone = "europe-west1-b"
project = "example-project"
```

The VM must be running. A stopped VM cannot be read, and the refusal says so. When your `gcloud` is neither on your `PATH` nor in the SDK's usual places, write its absolute path into the table as `gcloud_program`. [Cloud VMs](cloud-vms.md) covers the VM itself.

## What each route writes

| Network | `fleet hosts set` | Keys in `hosts.toml` |
|---|---|---|
| bastion with `ProxyJump` | `--ssh lab` | `name`, `ssh` |
| WireGuard mesh | `--ssh lab` | `name`, `ssh` |
| VM with no public IP | `--gcloud cloud-1 --zone europe-west1-b --project example-project` | `name`, `gcloud`, `zone`, `project` |
| a host that needs a `PATH` | add `--path PATH` | `path` |
| Docker on a non-default socket | add `--docker-host URL` | `docker_host` |

An `ssh` value is not empty, has no leading dash and no whitespace. The `gcloud`, `zone` and `project` values are lowercase letters, digits, dashes, dots and colons. [The hosts file](../reference/files/hosts-file.md) has every rule.

## When it fails

- [`FLEET_HOSTS_NOT_REACHED`](../troubleshooting.md#fleet_hosts_not_reached) means the read through the route failed and nothing was saved. The message prints the command to try yourself, and it says when this computer has no gcloud.
- [`FLEET_HOST_NOT_READ`](../troubleshooting.md#fleet_host_not_read) means the agents listing could not read a host you saved earlier.
- [`FLEET_HOSTS_ROUTE_NEEDED`](../troubleshooting.md#fleet_hosts_route_needed) means `set` needs `--ssh DEST`, or `--gcloud VM` with `--zone` and `--project`. It exits 2.
- [`FLEET_HOSTS_FILE_INVALID`](../troubleshooting.md#fleet_hosts_file_invalid) means a value in `hosts.toml` breaks a rule. The message names its place and never the value.
- [`FLEET_HOSTS_NAME_INVALID`](../troubleshooting.md#fleet_hosts_name_invalid) means the host's name holds a character a name cannot have. It exits 2.

## Sources

| Topic | Page |
|---|---|
| `ProxyJump` | https://man.openbsd.org/ssh_config |
| WireGuard | https://www.wireguard.com/quickstart/ |
| IAP TCP forwarding for `gcloud compute ssh` | https://docs.cloud.google.com/iap/docs/using-tcp-forwarding |
