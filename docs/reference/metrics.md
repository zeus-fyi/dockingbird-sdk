---
title: Metrics reference
summary: Every metric family Dockingbird serves, with its type, labels and unit, the agent families first, the fleet families second and the exporter's own gauges last.
audience: integrator
commands:
  - fleet scrape
  - fleet queue --metrics
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Metrics reference

This page is generated from the release's own `fleet scrape` and `fleet queue --metrics` output, and the names and types printed there are the authority. [The observability page](../concepts/observability.md) explains the sources. The Help column of each row is the release's own `# HELP` line. The Meaning column is a short gloss. In the exporter's table, the Help column names the probe field each series is read from.

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

The admitter serves these on its own port, and `dockingbird fleet queue --metrics` prints them. A family may carry more labels than listed. Use `rate()` or `increase()` on the counters only.

| Family | Type | Labels | Unit | Help | Meaning |
|---|---|---|---|---|---|
| `fleet_queue_depth` | gauge | `priority` | workloads | from the release's output | workloads in the queue, by priority |
| `fleet_reserved_millicores` | gauge | `host` | millicores | from the release's output | CPU reserved on the host |
| `fleet_reserved_mib` | gauge | `host` | MiB | from the release's output | memory reserved on the host |
| `fleet_headroom_millicores` | gauge | `host` | millicores | from the release's output | CPU left to reserve on the host |
| `fleet_headroom_mib` | gauge | `host` | MiB | from the release's output | memory left to reserve on the host |
| `fleet_gate_red` | gauge | `host` | count | from the release's output | red gate lines of the host |
| `fleet_host_stale` | gauge | `host` | 0 or 1 | from the release's output | the host's sample is stale |
| `fleet_interrupted` | gauge | `host` | workloads | from the release's output | interrupted workloads on the host |
| `fleet_holds` | gauge | `reason` | workloads | from the release's output | held workloads, by reason |
| `fleet_agent_cap` | gauge | `host` | agents | from the release's output | the host's agent cap against its fullest home |
| `fleet_admissions_total` | counter | `host` | count | from the release's output | workloads the host admitted |
| `fleet_starts_total` | counter | `host` | count | from the release's output | agent starts on the host |
| `fleet_queue_wait_seconds_total` | counter | `host` | seconds | from the release's output | seconds workloads waited before the host admitted them |
| `fleet_agent_seconds_total` | counter | `role`, `host` | seconds | from the release's output | agent seconds of the role on the host |
| `fleet_agent_idle_seconds_total` | counter | `role`, `host` | seconds | from the release's output | idle agent seconds of the role on the host |

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
