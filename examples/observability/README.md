---
title: Prometheus and Grafana for a fleet
summary: Run the exporter on each host, add two scrape jobs to Prometheus, import the default dashboard into Grafana and set one alert.
audience: team-admin
commands:
  - fleet scrape
  - fleet probe
  - fleet queue --metrics
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Prometheus and Grafana for a fleet

Say a team has one Mac, `lab.example`, running a home with agents, and an admitter at `control-plane.example`. By the end of this page a Grafana shows their queue, load, context fill and cost, and one rule warns someone before an agent compacts. Each step ends with the thing to look for. Prometheus and Grafana are not part of Dockingbird, so install them from their own pages: [Prometheus](https://prometheus.io/docs/prometheus/latest/installation/) and [Grafana](https://grafana.com/docs/grafana/latest/setup-grafana/installation/).

## The files

| File | What it is |
|---|---|
| [exporter.py](exporter.py) | The exporter. It reads `fleet probe` and `fleet scrape` and serves one page. |
| [prometheus.yml](prometheus.yml) | Two scrape jobs with placeholder targets. |
| [dashboard.json](dashboard.json) | The default Grafana dashboard. |
| [queries.md](queries.md) | Fourteen queries, each with one line on what it answers. |

## Before you start

- Dockingbird on the host, with a home that has agents. Check with `dockingbird status`.
- Python 3.12 on the host. Check with `python3 --version`.
- Prometheus and Grafana running somewhere that reaches the host. Check by opening each in a browser.
- For the fleet job, an admitter on a machine of your pool. [The fleet scheduler guide](../../docs/guides/fleet-scheduler.md) starts it.

## 1. Read the figures once by hand

```bash
dockingbird fleet scrape
dockingbird --json fleet probe
dockingbird fleet queue --metrics
```

Run each one on its own. `fleet scrape` prints the agents' text and ends with a line reading `# EOF`. `fleet probe` prints one envelope with `id` `FLEET_PROBE`, and only on a Mac. `fleet queue --metrics` prints the scheduler's text, and only with an org login. None of them starts or changes anything. When one fails, its message id says what to fix: [`FLEET_SCRAPE_NO_STATUS`](../../docs/troubleshooting.md#fleet_scrape_no_status), [`FLEET_PROBE_NOT_MACOS`](../../docs/troubleshooting.md#fleet_probe_not_macos) or [`ORG_NOT_CONFIGURED`](../../docs/troubleshooting.md#org_not_configured).

## 2. Run the exporter on the host

```bash
python3 exporter.py 9105 --bind PRIVATE_ADDRESS --home NAME
```

`PRIVATE_ADDRESS` is the host's address on your private network, and `NAME` is a home from `dockingbird homes`. Wait up to a minute for the first reading, then fetch the page.

```bash
curl http://PRIVATE_ADDRESS:9105/metrics
```

The step worked when the page holds `dockingbird_scrape_up{home="NAME"} 1`. A 0 means the home could not be read, so run `dockingbird --home NAME fleet scrape` and read its message id. Start the exporter from a LaunchAgent on a Mac or a systemd user unit on Linux so it survives a restart.

## 3. Point Prometheus at it

Copy the two jobs of [prometheus.yml](prometheus.yml) into your Prometheus configuration. Replace `lab.example:9105` with the exporter's address, and `control-plane.example:9107` with the admitter's address and the port that `FLEET_SCHED_METRICS_PORT` names. Restart Prometheus. Open `/targets` on its port. The step worked when both jobs show `UP`.

The host job runs every 30 seconds, as the probe refreshes. The fleet job runs every 60 seconds, as the admitter updates at least every 30. [The Prometheus guide](../../docs/guides/prometheus.md) explains each choice.

## 4. Import the dashboard

In Grafana, add your Prometheus as a data source. Then open Dashboards, New, Import, and upload [dashboard.json](dashboard.json). The step worked when `Dockingbird fleet` opens with five rows: Fleet, Hosts, Agents, Cost and Health. Pick your Prometheus in the `Datasource` variable at the top. [The Grafana guide](../../docs/guides/grafana.md) describes each row.

## 5. Set one alert

Open Alerting, Alert rules, New alert rule. Choose your Prometheus data source and paste this query.

```text
max by (home, agent) (dockingbird_agent_context_used_tokens / dockingbird_agent_compact_at_tokens)
```

Set the condition to above 0.9 for 5 minutes and pick your own contact point. The rule reads Normal while every agent is under 90% of its compact point, and Firing when one passes it. The [alert rule page](https://grafana.com/docs/grafana/latest/alerting/alerting-rules/create-grafana-managed-rule/) describes each field.

## When it fails

- [`FLEET_PROBE_NOT_MACOS`](../../docs/troubleshooting.md#fleet_probe_not_macos): the host is not a Mac. `dockingbird_probe_up` is 0 and the Hosts row is empty.
- [`FLEET_SCRAPE_NO_STATUS`](../../docs/troubleshooting.md#fleet_scrape_no_status): the home's status failed or the home is off. Its `dockingbird_scrape_up` is 0.
- [`ORG_NOT_CONFIGURED`](../../docs/troubleshooting.md#org_not_configured): no org login on this computer, so `fleet queue --metrics` has nothing to read.
- [`FLEET_DB_UNREACHABLE`](../../docs/troubleshooting.md#fleet_db_unreachable): the fleet database did not answer. Ends 69.
- [`FLEET_DB_REFUSED`](../../docs/troubleshooting.md#fleet_db_refused): the database turned a login down. Ends 78.
