---
title: Support
summary: Where to ask a question and where to report a problem with Dockingbird.
audience: first-day
commands: ["dockingbird --version", "dockingbird status --json"]
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](llms.txt).

# Support

Two places take questions and problem reports.

| What you have | Where it goes |
|---|---|
| A question the docs do not answer | an issue on this repository, once it is public; until then, a reply to the email that carried your licence key |
| A problem on screen | the same place, with the three items below attached |

Attach these three things to a problem report. They hold numbers and names only, never your repository's content.

1. The version line: the output of `dockingbird --version`.
2. The message id: run the failing command again with `--verbose`, and copy the id shown with the message. Its entry in the [troubleshooting catalogue](docs/troubleshooting.md) says when it happens and the next step.
3. The status: the output of `dockingbird status --json`.

The channel named here is provisional until the repository goes public.
