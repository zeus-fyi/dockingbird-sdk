# Rules for the agents in this repository

<!--
A template: copy it to your repository's root as AGENTS.md and fill in each part in your own words; delete this
comment. Claude Code and Codex read AGENTS.md when they start, so every agent Dockingbird runs on this repository
reads it after Dockingbird's own rules. `dockingbird claude --agent-md FILE` (and `codex`, `start`) gives one agent
another file in its place, without touching your checkout.
-->

## The project

What this repository builds, for whom, and where its documents are (one short paragraph).

## Before you change anything

- Read the documents the task names first, then the code it touches.
- Change only what the task asks for. Anything else you notice goes in your report, not in the code.
- Ask when the task is unclear instead of guessing: a question costs less than a wrong change.

## Build and test

- Set up: the command that installs the project's dependencies.
- Test: the command that runs the tests, and how to run only the ones a change touches.
- Check: the formatter, the linter and the type checker, each with its command.

Write the failing test first, then the change, then run the tests again. Never skip, weaken or delete a test to make
it pass.

## Code

- The style this repository follows, and where its guide is.
- No secrets in code, logs, tests or commits: read them from the environment the project names.
- Keep each change small and each function about one thing.

## Commits

- One commit per finished step, its message saying what changed and why.
- Never rewrite history that others have: no force push, no rebase of a shared branch.
- Your commits reach the repository's owner as commits only, and the owner reviews each one.

## When you are done

Say what you changed, what you ran to check it and what it printed, and what you could not check.
