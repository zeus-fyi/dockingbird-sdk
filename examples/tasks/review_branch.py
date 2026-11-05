"""Review the branch you are on in one shot: dockingbird claude -p.

Usage: python3 examples/tasks/review_branch.py [BASE]

Run it in a checkout of the branch to review. It takes the branch's diff
against BASE (main unless given) with your own git, hands it to a one-shot
Claude agent, dockingbird --json claude -p, on its standard input, and
prints the agent's review: a one-shot prints only the tool's answer on
stdout, and Dockingbird's own lines come as envelopes on stderr
(docs/reference/integration/json.md), of which the script prints each problem's
lines, and any other line on stderr as it came. Standard library only.

Exit status: the one-shot's own (Claude's, once it started; 1 when
Dockingbird stopped before starting it); 1 when git could not give the
diff; 2 for a wrong command line.
"""

import json
import subprocess
import sys

PROGRAM = "dockingbird"
JSON_OPTION = "--json"
GIT = "git"
DEFAULT_BASE = "main"
# MOST_ARGUMENTS: the one optional argument, the base branch.
MOST_ARGUMENTS = 1

# The script's exit statuses, as Dockingbird's own: done, a problem it
# printed, a usage error.
EXIT_DONE = 0
EXIT_PROBLEM = 1
EXIT_USAGE = 2

USAGE = "usage: python3 review_branch.py [BASE]"
ENVELOPE_START = "{"
PROMPT = (
    "Review the diff on your standard input: the changes this branch makes"
    " against {base}. List what to fix, file by file, most important first,"
    " and say what is fine. Change nothing."
)


def diff_against(base: str) -> subprocess.CompletedProcess[str]:
    """``git diff BASE...HEAD``: what the branch changed since it left
    ``base``."""
    return subprocess.run(
        [GIT, "diff", f"{base}...HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )


def problems(stderr: str) -> list[str]:
    """What stderr said: the lines of each envelope that is not ok, and
    each line that is no envelope, as it came."""
    lines = []
    for line in stderr.splitlines():
        if not line.startswith(ENVELOPE_START):
            lines.append(line)
            continue
        envelope = json.loads(line)
        if not envelope.get("ok"):
            lines.extend(envelope.get("lines", []))
    return lines


def main(argv: list[str]) -> int:
    _, *words = argv
    if len(words) > MOST_ARGUMENTS:
        print(USAGE, file=sys.stderr)
        return EXIT_USAGE
    base, *_ = words or [DEFAULT_BASE]
    diff = diff_against(base)
    if diff.returncode != EXIT_DONE:
        print(diff.stderr, end="", file=sys.stderr)
        return EXIT_PROBLEM
    if not diff.stdout:
        print(f"This branch changes nothing against {base}.")
        return EXIT_DONE
    review = subprocess.run(
        [PROGRAM, JSON_OPTION, "claude", "-p", PROMPT.format(base=base)],
        input=diff.stdout,
        capture_output=True,
        text=True,
        check=False,
    )
    print(review.stdout, end="")
    for line in problems(review.stderr):
        print(line, file=sys.stderr)
    return review.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv))
