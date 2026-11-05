---
title: Lock the tools your agents run
summary: Pin Claude Code or Codex to one version, check what runs, and follow the latest release again.
audience: daily
commands:
  - pin
  - pin --clear
  - update
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Lock the tools your agents run

This cookbook pins Claude Code to version 2.1.285 so that every agent you start from now on runs it. It then moves a running agent onto the pin, shows that `update` leaves the pin alone, and lets Claude Code follow the latest release again. The same steps work for Codex. Each step ends with the line the product prints when the step worked.

## Before you start

- Dockingbird is set up. `dockingbird --version` prints a version.
- You know the version you want. Claude Code versions look like `2.1.285` and Codex versions like `0.162.1`.
- You know which agents run now. `dockingbird status` lists them. A pin never changes an agent that already runs.

## 1. Pin the version

```bash
dockingbird pin claude 2.1.285
```

`pin` writes one line into `versions.toml` in the home. The step is done when the product prints this line.

```text
Claude Code will run 2.1.285 from its next start; agents already running keep theirs.
```

For Codex, use `dockingbird pin codex 0.162.1`.

## 2. Check the pin

```bash
dockingbird --version
```

The step is done when the line for the tool says it is pinned.

```text
Claude Code 2.1.285 (pinned)
```

The next start downloads the version if it is not there yet, and shows `Getting Claude Code 2.1.285 ...` while it does. If the vendor has no such version, the start says so (`TOOL_PIN_NOT_FOUND`).

## 3. Move a running agent to the pin

A running agent keeps the version it started with. `dockingbird status claude-1` shows the version it runs. To move it, stop it and pick it up.

```bash
dockingbird stop claude-1
dockingbird claude --as claude-1
```

The pick-up resumes the agent's conversation. The step is done when `dockingbird status claude-1` shows the pinned version.

## 4. Update without losing the pin

```bash
dockingbird update
```

`update` fetches the latest of each tool you used, except a tool you pinned. A start or an update never changes a pinned version. Check that the pin held.

```bash
dockingbird --version
```

The step is done when the line still reads `Claude Code 2.1.285 (pinned)`.

## 5. Follow the latest again

```bash
dockingbird pin --clear claude
```

The step is done when the product prints this line.

```text
Claude Code follows the latest release from its next start.
```

`dockingbird pin claude latest` does the same. `dockingbird pin claude stable` follows Claude Code's slower channel, and Codex has no stable channel. Then fetch the latest now.

```bash
dockingbird update
```

The step is done when `update` names the tool.

```text
Got Claude Code 2.1.296.
```

It says `Claude Code 2.1.296 is the latest.` when you already have it. You can also edit `versions.toml` by hand: a line is `claude = "2.1.285"`, `codex = "0.162.1"`, `"latest"` or `"stable"`, and removing the line follows the latest. See [updates](../../docs/guides/updates.md).

## When it fails

Four messages can stop the steps above. Each one changes nothing on disk, so you can correct the command and run it again.

- Typing `2.1` or `v2.1.285` gets you [`PIN_INVALID_VERSION`](../../docs/troubleshooting.md#pin_invalid_version), because only a release number, `latest` or `stable` is accepted. `dockingbird pin codex stable` fails the same way, since Codex has no stable channel.
- Running `dockingbird pin` with a tool and no version prints [`PIN_ARGUMENTS_REQUIRED`](../../docs/troubleshooting.md#pin_arguments_required) and exits 2.
- A hand edit of `versions.toml` that leaves a line which is no version stops every command with [`TOOL_PIN_INVALID`](../../docs/troubleshooting.md#tool_pin_invalid). Fix the line or delete it.
- A pin the vendor never published gives [`TOOL_PIN_NOT_FOUND`](../../docs/troubleshooting.md#tool_pin_not_found). Correct the number, or delete the line to run the latest.
