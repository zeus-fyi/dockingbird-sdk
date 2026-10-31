# Dockingbird quickstart

Dockingbird runs Claude Code and Codex side by side on your git repo, each in its own container, so they never overwrite each other or touch your Mac. Their work comes back to you as commits. You need an Apple silicon Mac (or arm64 Linux), Docker Desktop (it includes the buildx plugin; Docker Engine on Linux needs Docker's `docker-buildx-plugin` package) and uv.

## Install

```bash
UV_INDEX_ZEUSFYI_USERNAME=license UV_INDEX_ZEUSFYI_PASSWORD="$(pbpaste)" uv tool install dockingbird --index zeusfyi=https://license.zeusfyi.com/simple/
dockingbird license activate
```

No uv yet? `brew install uv`. With a license key, from Zeusfyi's release index: copy the key from your purchase email, then run the first line, which hands it to uv as the index's password without it reaching your shell's history. Then `dockingbird license activate` gives this computer its seat; from then on `dockingbird update` needs no key. `dockingbird completion --install` adds tab completion; open a new terminal for it. If `dockingbird` is not found afterwards, run `uv tool update-shell`, then open a new terminal. The first run sets everything up (downloads about 1 GB, once); the first start of each tool then fetches its latest release.

## First run

```bash
cd your-repo && dockingbird claude
```

Dockingbird checks your branch first: one holding files the agents don't take (a symlink leaving the repo, a submodule, a Git LFS file) is refused in seconds, each file named, before anything is set up. Then it sets itself up (about 5 minutes, the first time only), copies your branch for the agents and starts `claude-1`. Claude then signs in once, inside its container: open the link it shows on this Mac, sign in, and paste the code back. Codex works the same way with `dockingbird codex`: open its link and enter the one-time code. No Claude or ChatGPT account? Quit the sign-in, then use an API key: `dockingbird login claude --api-key` or `dockingbird login codex --api-key`. The repo's own settings, hooks and MCP servers load in the agent as they do outside Dockingbird, and Claude doesn't ask whether to trust `/work/your-repo`, its copy of this repo; for a repo you don't control, `dockingbird trust --off` in it keeps them off (the operator guide's "Trust" says what then changes). To leave it working, close this window: `claude-1` keeps going, and a bare `dockingbird claude` in that repo reconnects to it.

Run as many agents as you like, each in its own terminal, in as many repos as you like.

## Every day

```bash
dockingbird status    # who is working on what, and what needs you
dockingbird sync      # take the agents' commits, send them yours
dockingbird stop      # turn it all off; nothing is lost
```

- Agents start from your last commit, never from uncommitted edits, and their work reaches you only as commits, through `dockingbird sync`.
- `sync` never rewrites history. It keeps your uncommitted edits, and when both sides have new commits it offers to merge.
- Don't want an agent's commit? Undo it with a commit of your own: `git revert COMMIT`, then `dockingbird sync`. Resetting or deleting your branch doesn't remove it: the agents' copy keeps it.
- A one-shot works too: `dockingbird claude -p "Summarize the open TODOs"`.
- Every agent in one window: `dockingbird update` or `dockingbird ui --install` once, then `dockingbird ui`, mouse first; `ctrl+b q` leaves it, and every agent keeps working.
- Another computer's agents in the same window: `dockingbird fleet hosts set NAME --ssh DEST` (or `--gcloud VM --zone ZONE --project PROJECT`), then `dockingbird ui`; the operator guide's "Every agent on every host" has the rest.
- Sometimes: `dockingbird login claude` (sign in again), `dockingbird update` (the latest versions), `dockingbird clean` (free disk space).

Every command explains itself: `dockingbird -h`. When something goes wrong, the message says what to do next; all of them are in [troubleshooting](troubleshooting.md). The [operator guide](operator-guide.md) has the rest: sign-ins, API keys, what lives where, and the limits.

## Delegate

```bash
dockingbird start "Fix the flaky test"    # an agent works on it without a terminal
dockingbird wait claude-1                 # its next message, as it comes
dockingbird inbox                         # what waits for you, numbered
dockingbird read 1                        # one message, and the files it names
dockingbird search "closed issues"        # finds a message by its words
dockingbird send claude-1 "The new one"   # answers its question, or is a new task
dockingbird results claude-1              # saves the files it attached
dockingbird stop claude-1                 # stops it; its messages and results stay
```

The agent works in its own container on its own copy, as `dockingbird claude`'s agents do, and a question it asks you also leads `dockingbird status` until you answer it. A repo's own `.dockingbird/` configs add commands of their own: the operator guide's "Your own commands (configs)" explains them.

## Uninstall

```bash
dockingbird clean --all
uv tool uninstall dockingbird
```

Uninstalling first would leave Dockingbird's containers, volumes and image behind. `clean --all` keeps one empty folder, `~/.local/share/dockingbird/logs`, so a later start works while Docker Desktop still shares it; delete it after Docker Desktop restarts if you like.

Docker keeps the build cache of Dockingbird's image, shared with every other project's; `docker builder prune` frees all of it.
