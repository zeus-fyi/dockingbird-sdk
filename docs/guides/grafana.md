---
title: Draw the metrics in Grafana
summary: Import the default Dockingbird dashboard into your own Grafana, read its five rows, add a host, and set three alerts.
audience: team-admin
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Draw the metrics in Grafana

This page loads a ready dashboard into your Grafana and sets the three alerts most worth having. Grafana is yours to install. The [official install page](https://grafana.com/docs/grafana/latest/setup-grafana/installation/) covers every platform. The dashboard reads from the Prometheus that [the Prometheus guide](prometheus.md) sets up.

## Before you start

- Prometheus collects the exporter and, for the fleet row, the admitter. Check that `dockingbird_scrape_up` returns a series in the Prometheus expression browser.
- Grafana runs and you can sign in as an editor or an admin. Check by opening its address in a browser.
- Grafana has a Prometheus data source that points at your Prometheus. The [data source page](https://grafana.com/docs/grafana/latest/datasources/prometheus/configure/) shows how. Check that its Save and test button says it works.

## Import the dashboard

Open Dashboards, then New, then Import. Upload [dashboard.json](../../examples/observability/dashboard.json) and press Import. The [import page](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/import-dashboards/) shows the same screen. The step worked when a dashboard titled `Dockingbird fleet` opens with five rows.

The file holds no data source of its own. At the top of the dashboard, the variable `Datasource` picks your Prometheus. Pick it once. The variables `Host` and `Home` list every value of the `host` and `home` labels, and both default to all.

## The five rows

| Row | Panels | Source |
|---|---|---|
| Fleet | Queue depth by priority, headroom per host in millicores and in MiB, holds by reason, mean queue wait per host, idle share per role | The admitter |
| Hosts | Load against the load line, free memory, containers running | The probe |
| Agents | A table of every agent with state, model, context fill, age of the last turn and cost, agents by state, context fill, agents near the compact point, turns in the last hour | The agents |
| Cost | Cost so far per model, the change over the last hour, token throughput by type | The agents |
| Health | Sign-in retries and token failures, bus losses, API retries, agents silent for over an hour, homes the exporter could not read | The agents and the exporter |

The Fleet row stays empty when your organisation runs no fleet scheduler. The Hosts row is empty for a Linux host, because the probe reads macOS only. [The queries page](../../examples/observability/queries.md) states each query and what it answers.

## Read the dashboard

The `Every agent` table in the Agents row is the quickest check. Each row is one agent, with its host, home, state, model, effort, context fill, the seconds since its last turn, and its cost so far. Sort it by context fill to see which agent compacts next. The cost is Claude Code's own estimate, so a Codex agent shows none.

Cost panels read gauges that fall to zero when an agent restarts. The panel for the last hour uses `delta()`, so a restart appears as a dip. The queue panels read counters, so they use `rate()` over an hour.

The refresh is 30 seconds and the time range is the last 6 hours. Both are the dashboard's defaults. Change them in the dashboard settings.

## The variables

| Variable | Type | Values | Used by |
|---|---|---|---|
| `Datasource` (`DS`) | data source | Every Prometheus data source | Every panel |
| `Host` (`host`) | query | `label_values(dockingbird_scrape_up, host)`, from the job's `host` label | The agent, host and health panels |
| `Home` (`home`) | query | `label_values(dockingbird_scrape_up{host=~"$host"}, home)`, from the exporter's `home` label | The agent and health panels |

The fleet panels use none of them. The admitter serves its own `host` label for each pool host, and those names come from the pool, not from your Prometheus jobs.

## Keep your changes

Edits you make in Grafana stay in Grafana. To keep a copy next to your own configuration, open the dashboard's settings, choose JSON Model, and save the text to a file. Importing the shipped file again asks before it overwrites, because the dashboard keeps the uid `dockingbird-fleet`.

## Add a host

Add its exporter to the `dockingbird_hosts` job in your Prometheus configuration, with its own `host` label, and restart Prometheus. The step worked when the `Host` variable lists the new name after the next refresh of the page. No panel changes, because every panel filters on the variable.

## Alert on three signals

Grafana's [alerting pages](https://grafana.com/docs/grafana/latest/alerting/alerting-rules/create-grafana-managed-rule/) show how to create a rule. Open Alerting, then Alert rules, then New alert rule, choose your Prometheus data source, paste a query below and set the condition. The thresholds are examples. Choose your own.

| Signal | Query | Example condition |
|---|---|---|
| An agent's context is near its compact point | `max by (home, agent) (dockingbird_agent_context_used_tokens / dockingbird_agent_compact_at_tokens)` | Above 0.9 for 5 minutes |
| A host is over its load line | `dockingbird_host_load_one / dockingbird_host_load_line` | Above 1 for 10 minutes |
| The queue is waiting long | `rate(fleet_queue_wait_seconds_total[1h]) / rate(fleet_admissions_total[1h])` | Above 900 seconds for 15 minutes |

No family holds the oldest wait itself. The mean wait per host, from two counters, is the nearest figure. The probe's load line is 130% of the Mac's cores, and the compact point is the context size at which an agent compacts.

## When it fails

- [`FLEET_PROBE_NOT_MACOS`](../troubleshooting.md#fleet_probe_not_macos): a Linux host cannot run the probe. Its row in Hosts stays blank.
- [`FLEET_SCRAPE_NO_STATUS`](../troubleshooting.md#fleet_scrape_no_status): one home would not answer. Its agents vanish from the panels, and Health names the home.
- [`FLEET_DB_UNREACHABLE`](../troubleshooting.md#fleet_db_unreachable): the database behind the admitter is down or asleep, exit 69. Fleet shows nothing.
- [`FLEET_DB_REFUSED`](../troubleshooting.md#fleet_db_refused): the database rejected the admitter's login, exit 78. Fleet shows nothing.
