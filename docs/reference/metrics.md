---
title: Metrics reference
summary: Every metric family Dockingbird serves, with its type, labels and unit, the agent families first, the fleet scheduler's second, the control-plane relay's third and the exporter's own gauges last.
audience: integrator
commands:
  - fleet scrape
  - fleet queue --metrics
  - fleet admitter
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Metrics reference

This page is generated from the release's own `fleet scrape` and `fleet queue --metrics` output, and the names and types printed there are the authority. `fleet scrape` prints the agent families and, on a control-plane home, the relay families. `fleet queue --metrics` prints the fleet families. [The observability page](../concepts/observability.md) explains the sources. The Meaning column is a short gloss. Where a table has a Help column, it holds the release's own `# HELP` line, and in the exporter's table it names the probe field each series is read from.

## Agent families

Every family has the prefix `dockingbird_agent_`, the type gauge, and the labels `profile`, `agent`, `session` and `tool`, plus `team` and `role` for an agent of a swarm. `dockingbird fleet scrape` prints them and each agent's container serves them. The Extra labels column lists what a family adds.

| Family | Type | Extra labels | Unit | Help | Meaning |
|---|---|---|---|---|---|
| `dockingbird_agent_info` | gauge | `model`, `effort`, `state` | from the release's output | from the release's output | the agent's model, effort and state as labels |
| `dockingbird_agent_turns` | gauge | none | turns | from the release's output | turns finished since the process or thread started |
| `dockingbird_agent_turn_running` | gauge | none | 0 or 1 | from the release's output | a turn is running |
| `dockingbird_agent_last_turn` | gauge | `state` | from the release's output | from the release's output | the last turn, its state as a label |
| `dockingbird_agent_last_turn_timestamp_seconds` | gauge | none | seconds | from the release's output | Unix time the last turn ended |
| `dockingbird_agent_context_used_tokens` | gauge | none | tokens | from the release's output | context in use |
| `dockingbird_agent_context_window_tokens` | gauge | none | tokens | from the release's output | the model's context window |
| `dockingbird_agent_compact_at_tokens` | gauge | none | tokens | from the release's output | the context size at which the agent compacts |
| `dockingbird_agent_compactions` | gauge | none | count | from the release's output | compactions since the process or thread started |
| `dockingbird_agent_changed_paths` | gauge | none | paths | from the release's output | changed paths in the agent's copy |
| `dockingbird_agent_untracked_paths` | gauge | none | paths | from the release's output | untracked paths in the agent's copy |
| `dockingbird_agent_changing` | gauge | none | from the release's output | from the release's output | the agent's copy is changing |
| `dockingbird_agent_screen_held` | gauge | none | 0 or 1 | from the release's output | the agent's screen is held |
| `dockingbird_agent_sign_in_retry` | gauge | none | count | from the release's output | sign-in retries |
| `dockingbird_agent_token_failed` | gauge | none | 0 or 1 | from the release's output | the agent's token failed |
| `dockingbird_agent_bus_losses` | gauge | none | count | from the release's output | connections to the bus lost |
| `dockingbird_agent_api_retries` | gauge | none | count | from the release's output | API retry events, Claude only |
| `dockingbird_agent_model_tokens` | gauge | `model`, `type` | tokens | from the release's output | tokens per model, type is input, output, cache_read or cache_creation |
| `dockingbird_agent_model_cost_usd` | gauge | `model` | US dollars | from the release's output | cost per model, Claude only |
| `dockingbird_agent_result_input_tokens` | gauge | none | tokens | from the release's output | input tokens of the last result |
| `dockingbird_agent_result_output_tokens` | gauge | none | tokens | from the release's output | output tokens of the last result |
| `dockingbird_agent_result_cache_read_tokens` | gauge | none | tokens | from the release's output | cache read tokens of the last result |
| `dockingbird_agent_result_cache_creation_tokens` | gauge | none | tokens | from the release's output | cache creation tokens of the last result |
| `dockingbird_agent_result_reasoning_output_tokens` | gauge | none | tokens | from the release's output | reasoning output tokens of the last result, Codex only |
| `dockingbird_agent_result_cost_usd` | gauge | none | US dollars | from the release's output | cost of the last result, Claude only |
| `dockingbird_agent_result_duration_seconds` | gauge | none | seconds | from the release's output | duration of the last result |
| `dockingbird_agent_result_turns` | gauge | none | count | from the release's output | turns of the last result |

Model tokens and costs count from the start of an agent's process (Claude) or thread (Codex) and fall to zero when it restarts. Take `delta()` or `deriv()` of them. A Codex agent has no cost and no `api_retries`, and its per-model tokens and compactions stay empty until its rollout has been read.

## Fleet families

The admitter serves these on its own port, and `dockingbird fleet queue --metrics` prints them. The page leaves out a family with no sample. Every family is a gauge except the five that end in `_total`, which are counters: they only grow and survive every admitter restart, so use `rate()` or `increase()` on them only.

| Family | Type | Labels | Unit | Meaning |
|---|---|---|---|---|
| `fleet_queue_depth` | gauge | `priority` | workloads | Pending workloads, swarms and leases, at each priority |
| `fleet_reserved_millicores` | gauge | `host` | millicores | CPU reserved on the host by workloads that have not ended |
| `fleet_reserved_mib` | gauge | `host` | MiB | Memory reserved on the host by workloads that have not ended |
| `fleet_headroom_millicores` | gauge | `host` | millicores | The host's reservable CPU less the reserved CPU, below zero when a policy change lowered the share under the reservations |
| `fleet_headroom_mib` | gauge | `host` | MiB | The host's reservable memory less the reserved memory |
| `fleet_gate_red` | gauge | `host`, `figure` | 0 or 1 | 1 while the last admission pass left the host's gate line on that figure red |
| `fleet_host_stale` | gauge | `host` | 0 or 1 | 1 when the host's latest sample is older than `HOST_STALE_S`, or it has none |
| `fleet_host_probe` | gauge | `host`, `probe` | 1 | 1 for each stale host, labelled with the class of the check the admitter gave it when it went stale; absent for a host that is not stale |
| `fleet_interrupted` | gauge | `host` | workloads | Workloads interrupted on the host now |
| `fleet_placed_agents` | gauge | `host` | agents | Agents of workloads that have not ended placed on the host, every step but retired |
| `fleet_holds` | gauge | `reason` | workloads | Pending workloads the last pass held off at least one host for that reason |
| `fleet_home_agents` | gauge | `host` | agents | Agents of the host's fullest home, counted against the agent cap as the last pass judged them; absent for a host no pass has judged |
| `fleet_agent_cap` | gauge | `host` | agents | The host's agent cap: the most agents one of its homes runs |
| `fleet_host_agents` | gauge | `host` | agents | Agent containers the host's latest sample saw running, in every home, listed in `hosts.toml` or not; absent for a host with no sample |
| `fleet_admissions_total` | counter | `host` | count | First admissions on the host: every lease's and a swarm's first, never a re-admission's |
| `fleet_starts_total` | counter | `host` | count | Swarm starts on the host |
| `fleet_queue_wait_seconds_total` | counter | `host` | seconds | Seconds the host's first admissions waited from their submit |
| `fleet_agent_seconds_total` | counter | `role`, `host` | seconds | Seconds of the role's running agents on the host, one tick's interval per agent |
| `fleet_agent_idle_seconds_total` | counter | `role`, `host` | seconds | Seconds of the role's idle agents on the host, idle meaning no open request |

The `probe` label of `fleet_host_probe` is one of `ssh_timeout`, `ssh_refused`, `host_up_worker_silent`, `route_error` and `no_route`, or `unread` when the admitter recorded none. The `reason` label of `fleet_holds` is a hold word, or `unread`. No label holds a path, a token or an agent's text.

## Control-plane relay families

`dockingbird fleet scrape` prints these after the agent families, on the control plane's home only. On any other home it prints none and runs no `docker` command. Every counter and the histogram start at zero when the relay restarts. Each line carries the label `profile` first, the home's profile id, then the labels below. Prometheus gets them through the example exporter, which adds `home` to every sample line it passes on. The page leaves out a family with no sample: `dockingbird_relay_refused_total` has no line until the first refusal, and `dockingbird_relay_dropped_total` has none until the first drop.

| Family | Type | Labels | Unit | Help | Meaning |
|---|---|---|---|---|---|
| `dockingbird_relay_info` | gauge | `version`, `workers`, `per_node` | 1 | The relay's fleet version and its bounds on exchanges in flight, as the relay records them. | the relay's fleet version, the requests it serves at once (`workers`) and the most one node may hold (`per_node`) |
| `dockingbird_relay_start_timestamp_seconds` | gauge | none | seconds | When the relay started, in Unix seconds; its counters start at zero there. | Unix time of the relay's start |
| `dockingbird_relay_written_timestamp_seconds` | gauge | none | seconds | When the relay last wrote these figures, in Unix seconds. | Unix time of the snapshot you read |
| `dockingbird_relay_in_flight` | gauge | `node` | exchanges | Exchanges on the daemon's socket in flight now, per node. | requests being served for the node now |
| `dockingbird_relay_answered_total` | counter | `node` | requests | Requests answered with the daemon's response since the relay started, per node. | requests answered |
| `dockingbird_relay_refused_total` | counter | `node`, `reason`, `stage` | requests | Requests refused since the relay started, per node, by reason and by stage: check, before the socket; exchange, the socket's own refusal. | requests refused |
| `dockingbird_relay_dropped_total` | counter | `node`, `reason` | replies | Replies not published and library errors since the relay started, by node (empty for an error of no node) and reason. | replies not published, and library errors |
| `dockingbird_relay_request_seconds` | histogram | `node`, and `le` on the `_bucket` lines | seconds | Seconds from a request's arrival to its reply's publish, answered requests only, per node. | seconds per answered request |

- `node` is the id of the node that sent the request. On `dockingbird_relay_dropped_total` it is empty for a library error that names no node, and an empty label and an absent one are the same series.
- `stage` is `check` for a request the relay's own checks refused before the daemon's socket, and `exchange` for a refusal the socket's exchange raised.
- `reason` on `dockingbird_relay_refused_total` is the error's reason word, such as `RPC_SERVER_UNAVAILABLE`, or `unknown` when the error names none. On `dockingbird_relay_dropped_total` it is `no_reply` for a request that named no reply subject, or the class name of the error that dropped the reply.
- Each map keeps at most 64 distinct reason words besides `other` (`NATS_RELAY_REASONS_MAX`). A new word past that counts as `other`.
- The histogram has one bucket per bound of 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10 and 30 seconds, then `+Inf`. The 30 is the fleet request timeout (`NATS_REQUEST_TIMEOUT_S`). It counts answered requests only, from the request's arrival to the publish of its reply, so a refused request adds nothing. `_sum` and `_count` follow the buckets of each node.
- Every node has its `in_flight`, `answered_total` and `request_seconds` lines from the first snapshot, at zero.
- The relay writes its figures every 10 seconds (`NATS_RELAY_METRICS_WRITE_S`), so a scrape runs up to 10 seconds behind. The text holds at most 1,048,576 bytes (`NATS_RELAY_METRICS_MAX_BYTES`, about 300 nodes).
- With `--json`, the `relay` field of `fleet scrape` says `read`, with how many `nodes`, or names why not: `no-relay`, `docker-missing`, `exec-failed`, `no-snapshot`, `too-large` or `unexpected-shape`. A relay that cannot be read leaves the agent families whole.

## The exporter's gauges

These come from the [example exporter](../../examples/observability/exporter.py), not from the release. They sit on the same page as the agent families.

| Family | Type | Labels | Unit | Help |
|---|---|---|---|---|
| `dockingbird_scrape_up` | gauge | `home` | 0 or 1 | 1 when the home's last `fleet scrape` worked |
| `dockingbird_probe_up` | gauge | none | 0 or 1 | 1 when the last `fleet probe` worked and its `schema` is `dockingbird.fleet.probe/1` |
| `dockingbird_host_cores` | gauge | none | cores | from the probe's `--json` fields of this release: `cores` |
| `dockingbird_host_load_one` | gauge | none | load | from the probe's `--json` fields of this release: `load.one` |
| `dockingbird_host_load_line` | gauge | none | load | from the probe's `--json` fields of this release: `load.line` |
| `dockingbird_host_cpu_busy_pct` | gauge | none | percent | from the probe's `--json` fields of this release: `cpu.busy_pct` |
| `dockingbird_host_idle_cores` | gauge | none | cores | from the probe's `--json` fields of this release: `cpu.idle_cores` |
| `dockingbird_host_memory_free_bytes` | gauge | none | bytes | from the probe's `--json` fields of this release: `memory.free_bytes` |
| `dockingbird_host_memory_free_pct` | gauge | none | percent | from the probe's `--json` fields of this release: `memory.free_pct` |
| `dockingbird_host_swap_used_bytes` | gauge | none | bytes | from the probe's `--json` fields of this release: `swap.used_bytes` |
| `dockingbird_host_gpu_device_pct` | gauge | none | percent | from the probe's `--json` fields of this release: `gpu.device_pct` |
| `dockingbird_host_docker_containers_running` | gauge | none | containers | from the probe's `--json` fields of this release: `docker.containers_running` |
| `dockingbird_host_docker_containers_total` | gauge | none | containers | from the probe's `--json` fields of this release: `docker.containers_total` |
| `dockingbird_host_disk_free_bytes` | gauge | none | bytes | from the probe's `--json` fields of this release: `disk.free_bytes` |
| `dockingbird_host_category_count` | gauge | `category` | processes or containers | from the probe's `--json` fields of this release: `categories[].fields.count` |
| `dockingbird_host_category_memory_bytes` | gauge | `category` | bytes | from the probe's `--json` fields of this release: `categories[].fields.memory_used` |
| `dockingbird_host_category_cpu_pct` | gauge | `category` | percent of one core | from the probe's `--json` fields of this release: `categories[].fields.cpu, read from a string such as "39.4%"` |

On each agent line the exporter adds a `home` label. The `host` label is not the exporter's: your Prometheus attaches it from the job's `labels`, as [prometheus.yml](../../examples/observability/prometheus.yml) shows.
