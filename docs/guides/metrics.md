---
title: Read the metrics by hand
summary: Read the figures of a host, a home, its agents and the fleet scheduler with five commands, before you set up any collector.
audience: daily
commands:
  - fleet probe
  - fleet read-home
  - fleet scrape
  - fleet queue --metrics
  - status --json
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Read the metrics by hand

This page gets you the figures Dockingbird keeps, printed in your terminal, so you know what a collector will see. The commands only look. They start, stop and change nothing. [The observability page](../concepts/observability.md) explains where the figures come from.

## Before you start

- A Mac for `fleet probe`. Check with `uname -s`, which prints `Darwin`.
- A home that is ready, for `fleet read-home` and `fleet scrape`. Check with `dockingbird status`.
- An org login as `user`, only for `fleet queue --metrics`. Check with `dockingbird org status`.

## Read the host

```bash
dockingbird fleet probe
```

The probe reads this Mac and its Docker once. It prints one line per figure and ends 0, even when a part could not be read. The first line is the done line.

```text
This Mac: 12 cores, SIZE of memory.
```

SIZE stands for the memory the probe read. The next lines give the load against the load line, the CPU, free memory, swap, the GPU, Docker's CPUs and memory, the containers running, and then one row for each kind of process with its CPU, memory and count. A figure it could not read says `unread`, and the screen ends with `Not read:` and the parts.

```bash
dockingbird --json fleet probe
```

With `--json` the probe prints one envelope whose `id` is `FLEET_PROBE`. Its `fields` carry two forms of each figure: display strings for the screen, such as `"68.5"` and `"47%"`, and typed numbers in the nested objects `load`, `cpu`, `memory`, `swap`, `gpu`, `docker` and `disk`, with sizes in bytes. `schema` is `dockingbird.fleet.probe/1`, and `categories` is a list of envelopes, one per kind of process. A script reads the typed numbers. A figure it could not read is `null`, and `unread` lists each part with the reason. A script reads `id` and `fields`, never `lines`. [The envelope page](../reference/integration/json.md) lists the keys.

## Read one home

```bash
dockingbird fleet read-home
```

This prints the home's folder, its version and whether Dockingbird is ready there, how many agents it has in each state, how many rows wait in its inbox, and its open questions with the oldest one's age. The first line is the done line.

```text
Home: FOLDER
```

It never prints a name, a subject or any other text from the inbox. `--json` adds every agent by name with its tool, state, model and effort, and every open inbox row, up to 200 of each.

## Read an agent's figures

```bash
dockingbird fleet scrape
dockingbird --home NAME fleet scrape
```

The first line reads the home you are in. The second reads the home named `NAME`, which `dockingbird homes` lists. Scrape prints the Prometheus text of each running agent, the same lines the agent's container serves at `/metrics` inside its own network. It writes the text itself, so it connects to no container. The text ends with one `# EOF` line, which is the done line.

```text
# HELP dockingbird_agent_turns HELP TEXT FROM THE RELEASE
# TYPE dockingbird_agent_turns gauge
dockingbird_agent_turns{profile="PROFILE",agent="claude-1",session="SESSION",tool="claude"} 4
# EOF
```

Each family's `# HELP` and `# TYPE` lines appear once, then one sample line per agent. An agent that stopped, crashed, has no session yet, or is a kept copy prints nothing. The figures are as fresh as the last ones the container wrote, so they run seconds to a minute behind.

```bash
dockingbird --json fleet scrape
```

With `--json` the envelope's `id` is `FLEET_SCRAPE`. Its `fields` hold `read_at`, the home's folder and profile, every agent with its session, tool, state and labels (up to 200, the rest counted), the text as `exposition`, one string per line, and `relay`, described below. The lines read `Home: NAME` and `Agents: N, M with metrics.`.

## Read the control-plane relay

On the control plane's home, `fleet scrape` prints eight more families after the agents' families and before `# EOF`. Their names start with `dockingbird_relay_`. They count what the control plane's relay does: the requests it answered, the requests it refused by reason and by stage, the replies it dropped, the exchanges in flight now, and the seconds from a request's arrival to its reply, per node.

```bash
dockingbird --home CONTROL_PLANE_HOME fleet scrape
```

`CONTROL_PLANE_HOME` is the home you made with `cp init`. The relay writes its figures every 10 seconds, and `fleet scrape` reads that file with one `docker exec`, so the figures run up to 10 seconds behind. Counters start at zero each time the relay restarts, and `dockingbird_relay_start_timestamp_seconds` says when. A sample line looks like this.

```text
# HELP dockingbird_relay_answered_total Requests answered with the daemon's response since the relay started, per node.
# TYPE dockingbird_relay_answered_total counter
dockingbird_relay_answered_total{profile="PROFILE",node="NODE"} 1520
```

On any other home the eight families are absent, and no `docker` command runs. With `--json`, the field `relay` says what happened. `read` comes with the number of `nodes`. Anything else names the reason: `no-relay` for a home that is no control plane or a relay that is not running, `docker-missing`, `exec-failed`, `no-snapshot` before the relay's first write, `too-large`, or `unexpected-shape`. When the relay cannot be read, the agents' text still prints whole and the command ends as it would have. [The metrics reference](../reference/metrics.md) lists the eight families with their labels.

## Read the fleet scheduler

```bash
dockingbird fleet queue --metrics
```

This prints the admitter's families in the Prometheus text format, for the workloads your role can see. It takes neither `--json` nor `--host`. The queue's depth by priority, each host's reservations and headroom, red gate lines, stale hosts, interrupted workloads, holds by reason and each host's agents against its agent cap come first. Counters of admissions, starts, queue wait and agent seconds follow. The admitter serves the same text on its own port, at the fleet database's host.

## Read the status rows

```bash
dockingbird --json status
```

Each row of `status --json` is an envelope of its own. A running agent's row carries the figures its supervisor writes: `phase`, `turns`, `turn_running`, `last_turn_at`, `last_turn`, `context_window`, `compact_at_asked`, `changed`, `untracked`, `screen_held`, `token_failed`, `sign_in_retry`, `bus_losses`, the `result_` figures of the last result, `model_usage` per model, `compactions` and `api_retries`. Scrape turns these rows into the metric families. A value the tool did not report is `null`.

## The labels

| Label | What it names | Where it appears |
|---|---|---|
| `profile` | The home | Every agent line and every relay line |
| `agent` | The agent's name | Every agent line |
| `session` | The agent's session | Every agent line |
| `tool` | `claude` or `codex` | Every agent line |
| `team`, `role` | The swarm and the role of a fleet agent | An agent of a swarm |
| `node` | The node that sent the request | The relay's per-node lines |

## The JSON forms for a script

| Command | `id` | What `fields` hold |
|---|---|---|
| `fleet probe --json` | `FLEET_PROBE` | Each figure by name, the kinds of process, `unread` |
| `fleet read-home --json` | `FLEET_HOME` | The home's agents, state counts, inbox rows, `unread` |
| `fleet scrape --json` | `FLEET_SCRAPE` | `read_at`, the agents, `exposition`, `relay` |
| `fleet queue --metrics` | none | Prints text only, with no `--json` form |

[The example exporter](../../examples/observability/exporter.py) reads these envelopes with the standard library alone. [The metrics reference](../reference/metrics.md) lists every family. To collect the figures on a schedule, go on to [the Prometheus guide](prometheus.md).

## When it fails

- [`FLEET_PROBE_NOT_MACOS`](../troubleshooting.md#fleet_probe_not_macos): the probe reads macOS only and ends 1. Run it on a Mac.
- [`FLEET_PROBE_NO_SYSCTL`](../troubleshooting.md#fleet_probe_no_sysctl): the probe could not read the Mac's cores and stopped. Ends 1.
- [`FLEET_PROBE_UNREAD`](../troubleshooting.md#fleet_probe_unread): a part could not be read. The rest is printed and the command ends 0.
- [`FLEET_HOME_NO_STATUS`](../troubleshooting.md#fleet_home_no_status): the home's own `status` failed, so `read-home` stops. Ends 1.
- [`FLEET_HOME_UNREAD`](../troubleshooting.md#fleet_home_unread): the inbox could not be read, so it is `unread`. Ends 0.
- [`FLEET_SCRAPE_NO_STATUS`](../troubleshooting.md#fleet_scrape_no_status): the home's status failed or Dockingbird is not ready there, so no figures print. Ends 1.
- [`FLEET_SCRAPE_NO_DISK`](../troubleshooting.md#fleet_scrape_no_disk) and [`FLEET_HOME_NO_DISK`](../troubleshooting.md#fleet_home_no_disk): `--disk` belongs to the probe. Both end 2.
- [`ORG_NOT_CONFIGURED`](../troubleshooting.md#org_not_configured): this computer has no org login, which `fleet queue --metrics` needs. Run `dockingbird org login`.
- [`FLEET_DB_UNREACHABLE`](../troubleshooting.md#fleet_db_unreachable): the fleet database did not answer. Ends 69.
- [`FLEET_DB_REFUSED`](../troubleshooting.md#fleet_db_refused): the database turned the login down. Ends 78.
