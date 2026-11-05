---
title: Install
summary: Install the dockingbird command from Zeusfyi's release index with a license key, and check that it runs.
audience: first-day
commands:
  - uv tool install
  - dockingbird --version
  - uv tool update-shell
  - dockingbird completion --install
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Install

This page installs the `dockingbird` command from Zeusfyi's release index, checks that it runs, and adds tab completion.
Activation comes next, on the [activate](activate.md) page.

## Before you start

- The items on [prerequisites](prerequisites.md) pass their checks: `docker version`, `docker buildx version`, `uv --version` and `git --version`.
- Your license key is copied from your purchase email. A trial cannot install from the index, because the index serves an active license only.

## 1. Install on a Mac

Copy your key from the purchase email, then run the line below.
uv gets the key through its environment, so your shell history never holds it.
The record of the install keeps the index address and leaves the key out.

```bash
UV_INDEX_ZEUSFYI_USERNAME=license UV_INDEX_ZEUSFYI_PASSWORD="$(pbpaste)" uv tool install dockingbird --index zeusfyi=https://license.zeus.fyi/simple/
```

The index is named `zeusfyi`, and that name decides the variable names `UV_INDEX_ZEUSFYI_USERNAME` and `UV_INDEX_ZEUSFYI_PASSWORD`.
The user name is the word `license`, and the password is the key you copied.

Done when uv exits 0 and `dockingbird --version` finds the command (step 3).

## 2. Install on Linux

Linux has no `pbpaste`, so the key goes into a shell variable instead.
Run the first line, paste the key and press Enter. The terminal shows nothing while you paste.
The second line installs, and the third clears the variable.

```bash
read -rs UV_INDEX_ZEUSFYI_PASSWORD
UV_INDEX_ZEUSFYI_USERNAME=license UV_INDEX_ZEUSFYI_PASSWORD="$UV_INDEX_ZEUSFYI_PASSWORD" uv tool install dockingbird --index zeusfyi=https://license.zeus.fyi/simple/
unset UV_INDEX_ZEUSFYI_PASSWORD
```

Done when uv exits 0 and `unset` has run.

## 3. Check the install

```bash
dockingbird --version
```

The step is done when the command prints a line that starts with `dockingbird` and the version.

```text
dockingbird {version} (Claude Code {claude_code}, Codex {codex})
```

The two tool versions fill in after the first start, which downloads Claude Code and Codex.
[First run](first-run.md) covers that start.
If your shell reports that `dockingbird` is not found, run `uv tool update-shell` and open a new terminal.

## 4. Add tab completion

```bash
dockingbird completion --install
```

It writes the completion script for the shell that `$SHELL` names, or for the one you name (`zsh`, `bash` or `fish`).
The script goes into the `completion` folder of the Dockingbird home.
It also adds two lines to `~/.zshrc` or `~/.bashrc`, once however often you run it. One is a comment, and one loads the script.
For fish, the file `~/.config/fish/conf.d/dockingbird.fish` holds them.
`dockingbird update` keeps the script current.

Done when the command prints this, and you then open a new terminal.

```text
Installed tab completion for {shell}:
  {path}
  {rc} sources it
Open a new terminal.
```

A second run prints "Tab completion for {shell} was installed already; its script is current:" and the same two paths.
`dockingbird clean --all` removes the script but not the two lines. Delete them yourself if you like.

## A bare install is wrong

Never run `uv tool install dockingbird` without `--index`.
That name on PyPI is not this product, so a bare install puts a different program on your computer.
If you ran it, run `uv tool uninstall dockingbird`, then the install line for your platform.

## A failed install

The index serves an active license only.
A wrong key, a license that is not active, or a trial gives uv an authentication error, and no `dockingbird` command appears.
The error text is uv's own and is not a Dockingbird message, so it has no message id.
Copy the key from your purchase email again and run the install line again.

## When it fails

- [`COMPLETION_ALREADY`](../troubleshooting.md#completion_already) says completion was installed already and its script is current. Nothing is wrong.
- [`COMPLETION_SHELL_UNKNOWN`](../troubleshooting.md#completion_shell_unknown) means `$SHELL` names a shell Dockingbird has no completion for. Name one, as in `dockingbird completion --install zsh`.
- [`COMPLETION_RC_REFUSED`](../troubleshooting.md#completion_rc_refused) means Dockingbird could not write your shell's startup file. The script was written, and the startup file is unchanged.
