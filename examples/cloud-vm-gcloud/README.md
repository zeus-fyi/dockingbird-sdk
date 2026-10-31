# A Mac and a cloud VM, over gcloud

Your Mac reaches a Compute Engine VM, `cloud-1` in the zone `europe-west1-b` of the project `example-project`, that
runs Dockingbird on arm64 Linux with Docker Engine. Under the name `cloud`, the fleet commands and the GUI show its
homes and agents beside your Mac's own, `local`.

## Before you start

- Dockingbird is installed and set up on the VM, as on a Mac ([One Mac, day one](../one-mac/README.md)).
- The Google Cloud SDK is on your Mac and signed in: `gcloud compute ssh` reaches the VM. Dockingbird runs your own
  `gcloud` (from your `PATH`, else the SDK's usual places), with your own configuration, and never copies a key.
- The VM is running. A stopped VM can't be read; start it first:
  `gcloud compute instances start cloud-1 --zone europe-west1-b --project example-project`.

Try what Dockingbird will run first:

```bash
gcloud compute ssh cloud-1 --zone europe-west1-b --project example-project -- docker version
```

## Add `cloud`

```bash
dockingbird fleet hosts set cloud --gcloud cloud-1 --zone europe-west1-b --project example-project
```

`set` reaches the VM and reads its Docker and its Dockingbird homes as `dockingbird fleet agents --host cloud`
does; once that read succeeded, it saves the host, then prints what it read and says so:

```text
cloud: 4 agents running in 2 homes
...
cloud: gcloud cloud-1, saved in ~/.local/share/dockingbird/hosts.toml.
```

which writes [this file's](hosts.toml) table:

```toml
[[host]]
name = "cloud"
gcloud = "cloud-1"
zone = "europe-west1-b"
project = "example-project"
```

When it can't read the VM, it saves nothing and says what to try first. When your `gcloud` is neither on your `PATH`
nor in the SDK's usual places, write its absolute path into the table by hand as `gcloud_program`; a later `set` of
`cloud` over gcloud keeps it.

Any other cloud's VM, or a VM you reach by its address, is a host over ssh instead:
`dockingbird fleet hosts set cloud --ssh cloud.example` ([Two Macs, over ssh](../two-macs-ssh/README.md)).

## Every day

```bash
dockingbird fleet agents --host cloud    # the VM's homes and agents
```

A stopped VM reads as `Couldn't read cloud: ...` until it runs again. When the VM is also a host of your team's fleet
pool, it has the same name there, `cloud` ([a team fleet](../team-fleet/README.md)): the pool's admitter, whose own
`hosts.toml` names `cloud` with this gcloud route, starts the VM when work waits on it.
