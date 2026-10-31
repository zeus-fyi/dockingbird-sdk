# A team fleet: a pool of two hosts

A team shares a fleet pool: a PostgreSQL database that the fleet scheduler queues swarms in, and the hosts it places
them on. Here the pool holds two hosts, `lab`, a Mac, and `cloud`, a Compute Engine VM, and each member submits
[a swarm definition](swarm.toml) that the scheduler admits where it fits. The operator guide's "The fleet scheduler"
(`docs/operator-guide.md`) gives the database's install, its roles and every command.

## One name

A host has one name: the `name` of its `[[host]]` table in a member's `hosts.toml`, which is also its name in the
pool, the name its worker runs under (`dockingbird fleet worker --host lab`) and the name a swarm definition places
work on. Set each host in your `hosts.toml` under its pool name ([Two Macs, over ssh](../two-macs-ssh/README.md),
[a cloud VM](../cloud-vm-gcloud/README.md)):

```bash
dockingbird fleet hosts set lab --ssh lab.example
dockingbird fleet hosts set cloud --gcloud cloud-1 --zone europe-west1-b --project example-project
```

`fleet hosts rename` and `fleet hosts forget` of a host the pool holds are refused while it is there: drain and remove
it from the pool first, then rename it in your file, then enrol it again under its new name. A rename never changes a
swarm definition, which names pool hosts.

## `fleet.toml`

Every fleet scheduler command reads `fleet.toml` in your Dockingbird home (`~/.local/share/dockingbird/fleet.toml`),
which must be readable by you alone (`chmod 600`):

```toml
# Where the fleet database answers: an address every host of the pool reaches.
host = "fleet-db.example"
# The role you connect as: fleet_submitter_<project> for a member who submits
# swarms, fleet_worker_<host> for a host's worker, fleet_admin for the admin.
role = "fleet_submitter_example"
# Optional: the database's port and name, where they differ from the defaults.
port = 5432
database = "dockingbird_fleet"
```

and `password`, your role's password, which the admin gives you and you write in yourself; it never goes in a
repository. An admin's file adds `project`, the project the admin's own leases count against.

## The pool

The admin enrols each host once, with its reservable share and the gate lines its OS requires (the operator guide
names them), for example:

```bash
dockingbird fleet hosts add cloud --os linux --cores 60 --memory 230g --line idle_millicores=4000,8000 --line free_mib=16384,32768 --line psi_io_full=1500,1200 --power gcloud
```

`--power gcloud` lets the pool's admitter start the stopped VM when work waits on it. Each host then runs its worker,
`dockingbird fleet worker --host cloud`, and one machine of the pool that stays awake runs the admitter,
`dockingbird fleet admitter`, each under the machine's own service manager.

## A swarm

[swarm.toml](swarm.toml) places a reviewer, a tester and two builders on `lab` first, else `cloud`, in each host's home
`/opt/dockingbird/homes/team-1`, on the branch `feature/example` of `example-org/example-app`. A home of the placement
must already link a checkout of that repository on that branch, in a folder named `example-app` (the operator guide's
"The fleet scheduler" says how a home links one): `fleet submit` refuses a definition whose source no home of its
placement has checked out. Write a brief for each role beside it (`briefs/reviewer.md`, `briefs/tester.md` and
`briefs/builder.md`), then:

```bash
dockingbird fleet submit swarm.toml
dockingbird fleet queue
```

`fleet submit` checks the definition against the pool and queues it (`<id> pending, position <n>`); `fleet queue`
shows each host and each workload, and `dockingbird fleet why ID` what holds one that waits.
