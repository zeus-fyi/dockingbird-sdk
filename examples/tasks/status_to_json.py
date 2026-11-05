"""Print Dockingbird's status and every host's agents as one JSON document.

Usage: python3 examples/tasks/status_to_json.py

For a dashboard: it runs dockingbird --json status, dockingbird --json
fleet hosts, and dockingbird --json fleet agents for this computer and
then with --host NAME for each host the hosts file names, and prints one
JSON object on stdout:

    {"status": [...], "hosts": [...], "fleet": {"local": [...], "lab": [...]}}

each list holding every envelope a command printed, by its id, exit_code
and fields, never its lines (docs/reference/integration/json.md): "hosts" is fleet
hosts', so a hosts file Dockingbird refuses shows there, and a host that
could not be read has its refusal's envelope in its list, as fleet agents
gives it. A line that is no envelope goes to stderr. Standard library
only.

Exit status: 0; 1 when the status itself could not be read.
"""

import json
import subprocess
import sys
import typing

PROGRAM = "dockingbird"
JSON_OPTION = "--json"
HOST_OPTION = "--host"
LOCAL = "local"
# The ids of the envelopes the script reads (docs/troubleshooting.md).
HOST_LINE = "FLEET_HOSTS_ROW"
KEPT_KEYS = ("id", "exit_code", "fields")
ENVELOPE_START = "{"
# JSON_INDENT (spaces): the document's indentation, for a person reading it.
JSON_INDENT = 2

# The script's exit statuses: done, a problem it printed.
EXIT_DONE = 0
EXIT_PROBLEM = 1

Envelope = dict[str, typing.Any]


def envelopes(*words: str) -> tuple[int, list[Envelope]]:
    """Runs ``dockingbird --json WORDS``: its status and each envelope's
    kept keys, stdout's then stderr's; a line that is no envelope goes to
    stderr as it came, so nothing it said is lost."""
    done = subprocess.run(
        [PROGRAM, JSON_OPTION, *words],
        capture_output=True,
        text=True,
        check=False,
        stdin=subprocess.DEVNULL,
    )
    found = []
    for line in [*done.stdout.splitlines(), *done.stderr.splitlines()]:
        if line.startswith(ENVELOPE_START):
            envelope = json.loads(line)
            found.append({key: envelope.get(key) for key in KEPT_KEYS})
        else:
            print(line, file=sys.stderr)
    return done.returncode, found


def main() -> int:
    status, rows = envelopes("status")
    if status != EXIT_DONE:
        json.dump({"status": rows}, sys.stdout, indent=JSON_INDENT)
        print()
        return EXIT_PROBLEM
    _, listed = envelopes("fleet", "hosts")
    hosts = [row["fields"]["host"] for row in listed if row["id"] == HOST_LINE]
    _, local = envelopes("fleet", "agents")
    fleet = {LOCAL: local}
    for host in hosts:
        _, fleet[host] = envelopes("fleet", "agents", HOST_OPTION, host)
    document = {"status": rows, "hosts": listed, "fleet": fleet}
    json.dump(document, sys.stdout, indent=JSON_INDENT)
    print()
    return EXIT_DONE


if __name__ == "__main__":
    sys.exit(main())
