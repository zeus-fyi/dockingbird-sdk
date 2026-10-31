# Dockingbird

**Reliable coordination for independent coding agents.** A Zeusfyi product.

Dockingbird runs Claude Code and Codex side by side on your git repo, each in its own container, so they never overwrite each other or touch your Mac. Their work comes back to you as commits. You need an Apple silicon Mac (or arm64 Linux), Docker Desktop (it includes the buildx plugin; Docker Engine on Linux needs Docker's `docker-buildx-plugin` package) and uv.

## Install

One line installs it (no [uv](https://docs.astral.sh/uv/) yet? `brew install uv`). With a license key, from Zeusfyi's release index: copy the key from your purchase email, then run this line, which hands it to uv as the index's password without it reaching your shell's history:

```bash
UV_INDEX_ZEUSFYI_USERNAME=license UV_INDEX_ZEUSFYI_PASSWORD="$(pbpaste)" uv tool install dockingbird --index zeusfyi=https://license.zeusfyi.com/simple/
```

Then `dockingbird license activate` gives this computer its seat; from then on `dockingbird update` needs no key. The index serves an active license only, so a trial can't install from it.

`dockingbird completion --install` for tab completion; open a new terminal. If `dockingbird` is not found afterwards, run `uv tool update-shell` and open a new terminal. Never a bare `uv tool install dockingbird`: that PyPI name is not ours. The first run downloads about 1 GB, once, and the first start of each tool fetches its latest release. The one-page walk-through is the [quickstart](docs/quickstart.md).

## Use it

```
Work        cd ~/code/myapp
            dockingbird claude                    Claude Code works on this repo
            dockingbird codex                     Codex too, in another terminal

Check       dockingbird status                    who is working on what

Take work   dockingbird sync                      take their commits, send yours

Sometimes   dockingbird login claude|codex        sign in again
            dockingbird login claude --api-key    or use an API key
            dockingbird update                    get the latest versions
            dockingbird clean                     free disk space
            dockingbird stop                      turn it all off; nothing is lost
            dockingbird egress                    see or choose what agents can reach

Delegate    dockingbird start "fix the flaky test"   an agent works on it without a terminal
            dockingbird start --terminal          or in this terminal
            dockingbird start --as claude-2 "more"   continue an agent that ended
            dockingbird wait claude-1             its next message, as it comes
            dockingbird inbox                     what waits for you, numbered
            dockingbird read 1                    one message and the files it names
            dockingbird send claude-1 "yes"       answer its question, or a new task
            dockingbird results claude-1          save the files it attached
            dockingbird watch claude-1            watch its browser, when its config asks for one

Configs     dockingbird config add agents/triage.toml   commands of your own, in every repo
            dockingbird config list               yours and this repo's (guide: "Your own commands")
            dockingbird trust --off               keep this repo's own settings off

Harbor      dockingbird harbor baseline           oracle must score 1, nop 0 (run it in the task folder)
            dockingbird harbor run -a claude-code one real trial with your own login
            dockingbird harbor jobs|results JOB   what ran, and each trial's reward
            dockingbird harbor clean [--all]      remove its jobs and leftovers; --all Harbor itself

License     dockingbird license activate          paste your key when asked; this computer takes a seat
            dockingbird license trial             or start this computer's trial
            dockingbird license status            the plan, its seats and the day it ends

Uninstall   dockingbird clean --all               remove everything it made
            uv tool uninstall dockingbird         then remove the command
```

There is nothing to configure. The first `dockingbird claude` checks the branch you are on (one holding files the agents don't take, such as a symlink leaving the repo, a submodule or a Git LFS file, is refused in seconds, each such file named, and nothing is set up), then builds the image, starts Dockingbird and copies the branch for the agents; each tool then uses the login already on your Mac (Claude Code's or Codex's own), or signs in once, with its own sign-in, inside Docker. Every agent works in its own container on its own copy, and its work reaches you only as commits, through `dockingbird sync`. To leave an agent working, close its window. Nothing on your Mac is mounted into an agent unless you connect a folder by name (read-only, unless a config gives it write access); with a scratch config you need no git repo at all. Your Mac's own Claude and Codex logins are read to follow them, a copy kept without the refresh token, and never written. Every command explains itself (`dockingbird -h`), and every message it prints is in [troubleshooting](docs/troubleshooting.md). The [operator guide](docs/operator-guide.md) covers the rest: sign-ins and API keys, update and clean, licensing (a seat is one computer running Dockingbird), what lives where (`DOCKINGBIRD_HOME`, by default `~/.local/share/dockingbird`, and the Docker volumes), and what stays open (egress among it).

Exit codes: 0 done, 1 a problem it printed with its next step, 2 usage; `claude` and `codex` exit with the tool's own status.

