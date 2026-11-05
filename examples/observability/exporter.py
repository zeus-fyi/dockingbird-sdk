"""Serve this host's Dockingbird figures as one Prometheus text page.

Usage: python3 examples/observability/exporter.py PORT [--bind ADDRESS] [--home NAME]...

Every PROBE_INTERVAL_S seconds it runs dockingbird --json fleet probe, and
every HOME_INTERVAL_S seconds, for each --home NAME, dockingbird --home NAME
--json fleet scrape (the default home when no --home is given). It reads each
envelope's id and fields, never its lines (docs/reference/integration/json.md),
and serves GET /metrics: the probe's typed figures as dockingbird_host_*
gauges (never its display strings), dockingbird_probe_up (0 when the probe
fails or its schema is not PROBE_SCHEMA), each home's own text with one added
label, home="NAME", and dockingbird_scrape_up{home}, 1 when that home's last
read worked and 0 when it failed. Standard library only; it binds to loopback
unless --bind names an address.

Exit status: 0 after Ctrl-C; 2 for a usage error.
"""

import http.server
import json
import subprocess
import sys
import threading
import time
import typing

PROGRAM = "dockingbird"
JSON_OPTION = "--json"
HOME_OPTION = "--home"
BIND_OPTION = "--bind"
# The ids of the envelopes the exporter reads (docs/troubleshooting.md).
PROBE_ID = "FLEET_PROBE"
SCRAPE_ID = "FLEET_SCRAPE"
CATEGORIES_KEY, EXPOSITION_KEY = "categories", "exposition"  # the probe's kinds of process, the scrape's text
# The probe's schema this exporter reads; any other sets dockingbird_probe_up to 0.
PROBE_SCHEMA = "dockingbird.fleet.probe/1"
# HOST_FIGURES: each gauge's name after dockingbird_host_ and the dotted path of
# its number in the probe's fields. The screen's display strings ("68.5",
# "47%") are never exported; the typed numbers of the nested objects are.
HOST_FIGURES = {
    "cores": "cores", "load_one": "load.one", "load_line": "load.line",
    "cpu_busy_pct": "cpu.busy_pct", "idle_cores": "cpu.idle_cores",
    "memory_free_bytes": "memory.free_bytes", "memory_free_pct": "memory.free_pct",
    "swap_used_bytes": "swap.used_bytes", "gpu_device_pct": "gpu.device_pct",
    "docker_containers_running": "docker.containers_running",
    "docker_containers_total": "docker.containers_total", "disk_free_bytes": "disk.free_bytes",
}
HELP_HOST = "from the probe's --json fields"
# PROBE_INTERVAL_S (seconds): between two readings of the host.
PROBE_INTERVAL_S = 30
# HOME_INTERVAL_S (seconds): between two readings of one home.
HOME_INTERVAL_S = 60
# COMMAND_TIMEOUT_S (seconds): the probe stops itself after 60, so 30 more.
COMMAND_TIMEOUT_S = 90
DEFAULT_BIND = "127.0.0.1"
DEFAULT_HOME = "default"
METRICS_PATH = "/metrics"
CONTENT_TYPE = "text/plain; version=0.0.4; charset=utf-8"
HOST_PREFIX = "dockingbird_host_"
CATEGORY_PREFIX = "dockingbird_host_category_"
HTTP_OK, HTTP_NOT_FOUND = 200, 404
EXIT_DONE, EXIT_USAGE = 0, 2  # after Ctrl-C, after a usage error
PORT_MAX = 65535  # the highest TCP port

Families = dict[str, dict[str, list[str]]]


def read_fields(home: str | None, words: list[str], wanted: str) -> dict[str, typing.Any] | None:
    """Runs ``dockingbird [--home HOME] --json WORDS``; the fields of the
    envelope whose id is WANTED, or None when the command failed."""
    command = [PROGRAM, *([HOME_OPTION, home] if home else []), JSON_OPTION, *words]
    try:
        done = subprocess.run(command, capture_output=True, text=True, check=False,
                              stdin=subprocess.DEVNULL, timeout=COMMAND_TIMEOUT_S)
    except (OSError, subprocess.TimeoutExpired) as problem:
        print(f"{' '.join(command)}: {problem}", file=sys.stderr)
        return None
    for line in [*done.stdout.splitlines(), *done.stderr.splitlines()]:
        if line.startswith("{"):
            envelope = json.loads(line)
            if envelope.get("id") == wanted and envelope.get("exit_code") == 0:
                return envelope.get("fields") or {}
    print(f"{' '.join(command)}: no {wanted} envelope, exit {done.returncode}", file=sys.stderr)
    return None


def is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def quote(value: str) -> str:
    """A label value in the text format: backslash, quote and newline escaped."""
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def add_sample(families: Families, name: str, kind: str, help_text: str,
               labels: dict[str, str], value: float) -> None:
    entry = families.setdefault(
        name, {"meta": [f"# HELP {name} {help_text}", f"# TYPE {name} {kind}"], "samples": []}
    )
    pairs = ",".join(f'{key}="{quote(text)}"' for key, text in labels.items())
    entry["samples"].append(f"{name}{{{pairs}}} {value}" if pairs else f"{name} {value}")


def add_host(families: Families, fields: dict[str, typing.Any]) -> None:
    """The gauges of HOST_FIGURES, and per kind of process its count, memory in
    bytes and CPU in percent of one core; a figure it could not read is null."""
    for name, path in HOST_FIGURES.items():
        value: typing.Any = fields
        for key in path.split("."):
            value = value.get(key) if isinstance(value, dict) else None
        if is_number(value):
            add_sample(families, HOST_PREFIX + name, "gauge", HELP_HOST, {}, value)
    for envelope in fields.get(CATEGORIES_KEY) or []:
        row = envelope.get("fields") if isinstance(envelope, dict) else None
        if not isinstance(row, dict) or not isinstance(row.get("category"), str):
            continue
        cpu = str(row.get("cpu")).rstrip("%")
        figures = {"count": row.get("count"), "memory_bytes": row.get("memory_used"),
                   "cpu_pct": float(cpu) if cpu.replace(".", "", 1).isdigit() else None}
        for name, value in figures.items():
            if is_number(value):
                add_sample(families, CATEGORY_PREFIX + name, "gauge", HELP_HOST, {"category": row["category"]}, value)


def sample_name(line: str) -> str:
    ends = [line.index(mark) for mark in ("{", " ") if mark in line]
    return line[:min(ends, default=len(line))]


def add_label(line: str, home: str) -> str:
    """The sample line with home="HOME" first among its labels."""
    name = sample_name(line)
    rest = line[len(name):]
    label = f'home="{quote(home)}"'
    return f"{name}{{{label},{rest[1:]}" if rest.startswith("{") else f"{name}{{{label}}}{rest}"


def add_exposition(families: Families, home: str, lines: list[str]) -> None:
    """Merges a home's text into the page: each family's HELP and TYPE once,
    then every home's samples under it, so the page has one group a family."""
    for line in lines:
        if line.startswith(("# HELP ", "# TYPE ")):
            entry = families.setdefault(line.split(" ", 3)[2], {"meta": [], "samples": []})
            if line.split(" ", 2)[1] not in [m.split(" ", 2)[1] for m in entry["meta"]]:
                entry["meta"].append(line)
        elif line and not line.startswith("#"):
            entry = families.setdefault(sample_name(line), {"meta": [], "samples": []})
            entry["samples"].append(add_label(line, home))


class Readings:
    """The last reading of the host and of each home, shared by the threads."""

    def __init__(self, homes: list[str]) -> None:
        self.lock = threading.Lock()
        self.probe: dict[str, typing.Any] | None = None
        self.homes: dict[str, list[str] | None] = {home: None for home in homes}

    def page(self) -> str:
        families: Families = {}
        with self.lock:
            if self.probe is not None:
                add_host(families, self.probe)
            add_sample(families, "dockingbird_probe_up", "gauge", "1 when the last host read worked",
                       {}, int(self.probe is not None))
            for home, lines in self.homes.items():
                if lines is not None:
                    add_exposition(families, home, lines)
                add_sample(families, "dockingbird_scrape_up", "gauge",
                           "1 when the home's last read worked", {"home": home}, int(lines is not None))
        out = [line for entry in families.values() for line in (*entry["meta"], *entry["samples"])]
        return "\n".join(out) + "\n"


def probe_loop(readings: Readings) -> None:
    while True:
        fields = read_fields(None, ["fleet", "probe"], PROBE_ID)
        if fields is not None and fields.get("schema") != PROBE_SCHEMA:
            print(f"probe schema {fields.get('schema')}, not {PROBE_SCHEMA}", file=sys.stderr)
            fields = None
        with readings.lock:
            readings.probe = fields
        time.sleep(PROBE_INTERVAL_S)


def home_loop(readings: Readings, home: str) -> None:
    while True:
        fields = read_fields(None if home == DEFAULT_HOME else home, ["fleet", "scrape"], SCRAPE_ID)
        lines = (fields or {}).get(EXPOSITION_KEY)
        with readings.lock:
            readings.homes[home] = lines if isinstance(lines, list) else None
        time.sleep(HOME_INTERVAL_S)


def serve(readings: Readings, bind: str, port: int) -> None:
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            found = self.path.split("?")[0] == METRICS_PATH
            body = readings.page().encode("utf-8") if found else b"not found\n"
            self.send_response(HTTP_OK if found else HTTP_NOT_FOUND)
            self.send_header("Content-Type", CONTENT_TYPE if found else "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_: object) -> None:
            return None

    http.server.ThreadingHTTPServer((bind, port), Handler).serve_forever()


def fail() -> int:
    print(f"Usage: python3 exporter.py PORT [{BIND_OPTION} ADDRESS] [{HOME_OPTION} NAME]...", file=sys.stderr)
    return EXIT_USAGE


def main(argv: list[str]) -> int:
    port, bind, homes = None, DEFAULT_BIND, []
    words = iter(argv)
    for word in words:
        if word in (HOME_OPTION, BIND_OPTION):
            value = next(words, None)
            if value is None:
                return fail()
            if word == HOME_OPTION:
                homes.append(value)
            else:
                bind = value
        elif word.isdigit() and port is None and int(word) <= PORT_MAX:
            port = int(word)
        else:
            return fail()
    if port is None:
        return fail()
    readings = Readings(homes or [DEFAULT_HOME])
    threads = [threading.Thread(target=probe_loop, args=(readings,), daemon=True)]
    threads += [threading.Thread(target=home_loop, args=(readings, home), daemon=True) for home in readings.homes]
    for thread in threads:
        thread.start()
    try:
        serve(readings, bind, port)
    except KeyboardInterrupt:
        pass
    return EXIT_DONE


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
