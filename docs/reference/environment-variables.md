---
title: Environment variables
summary: The DOCKINGBIRD_ variables you may set, how Dockingbird treats a setting, and the variables of other tools it reads.
audience: daily
commands:
  - dockingbird homes
  - dockingbird stop
  - dockingbird status
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Environment variables

Settings reach Dockingbird through the shell that runs it, and each one is spelled `DOCKINGBIRD_` followed by its name.
Dockingbird hands every exported setting to the containers that read it, which is why a setting never sits at its default without you knowing.
Only one variable names a folder, `DOCKINGBIRD_HOME`. The database statement timeout, the MCP response size and the message settings below are documented by name.

## Variables you may set

| Variable | Values | Default | What it does |
|---|---|---|---|
| `DOCKINGBIRD_HOME` | an absolute path | `~/.local/share/dockingbird` | the folder of one Dockingbird installation, its home; another path gives a second, fully separate installation with its own containers, volumes and image tag |
| `DOCKINGBIRD_DB_QUERY_TIMEOUT_S` | a whole number within its bounds | its built-in value | how long one database statement may run, for the check of `connect --database` and for the agents' queries; `export DOCKINGBIRD_DB_QUERY_TIMEOUT_S=60` raises it |
| `DOCKINGBIRD_MCP_MAX_CHARS` | a whole number from 1350 to 8000 | 8000 | the most Unicode characters one response of Dockingbird's MCP tools holds, which bounds the context a tool response costs the agent; a value outside 1350 to 8000 stops the command before it runs, since 0.15.11 raised the minimum from 1200, and a home that set a value from 1200 to 1349 must raise it to 1350 or unset it |
| `DOCKINGBIRD_<NAME>` | a whole number within its bounds | its built-in value | any other runtime setting of Dockingbird: a poll interval, a timeout or a page size; the name is upper case and spelled exactly |

## Message settings

These runtime settings follow the rules of [how a setting behaves](#how-a-setting-behaves). Set one in the shell that runs `dockingbird`, then run `dockingbird stop` and the next command, as [the persistence page](../concepts/message-persistence.md#change-the-retention) shows. [limits.md](limits.md#messages-and-retention) lists the same bounds beside the others.

| Variable | Values | Default | What it does | Explained in |
|---|---|---|---|---|
| `DOCKINGBIRD_MESSAGE_BODY_RETENTION_DAYS` | a whole number from 1 to 365 | 90 days | how long a message body is kept before a read of it is refused with `CONTENT_EXPIRED` and the next retention pass deletes it | [message-persistence.md](../concepts/message-persistence.md#retention) |
| `DOCKINGBIRD_EVENT_RETENTION_DAYS` | a whole number from 1 to 3,650 | 30 days | how long the bus's replay history is kept | [message-persistence.md](../concepts/message-persistence.md#retention) |
| `DOCKINGBIRD_REQUEST_RECEIPT_RETENTION_DAYS` | a whole number from 3 to 3,650 | 90 days | how long the records that make a retried send return its first result are kept | [message-persistence.md](../concepts/message-persistence.md#retention) |
| `DOCKINGBIRD_RETENTION_PRUNE_BATCH_ROWS` | a whole number from 1 to 1,000,000 | 10,000 | the most rows one retention pass deletes from each table | [message-persistence.md](../concepts/message-persistence.md#retention) |
| `DOCKINGBIRD_MESSAGE_EXPIRY_DEFAULT_DAYS` | a whole number from 1 to 90 | 7 days | how long a delivery may stay `pending` before it expires; a sender that names no expiry gets it | [message-persistence.md](../concepts/message-persistence.md#limits-on-pending-work) |
| `DOCKINGBIRD_PENDING_DELIVERIES_MAX` | a whole number from 10 to 10,000 | 200 | the pending deliveries one target session holds; the next send past it is refused with `PROJECT_BUSY` and the reason `BACKPRESSURE` | [message-persistence.md](../concepts/message-persistence.md#limits-on-pending-work) |
| `DOCKINGBIRD_SURFACE_REMINDER_INTERVAL_S` | a whole number from 60 to 3,600 | 300 seconds | the time between reminders of one pending delivery | [reliable-messages.md](../guides/reliable-messages.md#2-what-happens-while-it-is-open) |
| `DOCKINGBIRD_STOP_REMINDERS_MAX` | a whole number from 0 to 5 | 2 | the reminders of one delivery | [reliable-messages.md](../guides/reliable-messages.md#2-what-happens-while-it-is-open) |
| `DOCKINGBIRD_P0_ACCEPTANCE_DEADLINE_S` | a whole number from 10 to 3,600 | 120 seconds | the time after the send when a P0 marked message is overdue | [reliable-messages.md](../guides/reliable-messages.md#2-what-happens-while-it-is-open) |
| `DOCKINGBIRD_P1_ACCEPTANCE_DEADLINE_S` | a whole number from 60 to 86,400 | 900 seconds | the same for P1 | [reliable-messages.md](../guides/reliable-messages.md#2-what-happens-while-it-is-open) |
| `DOCKINGBIRD_P2_ACCEPTANCE_DEADLINE_S` | a whole number from 300 to 604,800 | 14,400 seconds | the same for P2 | [reliable-messages.md](../guides/reliable-messages.md#2-what-happens-while-it-is-open) |
| `DOCKINGBIRD_P3_ACCEPTANCE_DEADLINE_S` | a whole number from 3,600 to 604,800 | 86,400 seconds | the same for P3 | [reliable-messages.md](../guides/reliable-messages.md#2-what-happens-while-it-is-open) |
| `DOCKINGBIRD_RECIPIENTS_MAX` | 0 or a positive whole number | 0, which bounds nothing | the most recipients one send lists or a group expands to; a send over a positive value is refused whole | [reliable-messages.md](../guides/reliable-messages.md#4-send-one-message-to-a-group) |

P0 must stay below P1, and P1 below P2. A value that breaks that order stops the command before it runs.

## Variables Dockingbird sets inside an agent's container

Dockingbird tells the tools that spread work across CPUs how many CPUs the container may use.
The agent's harness and every command it runs get these variables, each set to the container's CPU limit rounded up to a whole CPU.
You do not set them on your computer.

| Variable | Read by |
|---|---|
| `DOCKINGBIRD_CPUS` | the agent's own scripts; it names the budget itself |
| `PYINK_NUM_WORKERS`, `BLACK_NUM_WORKERS` | pyink and black |
| `PYTEST_XDIST_AUTO_NUM_WORKERS` | pytest-xdist, as the count of `-n auto` |
| `OMP_NUM_THREADS` | OpenMP |
| `MKL_NUM_THREADS` | MKL |
| `OPENBLAS_NUM_THREADS` | OpenBLAS |
| `CARGO_BUILD_JOBS` | cargo |
| `GOMAXPROCS` | Go |

Inside a container these tools count the host's CPUs on their own, so a check that started one worker per host CPU in a two-CPU container could use more memory than the container has. With the variables set, it starts two.
A value you set for one of the worker counts in the config's `[env]` or through mise stays yours.
A container with no CPU limit keeps the host's count, even when its memory limit is small.
Set the limit with `--cpus N` on `claude`, `codex` or `start` ([commands.md](commands.md)). The `[env]` table is in [app-config.md](files/app-config.md).

## What `DOCKINGBIRD_HOME` refuses

| Value or folder | Result |
|---|---|
| `/`, your home folder, or a folder above it | refused |
| a folder that holds native state (`operator.token`, `mode.json` or `pg`) | refused |
| an existing folder with files in it but no marker | refused; the empty `logs/` that `clean --all` keeps, your `instructions/` and `vaults/` folders, `versions.toml`, `config.toml`, `browser-solver.json`, `hosts.toml`, `fleet.toml` and Finder's `.DS_Store` do not count |
| a path with a space or `%$"'\` in it | not refused, but avoid it: `connect` passes a folder below it to ssh, which cannot take those characters |
| set together with `--home NAME` | exit 2: "--home and DOCKINGBIRD_HOME both name a home; use one of them." |

## How a setting behaves

| Case | Result |
|---|---|
| a value outside its bounds, or values that break a rule between settings | the command stops before it runs and names the variable, never its value |
| a name spelled in another case | the command stops before it runs, naming the variable |
| another variable that starts with `DOCKINGBIRD_` and that no command reads | the command stops before it does anything, exit 2, naming the variable |
| a setting of Dockingbird outside Docker (the database's address and roles, the developer's role switch, the host git's path) | the command stops the same way, since Docker mode never uses it |
| a setting changed while Dockingbird runs | the next command says "Dockingbird is running with other settings than this terminal's." and names `dockingbird stop`; the command after that starts Dockingbird with the new settings |
| `dockingbird status` after a change | shows the same lines under "Needs your attention" and restarts nothing |
| who sees a setting | the agents' harnesses read it too, none is a secret, and `docker inspect` shows them |

## Variables of other tools that Dockingbird reads

| Variable | Read by | What it does |
|---|---|---|
| `XDG_CONFIG_HOME` | the org login | when it is a path from `/`, `org.toml` lives in `$XDG_CONFIG_HOME/dockingbird/`; otherwise in `~/.config/dockingbird/` |
| `PGPASSFILE` | the org login and the fleet commands | names the PostgreSQL password file in place of `~/.pgpass`; it must be yours and readable by you alone |
| `DOCKER_HOST`, `DOCKER_CONTEXT` | every command that uses Docker | name the Docker daemon Dockingbird reaches, as for any docker command; Dockingbird otherwise uses the current context |
| `UV_INDEX_ZEUSFYI_USERNAME`, `UV_INDEX_ZEUSFYI_PASSWORD` | uv, at install | the index's user name (`license`) and your license key as its password; the key reaches uv in its environment only |
| `SHELL` | `dockingbird completion --install` | picks the shell whose completion script is written, unless you name one |

## Related

| Page | What it holds |
|---|---|
| [home-layout.md](files/home-layout.md) | what lives under `DOCKINGBIRD_HOME` and the `--home NAME` form |
| [org-file.md](files/org-file.md) | `org.toml`, `~/.pgpass` and the variables that move them |
| [commands.md](commands.md) | the global options, `--home` among them |
