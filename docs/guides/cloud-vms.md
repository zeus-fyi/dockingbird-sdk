---
title: Cloud VMs
summary: Prepare a Linux VM as a host, add it through gcloud or ssh, let the pool's admitter start it when stopped, size its disk, and join it to a fleet.
audience: team-admin
commands:
  - fleet hosts set --gcloud
  - fleet hosts add --power gcloud
  - fleet agents
  - fleet probe
  - cp token
  - node join
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Cloud VMs

This page makes a Linux VM a Dockingbird host. It lists what the VM needs, adds it, reads its agents, starts it from the fleet pool when it is stopped, sizes its disk and, if you want, joins it to a control plane. The examples use a Compute Engine VM, `cloud-1`, in the zone `europe-west1-b` of the project `example-project`. A VM of another cloud is a host over ssh ([hosts](hosts.md)).

## Before you start

Run these checks on the VM.

| Needs | Check |
|---|---|
| arm64 Linux, the only Linux platform; x86 Linux is not supported | `uname -m` prints `aarch64` |
| Docker Engine, version 28 or later if agents use the `allowlist` or `models` egress modes | `docker version` prints a client and a server |
| Docker's buildx plugin, from the `docker-buildx-plugin` package | `docker buildx version` prints a version |
| uv | `uv --version` prints a version |
| git at `/usr/bin/git` | `/usr/bin/git --version` prints a version |
| Dockingbird, installed and set up ([install](../getting-started/install.md)) | `dockingbird --version` prints a version |

A VM is one of the up to three computers of a seat. A VM re-imaged or recreated on each deploy counts as a new computer each time, so avoid re-imaging it ([licensing](licensing.md)). The first start on a computer builds Dockingbird's image, which takes about 5 minutes once.

On your own computer, the Google Cloud SDK is signed in. `gcloud compute ssh cloud-1 --zone europe-west1-b --project example-project -- docker version` must print Docker's versions.

## Start the VM

A stopped VM cannot be read.

```bash
gcloud compute instances start cloud-1 --zone europe-west1-b --project example-project
```

## Add the VM

```bash
dockingbird fleet hosts set cloud --gcloud cloud-1 --zone europe-west1-b --project example-project
```

The command reaches the VM through your own `gcloud compute ssh`, reads its Docker and its homes, saves the host only after that succeeds, and prints the rows it read.

```text
cloud: 4 agents running in 2 homes
...
cloud: gcloud cloud-1, saved in ~/.local/share/dockingbird/hosts.toml.
```

The last line is `FLEET_HOSTS_SET`. The gcloud route writes `name`, `gcloud`, `zone` and `project` into the host's table. When your `gcloud` is neither on your `PATH` nor where the SDK installs it, add its absolute path by hand as `gcloud_program`. A later `set` of the same host over gcloud keeps it.

## Fix a login that does not find docker

The gcloud route has no `path` key. When `gcloud compute ssh cloud-1 --zone europe-west1-b --project example-project -- docker version` fails with `docker` not found, find where it is on the VM.

```bash
gcloud compute ssh cloud-1 --zone europe-west1-b --project example-project -- 'command -v docker'
```

Either make the VM's login find it, so that the first command succeeds, or reach the VM over ssh and give the commands there a `PATH`.

```bash
dockingbird fleet hosts set cloud --ssh cloud.example --path /usr/local/bin:/usr/bin:/bin
```

`--path` holds the folders that contain `docker`. `--docker-host URL` sets `DOCKER_HOST` for a Docker whose socket is not the default one. Moving a host from `--gcloud` to `--ssh` drops its gcloud keys, `gcloud_program` included.

## Read the VM's agents

```bash
dockingbird fleet agents --host cloud
```

```text
cloud: 4 agents running in 2 homes
```

That is `FLEET_HOST_ROW`, followed by a row for each home and agent. A stopped VM reads as `Couldn't read cloud: ...` (`FLEET_HOST_NOT_READ`) until it runs again.

`dockingbird fleet probe` reads a Mac only, so it cannot read the VM's load. On Linux it ends 1 with `FLEET_PROBE_NOT_MACOS`. In a fleet pool, the VM's worker publishes its host sample every 30 seconds.

## Let the pool start a stopped VM

A team that runs the fleet scheduler can leave the VM stopped between jobs. The admin enrols it in the pool with `--power gcloud`. This line is the one the team fleet example uses; its gate lines depend on your VM, and [fleet scheduler](fleet-scheduler.md) explains each flag.

```bash
dockingbird fleet hosts add cloud --os linux --cores 60 --memory 230g --line idle_millicores=4000,8000 --line free_mib=16384,32768 --line psi_io_full=1500,1200 --power gcloud
```

With `--power gcloud`, the pool's admitter starts the stopped VM when work waits for it. The admitter finds the VM by the pool's name in its own `hosts.toml`, so the admitter's home must hold a `[[host]]` named `cloud` with the gcloud route above. The admitter runs on one machine of the pool that stays awake, and not on the VM. A host has one name across your file, the pool and swarm definitions.

## Size the disk

The sources give no single size, so measure it. Each agent's copy holds its repo's history, and Dockingbird keeps five Docker volumes, a toolchain store and Docker's build cache.

```bash
docker system df
dockingbird clean
```

`docker system df` shows what Docker's data uses, and `dockingbird clean` frees disk and prints the sizes it freed. A start offers to run `clean` when Docker is almost out of space. Read both after the first start and again after a week of real use, then size the boot disk with room to spare. [Clean and uninstall](clean-and-uninstall.md) has the rest.

## Join the VM to a control plane

A VM may join a control plane like any other computer ([Tailscale](tailscale.md) shows the commands), on these conditions.

- Its credential acts for its own home only. It opens fleet sessions under its own label and reads the replies to its own inbox.
- The credential lives only in `<home>/fleet/container/` and in the fleet-link's read-only bind. It is never in an agent's container, a log or a command line.
- `dockingbird cp remove LABEL` on the control plane cuts the VM off at once, with no precondition, and `dockingbird node leave` on the VM removes the credential.
- Its fleet sessions expire with their hours.

A compromised member can send instructions to any agent of the fleet, including agents whose grants reach repositories, and can read what is addressed to its own agents, attachments included. It cannot read another computer's inboxes, the harness's sign-in or either database.

## When it fails

- [`FLEET_HOSTS_NOT_REACHED`](../troubleshooting.md#fleet_hosts_not_reached): `set` could not read the VM and saved nothing. The message gives `gcloud compute ssh cloud-1 -- docker version` to try, and says a stopped VM must be started first. It also says when this computer has no `gcloud`.
- [`FLEET_HOST_NOT_READ`](../troubleshooting.md#fleet_host_not_read): `fleet agents` could not read the VM.
- [`FLEET_HOSTS_ROUTE_NEEDED`](../troubleshooting.md#fleet_hosts_route_needed): `--gcloud VM` needs `--zone` and `--project`. Exit 2.
- [`FLEET_HOSTS_IN_USE`](../troubleshooting.md#fleet_hosts_in_use): the pool holds the VM; drain and remove it there before renaming it here.
- [`DOCKER_NOT_INSTALLED`](../troubleshooting.md#docker_not_installed): there is no `docker` command on the VM.
- [`DOCKER_BUILDX_MISSING`](../troubleshooting.md#docker_buildx_missing): install the `docker-buildx-plugin` package.
- [`FLEET_PROBE_NOT_MACOS`](../troubleshooting.md#fleet_probe_not_macos): the probe reads macOS only.
- [`NODE_SESSIONS_LIVE`](../troubleshooting.md#node_sessions_live): `node leave` needs the agents that use the fleet stopped.

The worked example is [a Mac and a cloud VM over gcloud](../../examples/cloud-vm-gcloud/README.md). [Other networks](other-networks.md) covers a VM with no public IP.
