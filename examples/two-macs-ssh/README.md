# Two Macs, over ssh

You work on one Mac, and another Mac, `lab`, runs agents of its own. Once this Mac knows how to reach `lab`, the
fleet commands and the GUI show `lab`'s homes and agents beside this Mac's own, `local`.

## Before you start

- Dockingbird is installed and set up on both Macs ([One Mac, day one](../one-mac/README.md)).
- This Mac's ssh reaches `lab` with no question asked: `ssh lab.example true` returns at once. Dockingbird runs your
  own ssh, with your own configuration and keys, and never copies or forwards a key.
- `lab` has Remote Login on (System Settings, General, Sharing).

Try what Dockingbird will run first:

```bash
ssh lab.example docker version
```

## Add `lab`

```bash
dockingbird fleet hosts set lab --ssh lab.example
```

`set` reaches `lab` and reads its Docker and its Dockingbird homes as `dockingbird fleet agents --host lab` does;
once that read succeeded, it saves the host, then prints what it read and says so:

```text
lab: 2 agents running in 1 home
...
lab: ssh lab.example, saved in ~/.local/share/dockingbird/hosts.toml.
```

When it can't read `lab`, it saves nothing and says what to try. The usual cause on a Mac: a login over ssh has a
shorter `PATH` than a terminal, without the folder of Docker Desktop's `docker`. Give the commands run there a `PATH`
that holds it:

```bash
dockingbird fleet hosts set lab --ssh lab.example --path /Applications/Docker.app/Contents/Resources/bin:/usr/bin:/bin
```

which writes [this file's](hosts.toml) table:

```toml
[[host]]
name = "lab"
ssh = "lab.example"
path = "/Applications/Docker.app/Contents/Resources/bin:/usr/bin:/bin"
```

`path` names Docker Desktop's folder, then the system's. When `lab`'s Docker answers on a socket other than the
default one, `--docker-host URL` sets the `docker_host` key: the `DOCKER_HOST` value the commands run with there,
`unix://` followed by the socket's path. Docker Desktop keeps its socket in the login's own home folder, under
`.docker/run/`, unless its settings allow the default socket; `docker context inspect`, run on `lab`, prints the one
it uses.

## Every day

```bash
dockingbird fleet hosts                # the hosts this Mac reaches
dockingbird fleet agents --host lab    # lab's homes and agents
dockingbird fleet agents               # this Mac's, local
```

`dockingbird fleet attach --host lab --container ID` opens a terminal agent of `lab` here, its full container id
from `dockingbird --json fleet agents --host lab`. `dockingbird fleet hosts rename lab bench` renames it and
`dockingbird fleet hosts forget bench` removes it; [the hosts file's page](../../docs/integration/hosts-file.md) has
every key and rule of the file.
