---
title: Collect the metrics with Prometheus
summary: Run the example exporter on each host and point a Prometheus at it, and at the fleet scheduler's admitter, with two scrape jobs.
audience: team-admin
commands:
  - fleet probe
  - fleet scrape
  - fleet queue --metrics
  - fleet admitter
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Collect the metrics with Prometheus

This page puts a host's agent figures, the host's own load and the fleet queue into a Prometheus you run. Prometheus is yours to install. The [official install page](https://prometheus.io/docs/prometheus/latest/installation/) covers every platform. [The observability page](../concepts/observability.md) shows how the pieces connect: an agent's container serves its figures only inside its own network, so a small exporter on the host serves them for Prometheus.

## Before you start

- You have read the figures once by hand, as [the metrics guide](metrics.md) shows. Check with `dockingbird fleet scrape`, which ends with a `# EOF` line.
- Python 3.12 on each host. Check with `python3 --version`.
- Prometheus installed, on any computer that reaches your hosts. Check with `prometheus --version`.
- For the fleet job, a running admitter and its metrics port. [The fleet scheduler guide](fleet-scheduler.md) starts it.

## Copy the exporter to each host

Put [exporter.py](../../examples/observability/exporter.py) on each host that runs homes. Python is all it needs. Each 30 seconds it runs `dockingbird --json fleet probe`. Each 60 seconds it runs `dockingbird --home NAME --json fleet scrape` for every home you name, so a slow home never holds up the others. To collect the control plane's relay families, name the control plane's home with `--home`: `fleet scrape` prints them on that home only. From each envelope it keeps `id` and `fields`, and drops `lines`.

## Run it

```bash
python3 exporter.py 9105 --bind PRIVATE_ADDRESS --home NAME
```

The first word is the port. `--bind` is the address to listen on, and it defaults to loopback, so Prometheus on another computer needs the host's address on your private network. `--home NAME` names a home of this host and may repeat. With no `--home` the exporter reads the default home and labels it `default`. Run it as the user that owns the homes, with `dockingbird` on its `PATH`. To keep it running, start it from your service manager: a LaunchAgent on a Mac or a systemd user unit on Linux.

Check the page after the first reading, which takes up to a minute.

```bash
curl http://PRIVATE_ADDRESS:9105/metrics
```

The step worked when the page holds one `dockingbird_scrape_up` line per home with the value 1.

```text
dockingbird_scrape_up{home="NAME"} 1
```

## What the page holds

| Series | Type | Meaning |
|---|---|---|
| `dockingbird_host_*` | gauge | The probe's typed figures, such as `dockingbird_host_load_one`, `dockingbird_host_memory_free_bytes` and `dockingbird_host_docker_containers_running`, and `dockingbird_host_category_*{category}` per kind of process |
| `dockingbird_probe_up` | gauge | 1 when the last probe read worked and its schema is `dockingbird.fleet.probe/1`, else 0 |
| `dockingbird_agent_*` | gauge | Each home's own text, passed through with one added label, `home` |
| `dockingbird_relay_*` | gauge, counter, histogram | The control plane's relay: eight families, passed through with one added label, `home`, from the control plane's home only |
| `dockingbird_scrape_up{home}` | gauge | 1 when the home's last read worked, else 0 |

A home that fails to read serves no agent figures, only `scrape_up` 0. A home that is off, because it turned itself off after 30 minutes with no agent, reads as not ready and also shows 0. On a Linux host the probe cannot run, so `probe_up` is 0 and the agent figures still arrive. [The metrics reference](../reference/metrics.md) lists every family.

## Add the two jobs to Prometheus

Copy the jobs from [prometheus.yml](../../examples/observability/prometheus.yml) into your own configuration and replace the placeholder targets. The [configuration reference](https://prometheus.io/docs/prometheus/latest/configuration/configuration/) explains every key.

| Job | Target | Interval | Why |
|---|---|---|---|
| `dockingbird_hosts` | `lab.example:9105`, one per host, with a `host` label | 30 s | The probe refreshes every 30 s |
| `dockingbird_fleet` | `control-plane.example:9107`, the admitter | 60 s | One admission pass at least every 30 s, so 60 s sees each change |

The admitter serves its families at the fleet database's host, on the port that `FLEET_SCHED_METRICS_PORT` names, 9107 by default. Use that port in the target. To serve on another port, start the admitter with `dockingbird fleet admitter --metrics-port N`. `--metrics-port 0` asks the kernel for a free port, which the log line `FLEET_METRICS_SERVING` names. When the admitter cannot open its address, it logs `FLEET_METRICS_UNSERVED`, keeps admitting and tries the address again before each pass, so the fleet job shows the target down until the port is free. Leave the job out when your organisation runs no fleet scheduler. Restart Prometheus, or send it SIGHUP, so it reads the file.

## Check the targets

Open the Prometheus page at `/targets` on its own port. The step worked when both jobs show the state `UP`. Then run these queries in its expression browser.

```text
dockingbird_scrape_up
count by (state) (dockingbird_agent_info)
```

The first returns one series per home. The second counts agents by state. [The queries page](../../examples/observability/queries.md) holds fourteen queries. To draw them, go on to [the Grafana guide](grafana.md).

## When it fails

- [`FLEET_PROBE_NOT_MACOS`](../troubleshooting.md#fleet_probe_not_macos): the host is not a Mac, so `dockingbird_probe_up` is 0. The agent figures still arrive.
- [`FLEET_SCRAPE_NO_STATUS`](../troubleshooting.md#fleet_scrape_no_status): the home's status failed or Dockingbird is not ready there. Its `scrape_up` is 0.
- [`FLEET_METRICS_UNSERVED`](../troubleshooting.md#fleet_metrics_unserved): the admitter could not open its metrics address. Admission goes on. Free the port or wait for the address.
- [`FLEET_DB_UNREACHABLE`](../troubleshooting.md#fleet_db_unreachable): the admitter's database did not answer, so the fleet job has no target. Ends 69.
- [`FLEET_DB_REFUSED`](../troubleshooting.md#fleet_db_refused): the database turned the admitter's login down. Ends 78. Run `dockingbird org status`.
