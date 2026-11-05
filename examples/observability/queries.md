---
title: Observability queries
summary: Fourteen PromQL queries for a Dockingbird fleet, each with one line on what it answers.
audience: integrator
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Observability queries

These queries work on any installation, and none names a host. Paste one into the Prometheus expression browser or a Grafana panel. The default dashboard in [dashboard.json](dashboard.json) runs them with the filter `{host=~"$host",home=~"$home"}` added to the agent and host series. Every family is listed in [the metrics reference](../../docs/reference/metrics.md).

The agent families are gauges. `model_cost_usd` and `model_tokens` count from the start of an agent's process (Claude) or thread (Codex) and fall to zero when it restarts. A window query on them takes `delta()` or `deriv()`, and a restart reads as a negative change. `rate()` and `increase()` fit only the counters that end in `_total`.

## Agents

| Question | Query | What it answers |
|---|---|---|
| How full is each agent's context? | `dockingbird_agent_context_used_tokens / dockingbird_agent_context_window_tokens` | The share of its model's window each agent has used. |
| Which agents are near their compact point? | `dockingbird_agent_context_used_tokens / dockingbird_agent_compact_at_tokens > 0.9` | Agents within 10% of compacting, with their share. |
| How many agents are in each state? | `count by (state) (dockingbird_agent_info)` | The number of agents in each state. |
| What has each model cost so far? | `sum by (model) (dockingbird_agent_model_cost_usd)` | Cost since the agents' processes started, in US dollars, for Claude agents. |
| What did each model cost in the last hour? | `sum by (model) (delta(dockingbird_agent_model_cost_usd[1h]))` | The change in cost over one hour. |
| Token throughput by type, per second | `sum by (type) (deriv(dockingbird_agent_model_tokens[15m]))` | Input, output, cache read and cache creation tokens per second. |
| Turns in the last hour per agent | `delta(dockingbird_agent_turns[1h])` | How many turns each agent finished in the hour. |
| Agents whose sign-in is failing | `dockingbird_agent_sign_in_retry > 0 or dockingbird_agent_token_failed > 0` | Agents retrying their sign-in or with a failed token. |
| Agents silent for over an hour | `time() - dockingbird_agent_last_turn_timestamp_seconds > 3600` | Agents whose last turn ended over an hour ago, with the seconds since. |

## The fleet scheduler

| Question | Query | What it answers |
|---|---|---|
| Queue depth by priority | `fleet_queue_depth` | Workloads waiting, for each priority. |
| Mean queue wait per host | `rate(fleet_queue_wait_seconds_total[1h]) / rate(fleet_admissions_total[1h])` | The seconds a workload waited before each host admitted it. |
| Headroom per host | `fleet_headroom_millicores` and `fleet_headroom_mib` | The CPU and the memory each host can still reserve. |
| Idle share per role | `rate(fleet_agent_idle_seconds_total[1h]) / rate(fleet_agent_seconds_total[1h])` | The share of each role's agent time spent idle. |

## The exporter

| Question | Query | What it answers |
|---|---|---|
| Homes the exporter could not read | `dockingbird_scrape_up == 0` | Homes with no figures, because the read failed or the home is off. |

## Use them

For an alert, paste a query into a Grafana alert rule and add a condition. [The Grafana guide](../../docs/guides/grafana.md) shows three that are worth having. To change what a query covers, add a selector such as `{home="NAME"}` after the family name.
