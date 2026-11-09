---
title: A Mac and a cloud VM over gcloud
summary: Add a Compute Engine VM as a host through gcloud and read its agents.
audience: daily
commands:
  - fleet hosts set --gcloud
  - fleet agents --host
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# A Mac and a cloud VM, over gcloud

Your Mac reaches a Compute Engine VM, `cloud-1` in the zone `europe-west1-b` of the project `example-project`, that runs Dockingbird on arm64 Linux with Docker Engine. Under the name `cloud`, the fleet commands show its homes and agents beside your Mac's own, `local`. The [GUI](../../docs/guides/gui.md) lists the hosts in its sidebar and adds, renames or forgets one. [Cloud VMs](../../docs/guides/cloud-vms.md) is the guide behind this example.

## Before you start

- Dockingbird is installed and set up on the VM, as on a Mac ([One Mac, day one](../one-mac/README.md)).
- The Google Cloud SDK is on your Mac and signed in: `gcloud compute ssh` reaches the VM. Dockingbird runs your own `gcloud` (from your `PATH`, else the SDK's usual places), with your own configuration, and never copies a key.
- The VM is running. A stopped VM can't be read, so start it first.

```bash
gcloud compute instances start cloud-1 --zone europe-west1-b --project example-project
```

Try what Dockingbird will run first.

```bash
gcloud compute ssh cloud-1 --zone europe-west1-b --project example-project -- docker version
```

Done: Docker's client and server versions.

## Add `cloud`

```bash
dockingbird fleet hosts set cloud --gcloud cloud-1 --zone europe-west1-b --project example-project
```

`set` reaches the VM and reads its Docker and its Dockingbird homes as `dockingbird fleet agents --host cloud` does. Once that read succeeded, it saves the host, then prints what it read and says so. The last line is the done line (`FLEET_HOSTS_SET`).

```text
cloud: 4 agents running in 2 homes
...
cloud: gcloud cloud-1, saved in ~/.local/share/dockingbird/hosts.toml.
```

The command writes [this file's](hosts.toml) table.

```toml
[[host]]
name = "cloud"
gcloud = "cloud-1"
zone = "europe-west1-b"
project = "example-project"
```

When it can't read the VM, it saves nothing and says what to try first. When your `gcloud` is neither on your `PATH` nor in the SDK's usual places, write its absolute path into the table by hand as `gcloud_program`. A later `set` of `cloud` over gcloud keeps it.

Any other cloud's VM, or a VM you reach by its address, is a host over ssh instead: `dockingbird fleet hosts set cloud --ssh cloud.example` ([Two Macs, over ssh](../two-macs-ssh/README.md)).

## Every day

```bash
dockingbird fleet agents --host cloud    # the VM's homes and agents
```

The command prints this first line, then a row for each home and each agent (`FLEET_HOST_ROW`).

```text
cloud: 4 agents running in 2 homes
```

A VM that is stopped reads as `Couldn't read cloud: ...` until it runs again. If the VM also belongs to your team's fleet pool, it keeps the name `cloud` there too ([a team fleet](../team-fleet/README.md)). The pool's admitter starts a stopped VM when work waits for it, but only when the admitter's own hosts file names `cloud` with this gcloud route.

## When it fails

| Message id | What happened |
|---|---|
| [`FLEET_HOSTS_NOT_REACHED`](../../docs/troubleshooting.md#fleet_hosts_not_reached) | `set` could not read the VM and saved nothing; the message gives `gcloud compute ssh cloud-1 -- docker version` to try, says a stopped VM must be started first, and says when this Mac has no `gcloud` |
| [`FLEET_HOST_NOT_READ`](../../docs/troubleshooting.md#fleet_host_not_read) | `fleet agents --host cloud` could not read the VM; a stopped VM reads this way |
| [`FLEET_HOSTS_ROUTE_NEEDED`](../../docs/troubleshooting.md#fleet_hosts_route_needed) | `--gcloud VM` needs `--zone` and `--project`; exit 2 |
| [`FLEET_HOSTS_FILE_INVALID`](../../docs/troubleshooting.md#fleet_hosts_file_invalid) | a value in `hosts.toml` breaks a rule |
| [`FLEET_HOSTS_IN_USE`](../../docs/troubleshooting.md#fleet_hosts_in_use) | the VM is in a fleet pool; drain and remove it there before `rename` or `forget` |
