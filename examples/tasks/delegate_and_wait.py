"""Hand an agent a task, wait for its answer, read it and save its files.

Usage: python3 examples/tasks/delegate_and_wait.py "TASK"

Run it in the repo the agent works on. It runs the commands a person would
type, each with --json (docs/reference/integration/json.md): dockingbird start "TASK",
then dockingbird wait NAME until the agent sends a message, dockingbird
read on that message, which prints its body, and dockingbird results NAME,
which saves the files the agent attached and prints where. It reads each
envelope's id and fields, never its lines. Standard library only.

Exit status: 0 when the agent answered; 1 when a command refused (its
message printed) or no answer came in time; 2 for a wrong command line.
"""

import json
import subprocess
import sys
import typing

PROGRAM = "dockingbird"
JSON_OPTION = "--json"
SECONDS_OPTION = "--seconds"
# WAIT_SECONDS (seconds): how long one dockingbird wait waits for a message
# before the script waits again (the command's own default is 25).
WAIT_SECONDS = 45
# WAIT_ROUNDS: how many waits in a row before the script gives up: half an
# hour at WAIT_SECONDS each.
WAIT_ROUNDS = 40

# The script's exit statuses, as Dockingbird's own: done, a problem it
# printed, a usage error.
EXIT_DONE = 0
EXIT_PROBLEM = 1
EXIT_USAGE = 2

# TASK_ARGUMENTS: the one argument, the task.
TASK_ARGUMENTS = 1
USAGE = 'usage: python3 delegate_and_wait.py "TASK"'
# The ids of the envelopes the script reads (docs/troubleshooting.md).
STARTED = "AGENT_STARTED_BUS"
DELIVERY = "WAIT_DELIVERY"
BODY_LINE = "READ_BODY_LINE"
SAVED = "RESULTS_WRITTEN"
ENVELOPE_START = "{"

Envelope = dict[str, typing.Any]


def run(*words: str) -> tuple[int, list[Envelope]]:
    """Runs ``dockingbird --json WORDS``: its status and its envelopes,
    stdout's then stderr's, one per JSON line; a line that is no envelope
    goes to stderr as it came, so nothing it said is lost."""
    done = subprocess.run(
        [PROGRAM, JSON_OPTION, *words],
        capture_output=True,
        text=True,
        check=False,
        stdin=subprocess.DEVNULL,
    )
    envelopes = []
    for line in [*done.stdout.splitlines(), *done.stderr.splitlines()]:
        if line.startswith(ENVELOPE_START):
            envelopes.append(json.loads(line))
        else:
            print(line, file=sys.stderr)
    return done.returncode, envelopes


def fields_of(envelopes: list[Envelope], message_id: str) -> list[Envelope]:
    """The fields of every envelope whose id is ``message_id``, in order."""
    return [
        envelope["fields"]
        for envelope in envelopes
        if envelope.get("id") == message_id
    ]


def refused(envelopes: list[Envelope], status: int) -> int:
    """Prints the lines of a command's problems (its envelopes that are not
    ok) on stderr; returns its status, or 1 when it ended 0."""
    for envelope in envelopes:
        if not envelope.get("ok"):
            print("\n".join(envelope.get("lines", [])), file=sys.stderr)
    return status or EXIT_PROBLEM


def body_of(envelopes: list[Envelope]) -> str:
    """A message's body from dockingbird --json read: each of its lines in
    pieces, a piece's ``continued`` saying the next goes on with it."""
    pieces = []
    for fields in fields_of(envelopes, BODY_LINE):
        pieces.append(fields["line"])
        if not fields.get("continued"):
            pieces.append("\n")
    return "".join(pieces)


def main(argv: list[str]) -> int:
    _, *words = argv
    if len(words) != TASK_ARGUMENTS:
        print(USAGE, file=sys.stderr)
        return EXIT_USAGE
    (task,) = words
    status, envelopes = run("start", task)
    started = fields_of(envelopes, STARTED)
    if not started:
        return refused(envelopes, status)
    *_, last = started
    name = last["name"]
    print(f"{name} started; waiting for its first message.")
    for _ in range(WAIT_ROUNDS):
        status, envelopes = run("wait", name, SECONDS_OPTION, str(WAIT_SECONDS))
        if status != EXIT_DONE:
            return refused(envelopes, status)
        deliveries = fields_of(envelopes, DELIVERY)
        if deliveries:
            break
    else:
        print(f"No message from {name} came in time.", file=sys.stderr)
        return EXIT_PROBLEM
    first, *_ = deliveries
    status, envelopes = run("read", first["delivery_id"])
    if status != EXIT_DONE:
        return refused(envelopes, status)
    print(body_of(envelopes), end="")
    status, envelopes = run("results", name)
    if status != EXIT_DONE:
        return refused(envelopes, status)
    for saved in fields_of(envelopes, SAVED):
        print(f"saved: {saved['where']}")
    return EXIT_DONE


if __name__ == "__main__":
    sys.exit(main(sys.argv))
