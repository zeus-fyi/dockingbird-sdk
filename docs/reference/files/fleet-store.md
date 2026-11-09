---
title: The fleet store
summary: The three schemas of the organisation's PostgreSQL 18 store, its role groups, the order of a migration and which migrations need older workers restarted first.
audience: team-admin
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../../llms.txt).

# The fleet store

The fleet store is one PostgreSQL 18 database, `dockingbird_fleet` by default, that `dockingbird org create` fills. [The team fleet guide](../../guides/team-fleet.md) installs it.

## The three schemas

| Schema | Purpose |
|---|---|
| `fleet` | the fleet scheduler: hosts, workloads, leases, swarm rosters and the workers' samples, with row-level security so a project's role sees its own workloads only |
| `org` | the organisation: its projects, the model and effort of each kind of role, its people and which projects each belongs to |
| `work` | the organisation's work queue, read and written by `dockingbird work` ([the work queue guide](../../guides/work-queue.md)) |

## The roles and groups

| Role | Kind | What it is |
|---|---|---|
| `fleet_admin` | login | the admin; makes, grants, revokes and drops the groups itself (it needs `CREATEROLE`); acts for any project; takes no group |
| `fleet_worker_<host>` | login | one machine's worker; a member of `fleet_worker`; its row in `fleet.role_host` names the same host as its `--host` |
| a person's own role | login | one person's commands, their coordinators' and runners'; a member of each project's group they act for |
| `fleet_worker` | group, no login | the workers' rights |
| `fleet_submitter` | group, no login | the submitters' rights |
| `fleet_submitter_<project>` | group, no login | one project; `fleet submit` and `fleet run` take it before they write; `org members add PERSON --project SLUG` makes it when the project has none |

A name with a dash is written in double quotes in SQL. No project has a login of its own. Each login's password is set with psql's `\password`, which sends only the hash, and lives on each computer in a line of `~/.pgpass`, never in a TOML file.

## Rules

| Rule | Statement |
|---|---|
| making the store | `org create` makes the three schemas and the groups in one transaction, where the cluster has none, and says `The org store is ready, at version {version}.` |
| a second run | says `The org store is already at version {version}: nothing changed.` |
| who may run it | a role that is a member of `fleet_admin`; any other ends 77 |
| a store from an earlier build | upgraded once after the update by the owner of the `fleet` schema's tables; `org create` as `fleet_admin` applies each missing migration, each in one transaction, when `fleet_admin` owns them |
| another owner | `SELECT DISTINCT tableowner FROM pg_tables WHERE schemaname = 'fleet'` names the owner; the [operator guide](../../operator-guide.md) section "The fleet scheduler" gives the command to run as that owner |
| a build that lacks a migration | a worker or admitter refuses to start with `FLEET_STORE_BEHIND` and names the migration; a store that names migrations its build does not know is allowed |
| migration order | the admin's `org create` at the new build runs before any worker or admitter restarts at it; then each machine's worker that runs swarms and the admitter restart; only then use `fleet retire`, `add`, `replace` or `prune` |
| the control plane | its home updates after the admin's `org create` and before the members that joined it |
| a worker that cannot start | it publishes no sample, so after 180 seconds its host is stale and its swarms are interrupted until `org create` migrates the store |
| workers first | move the workers, each publishing one sample at the new build, then the admitter and the submitters; a `fleet submit` at the new build refuses a swarm whose hosts' workers have not published their homes' checkouts |

## A store made before the groups were the admin's to grant

Run these as the cluster's superuser, once, for a store whose groups the superuser made.

```sql
ALTER ROLE fleet_admin CREATEROLE;
GRANT fleet_submitter TO fleet_admin WITH ADMIN TRUE, INHERIT FALSE, SET FALSE;
GRANT "fleet_submitter_<project>" TO fleet_admin WITH ADMIN TRUE, INHERIT FALSE, SET FALSE;
```

The last statement is repeated for each project group the store holds.

## Older workers

Each row says whether the workers and the admitter of the release before it keep running against a store that migration changed, or restart at the new build first.

| Migration | Earlier workers | Why |
|---|---|---|
| `0001_roster_operations` | restart first | adds the roster steps `retire_asked`, `retired`, `pickup` and `held`, which an earlier worker reads as an agent gone and interrupts its swarm; restart every worker and the admitter before `fleet retire`, `add`, `replace` or `prune` |
| `0002_done_after_a_loss` | keep running | adds the state grants of three moves a `done` makes after a loss and changes no move an earlier worker or admitter makes |
| `0003_assignments_told` | keep running | adds `reviewer_told` and `tester_told`, which an earlier worker neither reads nor writes |
| `0004_efficiency` | keep running | its tables, kinds and column are new to earlier builds; move the workers to the new build before the admitter and the submitters |
| `0005_host_rank` | keep running | adds the host rank, null for every host enrolled before it |
| `0006_org` | keep running | earlier workers keep working through it; apply it before any worker, admitter or submitter restarts at the new build |
| `0007_membership` | keep running | as `0006_org`; a project's submitter login keeps working |
| `0008_sql_audit` | keep running | the policies admit the same rows and only plans change; a worker of this build against a store without it refuses to start |
| `0009_rolling_updates` | keep running | adds each process's release, schema, kind and homes and each roster row's release and code; newer records wait until every live process is updated |
| `0010_role_config` | keep running | adds each roster row's `config_digest` and the event kind `denied_by_role`; a worker writes them only once every live process is at this migration |
| `0011_work_queue` | keep running | adds the `work` schema, which no worker or admitter reads or writes, and changes nothing in `fleet` or `org` |
| `0012_agent_placement` | restart first | the admitter restarts first: it keys `fleet.reservation` by the workload and the host, so an earlier admitter's reservation insert fails with SQLSTATE `42P10` at its first admission and nothing is admitted until it restarts at the new build; run `org create`, restart the admitter, then move the workers and the submitters, with no `fleet submit` between `org create` and the admitter's restart; earlier workers and submitters keep running, and a swarm spreads across hosts only once every live process is at this migration |
| `0013_host_guard` | keep running | adds `host_sample.host_agents`, the table `host_sample_history` and the function `host_guard_facts`, which no earlier worker or admitter reads, writes or calls |
| `0014_harness_fallback` | keep running | adds `host_sample.logins`, each roster row's `harness`, `fallback_attempts` and `fallback_attempted_at`, the roster cause `fallback` and the event kind `agent_fallback_refused`; an earlier worker or admitter reads none of them, and a new worker writes them only once every live process is at this migration |

A worker or the admitter of the new build against a store without its migration refuses to start with `FLEET_STORE_BEHIND`, so `org create` runs before they restart. `org create` names the version it reached after each run.
