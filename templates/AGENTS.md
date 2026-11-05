---
title: Rules for the agents in this repository
summary: A template AGENTS.md for your own repository, which every agent Dockingbird runs there reads after Dockingbird's own rules.
audience: first-day
commands:
  - dockingbird claude --agent-md
  - dockingbird codex --agent-md
  - dockingbird start --agent-md
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../llms.txt).

# Rules for the agents in this repository

<!--
Copy this file to the root of your repository as AGENTS.md. Delete the front matter, the line that starts with ">"
and this comment. Then fill in each part for your project. Claude Code and Codex read AGENTS.md when they start, and
so does every agent Dockingbird runs on your repository, after Dockingbird's own rules. To give one agent a different
file and leave your checkout as it is, start it with `dockingbird claude --agent-md FILE` (or `codex`, or `start`).
For each rule, say what the agent should do and which command shows that it did.
-->

## The project

What this repository builds, who it is for, and where its documents are, in one short paragraph.

## Before you change anything

- Read the documents the task names first, then the code it touches.
- Change only what the task asks for. Anything else you notice goes in your report, not in the code.
- Ask when the task is unclear instead of guessing: a question costs less than a wrong change.

## Build and test

- Set up: the command that installs the project's dependencies.
- Test: the command that runs the tests, and how to run only the ones a change touches.
- Check: the formatter, the linter and the type checker, each with its command.

Write the failing test first, then the change, then run the tests again. A test stays as it is: change the code
until it passes, and never skip, weaken or delete a test to get there.

## Code

- The style this repository follows, and where its guide is.
- Read secrets from the environment the project names, so none lands in code, logs, tests or commits.
- Keep each change small and each function about one thing.

## Commits

- Commit once per finished step. The message says what changed and why.
- Add new commits on top of shared history. Do not force push or rebase a shared branch.
- Your work reaches the repository's owner only as commits, and the owner reviews every one.

## When you are done

Say what you changed, what you ran to check it and what it printed, and what you could not check. You are done when
every check named under "Build and test" has run on your change and its output is in your report.
