# Troubleshooting

Find your message: search this page for a few of its words, leaving out
names, numbers and paths, which show here as values in braces. Each entry
says when the message appears, what it says, the next step it gives and its
exit status. A value in braces, such as `{repo}`, is filled in when the
message prints: `{name}` is an agent's name, `{tool}` is claude or codex
and `{harness}` Claude or Codex, `{subcommand}` is the command that picks
an agent up as it ran (its config's command, such as notes, with
--terminal for one that ran at a terminal; else claude or codex, or start
for one that worked without a terminal) and `{config_command}` that
config's command alone, `{repo}` and `{branch}` are your repo and branch,
and `{checkout}` is its folder; `{count:commit|commits}` is a number with
its noun, a list such as `{names:and}` is filled in with its entries, and
`{names:first}` with the first one. The messages are grouped by what you
were doing.

With `--verbose`, every message also shows its ID, which is its heading here.
With `--json`, each message is one line of JSON with the same exit status.

Exit statuses: 0 done, 1 a problem Dockingbird printed (with its next step),
2 usage. `dockingbird claude` and `dockingbird codex` exit with the tool's own
status once it has started. The native commands (`dockingbird native ...`)
have their own messages and exit codes, in the
[operator guide](operator-guide.md).

<!-- This page is generated from src/dockingbird/hostcli/messages.py and
src/dockingbird_devtools/troubleshooting_when.py by
python3 tests/spec/check_documents.py --write. Never edit it by hand. -->

## Typing a command

### UNKNOWN_COMMAND

When: You typed a word where a command goes, and it isn't one of Dockingbird's commands. When it is close to one, the message suggests it. When the word is the removed command of an agent you named with `--as`, Dockingbird says instead that the agent waits until a config gives the command again.

```text
dockingbird: '{word}' is not a command.
See: dockingbird -h
```

Or:

```text
dockingbird: '{word}' is not a command. Did you mean '{suggestion}'?
See: dockingbird -h
```

Next step: dockingbird -h

Exit status: 2 (usage).

### ENV_NAME_UNKNOWN

When: A variable in your shell starts with Dockingbird's prefix but isn't a setting any Dockingbird command reads: a retired or misspelled name, or one spelled with a character outside plain ASCII. Dockingbird stops rather than ignore it. Test switches and the names Dockingbird's own commands read pass.

```text
{names} isn't a setting Dockingbird reads, so it would be ignored.
Unset it, or fix its spelling, then run this again.
```

Or:

```text
{names} aren't settings Dockingbird reads, so they would be ignored.
Unset them, or fix their spelling, then run this again.
```

Next step, as the message gives it:

- Unset it, or fix its spelling, then run this again.
- Unset them, or fix their spelling, then run this again.

Exit status: 2 (usage).

### SETTING_REFUSED

When: A setting in your shell (a variable with Dockingbird's prefix) can't be given to Dockingbird's containers as it stands, so the command stops before it runs rather than ignore it: its value isn't a whole number within the setting's range, two or more values break a rule between settings, its name is spelled in another case than upper case, or it is a setting of Dockingbird outside Docker (the database's address and roles, the developer's role switch and the host git's path), which Docker mode never uses.

```text
{names} must be a whole number from {low} to {high}.
Set a value in that range, or unset the variable, then run this again.
```

Or:

```text
{names:and} must each be a whole number within its own range.
Set each a value in its range, or unset the variables, then run this again.
```

Or:

```text
{names:and} would break a rule between Dockingbird's settings as they are set now.
Change or unset the settings named, then run this again.
```

Or:

```text
Dockingbird would not read {names:and}: a setting's name is spelled in upper case.
Spell each name in upper case, then run this again.
```

Or:

```text
Docker mode has no use for {names:and}: the value would be ignored.
Unset each variable named, then run this again.
```

Next step, as the message gives it:

- Set a value in that range, or unset the variable, then run this again.
- Set each a value in its range, or unset the variables, then run this again.
- Change or unset the settings named, then run this again.
- Spell each name in upper case, then run this again.
- Unset each variable named, then run this again.

Exit status: 2 (usage).

### NATIVE_ALIAS_HINT

When: You typed `init`, `doctor` or `state`, names of the low-level commands, which now live under `dockingbird native`. The message says what to type instead.

```text
dockingbird {command} is a low-level command now (dockingbird native -h).
Nothing needs setting up: cd into a repo, then dockingbird claude.
```

Or:

```text
dockingbird {command} is a low-level command now (dockingbird native -h).
To see how Dockingbird is doing: dockingbird status
```

Or:

```text
dockingbird {command} is a low-level command now (dockingbird native -h).
To see who is working on what: dockingbird status
```

Or:

```text
dockingbird {command} is a low-level command now (dockingbird native -h).
To start an agent: cd into a repo, then dockingbird claude.
```

Next step, as the message gives it:

- cd into a repo, then dockingbird claude
- dockingbird status

Exit status: 2 (usage).

### UNKNOWN_OPTION

When: You gave an option the command doesn't have. When it is close to one, the message suggests it; for `stop`, it says how to stop everything.

```text
dockingbird: '{word}' is not an option.
See: dockingbird -h
```

Or:

```text
dockingbird: '{word}' is not an option. Did you mean '{suggestion}'?
See: dockingbird -h
```

Or:

```text
dockingbird {command}: '{word}' is not an option.
See: dockingbird {command} -h
```

Or:

```text
dockingbird {command}: '{word}' is not an option. Did you mean '{suggestion}'?
See: dockingbird {command} -h
```

Or:

```text
dockingbird {command}: '{word}' is not an option. To stop everything: dockingbird stop
```

Next step, as the message gives it:

- dockingbird -h
- dockingbird {command} -h
- dockingbird stop

Exit status: 2 (usage).

### MISSING_VALUE

When: You gave an option without the value it needs.

```text
dockingbird: {option} needs a {value}.
See: dockingbird -h
```

Or:

```text
dockingbird {command}: {option} needs a {value}.
See: dockingbird {command} -h
```

Next step, as the message gives it:

- dockingbird -h
- dockingbird {command} -h

Exit status: 2 (usage).

### MISSING_ARGUMENT

When: You ran a command without the choice it needs, such as `dockingbird login` with no tool.

```text
dockingbird {command} needs one of: {choices}.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### UNKNOWN_CHOICE

When: You gave a choice the command doesn't have. When it is close to one, the message suggests it.

```text
dockingbird {command}: '{word}' is not one of: {choices}.
See: dockingbird {command} -h
```

Or:

```text
dockingbird {command}: '{word}' is not one of: {choices}. Did you mean '{suggestion}'?
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### UNEXPECTED_ARGUMENT

When: You gave the command a word it has no place for.

```text
dockingbird {command}: '{word}' was not expected here.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### OPTION_NEEDS_OPTION

When: You gave an option that only works together with another one.

```text
dockingbird {command}: {option} works only with {requires}.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### OPTIONS_NOT_BOTH

When: You gave two options that don't go together, such as a start's `--bus` with `--terminal`, or `dockingbird inbox --clear` with another inbox option. Nothing ran; keep the one you mean.

```text
dockingbird {command}: use either {option} or {other}, not both.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### OPTION_GIVEN_TWICE

When: You gave `--agent-md` or `--claude-md` twice on one command. Each takes one file; give it once.

```text
dockingbird {command}: give {option} once.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### VERSION

When: You ran `dockingbird --version` (or `-v`): Dockingbird's version, the commit it was installed from (or that it came from a local checkout, when you installed it from a folder), and the versions of Claude Code and Codex it runs.

```text
dockingbird {version} (Claude Code {claude_code}, Codex {codex})
```

Or:

```text
dockingbird {version} at commit {commit} (Claude Code {claude_code}, Codex {codex})
```

Or:

```text
dockingbird {version} from a local checkout (Claude Code {claude_code}, Codex {codex})
```

Next step: none; it only informs.

Exit status: 0 (done).

### NOT_BUILT_YET

When: You ran a command this version doesn't have yet, or the MCP server was asked to start an agent at a terminal: it starts agents without one.

```text
dockingbird {command} is not built yet.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### INTERNAL_ERROR

When: Something went wrong that Dockingbird has no words for. It printed no traceback; when it could, it wrote the details to its log, which the message names, so you can report it. When the log could not be written either (a full disk, for one), the first line names the kind of error in parentheses, for example `docker failed` or `OSError ENOSPC`.

```text
dockingbird {command}: an unexpected error stopped it.
Details are in {log}
Please report it: https://github.com/zeus-fyi/dockingbird/issues
```

Or:

```text
dockingbird {command}: an unexpected error stopped it.
Please report it: https://github.com/zeus-fyi/dockingbird/issues
```

Or:

```text
dockingbird {command}: an unexpected error stopped it ({failure}).
It could not be written to the log.
Please report it: https://github.com/zeus-fyi/dockingbird/issues
```

Next step: https://github.com/zeus-fyi/dockingbird/issues

Exit status: 1 (a problem Dockingbird printed).

## Docker, platform and setup

### DOCKER_NOT_RUNNING

When: Docker isn't running, and didn't start in time. Nothing was set up or started.

```text
Docker isn't running. Start Docker Desktop, then run this again.
```

Or:

```text
Docker isn't running. Start Docker, then run this again.
```

Next step, as the message gives it:

- Start Docker Desktop, then run this again.
- Start Docker, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### DOCKER_ANSWERING_SLOWLY

When: Docker is running but answers too slowly, as on a Mac too busy for it or a Docker Desktop in trouble. Nothing was built.

```text
Docker is answering slowly. Check Docker Desktop, then run this again.
```

Or:

```text
Docker is answering slowly. Check Docker, then run this again.
```

Next step, as the message gives it:

- Check Docker Desktop, then run this again.
- Check Docker, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### DOCKER_STARTING

When: Docker Desktop wasn't running, so Dockingbird started it. The line shows while it starts, then how long it took.

```text
Starting Docker Desktop ... ready ({elapsed})
```

Or:

```text
Starting Docker Desktop ...
```

Next step: none; it only informs.

Exit status: 0 (done).

### DOCKER_WAKING

When: Docker Desktop was asleep (its Resource Saver stops it when idle) or still starting, so Dockingbird waits for it to answer.

```text
Waking Docker ... ready ({elapsed})
```

Or:

```text
Waking Docker ...
```

Next step: none; it only informs.

Exit status: 0 (done).

### DOCKER_NOT_ANSWERING

When: Docker took a request and never answered: it is stuck, not off. Nothing was started.

```text
Docker isn't answering. Restart Docker Desktop, then run this again.
```

Or:

```text
Docker isn't answering. Restart Docker, then run this again.
```

Next step, as the message gives it:

- Restart Docker Desktop, then run this again.
- Restart Docker, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### DOCKER_NOT_INSTALLED

When: There is no `docker` command on this computer. Dockingbird needs Docker Desktop on a Mac, or Docker on Linux.

```text
Dockingbird needs Docker Desktop. Install it, then run this again:
  https://www.docker.com/products/docker-desktop/
```

Or:

```text
Dockingbird needs Docker. Install it, then run this again:
  https://docs.docker.com/engine/install/
```

Next step, as the message gives it:

- https://www.docker.com/products/docker-desktop/
- https://docs.docker.com/engine/install/

Exit status: 1 (a problem Dockingbird printed).

### DOCKER_UNSTARTED

When: There is a `docker` command on this computer, but it couldn't be run: the file is being replaced (Docker Desktop updating itself), it was removed, or the computer has no process or open file left for it. The message shows what the computer said. Nothing was started.

```text
The docker command couldn't be run. This computer said:
  {said}
Check the Docker install, then run this again.
```

Next step: Check the Docker install, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### DOCKER_BUILDX_MISSING

When: Dockingbird was about to build itself (during the set-up, or the rebuild that finishes an update), and Docker has no buildx plugin, which runs that build. Nothing was built. Docker Desktop includes the plugin; on Linux, Docker's `docker-buildx-plugin` package adds it.

```text
Docker's buildx plugin isn't available, and Dockingbird needs it.
Install or update Docker Desktop (it includes buildx), then run this again:
  https://www.docker.com/products/docker-desktop/
```

Or:

```text
Docker's buildx plugin isn't available, and Dockingbird needs it.
Install the docker-buildx-plugin package, then run this again:
  https://docs.docker.com/engine/install/
```

Next step, as the message gives it:

- https://www.docker.com/products/docker-desktop/
- https://docs.docker.com/engine/install/

Exit status: 1 (a problem Dockingbird printed).

### NOT_APPLE_SILICON

When: This computer is neither an Apple silicon Mac nor arm64 Linux, the two Dockingbird runs on for now.

```text
Dockingbird runs on Apple silicon Macs and arm64 Linux for now.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### SETTING_UP

When: The first command that needs Dockingbird to be set up, usually `dockingbird claude` or `dockingbird login`, sets it up, once. The line shows how far it has got and about how long is left, or that another terminal is setting it up and this one waits. When the output goes to a pipe or a file, the heading prints at once and a "still setting up" line follows once a minute while it runs, with the step, the time so far or how long the build has been quiet.

```text
Setting up Dockingbird, first time only ... done ({elapsed})
```

Or:

```text
Setting up Dockingbird, first time only  {bar}  about {left} left
```

Or:

```text
Setting up Dockingbird  {bar}  first time: about {estimate}
```

Or:

```text
Setting up Dockingbird  waking Docker ...
```

Or:

```text
Setting up Dockingbird  {bar}  no progress for {quiet}
```

Or:

```text
Setting up Dockingbird, first time only (about {estimate}):
```

Or:

```text
{bar}  about {left} left
```

Or:

```text
{bar}  about {estimate}
```

Or:

```text
waking Docker ...
```

Or:

```text
{bar}  no progress for {quiet}
```

Or:

```text
Dockingbird is being set up in another terminal; waiting ... done
```

Or:

```text
Dockingbird is being set up in another terminal; waiting ...
```

Or:

```text
  still setting up: step {index} of {count}, {elapsed} so far
```

Or:

```text
  still setting up: downloading the base system, {elapsed} so far
```

Or:

```text
  still setting up: step {index} of {count}, no output for {quiet}
```

Or:

```text
  waking Docker ...
```

Or:

```text
  still setting up: preparing the build, {elapsed} so far
```

Next step: none; it only informs.

Exit status: 0 (done).

### BUILD_QUIET

When: The set-up (or an update's rebuild) has printed nothing for a while. The note names the step it is on, often a download, and how long it has been quiet.

```text
Step {index} of {count} is quiet ({quiet}). Still waiting.
```

Or:

```text
Downloading {download} is quiet ({quiet}). Still waiting.
```

Or:

```text
Downloading the base system is quiet ({quiet}). Still waiting.
```

Or:

```text
Docker hasn't started the build yet ({quiet}). Still waiting.
```

Next step: none; it only informs.

Exit status: 0 (done).

### BUILD_QUIET_CHECK

When: The set-up has been quiet for several minutes, so a slow network or a stuck Docker is likely.

```text
Check your connection or Docker Desktop.
```

Or:

```text
Check your connection or Docker.
```

Next step, as the message gives it:

- Check your connection or Docker Desktop.
- Check your connection or Docker.

Exit status: 0 (done).

### SETUP_INTERRUPTED

When: You pressed Ctrl-C during the set-up. The build stopped and nothing was set up.

```text
Set-up didn't finish. Nothing changed. Run this again.
```

Next step: Run this again.

Exit status: 1 (a problem Dockingbird printed).

### IMAGE_BUILD_FAILED

When: Setting up Dockingbird failed. The message names the step, and `--verbose` shows Docker's own output.

```text
Setting up Dockingbird didn't work, at this step: {step}
To see why, run this again with --verbose.
```

Next step: To see why, run this again with --verbose.

Exit status: 1 (a problem Dockingbird printed).

### DOCKER_STOPPED_ANSWERING

When: Docker took the build but never started it, twice: Docker Desktop may be paused or still starting, or the base system couldn't be downloaded.

```text
Docker didn't start the build. Docker Desktop may be paused or still
starting, or the base system couldn't be downloaded.
Check Docker Desktop and your network, then run this again.
```

Or:

```text
Docker didn't start the build. Docker may be restarting, or the base
system couldn't be downloaded.
Check Docker and your network, then run this again.
```

Next step, as the message gives it:

- Check Docker Desktop and your network, then run this again.
- Check Docker and your network, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### IMAGE_SOURCE_UNAVAILABLE

When: This install of Dockingbird is missing the files it sets up from. Installing it again fixes it.

```text
This Dockingbird install is missing the files it sets up from.
Install it again. For example, from GitHub:
  uv tool install --force --from \
    git+https://github.com/zeus-fyi/dockingbird dockingbird
```

Next step: Install it again.

Exit status: 1 (a problem Dockingbird printed).

### DOCKINGBIRD_STARTING

When: Dockingbird had stopped (it stops when idle, or after a restart) and is starting again. The line shows only when that takes a moment, or while another terminal starts it.

```text
Starting Dockingbird ... ready ({elapsed})
```

Or:

```text
Starting Dockingbird ...
```

Or:

```text
Starting Dockingbird after the restart ... ready
```

Or:

```text
Starting Dockingbird after the restart ...
```

Or:

```text
Dockingbird is starting in another terminal; waiting ...
```

Next step: none; it only informs.

Exit status: 0 (done).

### COORDINATOR_UNHEALTHY

When: Dockingbird's container started but didn't report ready. The message names its log, or, when it never ran, what Docker said.

```text
Dockingbird didn't start properly. Run this again.
If it keeps happening, its log says why:
  {log}
```

Or:

```text
Dockingbird didn't start properly. Docker said:
  {said}
Restart Docker Desktop, then run this again.
```

Or:

```text
Dockingbird didn't start properly. Docker said:
  {said}
Restart Docker, then run this again.
```

Next step, as the message gives it:

- Run this again.
- Restart Docker Desktop, then run this again.
- Restart Docker, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### HOME_SETUP_TOOK_TOO_LONG

When: Dockingbird sets up each tool's home the first time it starts, and this took longer than Dockingbird waits, usually because the computer was busy. The next run sets it up again. When Docker couldn't remove the step's container, the message names it.

```text
Setting up {harness}'s home took longer than {bound}, so Dockingbird stopped it.
Run this again when this computer is less busy.
```

Or:

```text
Setting up {harness}'s home took longer than {bound}.
Dockingbird couldn't stop its container {container}.
Run this again when this computer is less busy.
```

Next step: Run this again when this computer is less busy.

Exit status: 1 (a problem Dockingbird printed).

### STEP_TOOK_TOO_LONG

When: One of the steps Dockingbird asks Docker for while it sets itself up or starts, or starts an agent, took longer than Dockingbird waits, usually because the computer was busy. The message names the step; the next run picks up what Docker finished meanwhile. When the step was sending an agent its task, the agent is running and the task may have reached it: `dockingbird status NAME` shows what it works on.

```text
Checking Dockingbird's setup took longer than {bound},
so Dockingbird stopped waiting.
Run this again when this computer is less busy.
```

Or:

```text
Preparing Dockingbird's storage took longer than {bound},
so Dockingbird stopped waiting.
Run this again when this computer is less busy.
```

Or:

```text
Starting Dockingbird took longer than {bound},
so Dockingbird stopped waiting.
Run this again when this computer is less busy.
```

Or:

```text
Listing Dockingbird's containers took longer than {bound},
so Dockingbird stopped waiting.
Run this again when this computer is less busy.
```

Or:

```text
Connecting to Dockingbird took longer than {bound},
so Dockingbird stopped waiting.
Run this again when this computer is less busy.
```

Or:

```text
Starting {repo}'s toolchain install took longer than {bound},
so Dockingbird stopped waiting.
Run this again when this computer is less busy.
```

Or:

```text
{name} started, but sending it the task took longer than {bound},
so Dockingbird stopped waiting. The task may or may not have reached it.
To find out: dockingbird status {name}
```

Or:

```text
Making {name}'s network took longer than {bound},
so Dockingbird stopped waiting.
Run this again when this computer is less busy.
```

Or:

```text
Making {name}'s container took longer than {bound},
so Dockingbird stopped waiting.
Run this again when this computer is less busy.
```

Or:

```text
Starting {name}'s container took longer than {bound},
so Dockingbird stopped waiting.
Run this again when this computer is less busy.
```

Or:

```text
Starting {name}'s egress proxy took longer than {bound},
so Dockingbird stopped waiting.
Run this again when this computer is less busy.
```

Or:

```text
Starting {name}'s browser took longer than {bound},
so Dockingbird stopped waiting.
Run this again when this computer is less busy.
```

Or:

```text
Making {name}'s dependency cache took longer than {bound},
so Dockingbird stopped waiting.
Run this again when this computer is less busy.
```

Or:

```text
Checking Docker Model Runner took longer than {bound},
so Dockingbird stopped waiting.
Run this again when this computer is less busy.
```

Next step, as the message gives it:

- Run this again when this computer is less busy.
- dockingbird status {name}

Exit status: 1 (a problem Dockingbird printed).

### LOGS_NOT_VISIBLE

When: Docker Desktop can't see Dockingbird's log folder, though it is there. This happens after the folder was deleted and made again, until Docker Desktop restarts.

```text
Docker Desktop can't see {folder}, so Dockingbird couldn't start.
Restart Docker Desktop, then run this again.
```

Or:

```text
Docker can't see {folder}, so Dockingbird couldn't start.
Restart Docker, then run this again.
```

Next step, as the message gives it:

- Restart Docker Desktop, then run this again.
- Restart Docker, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### COORDINATOR_ROLLED_BACK

When: An update's new version didn't start, so the version you had is running again. The reason follows.

```text
The update to {version} didn't start, so Dockingbird {old} is running again.
```

Next step: none; it only informs.

Exit status: 0 (done).

### VERSION_MISMATCH

When: The `dockingbird` command you ran is older than the Dockingbird that is running, so it won't talk to it. `dockingbird status NAME` says this too, since its own record can't answer for the agent.

```text
Dockingbird {running} is running, and this dockingbird is the older {version}.
Use the newer one, or update this one: dockingbird update
```

Next step: dockingbird update

Exit status: 1 (a problem Dockingbird printed).

### SETTINGS_CHANGED

When: Dockingbird was started with other settings (the variables with its prefix in that shell) than this terminal gives now, and a running Dockingbird keeps the settings it started with. No command restarts it on its own: stop it, then run the command again, and it starts with this terminal's settings. `dockingbird status` shows the same lines under "Needs your attention".

```text
Dockingbird is running with other settings than this terminal's.
Stop it, then run this again: dockingbird stop
```

Or:

```text
Dockingbird is running with other settings than this terminal's.
{name} is still working.
Let it finish or stop it, then run this again: dockingbird stop
```

Or:

```text
Dockingbird is running with other settings than this terminal's.
{names:and} are still working.
Let them finish or stop them, then run this again: dockingbird stop
```

Next step: dockingbird stop

Exit status: 1 (a problem Dockingbird printed).

### STATE_NEWER

When: A newer Dockingbird last wrote the files Dockingbird keeps for you (`state.json` in its folder), and the `dockingbird` command you ran is older, so it reads them but won't change them. Update it, or run the newer one.

```text
Dockingbird's files were written by a newer Dockingbird.
Run dockingbird update, or use that version.
```

Next step: dockingbird update

Exit status: 1 (a problem Dockingbird printed).

### STATE_FILE_REFUSED

When: Dockingbird keeps its records of your agents, sign-ins and kept copies in `state.json` in its folder, and reads that file only when it is a plain file within its size limit. The file is over the limit, or is a link, a folder or a file Dockingbird can't open; or the change the command would make would take it past the limit. Rather than write over what it can't read, Dockingbird changed nothing. `dockingbird status` shows the same lines under "Needs your attention".

```text
Dockingbird's state file is {size_bytes:byte|bytes}, past its limit of {limit_bytes:byte|bytes}:
  {path}
Nothing changed.
```

Or:

```text
Dockingbird can't read its state file whole.
It is a link, a folder or a file Dockingbird can't open:
  {path}
Nothing changed.
```

Or:

```text
This change would take Dockingbird's state file to {size_bytes:byte|bytes}, past its limit of {limit_bytes:byte|bytes}:
  {path}
Nothing changed.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### STATE_FILE_NOT_UPDATED

When: A command did what you asked, but the record of it couldn't go into `state.json`: the file is over its size limit, a link, a folder or a file Dockingbird can't open, or this record would have taken it past the limit. What the command did stands; Dockingbird left the file as it was.

```text
Dockingbird's state file is {size_bytes:byte|bytes}, past its limit of {limit_bytes:byte|bytes},
so this wasn't recorded in it:
  {path}
```

Or:

```text
Dockingbird can't read its state file whole, so this wasn't recorded in it:
  {path}
```

Or:

```text
Recording this would take Dockingbird's state file to {size_bytes:byte|bytes},
past its limit of {limit_bytes:byte|bytes}, so it wasn't recorded:
  {path}
```

Next step: none; it only informs.

Exit status: 0 (done) or 1 (a problem Dockingbird printed), as "When:" says.

### HOME_NOT_SHARED

When: Docker Desktop doesn't share the folder Dockingbird keeps its files in, so its container can't use it.

```text
Docker Desktop isn't sharing {folder} with Dockingbird.
Add it in Docker Desktop > Settings > Resources > File sharing,
then run this again.
```

Next step: Add it in Docker Desktop > Settings > Resources > File sharing, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### HOME_IS_NATIVE

When: `DOCKINGBIRD_HOME` points at a folder a native-mode Dockingbird uses, which Docker mode can't share.

```text
{folder} is a native Dockingbird folder, so Docker mode can't use it.
Point DOCKINGBIRD_HOME at another folder, then run this again.
```

Next step: Point DOCKINGBIRD_HOME at another folder, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### HOME_UNSAFE

When: `DOCKINGBIRD_HOME` isn't a full path, points through a link or at someone else's folder, or has a character Docker can't take in a path. `dockingbird sync` also stops, before it takes anything, when that folder or its `tmp` folder is a link, someone else's or open to other users' writes.

```text
DOCKINGBIRD_HOME isn't safe to use. It must be a full path to a folder that
is yours and not a link, with no commas, quotes, backslashes or = in it.
Point DOCKINGBIRD_HOME at another folder, then run this again.
```

Next step: Point DOCKINGBIRD_HOME at another folder, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### HOME_NOT_EMPTY

When: The folder Dockingbird would keep its files in already has files it didn't make, so it leaves it alone. The message lists what it found. Your own `instructions` and `vaults` folders, your `versions.toml`, `config.toml`, `browser-solver.json`, `hosts.toml` and `fleet.toml`, the hidden file Finder leaves in a folder it has shown, and the empty `logs` folder `dockingbird clean --all` keeps don't count: a folder holding only those is used.

```text
{folder} already has files Dockingbird didn't make, so it won't use it.
In it: {names:and}.
Unset DOCKINGBIRD_HOME, or point it at an empty or new folder,
then run this again.
```

Or:

```text
{folder} already has something Dockingbird didn't make, so it won't use it.
In it: {names:and}.
Unset DOCKINGBIRD_HOME, or point it at an empty or new folder,
then run this again.
```

Or:

```text
{folder} already has files Dockingbird didn't make, so it won't use it.
In it: {names:and}.
Move those files out of it (your own rules can stay in instructions/),
or set DOCKINGBIRD_HOME to an empty or new folder, then run this again.
```

Or:

```text
{folder} already has something Dockingbird didn't make, so it won't use it.
In it: {names:and}.
Move it out (your own rules can stay in instructions/),
or set DOCKINGBIRD_HOME to an empty or new folder, then run this again.
```

Or:

```text
{folder} is your home folder or one above it, so Dockingbird won't use it.
Point DOCKINGBIRD_HOME at an empty or new folder, then run this again.
```

Next step, as the message gives it:

- Unset DOCKINGBIRD_HOME, or point it at an empty or new folder, then run this again.
- Move those files out of it (your own rules can stay in instructions/), or set DOCKINGBIRD_HOME to an empty or new folder, then run this again.
- Move it out (your own rules can stay in instructions/), or set DOCKINGBIRD_HOME to an empty or new folder, then run this again.
- Point DOCKINGBIRD_HOME at an empty or new folder, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### INSTRUCTIONS_UNREADABLE

When: Your rules file for Claude or Codex (in Dockingbird's `instructions` folder) can't be read: it isn't a plain text file, is too large, or is a link.

```text
Dockingbird can't read your rules for {harness} in {path}.
Fix or remove that file, then run this again.
```

Next step: Fix or remove that file, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### INSTRUCTIONS_TIMED_OUT

When: You started an agent, and saving your rules file for Claude or Codex for it took longer than Dockingbird waits, usually because the computer was busy. No agent started. When Docker couldn't remove the step's container, the message names it.

```text
Saving your rules for {harness} took longer than {bound}, so no agent started.
Run this again when this computer is less busy.
```

Or:

```text
Saving your rules for {harness} took longer than {bound}, so no agent started.
Dockingbird couldn't stop its container {container}.
Once it has ended, run this again.
```

Next step, as the message gives it:

- Run this again when this computer is less busy.
- Once it has ended, run this again.

Exit status: 1 (a problem Dockingbird printed).

### DOCKER_ARGV_REFUSED

When: Dockingbird stopped one of its own Docker commands because it broke a safety rule. You should never see this; it is a bug, and the message gives the address to report it.

```text
Dockingbird refused its own docker command (rule {rule}), so nothing ran.
This is a Dockingbird bug.
Please report it: https://github.com/zeus-fyi/dockingbird/issues
```

Next step: https://github.com/zeus-fyi/dockingbird/issues

Exit status: 1 (a problem Dockingbird printed).

## Update

### UPDATE_GETTING

When: You ran `dockingbird update`: the first step gets the latest Dockingbird, and its line ends with the versions before and after. When the output goes to a pipe or a file, the line prints at once and a "still getting the latest Dockingbird" line follows once a minute while it runs.

```text
Getting the latest Dockingbird ... done ({old} -> {new})
```

Or:

```text
Getting the latest Dockingbird ...
```

Or:

```text
  still getting the latest Dockingbird, {elapsed} so far
```

Next step: none; it only informs.

Exit status: 0 (done).

### UPDATE_REBUILDING

When: `dockingbird update` rebuilds Dockingbird, with an estimate from the last build when a build runs, and none when the new version is already built; then it gets the tools' latest releases, one line each. When the output goes to a pipe or a file, the line prints at once and a "still updating" line follows once a minute while it runs.

```text
Rebuilding Dockingbird (about {estimate}) ... done ({elapsed})
```

Or:

```text
Rebuilding Dockingbird (about {estimate}) ...
```

Or:

```text
Rebuilding Dockingbird ... done ({elapsed})
```

Or:

```text
Rebuilding Dockingbird ...
```

Or:

```text
Rebuilding Dockingbird: waking Docker ...
```

Or:

```text
Rebuilding Dockingbird: no progress for {quiet}
```

Or:

```text
  still updating: step {index} of {count}, {elapsed} so far
```

Or:

```text
  still updating: step {index} of {count}, no output for {quiet}
```

Or:

```text
  still updating: waking Docker ...
```

Or:

```text
  still updating: preparing the build, {elapsed} so far
```

Next step: none; it only informs.

Exit status: 0 (done).

### UPDATE_DONE

When: `dockingbird update` finished. After a rebuild, it says what was kept: your repos, their history, and the sign-ins and API keys you have.

```text
Up to date.
```

Or:

```text
Up to date. Your {kept:and} are kept.
```

Next step: none; it only informs.

Exit status: 0 (done).

### UPDATE_TOOLS

When: After its rebuild, `dockingbird update` got each tool you have used once at its latest version, or found the one you have is the latest, and says which; when the channel names an older version than the one you have, the one you have stays. It doesn't get a tool you never used.

```text
{tool_name} {version} is the latest.
```

Or:

```text
Got {tool_name} {version}.
```

Or:

```text
{tool_name} {version} stays: the channel names an older version, {offered}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### TOOL_GETTING

When: The tool isn't downloaded yet, or you pinned a version that isn't, so Dockingbird fetches it before the command goes on; or a newer release is out, and a start waits a short while for it (the line shows the download's progress) before it runs the version you have instead. Downloads are verified against the vendor's signature before anything is installed. When the output goes to a pipe or a file, the first line prints at once and a "still getting" line follows once a minute while it runs, with the bytes so far or how long the download has been quiet.

```text
Getting {tool_name} {version} ... done ({elapsed})
```

Or:

```text
Getting {tool_name} {version} ({size}) ... done ({elapsed})
```

Or:

```text
Getting the latest {tool_name} ...
```

Or:

```text
Getting {tool_name} {version} ...
```

Or:

```text
Getting {tool_name} {version}  {bar}  {got} of {size}
```

Or:

```text
Getting {tool_name} {version}  {got} so far
```

Or:

```text
Getting {tool_name} {version}  no progress for {quiet}
```

Or:

```text
Getting {tool_name} {version}:
```

Or:

```text
{bar}  {got} of {size}
```

Or:

```text
{got} so far
```

Or:

```text
no progress for {quiet}
```

Or:

```text
  still getting {tool_name} {version}: {got} of {size}, {elapsed} so far
```

Or:

```text
  still getting {tool_name} {version}: {got} so far ({elapsed})
```

Or:

```text
  still getting the latest {tool_name}, {elapsed} so far
```

Or:

```text
  still getting {tool_name} {version}: no output for {quiet}
```

Or:

```text
  still getting {tool_name} {version}, {elapsed} so far
```

Next step: none; it only informs.

Exit status: 0 (done).

### TOOL_FETCH_FAILED

When: A newer version couldn't be downloaded this time (offline, a slow connection, the download store busy or Docker's disk full), so the version you have runs. Nothing to do; the next start tries again. `--verbose` says why.

```text
Couldn't get {tool_name} {version}; using {running}.
Dockingbird tries again next time.
```

Or:

```text
Couldn't get the latest {tool_name}; using {running}.
Dockingbird tries again next time.
```

Next step: none; it only informs.

Exit status: 0 (done).

### TOOL_VERIFY_FAILED

When: A download's signature, digest or size didn't match the vendor's, so it wasn't installed and that version is set aside until `dockingbird update`. The version you have runs. If it keeps happening, something between you and the download host is wrong: check your network. With no version downloaded at all the command exits 1.

```text
{tool_name} {version}'s download didn't verify, so it wasn't installed.
Using {running}. If this keeps happening, check your network.
```

Or:

```text
{tool_name} {version}'s download didn't verify, so it wasn't installed,
and no other version is downloaded.
If this keeps happening, check your network.
```

Next step: none; it only informs.

Exit status: 0 (done) or 1 (a problem Dockingbird printed), as "When:" says.

### TOOL_BROKEN

When: The new version was downloaded and verified but didn't print its version when Dockingbird ran it, so Dockingbird keeps the version you have and sets the new one aside until `dockingbird update`. To use it anyway, pin it in `versions.toml` in your Dockingbird folder. When the version that didn't start is the one Dockingbird has been running and an older version is downloaded but not yet checked, Dockingbird doesn't run the older one unasked, and the command exits 1: pin it in `versions.toml` to use it (it is checked first), or run the command again later. With no version downloaded at all the command exits 1.

```text
{tool_name} {version} didn't start, so Dockingbird keeps {running}.
To use it anyway, pin it in {path}: {tool} = "{version}"
```

Or:

```text
{tool_name} {version} didn't start, and no other version is downloaded.
Run this again later, or pin another version in {path}.
```

Or:

```text
{tool_name} {version} didn't start its check, but it is pinned, so Dockingbird runs it anyway.
```

Or:

```text
{tool_name} {version} didn't start.
An older version, {offered}, is downloaded but hasn't been checked.
Run this again later, or pin it in {path}: {tool} = "{offered}"
```

Next step: none; it only informs.

Exit status: 0 (done) or 1 (a problem Dockingbird printed), as "When:" says.

### TOOL_CHECK_FAILED

When: Dockingbird couldn't run the new version's check (Docker didn't answer in time), so the version you have runs, the download is kept and nothing is set aside; the next start checks it again without downloading it. With no version downloaded at all the command exits 1: run it again.

```text
Dockingbird couldn't check {tool_name} {version} ({why}); using {running}.
It tries again next time.
```

Or:

```text
Dockingbird couldn't check {tool_name} {version} ({why}),
and no other version is downloaded. Run this again.
```

Next step: none; it only informs.

Exit status: 0 (done) or 1 (a problem Dockingbird printed), as "When:" says.

### TOOL_NOT_AVAILABLE

When: This is the tool's first run on this Mac and it couldn't be downloaded (no network, or the download host didn't answer). Connect, then run the command again.

```text
{tool_name} isn't downloaded yet, and it couldn't be downloaded ({why}).
Connect, then run this again.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### TOOL_PIN_NOT_FOUND

When: Your `versions.toml` pins the tool to a version the vendor doesn't have and that isn't downloaded. Fix the version, or remove the line to run the latest.

```text
{tool_name} {version}, pinned in {path}, doesn't exist at {source}.
Fix the pin, or remove it to use the latest.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### TOOL_PIN_INVALID

When: Your `versions.toml` (in your Dockingbird folder) couldn't be read: one line per tool, `claude` or `codex`, then a quoted version like "2.1.285", or "latest", or (Claude Code only) "stable"; nothing else, and the file must be a plain file of yours. Fix it, or remove it to run the latest.

```text
{path}: the {key} line isn't a version, latest or stable.
Fix it, or remove it to use the latest.
```

Or:

```text
{path} has a line that isn't claude or codex.
Fix it, or remove it to use the latest.
```

Or:

```text
{path}: Codex has no stable channel, so codex can't be stable.
Fix it, or remove it to use the latest.
```

Or:

```text
{path} isn't TOML: one line each, claude or codex, equals,
then a quoted version, latest or stable.
Fix it, or remove it to use the latest.
```

Or:

```text
{path} isn't a regular file of yours, or is too large to read.
Fix it, or remove it to use the latest.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### PIN_DONE

When: You ran `dockingbird pin` with a tool and a version, and it wrote that version into `versions.toml` in your Dockingbird folder. The tool's next start runs it, downloading it first if it isn't there; agents already running keep the version they started with.

```text
{tool_name} will run {version} from its next start; agents already running keep theirs.
```

Next step: none; it only informs.

Exit status: 0 (done).

### PIN_FOLLOWS

When: You ran `dockingbird pin --clear`, or `pin` with `latest` or (Claude Code only) `stable`. The tool now follows that release from its next start: for the latest, its line is gone from `versions.toml`. Agents already running keep their version.

```text
{tool_name} follows the latest release from its next start.
```

Or:

```text
{tool_name} follows the stable release from its next start.
```

Next step: none; it only informs.

Exit status: 0 (done).

### PIN_INVALID_VERSION

When: The version you gave `dockingbird pin` isn't a release number like `2.1.285`, `latest`, or (Claude Code only) `stable`. Nothing was written.

```text
VERSION must be a version like 2.1.285, or latest.
See: dockingbird pin -h
```

Or:

```text
Codex has no stable channel, so codex can't be stable.
See: dockingbird pin -h
```

Next step: dockingbird pin -h

Exit status: 2 (usage).

### PIN_ARGUMENTS_REQUIRED

When: You ran `dockingbird pin` without a tool and a version, or gave `--clear` a version too. The message shows both forms of the command.

```text
Use dockingbird pin claude|codex VERSION,
or dockingbird pin --clear claude|codex.
```

Next step: none; it only informs.

Exit status: 2 (usage).

### TOOL_CHECK_SKIPPED

When: `--verbose` only: the version you have is the latest, or the one you pinned, so there was nothing to fetch; or the quick check for a newer release gave no answer (offline, or the answer couldn't be read), or named an older version than the one you have, which stays.

```text
{tool_name} {version} is the latest; nothing to fetch.
```

Or:

```text
{tool_name} {version} is pinned in {path}.
```

Or:

```text
{tool_name} {version} is pinned in this agent's config.
```

Or:

```text
Couldn't check for a newer {tool_name}; the version you have runs.
```

Or:

```text
{tool_name} {version} stays: the channel names an older version, {offered};
nothing to fetch.
```

Next step: none; it only informs.

Exit status: 0 (done).

### TOOL_FETCHING

When: An agent started over MCP (by your own harness, through `dockingbird mcp`) found the tool still downloading and no version of it to run yet: a start over MCP doesn't wait for a download. Try again in a minute; the download goes on. A start from the command line, with or without `--json`, waits for the download instead.

```text
{tool_name} is being downloaded; try again in a minute.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### TOOL_STILL_DOWNLOADING

When: A newer version is downloading and didn't arrive within the time a start waits, so this start runs the version you have; when another command (an `update`, or a start in another terminal) is doing the download, the line says so and the next start checks again. Nothing to do; the download goes on.

```text
Still getting {tool_name} {version}; this start uses {running}.
The next start uses the new one.
```

Or:

```text
Another command is getting {tool_name} {version}; this start uses {running}.
The next start checks again.
```

Or:

```text
Another command is getting the latest {tool_name}; this start uses {running}.
The next start checks again.
```

Next step: none; it only informs.

Exit status: 0 (done).

### TOOL_PRUNE_FAILED

When: `--verbose` only: removing a tool's unused versions from the download store didn't work this time. Nothing is lost; the next start or `dockingbird clean` tries again.

```text
Dockingbird couldn't remove the unused {tool_name} versions this time.
It tries again next time.
```

Next step: none; it only informs.

Exit status: 0 (done).

### TOOL_STORE_BUSY

When: `clean`, `update` or another start is removing that tool's unused versions; run the command again in a minute.

```text
Dockingbird is removing unused {tool_name} versions in another terminal;
try again in a minute.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### UPDATE_LOCAL_INSTALL

When: You installed Dockingbird from a folder on this Mac, so `update` doesn't change its version; it still rebuilds Dockingbird.

```text
Dockingbird was installed from a folder on this Mac, so it stays at {version}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### UPDATE_COMMIT_INSTALL

When: You installed Dockingbird pinned to one commit (`uv tool install git+...@<commit>`), so `update` doesn't change its version; it still rebuilds Dockingbird. `update --check` says only this. To move on, install the release or commit you want the same way.

```text
Dockingbird was installed pinned to commit {commit}, so it stays at {version}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### UPDATE_NOT_SET_UP

When: You ran `dockingbird update` before the first set-up. It updated only the command; the first `dockingbird claude` sets up the rest.

```text
Dockingbird isn't set up yet; the first dockingbird claude will set it up.
```

Next step: dockingbird claude

Exit status: 0 (done).

### UPDATE_LATEST

When: `dockingbird update` (or `update --check`) found nothing newer: for an install from a release tag, no release tag above the one you installed; `update --check` names that tag.

```text
Dockingbird {version} is the latest. Nothing to do.
```

Or:

```text
Dockingbird {version} is the latest.
```

Or:

```text
Dockingbird {release} is the latest.
```

Next step: none; it only informs.

Exit status: 0 (done).

### UPDATE_AVAILABLE

When: `dockingbird update --check` found a newer version.

```text
A newer Dockingbird is out. Get it: dockingbird update
```

Next step: dockingbird update

Exit status: 0 (done).

### UPDATE_RELEASE_AVAILABLE

When: You installed Dockingbird from a release tag (`uv tool install git+...@v0.1.0`), and `dockingbird update --check` found a newer release tag; `dockingbird update` moves to it.

```text
A newer Dockingbird is out: {release}. Get it: dockingbird update
```

Next step: dockingbird update

Exit status: 0 (done).

### UPDATE_FINISHING

When: You upgraded the command yourself (with uv), so the next command finishes the update by rebuilding Dockingbird. When the output goes to a pipe or a file, the line prints at once and a "still updating to" line follows once a minute while it runs.

```text
Finishing the update to {version} (about {estimate}) ... done ({elapsed})
```

Or:

```text
Finishing the update to {version} (about {estimate}) ...
```

Or:

```text
Finishing the update to {version} ... done ({elapsed})
```

Or:

```text
Finishing the update to {version} ...
```

Or:

```text
Finishing the update to {version}: waking Docker ...
```

Or:

```text
Finishing the update to {version}: no progress for {quiet}
```

Or:

```text
  still updating to {version}: step {index} of {count}, {elapsed} so far
```

Or:

```text
  still updating to {version}: step {index} of {count}, no output for {quiet}
```

Or:

```text
  still updating to {version}: waking Docker ...
```

Or:

```text
  still updating to {version}: preparing the build, {elapsed} so far
```

Next step: none; it only informs.

Exit status: 0 (done).

### UPDATE_UV_FAILED

When: Getting the latest Dockingbird with uv failed. The message shows the exact command (for an install from a release tag, the install of the newer tag), so you can run it yourself and see why; nothing else changed. For an install from Zeusfyi's release index the command ran with this computer's download token, so check the network and `dockingbird license status` instead.

```text
Getting the latest Dockingbird didn't work. Dockingbird ran:
  uv tool install --force --from \
    git+https://github.com/zeus-fyi/dockingbird dockingbird
Run it yourself to see why. Nothing else changed.
```

Or:

```text
Getting the latest Dockingbird didn't work. Dockingbird ran:
  uv tool upgrade dockingbird
Run it yourself to see why. Nothing else changed.
```

Or:

```text
Getting the latest Dockingbird didn't work. Dockingbird ran:
  uv tool install --force \
    git+https://github.com/zeus-fyi/dockingbird@{release}
Run it yourself to see why. Nothing else changed.
```

Or:

```text
Getting the latest Dockingbird didn't work. Dockingbird ran:
  uv tool upgrade dockingbird
with this computer's download token for the release index.
Check the network and dockingbird license status, then run dockingbird update again. Nothing else changed.
```

Next step, as the message gives it:

- Run it yourself to see why.
- dockingbird license status

Exit status: 1 (a problem Dockingbird printed).

### UPDATE_CHECK_FAILED

When: `dockingbird update --check` (or, for an install from a release tag, `dockingbird update`, which reads the source's release tags first) couldn't read the source's versions from `https://github.com/zeus-fyi/dockingbird`: the network is down, or git on this Mac can't read that private repository over https (the operator guide's Install section gives the one-time git line for it); or the source lists no release tag at all. Nothing changed. For an install from Zeusfyi's release index, the index's listing couldn't be read: the network, or a license that is no longer active (the index refuses it); `dockingbird license status` says which.

```text
Dockingbird couldn't read versions from https://github.com/zeus-fyi/dockingbird.
Check the network, and that git on this Mac can read that repository
(see Install in the operator guide),
then run dockingbird update --check again.
```

Or:

```text
Dockingbird couldn't read versions from https://github.com/zeus-fyi/dockingbird.
Check the network, and that git on this Mac can read that repository
(see Install in the operator guide),
then run dockingbird update again.
```

Or:

```text
Dockingbird couldn't read versions from its release index.
Check the network, and that this computer's license is active
(dockingbird license status), then run dockingbird update --check again.
```

Or:

```text
Dockingbird couldn't read versions from its release index.
Check the network, and that this computer's license is active
(dockingbird license status), then run dockingbird update again.
```

Next step, as the message gives it:

- dockingbird update --check
- dockingbird update

Exit status: 1 (a problem Dockingbird printed).

### UPDATE_SCRIPT_FAILED

When: `dockingbird update` got the new version, but the new version couldn't start its rebuild. Nothing was rebuilt.

```text
The new Dockingbird didn't start, so nothing was rebuilt.
Run dockingbird update again.
```

Next step: dockingbird update

Exit status: 1 (a problem Dockingbird printed).

### UPDATE_MOVING_PYTHON

When: `dockingbird update` found Dockingbird's own tool on a Python other than 3.12, as an install made before this change is, and moves it with `uv tool upgrade --python 3.12 dockingbird` before it rebuilds. When the output goes to a pipe or a file, the line prints at once and a "still moving" line follows once a minute while it runs.

```text
Dockingbird now runs on Python 3.12.
```

Or:

```text
Moving Dockingbird to Python 3.12 ...
```

Or:

```text
  still moving Dockingbird to Python 3.12, {elapsed} so far
```

Next step: none; it only informs.

Exit status: 0 (done).

### UPDATE_PYTHON_MOVE_FAILED

When: `dockingbird update` ran `uv tool upgrade --python 3.12 dockingbird` to move Dockingbird's own tool to Python 3.12, and uv failed, or Dockingbird found no uv. Nothing was rebuilt.

```text
Moving Dockingbird to Python 3.12 didn't work. Dockingbird ran:
  uv tool upgrade --python 3.12 dockingbird
Run it yourself to see why. Nothing else changed.
```

Next step: Run it yourself to see why.

Exit status: 1 (a problem Dockingbird printed).

### UPDATE_PYTHON_NOT_MOVED

When: `dockingbird update` moved Dockingbird's tool to Python 3.12, but the moved program still ran on another Python, so it stopped instead of moving it again. Nothing was rebuilt.

```text
Dockingbird still runs on Python {running} after its move to
Python 3.12, so nothing was rebuilt.
Run uv tool upgrade --python 3.12 dockingbird, then dockingbird update again.
```

Next step: uv tool upgrade --python 3.12 dockingbird

Exit status: 1 (a problem Dockingbird printed).

### UPDATE_KEEPING

When: You ran `dockingbird update` while agents are working: before it installs the new version, it keeps a copy of the version they run, which your commands use until they end. When the output goes to a pipe or a file, the line prints at once and a "still keeping" line follows once a minute while it runs.

```text
Keeping Dockingbird {old} for your running agents ...
```

Or:

```text
Keeping Dockingbird {old} for your running agents ... done
```

Or:

```text
  still keeping {old} for your running agents, {elapsed} so far
```

Next step: none; it only informs.

Exit status: 0 (done).

### UPDATE_STAGED

When: `dockingbird update` installed and built the new version while agents are working. They keep running on the version they started with, and so do your commands, until the last one ends; then Dockingbird switches to the new version by itself, with no command typed. When the agents ended while it worked, it switches now. Running `update` again with nothing newer out says the same and changes nothing.

```text
Dockingbird {new} is installed. {name} still runs on {old},
and your commands run {old} until it ends.
Then Dockingbird switches to {new} by itself.
```

Or:

```text
Dockingbird {new} is installed. {names:and} still run on {old},
and your commands run {old} until they end.
Then Dockingbird switches to {new} by itself.
```

Or:

```text
{name} still runs on Dockingbird {old}.
When it ends, Dockingbird switches to {new} by itself.
```

Or:

```text
{names:and} still run on Dockingbird {old}.
When they end, Dockingbird switches to {new} by itself.
```

Or:

```text
Dockingbird {new} is installed, and no agent runs, so it switches now.
```

Next step: none; it only informs.

Exit status: 0 (done).

### UPDATE_IN_PROGRESS

When: You ran `dockingbird update` while another `update` on this computer is installing a version or switching to one. Nothing changed; run it again when that one ends.

```text
Another dockingbird update is under way here.
Run dockingbird update again when it ends.
```

Next step: dockingbird update

Exit status: 1 (a problem Dockingbird printed).

### UPDATE_SWITCHING

When: Dockingbird is switching to the version `dockingbird update` installed, and your command waits until the switch is done, then goes on. A start can also wait while `dockingbird stop` or `dockingbird clean --all` runs. When the output goes to a pipe or a file, a "still switching" line follows once a minute while it waits.

```text
Switching Dockingbird to {version} ...
```

Or:

```text
Switching Dockingbird to {version} ... done ({elapsed})
```

Or:

```text
  still switching to {version}, {elapsed} so far
```

Or:

```text
Waiting for another dockingbird command here to finish ...
```

Next step: none; it only informs.

Exit status: 0 (done).

### UPDATE_SWITCH_UNDER_WAY

When: Your command met a newer Dockingbird in the middle of its work, where it can't wait for the switch, so it started the switch and stopped. Run it again once `dockingbird status` shows the new version.

```text
Dockingbird is switching to {version}, so this command stopped.
Run it again once dockingbird status shows {version}.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### UPDATE_SWITCH_FAILED

When: The switch to the version `dockingbird update` installed didn't work, so the older version still runs, and your commands with it. Dockingbird doesn't try again by itself; `dockingbird update` shows why and tries again. `status` shows it under "Needs your attention".

```text
Dockingbird didn't switch to {version}, so {old} still runs.
See why and try again: dockingbird update
```

Next step: dockingbird update

Exit status: 1 (a problem Dockingbird printed).

### UPDATE_SWITCHED_UNDER

When: Dockingbird switched to the version `dockingbird update` installed while your command ran, so the command stopped; run it again. When it was the start of an agent, the agent didn't start and nothing of it was made.

```text
Dockingbird switched to {version} while this command ran, so it stopped.
Run it again.
```

Or:

```text
Dockingbird switched to {version} while {name} started, so {name} didn't start.
Run the same command again.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### UPDATE_TWO_PROGRAMS

When: Two `dockingbird` programs with different code use this home, such as the one on your path and a checkout's, or the GUI's. The other one switched Dockingbird last, so this one won't switch it back by itself, which would go back and forth. Use one program for the home; `dockingbird update` run from this one switches to it.

```text
Another dockingbird program with different code switched this home last,
so this one ({version}) won't switch it back by itself.
Use one program for this home. To switch to this one: dockingbird update
```

Next step: dockingbird update

Exit status: 1 (a problem Dockingbird printed).

### UPDATE_STAGE_UNREADABLE

When: You ran `dockingbird update`, and the record of an update staged in this home (`update/stage.json`) can't be read: it was changed, or a newer Dockingbird wrote it. Nothing changed. If no other `dockingbird` program on this computer staged it, move it aside and run `dockingbird update` again.

```text
Dockingbird can't read the update staged here, so it changed nothing:
  {path}
If no other dockingbird program on this computer staged it,
move it aside and run dockingbird update again.
```

Next step: dockingbird update

Exit status: 1 (a problem Dockingbird printed).

### AGENTS_RUNNING_UPDATE_REFUSED

When: You ran `dockingbird update` while agents are working, and Dockingbird couldn't keep a copy of the version they run, so it changed nothing and waits for you: the copy's install failed, or an older copy is still in use. The same lines show when agents started while an update was finishing.

```text
{count} agents are still running ({names}).
Update when they finish: dockingbird update. Or stop them now: dockingbird stop
```

Or:

```text
1 agent is still running ({name}).
Update when it finishes: dockingbird update. Or stop it now: dockingbird stop
```

Or:

```text
1 agent is still running ({name}),
and Dockingbird couldn't keep {old} for it, so nothing changed.
Update when it finishes: dockingbird update. Or stop it now: dockingbird stop
```

Or:

```text
{count} agents are still running ({names}),
and Dockingbird couldn't keep {old} for them, so nothing changed.
Update when they finish: dockingbird update. Or stop them now: dockingbird stop
```

Next step: dockingbird update

Exit status: 1 (a problem Dockingbird printed).

### VERSION_MISMATCH_AGENTS_RUNNING

When: A newer Dockingbird is installed, but agents still run on the older one. Most commands wait until they end; `status` shows the same lines. When Dockingbird was installed from a folder on this Mac and its code changed while its version stayed the same, the message says the code changed since the agents started, and names the version once. When `dockingbird update` staged the new version, the message says Dockingbird switches by itself when they end.

```text
Dockingbird {version} is installed, and {name} still runs on {running}.
When it ends, any command finishes the update. Or stop it now: dockingbird stop
```

Or:

```text
Dockingbird {version} is installed, and {names:and} still run on {running}.
When they end, any command finishes the update.
Or stop them now: dockingbird stop
```

Or:

```text
Dockingbird's code changed since {name} started (both are version {version}).
When it ends, the next start finishes the update.
Or stop it now: dockingbird stop
```

Or:

```text
Dockingbird's code changed since {names:and} started (all are version {version}).
When they end, the next start finishes the update.
Or stop them now: dockingbird stop
```

Or:

```text
Dockingbird {version} is installed, and {name} still runs on {running}.
When it ends, Dockingbird switches by itself. Or stop it now: dockingbird stop
```

Or:

```text
Dockingbird {version} is installed, and {names:and} still run on {running}.
When they end, Dockingbird switches by itself.
Or stop them now: dockingbird stop
```

Or:

```text
Dockingbird's code changed since {name} started (both are version {version}).
When it ends, Dockingbird switches by itself. Or stop it now: dockingbird stop
```

Or:

```text
Dockingbird's code changed since {names:and} started (all are version {version}).
When they end, Dockingbird switches by itself.
Or stop them now: dockingbird stop
```

Next step: dockingbird stop

Exit status: 1 (a problem Dockingbird printed).

### CLEAN_ALL_NO_SYNC_LIST

When: You ran `dockingbird clean --all` while an update is half done, so Dockingbird can't list the commits you haven't synced.

```text
An update is half done, so Dockingbird can't list commits you haven't synced.
To keep them, run dockingbird sync in each repo first.
```

Next step: To keep them, run dockingbird sync in each repo first.

Exit status: 0 (done).

## Repos and branches

### NOT_A_GIT_REPO

When: You ran a command that works on a repo, in a folder that isn't in a git repo.

```text
Not a git repo: {path}.
cd into your project, then run this again.
```

Next step: cd into your project, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### DETACHED_HEAD

When: Your checkout is on no branch (a detached HEAD), and Dockingbird works on branches.

```text
You're not on a branch (detached at {commit}). Switch to one, for example
git switch main, then run this again.
```

Next step: Switch to one, for example git switch main, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### EMPTY_REPO

When: The repo has no commits yet, so there is nothing to copy.

```text
This repo has no commits yet. Make one (git commit), then run this again.
```

Next step: Make one (git commit), then run this again.

Exit status: 1 (a problem Dockingbird printed).

### WORKTREE_NOT_YET

When: You ran Dockingbird in a git worktree, which it doesn't support yet.

```text
Dockingbird doesn't work in a git worktree yet. cd into the repository's
main checkout, or a git clone of it, then run this again.
```

Next step: cd into the repository's main checkout, or a git clone of it, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### SUBMODULE_NOT_YET

When: You ran Dockingbird inside a submodule, which it doesn't support yet.

```text
Dockingbird doesn't work inside a submodule yet. cd into the main repo,
then run this again.
```

Next step: cd into the main repo, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### REPO_LINKING

When: The first start on a branch copies its history for the agents. The line shows the size so far, then the total.

```text
Copying {repo} ({branch}) for the agents ({size}) ... done ({elapsed})
```

Or:

```text
Copying {repo} ({branch}) for the agents  {size} so far
```

Next step: none; it only informs.

Exit status: 0 (done).

### REPO_NAME_TAKEN

When: Another checkout already has this folder's name, so this one gets a numbered name, which its lines and `status` use.

```text
Another checkout is already called {old}, so this one is {repo}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### REPO_LINK_TOOK_TOO_LONG

When: Copying the branch for the agents took too long, so it stopped. Nothing was linked.

```text
Copying {repo} ({branch}) for the agents took too long, so it stopped.
Nothing was linked. Run this again.
```

Next step: Run this again.

Exit status: 1 (a problem Dockingbird printed).

### REPO_DISK_FULL

When: The first start on a branch copies its history to the agents' disk (Docker's virtual disk), and that disk ran out of room for it: the message shows the free space. Nothing was linked. Free space there (in Docker Desktop, Settings, Resources, or with `docker system prune`), then run the command again.

```text
The agents' disk (Docker's) has {free} free, too little to copy {repo} ({branch}).
Nothing was linked. Free some of Docker's disk, or give it more, then run this again.
```

Or:

```text
The agents' disk (Docker's) ran out of room while copying {repo} ({branch}).
Nothing was linked. Free some of Docker's disk, or give it more, then run this again.
```

Next step: Free some of Docker's disk, or give it more, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### LINK_TREE_POLICY

When: The branch has files the agents don't take: a symlink that points outside the repo, by an absolute path, into `.git`, in a loop or to nothing usable, or one in place of a git file such as `.gitignore`; a submodule; or a Git LFS file. A symlink that points inside the repo by a relative path is fine. Dockingbird checks this before it sets anything up, and nothing was linked. The message lists each one with its kind, and a symlink with where it points; past the list's bound it says how many more there are, which are listed once these are fixed.

```text
{repo} ({branch}) can't be linked yet: it has {count} files the agents don't take:
{entries}
Fix them, commit, then run this again.
```

Or:

```text
{repo} ({branch}) can't be linked yet: it has 1 file the agents don't take:
{entries}
Fix it, commit, then run this again.
```

Or:

```text
{repo} ({branch}) can't be linked yet: it has {count} files the agents don't take:
{entries}
Fix these, commit, then run this again: the next ones are listed then.
```

Next step, as the message gives it:

- Fix them, commit, then run this again.
- Fix it, commit, then run this again.
- Fix these, commit, then run this again: the next ones are listed then.

Exit status: 1 (a problem Dockingbird printed).

### REPO_RELINKED

When: You cloned a repo again at the same place, made a branch again from the agents' copy after deleting it (`git switch -c feature/x dockingbird/feature/x`), or said yes when Dockingbird asked about a new branch with a deleted branch's name, and Dockingbird linked it back to the agents' copy it had. A branch that already has all the agents' commits is linked back without a question too. Once linked, `git branch -m` keeps the link.

```text
Linked {repo} ({branch}) to its agents' copy again.
```

Next step: none; it only informs.

Exit status: 0 (done).

### BRANCH_NAME_REUSED

When: You started an agent or ran `dockingbird sync` on a branch you made under the name of a branch you deleted, and that branch's agents' copy has commits the new one doesn't. Dockingbird asks before it links the two; the default is no. It doesn't ask for a branch you made from the agents' copy, in a repo you cloned again, or for one that already has their commits. When you pick up an agent with `--as NAME` whose work is kept on the branch you deleted, the question names that agent first and asks whether to pick it up too.

```text
{repo} ({branch}) has the name of a branch you deleted.
The agents' copy of that branch has {count:commit|commits} this one doesn't:
{commits}
Carry on from them here? [y/N]
```

Or:

```text
{repo} ({branch}) has the name of a branch you deleted.
The agents' copy of that branch has commits this one doesn't.
Carry on from them here? [y/N]
```

Or:

```text
{repo} ({branch}) has the name of a branch you deleted.
The agents' copy of that branch has {count:commit|commits} this one doesn't:
{commits}
```

Or:

```text
{repo} ({branch}) has the name of a branch you deleted.
The agents' copy of that branch has commits this one doesn't.
```

Or:

```text
{name}'s work is on the {branch} you deleted.
The agents' copy of that branch has {count:commit|commits} this one doesn't:
{commits}
Carry on from them here, and pick {name} up? [y/N]
```

Or:

```text
{name}'s work is on the {branch} you deleted.
The agents' copy of that branch has commits this one doesn't.
Carry on from them here, and pick {name} up? [y/N]
```

Or:

```text
{name}'s work is on the {branch} you deleted.
The agents' copy of that branch has {count:commit|commits} this one doesn't:
{commits}
```

Or:

```text
{name}'s work is on the {branch} you deleted.
The agents' copy of that branch has commits this one doesn't.
```

Next step, as the message gives it:

- answer y to go on; anything else is no
- none, where the message only informs

Exit status: 1 (a problem Dockingbird printed), unless you go on at its question; then the command ends with its own status.

### NOTHING_LINKED

When: You said no (or pressed Ctrl-C) when Dockingbird asked whether a branch with a deleted branch's name should carry on from that branch's agents' commits, or there was no terminal to ask on. Nothing was linked, started or synced. Renaming the branch with `git branch -m` keeps it apart, and the next start gives it its own copy; without a terminal, `dockingbird sync` on one asks again. When you were picking up an agent, its work stays kept. After a no to `dockingbird sync`, the message also offers `dockingbird sync --let-go`, which lets the agents' commits go and makes yours the branch.

```text
Nothing linked. To keep this branch apart, rename it:
git branch -m {branch} NEWNAME
To let their commits go and make yours the branch: dockingbird sync --let-go
```

Or:

```text
Nothing linked. To keep this branch apart, rename it, then run this again:
git branch -m {branch} NEWNAME
```

Or:

```text
Nothing linked. To carry on from them, run dockingbird sync on a terminal.
To keep this branch apart, rename it:
git branch -m {branch} NEWNAME
```

Or:

```text
Nothing linked. To carry on from them, run dockingbird sync on a terminal first.
To keep this branch apart, rename it, then run this again:
git branch -m {branch} NEWNAME
```

Or:

```text
Nothing linked; {name}'s work stays kept.
To keep this branch apart, rename it: git branch -m {branch} NEWNAME
```

Or:

```text
Nothing linked; {name}'s work stays kept.
To carry on from them, run dockingbird sync on a terminal first.
To keep this branch apart, rename it: git branch -m {branch} NEWNAME
```

Next step, as the message gives it:

- git branch -m {branch} NEWNAME
- dockingbird sync

Exit status: 1 (a problem Dockingbird printed).

### BRANCH_NAME_UNSUPPORTED

When: The branch's name has characters the agents' copy can't hold. Only letters, digits, `.`, `_`, `-` and `/` work.

```text
Dockingbird can't link the branch {branch} yet: a branch name may hold
only letters, digits, '.', '_', '-' and '/', and no part may start with
'.' or '-'.
Rename it, then run this again: git branch -m NEWNAME
```

Next step: git branch -m NEWNAME

Exit status: 1 (a problem Dockingbird printed).

### NAME_HOLDS_KEY_MARK

When: A folder or branch name has `dbk1.` in it, which Dockingbird keeps for its own keys.

```text
Dockingbird can't link {repo} ({branch}) yet: 'dbk1.' in a folder or
branch name is kept for Dockingbird's own keys.
Rename it, then run this again.
```

Next step: Rename it, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### NAME_HOLDS_SOCKET_MARK

When: A folder or branch name has `docker.sock` in it, which Dockingbird keeps out of its Docker commands.

```text
Dockingbird can't link {repo} ({branch}) yet: 'docker.sock' in a folder or
branch name is kept from Dockingbird's docker commands.
Rename it (for example git branch -m NEWNAME), then run this again.
```

Next step: git branch -m NEWNAME

Exit status: 1 (a problem Dockingbird printed).

### REPO_HISTORY_REFUSED

When: The branch's history has an object git's strict checks refuse, often from an old tool. `git fsck` shows it.

```text
Dockingbird can't copy {repo} ({branch}): its history has an object
that git's strict checks refuse (often an old tool's file mode or name).
Dockingbird refuses it even where git fsck only warns.
To see it, run git fsck in its checkout.
```

Next step: git fsck

Exit status: 1 (a problem Dockingbird printed).

### LINK_NO_ANSWER

When: Dockingbird didn't answer while it linked the branch. Nothing was linked.

```text
Dockingbird didn't answer while linking {repo} ({branch}).
Nothing was linked. Run this again.
```

Next step: Run this again.

Exit status: 1 (a problem Dockingbird printed).

### REPOS_FILE_UNREADABLE

When: Dockingbird's list of linked repos can't be read: it is a link, not yours, too large, or not in its format.

```text
Dockingbird can't read its list of linked repos:
  {path}
Move it aside, then run this again.
```

Next step: Move it aside, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### LINK_INVALID

When: The branch's Dockingbird link in `.git/config` has something that isn't a link Dockingbird made.

```text
{repo} ({branch}) has a Dockingbird link that isn't valid. Remove it,
git config --unset branch.{branch}.dockingbird, then run this again.
```

Next step: git config --unset branch.{branch}.dockingbird

Exit status: 1 (a problem Dockingbird printed).

### TREE_ROW

When: One file in a list of files the agents don't take, with its kind: a submodule or a Git LFS file.

One row of a table; its cells line up with the rows around it.

```text
  {file}     ({kind})
```

Next step: none; it only informs.

Exit status: 0 (done).

### TREE_LINK_ROW

When: One symlink in a list of files the agents don't take: its path, where it points, and why it isn't taken. A symlink that points inside the repo by a relative path is fine.

One row of a table; its cells line up with the rows around it.

```text
  {file} -> {link_target}     ({kind})
```

Next step: none; it only informs.

Exit status: 0 (done).

## Agents: starting

### AGENT_STARTING

When: You ran `dockingbird claude` or `dockingbird codex`, and a new agent starts on this repo's branch; a command whose config gives its agents a scratch folder says it starts there instead.

```text
Starting {name} on {repo} ({branch}).
```

Or:

```text
Starting {name} in a scratch folder.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SIGNIN_FIRST_TIME

When: An agent starts and the tool isn't signed in yet (and no API key is saved for it). The line says what its sign-in screen will ask; you do it only once.

```text
Starting {name} on {repo} ({branch}). Claude will show a sign-in link:
open it on this Mac, sign in, then paste the code here. Only this once.
```

Or:

```text
Starting {name} on {repo} ({branch}). Codex will show a code and a link:
open the link on this Mac and enter the code. Only this once.
```

Or:

```text
Starting {name} in a scratch folder. Claude will show a sign-in link:
open it on this Mac, sign in, then paste the code here. Only this once.
```

Or:

```text
Starting {name} in a scratch folder. Codex will show a code and a link:
open the link on this Mac and enter the code. Only this once.
```

Next step, as the message gives it:

- Claude will show a sign-in link: open it on this Mac, sign in, then paste the code here.
- Codex will show a code and a link: open the link on this Mac and enter the code.

Exit status: 0 (done).

### AGENT_LEAVE_HINT

When: The last start line when the agent takes this terminal (a Codex start that waits for Enter prints one more): closing the window leaves it working.

```text
To leave it working, close this window.
```

Next step: none; it only informs.

Exit status: 0 (done).

### TRUST_NOTE

When: The first attached start of a tool on a repo (`dockingbird claude` or `codex`, or `start --terminal`) where the repo's own settings are off: a repo that isn't trusted on this Mac (one you marked with `dockingbird trust --off`, or one with no mark while `config.toml` in Dockingbird's folder says `trust = "untrusted"`), a command whose config leaves them off, or a tool whose sign-in isn't yet proven safe from them. Every other repo is trusted, and where its settings load neither tool asks, so nothing prints. With or without a terminal; a `start` on the bus prints none, and an agent in a scratch folder gets the scratch form on every attached start: the folder is its own, and nothing in it ever loads. Claude may ask whether to trust its folder, and Codex, in a repo that isn't trusted, shows its folder-access notice each time it opens its screen (one Enter opens the folder restricted; a one-shot `codex exec` shows none); that folder is the agent's own copy. Codex's note ends with the keys: Codex asks as it opens, before or just after its prompt box shows, so press Enter at that question before you type, since `n`, `q`, `2` or Esc there close Codex and end the agent. At a terminal a Codex start prints its note every time, a pick-up's too, and waits for Enter before Codex opens (with `--json` it never waits), since Codex's screen hides it. The second line says what your answer changes about the repo's own settings, hooks and MCP servers (for Codex, its settings; its AGENTS.md loads either way): in a repo that isn't trusted they stay off whatever you answer (`dockingbird trust` turns them back on; for a tool whose sign-in isn't yet proven safe from them, nothing does). When the line before said why they stay off (the command's config leaves them off), the note says nothing more about them (Codex's still ends with the keys), marked or not, and the tool may still ask.

```text
{harness} may ask whether to trust {work_path}: that is its copy of this repo.
Whatever you answer, the repo's own settings, hooks and MCP servers stay off
until you run dockingbird trust.
```

Or:

```text
Codex may ask for folder access to {work_path}: that is its copy of this repo.
Open it restricted: AGENTS.md loads but the repo's own settings stay off
until you run dockingbird trust.
Codex asks for folder access as it opens, before or just after its prompt
box: press Enter at that question before you type; n, q, 2 or Esc there
close Codex and end this agent.
```

Or:

```text
{harness} may ask whether to trust {work_path}: that is its copy of this repo.
The repo's own settings, hooks and MCP servers never load, whatever you answer.
```

Or:

```text
Codex may ask for folder access to {work_path}: that is its copy of this repo.
Open it restricted: AGENTS.md loads but the repo's own settings never load here.
Codex asks for folder access as it opens, before or just after its prompt
box: press Enter at that question before you type; n, q, 2 or Esc there
close Codex and end this agent.
```

Or:

```text
{harness} may ask whether to trust {work_path}: that is its copy of this repo.
```

Or:

```text
Codex may ask for folder access to {work_path}: that is its copy of this repo.
Codex asks for folder access as it opens, before or just after its prompt
box: press Enter at that question before you type; n, q, 2 or Esc there
close Codex and end this agent.
```

Or:

```text
{harness} may ask whether to trust {work_path}: that is its own scratch folder.
Whatever you answer, its settings, hooks and MCP servers never load.
```

Or:

```text
Codex may ask for folder access to {work_path}, its own scratch folder.
Open it restricted: AGENTS.md loads but its settings never load here.
Codex asks for folder access as it opens, before or just after its prompt
box: press Enter at that question before you type; n, q, 2 or Esc there
close Codex and end this agent.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CODEX_PRESS_ENTER

When: A Codex start at a terminal where Codex will ask for folder access: Dockingbird printed its note about that question and waits for Enter before Codex opens its screen, which hides every line above. Press Enter (any line goes on; ctrl-C ends the start before Codex runs, and a new agent ended so is not kept: `status` lists none of it), then press Enter again at Codex's folder question before you type.

```text
Press Enter to open Codex.
```

Next step: none; it only informs.

Exit status: 0 (done).

### NAME_OTHER_TOOL

When: You picked a name with `--as` that belongs to the other tool: a Claude name for Codex, or the reverse. A name stays with the tool that first used it while its agent runs or its work is kept; for an agent that works without a terminal, the message gives the send that reaches it; for kept work, it says where it is and gives the command that picks it up from where you are; for an agent of the other tool that ended, it gives the command that continues it; for a name whose last agent ran as neither a Claude nor a Codex (one `dockingbird native launch` opened with another harness), nothing continues it, and the message says to pick another name. For kept work, an agent that ended, or a name neither tool continues, the message also gives the command that deletes the agent's copy, results and history, `dockingbird clean NAME --yes`, which frees the name.

If you deleted that branch, the message says `({branch}, no longer in your checkout)` where the forms below say `({branch})`, and its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where they say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

```text
{name} is a name for a {other}. Pick another name for this {harness}.
```

Or:

```text
{name} is a {other} that is running. Pick another name for this {harness},
or reconnect to it: dockingbird {other_tool} --as {name}
```

Or:

```text
{name} is a {other} that works on the bus. Pick another name for this {harness},
or send it a task: dockingbird send {name} TEXT
```

Or:

```text
{name} is a {other} whose copy is kept in {repo} ({branch}).
Pick another name for this {harness},
or pick it up: dockingbird {subcommand} --as {name}
Or delete its copy, results and history: dockingbird clean {name} --yes
```

Or:

```text
{name} is a {other} whose copy is kept in {repo} ({branch}).
Pick another name for this {harness},
or pick it up: git switch {branch}, then dockingbird {subcommand} --as {name}
Or delete its copy, results and history: dockingbird clean {name} --yes
```

Or:

```text
{name} is a {other} whose copy is kept in {repo} ({branch}).
Pick another name for this {harness},
or pick it up: cd {checkout}, then dockingbird {subcommand} --as {name}
Or delete its copy, results and history: dockingbird clean {name} --yes
```

Or:

```text
{name} is a {other} whose copy is kept in {repo} ({branch}).
Pick another name for this {harness},
or pick it up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
Or delete its copy, results and history: dockingbird clean {name} --yes
```

Or:

```text
{name} is a {other} whose copy is kept. Pick another name for this {harness},
or pick it up: dockingbird {subcommand} --as {name}
Or delete its copy, results and history: dockingbird clean {name} --yes
```

Or:

```text
{name} is a {other} that ended. Pick another name for this {harness},
or continue it: dockingbird {subcommand} --as {name}
Or delete its copy, results and history: dockingbird clean {name} --yes
```

Or:

```text
{name} ran as neither a Claude nor a Codex, so nothing here continues it.
Pick another name for this {harness}.
Or delete its copy, results and history: dockingbird clean {name} --yes
```

Or, if you deleted that branch:

```text
{name} is a {other} whose copy is kept in {repo} ({branch}, no longer in your checkout).
Pick another name for this {harness},
or pick it up: git switch -c {branch} dockingbird/{branch}, then dockingbird {subcommand} --as {name}
Or delete its copy, results and history: dockingbird clean {name} --yes
```

Next step, as the message gives it:

- Pick another name for this {harness}.
- dockingbird {other_tool} --as {name}
- dockingbird send {name} TEXT
- dockingbird {subcommand} --as {name}
- git switch {branch}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}

Exit status: 1 (a problem Dockingbird printed).

### NAME_OTHER_COMMAND

When: You picked up an agent with `--as` by a command other than the one it ran: a config's command for an agent of `dockingbird claude` or `codex`, the tool's own command for an agent of a config's command, or a terminal for an agent that worked without one, whose messages that terminal can't read. An agent goes on only as it ran, so the message gives the command that continues it; nothing was started. With `dockingbird claude` or `codex`, it says so only for an agent whose config runs it without a terminal. When the agent's config is no longer the one that gives its command here (a renamed config file, or the command moved to another config), nothing can continue it, and the message gives the bare start of a new agent instead.

```text
{name} is a {config_command} agent. Continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} is a {tool} agent of this checkout, not {command}'s.
Continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} works on the bus, which this terminal can't read.
Continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} runs on the bus only, as its config says. Continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} is a {config_command} agent of the config {config},
which isn't the one that gives {config_command} here, so it can't be continued.
Start a new one: dockingbird {subcommand}
```

Next step, as the message gives it:

- dockingbird {subcommand} --as {name}
- dockingbird {subcommand}

Exit status: 1 (a problem Dockingbird printed).

### COPY_OTHER_ENVIRONMENT

When: You started an agent by name, and the work kept under that name ran in another setup, such as another command's or one without a terminal. This start can't take it, so nothing was started; `dockingbird status NAME` gives the command that picks it up.

```text
{name}'s kept copy ran in another setup, so this start can't take it.
Pick it up as status shows: dockingbird status {name}
```

Next step: dockingbird status {name}

Exit status: 1 (a problem Dockingbird printed).

### NAME_HAS_WORK_ELSEWHERE

When: You started an agent by name, and its work is kept on another branch or in another checkout. The message gives the command that picks it up from where you are; nothing was copied or started.

If you deleted that branch, the message says `({branch}, no longer in your checkout)` where the forms below say `({branch})`, and its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where they say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

```text
{name} has work kept in {repo} ({branch}).
To pick it up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} has work kept in {repo} ({branch}).
To pick it up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} has work kept in {repo} ({branch}).
To pick it up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} has work kept on another branch. See where: dockingbird status {name}
```

Or, if you deleted that branch:

```text
{name} has work kept in {repo} ({branch}, no longer in your checkout).
To pick it up: git switch -c {branch} dockingbird/{branch}, then dockingbird {subcommand} --as {name}
```

Next step, as the message gives it:

- git switch {branch}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
- dockingbird status {name}

Exit status: 1 (a problem Dockingbird printed).

### NAME_ENDED_ELSEWHERE

When: You continued an agent with `dockingbird claude --as NAME` (or `codex`), and it last worked on another repository. Its conversation is about that code, so the message gives the command that continues it there, from where you are; nothing was started.

If you deleted that branch, the message says `({branch}, no longer in your checkout)` where the forms below say `({branch})`, and its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where they say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

```text
{name} ended in {repo} ({branch}).
To continue it: git switch {branch}, then dockingbird {subcommand} --as {name}
Or start a new agent under that name here: dockingbird {subcommand} --new --as {name}
```

Or:

```text
{name} ended in {repo} ({branch}).
To continue it: cd {checkout}, then dockingbird {subcommand} --as {name}
Or start a new agent under that name here: dockingbird {subcommand} --new --as {name}
```

Or:

```text
{name} ended in {repo} ({branch}).
To continue it: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
Or start a new agent under that name here: dockingbird {subcommand} --new --as {name}
```

Or:

```text
{name} ended on another repository. See where: dockingbird status {name}
Or start a new agent under that name here: dockingbird {subcommand} --new --as {name}
```

Or, if you deleted that branch:

```text
{name} ended in {repo} ({branch}, no longer in your checkout).
To continue it: git switch -c {branch} dockingbird/{branch}, then dockingbird {subcommand} --as {name}
Or start a new agent under that name here: dockingbird {subcommand} --new --as {name}
```

Next step, as the message gives it:

- git switch {branch}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
- dockingbird status {name}

Exit status: 1 (a problem Dockingbird printed).

### NAME_HAS_WORK_KEPT

When: You started an agent with `--as` and `--new`, but that name's work is still kept. A name has one copy, so the message gives the command that picks the work up from where you are, or starts a new agent under a name of its own; nothing was copied or started. Every form also gives the command that deletes the agent's copy, results and history, `dockingbird clean NAME --yes`, which frees the name.

If you deleted that branch, the message says `({branch}, no longer in your checkout)` where the forms below say `({branch})`, and its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where they say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

```text
{name} has work kept, so --new can't take its name.
Pick it up: dockingbird {subcommand} --as {name}
Or start a new {harness}: dockingbird {tool} --new
Or delete its copy, results and history: dockingbird clean {name} --yes
```

Or:

```text
{name} has work kept in {repo} ({branch}), so --new can't take its name.
To pick it up: git switch {branch}, then dockingbird {subcommand} --as {name}
Or start a new {harness}: dockingbird {tool} --new
Or delete its copy, results and history: dockingbird clean {name} --yes
```

Or:

```text
{name} has work kept in {repo} ({branch}), so --new can't take its name.
To pick it up: cd {checkout}, then dockingbird {subcommand} --as {name}
Or start a new {harness}: dockingbird {tool} --new
Or delete its copy, results and history: dockingbird clean {name} --yes
```

Or:

```text
{name} has work kept in {repo} ({branch}), so --new can't take its name.
To pick it up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
Or start a new {harness}: dockingbird {tool} --new
Or delete its copy, results and history: dockingbird clean {name} --yes
```

Or:

```text
{name} has work kept on another branch, so --new can't take its name.
See where: dockingbird status {name}
Or start a new {harness}: dockingbird {tool} --new
Or delete its copy, results and history: dockingbird clean {name} --yes
```

Or, if you deleted that branch:

```text
{name} has work kept in {repo} ({branch}, no longer in your checkout), so --new can't take its name.
To pick it up: git switch -c {branch} dockingbird/{branch}, then dockingbird {subcommand} --as {name}
Or start a new {harness}: dockingbird {tool} --new
Or delete its copy, results and history: dockingbird clean {name} --yes
```

Next step, as the message gives it:

- dockingbird {subcommand} --as {name}
- git switch {branch}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
- dockingbird status {name}

Exit status: 1 (a problem Dockingbird printed).

### NAME_INVALID

When: You gave `--as` a name with characters an agent name can't have, or `host`, Dockingbird's name for you, the parent; or you gave `dockingbird mcp install --connected` a name with such characters. Names use lowercase letters, digits and `-`; for a name with other characters, the `--as` message suggests the closest one.

```text
dockingbird {command}: '{word}' can't be a name; use lowercase letters, digits and -.
Try: dockingbird {command} --as {suggestion}
```

Or:

```text
dockingbird {command}: '{word}' can't be a name; use lowercase letters, digits and -.
```

Or:

```text
{name} is Dockingbird's name for you, the parent. Pick another name.
```

Next step, as the message gives it:

- dockingbird {command} --as {suggestion}
- none, where the message only informs

Exit status: 2 (usage).

### START_CONFIG_FIXED

When: You started a config's command with `--harness`, `--terminal`, `--bus` or `--egress`, and the config file fixes that setting to another value (a start on the bus passes `--bus`, so a command whose `mode` is `terminal` is refused there instead of taking the terminal the start runs on). Nothing was started; drop the flag, or change the file.

```text
{command} runs with {key} = {value}: {file} says so.
Drop the flag, or change the file.
```

Next step: none; it only informs.

Exit status: 2 (usage).

### START_CPUS_INVALID

When: You gave `--cpus` a value that isn't a number of CPUs above zero: a whole number such as `2`, or one with a point such as `1.5` (at most nine digits after it). Nothing was started.

```text
dockingbird {command}: --cpus takes a count of CPUs above zero, such as 2 or 1.5, not '{value}'.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### START_MEMORY_INVALID

When: You gave `--memory` a value that isn't a size: a whole number above zero followed by its unit, `b`, `k`, `m` or `g` (`512m`, `4g`). Nothing was started.

```text
dockingbird {command}: --memory takes a size above zero with its unit,
b, k, m or g, such as 4g or 512m, not '{value}'.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### START_CPU_SHARES_INVALID

When: You gave `start --cpu-shares` (or a config's command) a value that isn't a whole CPU weight from 2 to 262144, such as `1024`. Nothing was started.

```text
dockingbird {command}: --cpu-shares takes a whole CPU weight from 2 to
262144, such as 1024, not '{value}'.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### START_PIDS_LIMIT_INVALID

When: You gave `start --pids-limit` a value that isn't a whole count of processes from 1 to 4194304, such as `512`. Nothing was started.

```text
dockingbird {command}: --pids-limit takes a whole count of processes
from 1 to 4194304, such as 512, not '{value}'.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### START_COMPACT_AT_INVALID

When: You gave `start --compact-at` (or a config's command) a value in no form Claude Code's own `/autocompact` takes (`auto`, a token count, `500k`, `1M`, or `500` for 500 thousand), or outside the agent's range: for a Claude Code agent 100K to 1M, the range its docs give (another value it would clamp or ignore without a word); for a Codex agent any count of tokens, since Codex documents no range. Nothing was started.

```text
dockingbird {command}: {field} (--compact-at), the compact point, must be
auto, or 100K to 1M tokens in Claude Code's own forms:
500000, 500k, 1M, or 500 for 500 thousand.
See: dockingbird {command} -h
```

Or:

```text
dockingbird {command}: {field} (--compact-at), the compact point, must be
auto, or a count of tokens in these forms:
500000, 500k, 1M, or 500 for 500 thousand.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### START_SESSION_HOURS_INVALID

When: You gave `start --session-hours` (or a config's command) a value that isn't a whole number of hours from 1 to 168, such as `48`: the most the agent may run before it ends itself. Nothing was started.

```text
dockingbird {command}: {field} (--session-hours), the hours the agent may
run, must be a whole number from 1 to 168, such as 48.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### START_SWARM_INVALID

When: You gave `start --swarm` (or a config's command) a name that isn't a swarm's name: lowercase letters, digits and `-`, up to 63 characters, the same rule as an agent's name in `--as`. Nothing was started.

```text
dockingbird {command}: --swarm takes a swarm's name, lowercase letters, digits
and -, up to 63 characters, not '{swarm}'.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### START_ROLE_INVALID

When: You gave `start --role` a name that isn't a role's name: lowercase letters, digits and `-`, up to 63 characters. Nothing was started.

```text
dockingbird {command}: --role takes a role's name, lowercase letters, digits
and -, up to 63 characters, not '{role}'.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### START_ROLE_NEEDS_SWARM

When: You gave `start --role` (or the engine's own `--engine`) without `--swarm`. A role is a place in a swarm, so name the swarm the agent joins. Nothing was started.

```text
dockingbird {command}: {option} works only with --swarm, the swarm the agent joins.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### START_ENGINE_INVALID

When: You gave `start --engine`, the fleet engine's own mark, a value that isn't a workload's id (a UUID). A person never types it; drop it. Nothing was started.

```text
dockingbird {command}: --engine takes a workload's id, a UUID, not '{value}'.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### START_EGRESS_UNTRUSTED

When: You started a command from a repo's own `.dockingbird/` folder, in a checkout that isn't trusted on this Mac (one you marked with `dockingbird trust --off`, or one with no mark while `config.toml` in Dockingbird's folder says `trust = "untrusted"`), whose `egress` would let the agent reach more than this computer's default does: `full`, or an `allow` entry the default's hosts don't cover. A repo you don't trust can't widen what its agents reach, so nothing was started. Keep to hosts the default covers, use `models`, or mark the checkout trusted with `dockingbird trust`.

```text
{command} asks for egress = {mode}, wider than this computer's default,
and {file} is in a checkout that isn't trusted on this Mac, so nothing was started.
Write an entry the installation default covers, or egress = "models",
or run dockingbird trust for this checkout.
```

Next step: Write an entry the installation default covers, or egress = "models", or run dockingbird trust for this checkout.

Exit status: 1 (a problem Dockingbird printed).

### EGRESS_PROXY_FAILED

When: You started an agent whose egress is `models` or `allowlist`, and the proxy that keeps it to its allowed hosts didn't start or didn't answer in time. Everything the start made was removed. The message shows the proxy's last lines, or what Docker said when it printed none.

```text
{name}'s egress proxy didn't start, so nothing was started. Its last lines:
{entries}
Run this again.
```

Or:

```text
{name}'s egress proxy didn't start, so nothing was started. Docker said:
  {said}
Run this again.
```

Next step: Run this again.

Exit status: 1 (a problem Dockingbird printed).

### EGRESS_LOG_ROW

When: One line of an agent's egress proxy's log, under the message that says the proxy didn't start.

One row of a table; its cells line up with the rows around it.

```text
  {line}
```

Next step: none; it only informs.

Exit status: 0 (done).

### START_NETWORK_POOLS_FULL

When: You started an agent, and Docker couldn't make the agent's own network: every address range of its address pools is taken. Docker's default pools hold about 30 networks, shared by every Docker network on this computer: your running agents', another Dockingbird folder's and other programs'. Dockingbird removed its own unused networks first, so nothing was started. `docker network ls` lists the networks; `docker network prune` removes every network no container uses, other programs' included; or add pools to Docker's `default-address-pools` setting (in Docker Desktop: Settings > Docker Engine), then run the command again.

```text
Docker has no address range left for {name}'s own network, so nothing was started.
Other networks use every range; Dockingbird removed its own unused ones.
To see them: docker network ls
To remove every network no container uses, other programs' included:
docker network prune
Or give Docker more address pools: its Engine setting default-address-pools.
```

Next step: docker network ls

Exit status: 1 (a problem Dockingbird printed).

### EGRESS_FILE_INVALID

When: You started an agent, ran `dockingbird status` or ran `dockingbird egress`, and `egress.toml` in Dockingbird's folder, the file `dockingbird egress` writes, can't be read as written: it isn't TOML, it has a line other than `egress` and `allow`, `egress` is missing or isn't one of the four modes, `allow` is missing under `allowlist`, is left over beside another mode or has something that isn't a host or a preset, or the file is a link or too large, or is a folder. No agent starts on a guess, so fix the file, or remove it with `dockingbird egress --reset` to go back to Dockingbird's own default. A folder is the one thing `dockingbird egress --reset` and a new mode both refuse and leave as it is, since it may be yours: move it aside (rename it, or move it out of Dockingbird's folder), then run the command again. Only `dockingbird clean --all`, which empties Dockingbird's folder, removes it with the rest. `dockingbird status` only looks, so it says this in the place of its egress line and still exits 0; a start and `dockingbird egress` exit 1.

```text
{path}: egress must be one of: {choices}.
No new agent starts until it is fixed.
Fix it, or run dockingbird egress --reset to remove it.
```

Or:

```text
{path}: {key} isn't right.
With allowlist, allow is a list of hosts and presets, such as
["registries", "docs.python.org"].
No new agent starts until it is fixed.
Fix it, or run dockingbird egress --reset to remove it.
```

Or:

```text
{path}: allow works only with egress = "allowlist".
No new agent starts until it is fixed.
Fix it, or run dockingbird egress --reset to remove it.
```

Or:

```text
{path} has a line that isn't egress or allow.
No new agent starts until it is fixed.
Fix it, or run dockingbird egress --reset to remove it.
```

Or:

```text
{path} isn't TOML. It is egress = "MODE" and, with allowlist,
allow = ["HOST", ...].
No new agent starts until it is fixed.
Fix it, or run dockingbird egress --reset to remove it.
```

Or:

```text
{path} isn't a regular file of yours, or is too large to read.
No new agent starts until it is fixed.
Remove it, then run this again.
```

Or:

```text
{path} is a folder, not Dockingbird's egress file.
No new agent starts while it is there; only dockingbird clean --all removes it.
Move it aside, then run this again.
```

Next step, as the message gives it:

- Fix it, or run dockingbird egress --reset to remove it.
- Remove it, then run this again.
- Move it aside, then run this again.

Exit status: 0 (done) or 1 (a problem Dockingbird printed), as "When:" says.

### EGRESS_SHOWN

When: You ran `dockingbird egress` with no argument: what new agents may reach, the `allow` list of `allowlist`, and whether `egress.toml` sets it or it is Dockingbird's own default.

```text
Egress for new agents: {mode} ({allow}).
Set in {path}.
```

Or:

```text
Egress for new agents: {mode}.
Set in {path}.
```

Or:

```text
Egress for new agents: {mode}.
Nothing is set: this is Dockingbird's own default.
```

Next step: none; it only informs.

Exit status: 0 (done).

### EGRESS_SET

When: You ran `dockingbird egress` with a mode, such as `models` or `allowlist --allow github`, and it wrote `egress.toml`. New agents get that; agents already running keep what they started with.

```text
Egress for new agents is now {mode} ({allow}).
Agents already running keep theirs.
```

Or:

```text
Egress for new agents is now {mode}.
Agents already running keep theirs.
```

Next step: none; it only informs.

Exit status: 0 (done).

### EGRESS_RESET

When: You ran `dockingbird egress --reset`, which removes `egress.toml` (or finds none). New agents get Dockingbird's own default again.

```text
Egress for new agents is Dockingbird's own default: {mode}.
Agents already running keep theirs.
```

Next step: none; it only informs.

Exit status: 0 (done).

### EGRESS_ENTRY_INVALID

When: You gave `dockingbird egress` an `--allow` entry that isn't a host such as `docs.python.org`, or `*.corp.example` for every name under it, or a preset (`registries`, `github`), or more entries than an allow list takes. The message names the entry by its number among your `--allow` options, and nothing was written.

```text
dockingbird {command}: --allow number {index} isn't a host or a preset.
A host is a name such as docs.python.org, or *.corp.example for
every name under it; a preset is registries or github.
See: dockingbird {command} -h
```

Or:

```text
dockingbird {command}: --allow takes at most {count} entries.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### AGENT_RUNNING_ARGS

When: You gave `--as` with arguments for the tool, with `--egress`, or with `--new`, for an agent that is already running. A running agent can't take new arguments or another egress, and `--new` can't take its name; you can reconnect to it or stop it, and with `--new` start a new agent under a name of its own. With `dockingbird start --as`, the agent runs already, so the message says how to send it a task instead. `dockingbird claude --as NAME` (or `codex`) of an agent that works on the bus, or whose container is gone, says the same: there is no terminal to reconnect to. Dockingbird itself refuses to start a second agent under a name that is running, so the same words come back when an agent started between the check and the start. The still-starting form: another command is starting the agent right now; a task you send reaches it once it runs. When that command starts it at a terminal (Codex waiting there for Enter before it opens, say), the message says to use it in that terminal instead: a terminal agent reads a task when you type in it. The form that asks you to run the command again: another command is starting an agent with no name yet, which may be this one, and is still making its copy, which takes minutes for a big repository's first agent.

```text
{name} is already running, so it can't take these arguments.
Reconnect to it without them: dockingbird {tool} --as {name}
```

Or:

```text
{name} is already running, so it can't take these arguments.
Use its terminal, or stop it: dockingbird stop {name}
```

Or:

```text
{name} is already running, so --new can't take its name.
Reconnect to it: dockingbird {tool} --as {name}
Or start a new {harness}: dockingbird {tool} --new
```

Or:

```text
{name} is already running, so --new can't take its name.
Use its terminal, or stop it: dockingbird stop {name}
Or start a new {harness}: dockingbird {tool} --new
```

Or:

```text
{name} is already running, so it can't start again.
Send it a task: dockingbird send {name} TEXT
```

Or:

```text
{name} is still starting in another dockingbird command, so it can't start again.
Send it a task: dockingbird send {name} TEXT
```

Or:

```text
{name} is still starting in another dockingbird command, so it can't start again.
Use it in the terminal where it is starting.
```

Or:

```text
{name} can't start while another start is still making its agent's copy.
Run this again once it has.
```

Next step, as the message gives it:

- dockingbird {tool} --as {name}
- dockingbird stop {name}
- dockingbird send {name} TEXT
- Use it in the terminal where it is starting.
- Run this again once it has.

Exit status: 1 (a problem Dockingbird printed).

### AGENT_UNKNOWN

When: You named an agent, with `stop`, `status`, `send`, `read`, `results` or `inspect config --agent`, that isn't running and has no work kept, or one that isn't running with `wait`.

```text
No agent named {name} is running or has work kept. See: dockingbird status
```

Next step: dockingbird status

Exit status: 1 (a problem Dockingbird printed).

### START_MERGE_OFFER

When: You started an agent on a branch where you and the agents both have new commits. Dockingbird offers to merge theirs into yours first, so the agent starts from both.

```text
{repo} ({branch}): you and the agents both have new commits.
{commits}
Merge theirs into yours now, then start {harness}? [Y/n]
```

Next step: press Enter (or answer y) to go on; anything else is no

Exit status: 1 (a problem Dockingbird printed), unless you go on at its question; then the command ends with its own status.

### BOTH_MOVED_ROW

When: One commit in a list of new commits on both sides, yours or the agents'.

One row of a table; its cells line up with the rows around it.

```text
  yours    {commit}  {subject}
```

Or:

```text
           {commit}  {subject}
```

Or:

```text
  agents   {commit}  {subject}     ({name})
```

Or:

```text
           {commit}  {subject}     ({name})
```

Next step: none; it only informs.

Exit status: 0 (done).

## Agents: reconnecting and resuming

### AGENT_RECONNECTING

When: You started the tool with no arguments, or with `--as` and the name of one of its agents, while that agent was still working without a terminal, so this terminal reconnects to it.

```text
Reconnecting to {name} (still running from an earlier terminal).
  Another Claude instead:  dockingbird claude --new
  Stop this one:           dockingbird stop {name}
```

Or:

```text
Reconnecting to {name} (still running from an earlier terminal).
  Another Codex instead:  dockingbird codex --new
  Stop this one:          dockingbird stop {name}
```

Next step: none; it only informs.

Exit status: 0 (done).

### AGENTS_WITHOUT_TERMINAL

When: You started the tool with no arguments while two or more of its agents work without a terminal. The message lists the command for each.

```text
{names:and} are running without a terminal. Reconnect to one:
{entries}
Or start another: dockingbird {tool} --new
```

Next step: dockingbird {tool} --new

Exit status: 1 (a problem Dockingbird printed).

### AS_HINT_ROW

When: One agent's reconnect command, in a list of them.

One row of a table; its cells line up with the rows around it.

```text
  dockingbird {tool} --as {name}
```

Next step: none; it only informs.

Exit status: 0 (done).

### AGENT_RESUMING

When: An agent picks up its own kept copy: the line says what the copy has (beside the files it counted, that it may also hold commits not shared yet when Dockingbird couldn't count those), and how to start fresh instead.

```text
Resuming {name}: {count:commit|commits} not shared yet.
{others}
(Start fresh instead: dockingbird {tool} --new)
```

Or:

```text
Resuming {name}: {count:file|files} not committed.
{others}
(Start fresh instead: dockingbird {tool} --new)
```

Or:

```text
Resuming {name}: {count:file|files} not committed; it may also hold commits not shared yet.
{others}
(Start fresh instead: dockingbird {tool} --new)
```

Or:

```text
Resuming {name} where it stopped.
{others}
(Start fresh instead: dockingbird {tool} --new)
```

Next step: dockingbird {tool} --new

Exit status: 0 (done).

### ALSO_HAS_WORK_ROW

When: Another agent, of either tool, also has work kept on this branch; the line gives the command that picks it up.

One row of a table; its cells line up with the rows around it.

```text
({name} also has work here: dockingbird {subcommand} --as {name})
```

Next step: none; it only informs.

Exit status: 0 (done).

### OTHERS_HAVE_WORK

When: You started a new agent while other agents, of either tool, have work kept on this branch: one line each, with the command that picks it up.

```text
{others}
```

Next step: none; it only informs.

Exit status: 0 (done).

### AGENT_OPEN_ELSEWHERE

When: You asked for an agent that another terminal is showing, and Dockingbird couldn't move it here: that terminal belongs to another user or to an older Dockingbird, or it didn't let go of the agent when asked, and the line names its process, or it ended but its connection to the agent stayed open. One terminal shows an agent at a time.

```text
{name} is open in another terminal. Use that one, or stop it:
dockingbird stop {name}
```

Or:

```text
{name} is open in another terminal, and its process {pid} did not answer in {seconds:second|seconds}.
Use that one, or stop it: dockingbird stop {name}
```

Next step: dockingbird stop {name}

Exit status: 1 (a problem Dockingbird printed).

## Agents: ending

### AGENT_KEEPS_WORKING

When: The terminal let go of the agent (you closed the window, or the connection dropped), and it keeps working. The line gives the command that reconnects.

```text
{name} keeps working without a terminal: dockingbird {tool} --as {name}
```

Or:

```text
{name} keeps working on the bus, with or without its screen shown.
To show its screen again: dockingbird {tool} --as {name}
```

Next step: dockingbird {tool} --as {name}

Exit status: 0 (done).

### AGENT_SCREEN_HELD

When: A message for an agent waits because its screen has something you typed and did not send, or a menu you opened: Dockingbird never types a message over your typing. Send what you typed in that screen and the message goes in. Left unsent, once the message's wait has been told and no key has come for five minutes, Dockingbird clears it itself, the way you would, and the message goes in. When the screen took bytes, the line says what kind, when, how many bytes that read had and the bytes that decided it in hex, so a key can be told from a terminal's answer.

```text
A message waits until you finish typing in {name}'s screen.
```

Or:

```text
A message waits until you finish typing in {name}'s screen. It took
{touch_kind} at {touch_at}, in a read of {touch_bytes:byte|bytes}; the bytes that decided it, in hex: {touch_head}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### DELIVERY_HELD_IN_SCREEN

When: A message you or another agent sent has waited a while at the agent's screen: someone is typing in it, its tool hasn't started yet or is still working, or its screen is still drawing. It says so once, in the message's own thread, with how long the message has waited and which of these keeps it waiting, and the message goes in once that is over: the typing sent, the tool at its prompt and done, its screen still. Typing left unsent is cleared by Dockingbird once that has been said and no key has come for five minutes, which it says once more; a box taller than the screen, or a menu left open, can keep text the clear does not reach, and the message's turn is then told as failed. When the screen took bytes, the line says what kind, when, how many bytes that read had and the bytes that decided it in hex, so a key can be told from a terminal's answer.

```text
This message has waited {elapsed} for {name}.
Someone is typing in its screen.
```

Or:

```text
This message has waited {elapsed} for {name}.
Its tool has not started yet.
```

Or:

```text
This message has waited {elapsed} for {name}.
Its tool is still working.
```

Or:

```text
This message has waited {elapsed} for {name}.
Its screen is still drawing.
```

Or:

```text
Cleared unsent text left in {name}'s screen.
This message had waited {elapsed}.
```

Or:

```text
This message has waited {elapsed} for {name}: its screen took {touch_kind} at {touch_at} (in a read of
{touch_bytes:byte|bytes}; the bytes that decided it, in hex: {touch_head}), and no turn has ended since.
```

Next step: none; it only informs.

Exit status: 0 (done).

### TURN_UNSIGNALLED

When: A message you or another agent sent went into a Codex agent's screen, and no sign came that its work was done: nothing was drawn after it for the time a tool takes to show it took a message, or what was drawn then stopped for that long. Dockingbird stops waiting for that one message and says which, in its own thread; the agent goes on, and sits idle when it has nothing to do.

```text
No completion signal; nothing drawn for {elapsed} after the paste.
```

Or:

```text
No completion signal; the drawing still for {elapsed} since its last change.
```

Next step: none; it only informs.

Exit status: 0 (done).

### TURN_COMPLETION_UNSEEN

When: A message went into a Codex agent's screen and the agent took it: its screen showed it at work. Then its screen stayed still with no sign that the work was done, as when the agent asks a question of its own and waits for the answer. Dockingbird stops waiting for that one message and says so in its own thread; the message counts as read and is not told as failed. Look at the agent's screen: it may be waiting for an answer.

```text
{name} took this message, but its completion was not seen.
Turn {number} is counted as completed.
```

Next step: none; it only informs.

Exit status: 0 (done).

### TURN_INTERRUPTED_BY_OWNER

When: While an agent worked on a message, the owner pressed Esc or Ctrl-C in its screen, and the next thing it worked on was a line of the owner's own: one they sent while it worked, or right after the key. The message's turn ended there, so this summary carries no result: what the agent answered next was the owner's line, and stays with it. Whatever the agent had already sent or done for the message stands.

```text
The owner interrupted this message's turn in {name}'s screen.
Turn {number} ended there.
```

Next step: none; it only informs.

Exit status: 0 (done).

### TURN_DEADLINE_IN_OWNERS_TURN

When: While an agent worked on a message, the owner pressed Esc or Ctrl-C in its screen, and the agent then worked on a turn of the owner's own there. The message's time ran out while that turn ran. Dockingbird ends a message's turn at its deadline by pressing Esc, but never presses a key in the owner's own turn, so it pressed none: the message's turn ended there, with no result, and the owner's turn went on. Whatever the agent had already sent or done for the message stands.

```text
This message's turn passed its deadline in {name}'s screen.
Turn {number} ended while the owner's own turn ran.
No key was typed into it.
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_UNSENDABLE

When: An agent's Dockingbird made a status for you, such as the summary of a message's turn, that the bus would refuse, for instance with a subject longer than it takes. You should never see this; it is a bug. The status still came, its subject and words in the body, and the agent goes on with its next message.

```text
Dockingbird made a status the bus would refuse.
Its {field} broke the bus's rules: {code}.
Its subject and words follow.
This is a Dockingbird bug.
Please report it: https://github.com/zeus-fyi/dockingbird/issues
```

Next step: https://github.com/zeus-fyi/dockingbird/issues

Exit status: 0 (done).

### AGENT_TAKEN_OVER

When: You opened this agent in another terminal (or with Enter in `dockingbird ui`), so this terminal let go of it. The agent keeps working there. The line gives the command that shows it here again.

```text
{name} is now shown in another terminal. It keeps working.
To show it here again: dockingbird {tool} --as {name}
```

Next step: dockingbird {tool} --as {name}

Exit status: 0 (done).

### AGENT_DONE

When: The agent ended after sharing commits on its branch. The line says "done" only when the tool ended normally; otherwise it gives the tool's status, and the command ends with it. Its last line gives the command that continues the agent's conversation.

If you deleted that branch, its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where the forms below say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

```text
{name} is done: {count:commit|commits} shared on {branch}. Get them: dockingbird sync
To continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} is done: {count:commit|commits} shared on {branch}. Get it: dockingbird sync
To continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} ended with status {status} after sharing {count:commit|commits} on {branch}. Get them: dockingbird sync
To continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} ended with status {status} after sharing {count:commit|commits} on {branch}. Get it: dockingbird sync
To continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} is done: {count:commit|commits} shared on {branch}.
Get them: git switch {branch}, then dockingbird sync
To continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} is done: {count:commit|commits} shared on {branch}.
Get them: cd {checkout}, then dockingbird sync
To continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} is done: {count:commit|commits} shared on {branch}.
Get them: cd {checkout}, then git switch {branch}, then dockingbird sync
To continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} is done: {count:commit|commits} shared on {branch}.
Get it: git switch {branch}, then dockingbird sync
To continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} is done: {count:commit|commits} shared on {branch}.
Get it: cd {checkout}, then dockingbird sync
To continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} is done: {count:commit|commits} shared on {branch}.
Get it: cd {checkout}, then git switch {branch}, then dockingbird sync
To continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} ended with status {status} after sharing {count:commit|commits} on {branch}.
Get them: git switch {branch}, then dockingbird sync
To continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} ended with status {status} after sharing {count:commit|commits} on {branch}.
Get them: cd {checkout}, then dockingbird sync
To continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} ended with status {status} after sharing {count:commit|commits} on {branch}.
Get them: cd {checkout}, then git switch {branch}, then dockingbird sync
To continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} ended with status {status} after sharing {count:commit|commits} on {branch}.
Get it: git switch {branch}, then dockingbird sync
To continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} ended with status {status} after sharing {count:commit|commits} on {branch}.
Get it: cd {checkout}, then dockingbird sync
To continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} ended with status {status} after sharing {count:commit|commits} on {branch}.
Get it: cd {checkout}, then git switch {branch}, then dockingbird sync
To continue it: dockingbird {subcommand} --as {name}
```

Or, if you deleted that branch:

```text
{name} is done: {count:commit|commits} shared on {branch}.
Get them: git switch -c {branch} dockingbird/{branch}, then dockingbird sync
To continue it: dockingbird {subcommand} --as {name}
```

Next step, as the message gives it:

- dockingbird sync
- git switch {branch}, then dockingbird sync
- cd {checkout}, then dockingbird sync
- cd {checkout}, then git switch {branch}, then dockingbird sync

Exit status: 0 (done), or the tool's own status when the agent's run failed.

### AGENT_DONE_NOTHING

When: The agent ended without sharing anything new. The line says "done" only when the tool ended normally. Its last line gives the command that continues the agent's conversation.

```text
{name} is done. Nothing new to share.
To continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} ended with status {status}. Nothing new to share.
To continue it: dockingbird {subcommand} --as {name}
```

Next step: dockingbird {subcommand} --as {name}

Exit status: 0 (done), or the tool's own status when the agent's run failed.

### AGENT_REFUSED

When: Dockingbird stopped the agent before its tool ran. The line says why, in one of these words: `{harness} isn't signed in`, `{harness}'s sign-in check failed`, `its provider refused the saved {harness} key`, `{harness}'s settings couldn't be written`, `a file for {harness} isn't safe to use`, `its key and rules folder isn't safe to use`, `the saved {harness} API key can't be used`, `your rules for {harness} can't be used`, `the repo's config replaces {harness}'s rules`, `an argument for {harness} isn't allowed`, `{harness}'s saved sign-in isn't safe to use`, `{harness}'s saved sign-in can't be read`, `{harness}'s saved sign-in was busy`, `Dockingbird couldn't save {harness}'s sign-in`, `Dockingbird's own folder isn't safe to use`, `its copy wasn't where it should be`, `it couldn't talk to Dockingbird`, `its log folder isn't safe to use`, `its home folder isn't private`, `Dockingbird couldn't confirm its identity`, `another container already runs it`, `{harness}'s version isn't installed`, `its environment couldn't be set up`, `its dependencies couldn't be installed`, `its dependencies couldn't install offline`, `one of Dockingbird's settings isn't valid`, `a Dockingbird variable isn't one it reads`, `{harness} wouldn't read its given file`, `its given file couldn't be put in its copy`, `its given file would overwrite its changes`, or `Dockingbird couldn't get it ready`; and it names the log. When it says your rules can't be used, the rules file in Dockingbird's `instructions` folder isn't plain UTF-8 text, or it is so long that it no longer fits once Dockingbird adds the line naming the agent and its own rules: shorten it. When the provider refused the saved key, save a working one with `dockingbird login claude --api-key` or `dockingbird login codex --api-key`.

```text
{name} stopped before it started: {why}.
Log: {log}
```

Or:

```text
{name} stopped before it started: {why}.
Its copy is kept: dockingbird {subcommand} --as {name}
Log: {log}
```

Or:

```text
{name} stopped: {why}.
Log: {log}
```

Or:

```text
{name} stopped: {why}.
Its copy is kept: dockingbird {subcommand} --as {name}
Log: {log}
```

Or:

```text
{name} stopped before it started: {why}.
To use your file now, run the same command again with --new; this agent's
copy is kept with its change.
Log: {log}
```

Next step, as the message gives it:

- none, where the message only informs
- dockingbird {subcommand} --as {name}
- To use your file now, run the same command again with --new; this agent's copy is kept with its change.

Exit status: 1 (a problem Dockingbird printed).

### AGENT_STOPPED_NOT_SHARED

When: The agent ended and its copy is kept: commits not shared yet, files not committed, or work Dockingbird couldn't count. The line says "stopped", or "ended with status N" when the tool failed, and gives the command that picks the work up from where you are. It says "may" when Dockingbird couldn't count the copy's own commits: usually because the branch moved on since the copy started (another agent shared, or you sent your own commits), else because git couldn't read or fully count the copy. Nothing in it is lost: it stays kept, with its files and commits, until you pick it up or `dockingbird clean` removes it.

If you deleted that branch, its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where the forms below say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

```text
{name} stopped, with {count:commit|commits} not shared yet. Pick it up:
dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped, with {count:file|files} not committed. Pick it up:
dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped. Its copy is kept: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped, with {count:commit|commits} not shared yet. Pick it up:
git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped, with {count:commit|commits} not shared yet. Pick it up:
cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped, with {count:commit|commits} not shared yet. Pick it up:
cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped, with {count:file|files} not committed. Pick it up:
git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped, with {count:file|files} not committed. Pick it up:
cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped, with {count:file|files} not committed. Pick it up:
cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped. Its copy is kept:
git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped. Its copy is kept:
cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped. Its copy is kept:
cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped. Its copy is kept and may hold work:
dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped. Its copy is kept and may hold work:
git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped. Its copy is kept and may hold work:
cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped. Its copy is kept and may hold work:
cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or, if you deleted that branch:

```text
{name} stopped, with {count:commit|commits} not shared yet. Pick it up:
git switch -c {branch} dockingbird/{branch}, then dockingbird {subcommand} --as {name}
```

Next step, as the message gives it:

- dockingbird {subcommand} --as {name}
- git switch {branch}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}

Exit status: the tool's own status.

### AGENT_SHARED_AND_STOPPED

When: The agent shared commits and ended with more work left in its copy, or work Dockingbird couldn't count. The line says both ("ended with status N" in place of "stopped" when the tool failed), with the command that gets the commits and the one that picks up the rest, from where you are.

If you deleted that branch, its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where the forms below say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:file|files} not committed.
Get the commit: dockingbird sync
Pick the file up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:file|files} not committed.
Get the commit: dockingbird sync
Pick the files up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:commit|commits} not shared yet.
Get the shared one: dockingbird sync
Pick the other one up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:commit|commits} not shared yet.
Get the shared one: dockingbird sync
Pick the others up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped. Its copy is kept.
Get the commit: dockingbird sync
Pick it up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:file|files} not committed.
Get the commits: dockingbird sync
Pick the file up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:file|files} not committed.
Get the commits: dockingbird sync
Pick the files up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:commit|commits} not shared yet.
Get the shared ones: dockingbird sync
Pick the other one up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:commit|commits} not shared yet.
Get the shared ones: dockingbird sync
Pick the others up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped. Its copy is kept.
Get the commits: dockingbird sync
Pick it up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped. Its copy is kept and may hold work.
Get the commit: dockingbird sync
Pick it up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped. Its copy is kept and may hold work.
Get the commits: dockingbird sync
Pick it up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:file|files} not committed.
Get the commit: git switch {branch}, then dockingbird sync
Pick the file up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:file|files} not committed.
Get the commit: cd {checkout}, then dockingbird sync
Pick the file up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:file|files} not committed.
Get the commit: cd {checkout}, then git switch {branch}, then dockingbird sync
Pick the file up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:file|files} not committed.
Get the commit: git switch {branch}, then dockingbird sync
Pick the files up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:file|files} not committed.
Get the commit: cd {checkout}, then dockingbird sync
Pick the files up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:file|files} not committed.
Get the commit: cd {checkout}, then git switch {branch}, then dockingbird sync
Pick the files up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:commit|commits} not shared yet.
Get the shared one: git switch {branch}, then dockingbird sync
Pick the other one up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:commit|commits} not shared yet.
Get the shared one: cd {checkout}, then dockingbird sync
Pick the other one up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:commit|commits} not shared yet.
Get the shared one: cd {checkout}, then git switch {branch}, then dockingbird sync
Pick the other one up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:commit|commits} not shared yet.
Get the shared one: git switch {branch}, then dockingbird sync
Pick the others up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:commit|commits} not shared yet.
Get the shared one: cd {checkout}, then dockingbird sync
Pick the others up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:commit|commits} not shared yet.
Get the shared one: cd {checkout}, then git switch {branch}, then dockingbird sync
Pick the others up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped. Its copy is kept.
Get the commit: git switch {branch}, then dockingbird sync
Pick it up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped. Its copy is kept.
Get the commit: cd {checkout}, then dockingbird sync
Pick it up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped. Its copy is kept.
Get the commit: cd {checkout}, then git switch {branch}, then dockingbird sync
Pick it up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:file|files} not committed.
Get the commits: git switch {branch}, then dockingbird sync
Pick the file up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:file|files} not committed.
Get the commits: cd {checkout}, then dockingbird sync
Pick the file up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:file|files} not committed.
Get the commits: cd {checkout}, then git switch {branch}, then dockingbird sync
Pick the file up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:file|files} not committed.
Get the commits: git switch {branch}, then dockingbird sync
Pick the files up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:file|files} not committed.
Get the commits: cd {checkout}, then dockingbird sync
Pick the files up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:file|files} not committed.
Get the commits: cd {checkout}, then git switch {branch}, then dockingbird sync
Pick the files up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:commit|commits} not shared yet.
Get the shared ones: git switch {branch}, then dockingbird sync
Pick the other one up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:commit|commits} not shared yet.
Get the shared ones: cd {checkout}, then dockingbird sync
Pick the other one up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:commit|commits} not shared yet.
Get the shared ones: cd {checkout}, then git switch {branch}, then dockingbird sync
Pick the other one up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:commit|commits} not shared yet.
Get the shared ones: git switch {branch}, then dockingbird sync
Pick the others up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:commit|commits} not shared yet.
Get the shared ones: cd {checkout}, then dockingbird sync
Pick the others up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:commit|commits} not shared yet.
Get the shared ones: cd {checkout}, then git switch {branch}, then dockingbird sync
Pick the others up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped. Its copy is kept.
Get the commits: git switch {branch}, then dockingbird sync
Pick it up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped. Its copy is kept.
Get the commits: cd {checkout}, then dockingbird sync
Pick it up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped. Its copy is kept.
Get the commits: cd {checkout}, then git switch {branch}, then dockingbird sync
Pick it up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped. Its copy is kept and may hold work.
Get the commit: git switch {branch}, then dockingbird sync
Pick it up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped. Its copy is kept and may hold work.
Get the commit: cd {checkout}, then dockingbird sync
Pick it up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped. Its copy is kept and may hold work.
Get the commit: cd {checkout}, then git switch {branch}, then dockingbird sync
Pick it up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped. Its copy is kept and may hold work.
Get the commits: git switch {branch}, then dockingbird sync
Pick it up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped. Its copy is kept and may hold work.
Get the commits: cd {checkout}, then dockingbird sync
Pick it up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} shared {shared:commit|commits} on {branch} and stopped. Its copy is kept and may hold work.
Get the commits: cd {checkout}, then git switch {branch}, then dockingbird sync
Pick it up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or, if you deleted that branch:

```text
{name} shared {shared:commit|commits} on {branch} and stopped, with {count:file|files} not committed.
Get the commit: git switch -c {branch} dockingbird/{branch}, then dockingbird sync
Pick the file up: git switch -c {branch} dockingbird/{branch}, then dockingbird {subcommand} --as {name}
```

Next step, as the message gives it:

- dockingbird sync
- git switch {branch}, then dockingbird sync
- cd {checkout}, then dockingbird sync
- cd {checkout}, then git switch {branch}, then dockingbird sync

Exit status: the tool's own status.

### AGENT_CRASHED

When: The agent was killed, most likely because it ran out of memory. Its copy is kept, and the line gives the command that picks it up from where you are.

If you deleted that branch, its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where the forms below say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

```text
{name} crashed {ago} ago, probably out of memory (more memory: Docker
Desktop > Settings > Resources). Its copy is kept and may hold work:
dockingbird {subcommand} --as {name}
Log: {log}
```

Or:

```text
{name} crashed {ago} ago, probably out of memory (more memory: Docker
Desktop > Settings > Resources). Its copy is kept and may hold work:
git switch {branch}, then dockingbird {subcommand} --as {name}
Log: {log}
```

Or:

```text
{name} crashed {ago} ago, probably out of memory (more memory: Docker
Desktop > Settings > Resources). Its copy is kept and may hold work:
cd {checkout}, then dockingbird {subcommand} --as {name}
Log: {log}
```

Or:

```text
{name} crashed {ago} ago, probably out of memory (more memory: Docker
Desktop > Settings > Resources). Its copy is kept and may hold work:
cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
Log: {log}
```

Or:

```text
{name} crashed, probably out of memory (more memory: Docker
Desktop > Settings > Resources). Its copy is kept and may hold work:
dockingbird {subcommand} --as {name}
Log: {log}
```

Or:

```text
{name} crashed, probably out of memory (more memory: Docker
Desktop > Settings > Resources). Its copy is kept and may hold work:
git switch {branch}, then dockingbird {subcommand} --as {name}
Log: {log}
```

Or:

```text
{name} crashed, probably out of memory (more memory: Docker
Desktop > Settings > Resources). Its copy is kept and may hold work:
cd {checkout}, then dockingbird {subcommand} --as {name}
Log: {log}
```

Or:

```text
{name} crashed, probably out of memory (more memory: Docker
Desktop > Settings > Resources). Its copy is kept and may hold work:
cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
Log: {log}
```

Or, if you deleted that branch:

```text
{name} crashed {ago} ago, probably out of memory (more memory: Docker
Desktop > Settings > Resources). Its copy is kept and may hold work:
git switch -c {branch} dockingbird/{branch}, then dockingbird {subcommand} --as {name}
Log: {log}
```

Next step, as the message gives it:

- dockingbird {subcommand} --as {name}
- git switch {branch}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}

Exit status: 0 (done), or the tool's own status when the agent's run failed.

### AGENT_STOPPED_UNEXPECTEDLY

When: The agent ended for a reason Dockingbird can't name. Its work is kept; the line names its log and gives the command that picks it up from where you are.

If you deleted that branch, the message says `({branch}, no longer in your checkout)` where the forms below say `({branch})`, and its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where they say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

```text
{name} stopped unexpectedly {ago} ago. Its work is kept:
dockingbird {subcommand} --as {name}
Log: {log}
```

Or:

```text
{name} stopped unexpectedly {ago} ago. Its work is kept in {repo} ({branch}).
To pick it up: git switch {branch}, then dockingbird {subcommand} --as {name}
Log: {log}
```

Or:

```text
{name} stopped unexpectedly {ago} ago. Its work is kept in {repo} ({branch}).
To pick it up: cd {checkout}, then dockingbird {subcommand} --as {name}
Log: {log}
```

Or:

```text
{name} stopped unexpectedly {ago} ago. Its work is kept in {repo} ({branch}).
To pick it up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
Log: {log}
```

Or, if you deleted that branch:

```text
{name} stopped unexpectedly {ago} ago. Its work is kept in {repo} ({branch}, no longer in your checkout).
To pick it up: git switch -c {branch} dockingbird/{branch}, then dockingbird {subcommand} --as {name}
Log: {log}
```

Next step, as the message gives it:

- dockingbird {subcommand} --as {name}
- git switch {branch}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}

Exit status: 0 (done).

### AGENT_FEEDER_FAILED

When: A bus agent's supervisor failed while it fed the agent its messages; the agent stopped, and its parent got this message with the error's name. Its work is kept; please report it.

```text
{name} stopped: Dockingbird failed inside it ({error}).
Please report it: https://github.com/zeus-fyi/dockingbird/issues
```

Next step: none; it only informs.

Exit status: 0 (done).

### SESSION_SWEPT

When: A restart of Docker or Dockingbird stopped the agent. Its copy is kept and may hold work; the line gives the command that picks it up from where you are, and says where the copy is when that is another branch or checkout.

If you deleted that branch, the message says `({branch}, no longer in your checkout)` where the forms below say `({branch})`, and its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where they say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

```text
{name} was stopped by the restart. Its copy is kept and may hold work:
dockingbird {subcommand} --as {name}
```

Or:

```text
{name} was stopped by the restart. Its copy is kept in {repo} ({branch}) and may hold work.
To pick it up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} was stopped by the restart. Its copy is kept in {repo} ({branch}) and may hold work.
To pick it up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} was stopped by the restart. Its copy is kept in {repo} ({branch}) and may hold work.
To pick it up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or, if you deleted that branch:

```text
{name} was stopped by the restart. Its copy is kept in {repo} ({branch}, no longer in your checkout) and may hold work.
To pick it up: git switch -c {branch} dockingbird/{branch}, then dockingbird {subcommand} --as {name}
```

Next step, as the message gives it:

- dockingbird {subcommand} --as {name}
- git switch {branch}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}

Exit status: 0 (done).

### AGENT_LABEL_MISMATCH

When: With `--verbose` only: Dockingbird left a container alone because its label names another agent.

```text
Left {name}'s container alone: its label names another agent.
```

Next step: none; it only informs.

Exit status: 0 (done).

### START_NOTES_SKIPPED

When: With `--verbose` only: your git didn't answer in time for the start notes, so they were skipped; the agent started anyway.

```text
Skipped the start notes: your git gave no answer.
```

Next step: none; it only informs.

Exit status: 0 (done).

## Agents: start notes

### START_SENT_YOURS

When: At a start, you had commits the agents didn't, so Dockingbird sent them first; the agent starts from them.

```text
Sent your {count:new commit|new commits} to the agents first.
```

Next step: none; it only informs.

Exit status: 0 (done).

### START_DIRTY_NOTE

When: At a start, you had changes not committed. They stay in your checkout; the agent sees only your commits.

```text
Note: your {count} uncommitted changes stay here; {harness} sees only your commits.
```

Or:

```text
Note: your 1 uncommitted change stays here; {harness} sees only your commits.
```

Next step: none; it only informs.

Exit status: 0 (done).

### START_BEHIND_NOTE

When: At a start, the agents had commits you haven't taken yet.

```text
(The agents have {count:commit|commits} you don't: dockingbird sync)
```

Next step: dockingbird sync

Exit status: 0 (done).

## Sync

### SYNC_UPDATED

When: `dockingbird sync` took the agents' new commits into your branch. It lists each one with the agent that shared it, and gives the command to review them.

```text
{repo} ({branch}): {count} new commits from the agents
{commits}
Updated your {branch} to {head}. Review them: git log -p {base}..{head}
```

Or:

```text
{repo} ({branch}): 1 new commit from the agents
{commits}
Updated your {branch} to {head}. Review it: git log -p {base}..{head}
```

Next step: git log -p {base}..{head}

Exit status: 0 (done).

### COMMIT_ROW

When: One commit sync took, with the agent that shared it (or "you", or "changed outside Dockingbird"). When the commit's author field says something else, the row shows that too.

One row of a table; its cells line up with the rows around it.

```text
  {commit}  {name}  {subject}
```

Or:

```text
  {commit}  {name} (author says "{author}")  {subject}
```

Or:

```text
  {commit}  you  {subject}
```

Or:

```text
  {commit}  changed outside Dockingbird  {subject}
```

Next step: none; it only informs.

Exit status: 0 (done).

### SYNC_SENT

When: `dockingbird sync` sent your new commits to the agents, so their next work builds on them.

```text
{repo} ({branch}): sent your {count} commits to the agents. They'll build on them.
```

Or:

```text
{repo} ({branch}): sent your 1 commit to the agents. They'll build on it.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SYNC_UP_TO_DATE

When: `dockingbird sync` found nothing new either way on this branch.

```text
{repo} ({branch}): up to date.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SYNC_BEHIND_TOO

When: After a sync that took the agents' commits, another linked branch of this checkout lacks theirs too. The line gives the command that takes them. A branch you made under the name of a branch you deleted gets a line of its own instead, which says so.

```text
{repo} ({branch}) is behind too: git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch}) has new commits from the agents too: git switch {branch}, then dockingbird sync
```

Next step: git switch {branch}, then dockingbird sync

Exit status: 0 (done).

### SYNC_BOTH_MOVED

When: You and the agents both have new commits on this branch, so sync must merge. On a terminal it asks first; without one, it says how to merge yourself.

```text
{repo} ({branch}): you and the agents both have new commits.
{commits}
Merge theirs into yours now? [Y/n]
```

Or:

```text
{repo} ({branch}): you and the agents both have new commits.
{commits}
Take theirs first: dockingbird sync (on a terminal, it offers to merge),
then run this again.
```

Or:

```text
{repo} ({branch}): you and the agents both have new commits.
{commits}
```

Next step, as the message gives it:

- press Enter (or answer y) to go on; anything else is no
- dockingbird sync
- none, where the message only informs

Exit status: 1 (a problem Dockingbird printed), unless you go on at its question; then the command ends with its own status.

### SYNC_MERGED

When: You said yes: sync merged the agents' commits into yours and sent the merge to them. The line gives the command to review it.

```text
Merged, and sent the merge to the agents. Review: git log -p {base}..{branch}
```

Next step: git log -p {base}..{branch}

Exit status: 0 (done).

### SYNC_MERGED_NOT_SENT

When: Sync merged the agents' commits into yours, but the agents' branch moved again before the merge could be sent. Running sync again sends it.

```text
Merged their commits into yours, but the agents' {branch} moved
before yours was sent. Review: git log -p {base}..{branch}
Run this again to send it.
```

Next step: Run this again to send it.

Exit status: 1 (a problem Dockingbird printed).

### SYNC_MERGED_BUSY

When: Sync merged the agents' commits into yours, but the agents' branch was busy when the merge was to be sent: an agent was sharing a commit to it, or another Dockingbird command was using it. Nothing moved, and your branch keeps the merge. Running sync again in a moment sends it.

```text
Merged their commits into yours, but the agents' {branch} was busy
before yours was sent. An agent is sharing a commit to it, or
another Dockingbird command is using it.
Review: git log -p {base}..{branch}
Run this again in a moment to send it.
```

Next step: Run this again in a moment to send it.

Exit status: 1 (a problem Dockingbird printed).

### SYNC_MERGE_KEPT

When: Sync merged the agents' commits into yours, then stopped on another problem, shown above. Your branch keeps the merge; the line gives the command that shows it, which names the branch, so it works even when your checkout has moved to another one.

```text
The merge of their commits stays. Review: git log -p {base}..{branch}
```

Next step: git log -p {base}..{branch}

Exit status: 1 (a problem Dockingbird printed).

### SYNC_CONFLICTS

When: Sync's merge stopped on conflicts. The files are listed; fix them, commit, and run the command again.

```text
Conflicts in {count} files ({files}).
Fix them, commit, then run this again.
```

Or:

```text
Conflicts in 1 file ({files}).
Fix it, commit, then run this again.
```

Next step, as the message gives it:

- Fix them, commit, then run this again.
- Fix it, commit, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### SYNC_MERGE_UNFINISHED

When: Your checkout has a merge in progress, so sync (and a start) waits until you finish it.

```text
A merge is still in progress here, with {count} files in conflict
({files}). Fix them, commit, then run this again.
```

Or:

```text
A merge is still in progress here, with 1 file in conflict
({files}). Fix it, commit, then run this again.
```

Or:

```text
A merge is still in progress here. Commit it, then run this again.
```

Next step, as the message gives it:

- Fix them, commit, then run this again.
- Fix it, commit, then run this again.
- Commit it, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### SYNC_MERGE_FAILED

When: You said yes to sync's merge (or a start's), and git stopped: before it merged anything, for example because your git has no name and email set (`git config --global user.name` and `user.email`), or after it started a merge it could not finish. A started merge that changed none of your files is cleared for you (or the message gives `git merge --quit` to clear it); one that changed your files is left as it is, to commit or to undo with `git merge --abort`. The message shows git's status and its last lines; fix what they say and run the command again.

```text
git merge stopped with status {status} before it began. Its last lines:
{entries}
Fix what git says, then run this again.
```

Or:

```text
git merge stopped with status {status} before it began and said nothing.
Run this again.
```

Or:

```text
git merge stopped with status {status} before it changed your files;
Dockingbird cleared the merge it had started. Its last lines:
{entries}
Fix what git says, then run this again.
```

Or:

```text
git merge stopped with status {status} before it changed your files,
and Dockingbird couldn't clear the merge it had started. Its last lines:
{entries}
When no other git runs here: git merge --quit, then run this again.
```

Or:

```text
git merge stopped with status {status} after it changed your files,
and the merge is still in progress. Its last lines:
{entries}
Fix what git says, then commit the merge (git commit), or undo it
(git merge --abort).
```

Next step, as the message gives it:

- Fix what git says, then run this again.
- Run this again.
- git merge --quit, then run this again.
- Fix what git says, then commit the merge (git commit), or undo it (git merge --abort).

Exit status: 1 (a problem Dockingbird printed).

### SYNC_GIT_SAID_ROW

When: One line git printed, under the message that says sync's merge failed.

One row of a table; its cells line up with the rows around it.

```text
  {said}
```

Next step: none; it only informs.

Exit status: 0 (done).

### SYNC_GIT_REFUSED

When: You ran sync or started an agent, and your git stopped at once in this checkout: it refuses every command here, for example because a setting in your git config names a path under a user this machine doesn't have (`~name/...`). The message shows git's status and its last line; fix what it says and run the command again.

```text
Your git stopped with status {status} before Dockingbird could read this checkout.
git said:
  {said}
Fix what git says (often a setting in your git config), then run this again.
```

Or:

```text
Your git stopped with status {status} before Dockingbird could read this checkout,
and said nothing.
Check that git runs here (git status), then run this again.
```

Next step, as the message gives it:

- Fix what git says (often a setting in your git config), then run this again.
- git status

Exit status: 1 (a problem Dockingbird printed).

### SYNC_MERGE_LATER

When: You said no to sync's merge, or there was no terminal to ask on. The message gives the command to look at their commits first, and the one that merges when you are ready.

```text
Look first: git log -p {branch}..dockingbird/{branch}
When you are ready: git merge dockingbird/{branch}, then dockingbird sync
```

Next step: git merge dockingbird/{branch}, then dockingbird sync

Exit status: 1 (a problem Dockingbird printed).

### START_MERGE_DECLINED

When: You said no to the merge offered at a start, so the agent didn't start.

```text
Nothing started. When you are ready: dockingbird sync
(or git merge dockingbird/{branch}), then run this again.
```

Next step: dockingbird sync

Exit status: 1 (a problem Dockingbird printed).

### SYNC_HOOKS_CHANGED

When: The agents' commits change scripts your git runs as hooks, so sync didn't merge them. Review them first; the message gives the command that merges. When sync had already merged earlier commits of theirs in the same run, that merge stays, so the message doesn't say nothing was merged, and a last line says the merge stays.

```text
The agents changed scripts your git runs as hooks ({files}).
Nothing was merged. Review them, then: git merge --ff-only dockingbird/{branch}
```

Or:

```text
The agents changed scripts your git runs as hooks ({files}).
Nothing was merged. Review them, then: git merge dockingbird/{branch}
```

Or:

```text
The agents changed scripts your git runs as hooks ({files}).
Review them, then: git merge dockingbird/{branch}
```

Next step, as the message gives it:

- git merge --ff-only dockingbird/{branch}
- git merge dockingbird/{branch}

Exit status: 1 (a problem Dockingbird printed).

### SYNC_OVERLAP

When: The agents' commits change files you are editing and haven't committed. Nothing was merged; commit or stash your changes first.

```text
The agents changed {count} files you are editing ({files:first},
{files:rest}). Commit or stash those, then run this again.
```

Or:

```text
The agents changed 1 file you are editing ({files}).
Commit or stash it, then run this again.
```

Or:

```text
The agents changed files you are editing.
Commit or stash those, then run this again.
```

Next step, as the message gives it:

- Commit or stash those, then run this again.
- Commit or stash it, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### SYNC_NOT_LINKED

When: You ran `dockingbird sync` on a branch no agent has worked on. When another branch of this checkout has the agents' commits waiting, the next line says how to get them.

```text
No agent has worked on {branch} yet. Start one: dockingbird claude
```

Or:

```text
No agent has worked on {branch} yet.
```

Next step, as the message gives it:

- dockingbird claude
- none, where the message only informs

Exit status: 1 (a problem Dockingbird printed).

### SYNC_OTHER_BEHIND

When: Another linked branch of this checkout has the agents' commits waiting, after a sync on a branch no agent has worked on, or after a sync that took nothing on this branch (it was up to date, or only sent your commits). The line gives the command that takes them. After a sync on a branch no agent has worked on, the command exits 1; after the others, 0. A branch you made under the name of a branch you deleted gets a line of its own instead, which says so.

```text
{repo} ({branch}) is behind: git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch}) has new commits from the agents: git switch {branch}, then dockingbird sync
```

Next step: git switch {branch}, then dockingbird sync

Exit status: 0 (done) or 1 (a problem Dockingbird printed), as "When:" says.

### SYNC_OTHER_NAME_REUSED

When: After a sync, or a sync on a branch no agent has worked on, another branch of this checkout is one you made under the name of a branch you deleted, while that branch's agents have commits it doesn't. The line says so, as `status` does, never that the branch is behind, and gives the command that syncs it: sync there asks first whether to carry on from those commits. After a sync on a branch no agent has worked on, the command exits 1; otherwise 0.

```text
{repo} ({branch}) has a deleted branch's name, so sync asks first: git switch {branch}, then dockingbird sync
```

Next step: git switch {branch}, then dockingbird sync

Exit status: 0 (done) or 1 (a problem Dockingbird printed), as "When:" says.

### SYNC_MOVED

When: The agents' branch changed while sync was checking it. Nothing changed; run the command again.

```text
{repo}: the agents' {branch} changed while Dockingbird was checking.
Nothing changed. Run this again.
```

Next step: Run this again.

Exit status: 1 (a problem Dockingbird printed).

### SYNC_BUSY

When: An agent was sharing a commit to the branch, or another Dockingbird command held it, while sync was checking it. Nothing changed; run the command again in a moment.

```text
{repo}: the agents' {branch} is busy: an agent is sharing a commit to it,
or another Dockingbird command is using it.
Nothing changed. Run this again in a moment.
```

Next step: Run this again in a moment.

Exit status: 1 (a problem Dockingbird printed).

### SYNC_TREE_POLICY

When: Your branch has files the agents don't take: a symlink that points outside the repo, into `.git` or to nothing usable, a submodule, or a Git LFS file. Nothing was sent, and a start sets nothing up; the message lists each one with its kind, and a symlink with where it points.

```text
{repo} ({branch}) can't go to the agents yet: it has {count} files the agents don't take:
{entries}
Fix them, commit, then run this again.
```

Or:

```text
{repo} ({branch}) can't go to the agents yet: it has 1 file the agents don't take:
{entries}
Fix it, commit, then run this again.
```

Or:

```text
{repo} ({branch}) can't go to the agents yet: it has {count} files the agents don't take:
{entries}
Fix these, commit, then run this again: the next ones are listed then.
```

Next step, as the message gives it:

- Fix them, commit, then run this again.
- Fix it, commit, then run this again.
- Fix these, commit, then run this again: the next ones are listed then.

Exit status: 1 (a problem Dockingbird printed).

### SYNC_LINKS_CHANGED

When: The commits sync took add symlinks or change where they point. Each one points inside the repo by a relative path (any other is refused), and the note names it with its target, so you can look before you build or run anything.

```text
Note: the agents added or changed {count} symlinks:
{links}
```

Or:

```text
Note: the agents added or changed a symlink:
{links}
```

Next step: none; it only informs.

Exit status: 0 (done).

### LINK_ROW

When: One symlink the agents added or changed, and where it points.

One row of a table; its cells line up with the rows around it.

```text
  {file} -> {link_target}
```

Next step: none; it only informs.

Exit status: 0 (done).

### SYNC_ATTRIBUTES_CHANGED

When: The commits sync took change `.gitattributes`, `.gitmodules` or `.lfsconfig`, which your own git commands follow from now on. The note shows the new lines.

```text
Note: the agents changed {file}. Your own git commands will follow
it from now on. The new lines:
{changes}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CHANGE_ROW

When: One new line of such a file.

One row of a table; its cells line up with the rows around it.

```text
  + {line}
```

Next step: none; it only informs.

Exit status: 0 (done).

### SYNC_SUBMODULES_SKIPPED

When: The commits sync took change a submodule, which wasn't updated; review them first.

```text
Submodules were not updated; after review: git submodule update
```

Next step: git submodule update

Exit status: 0 (done).

### SYNC_PAUSED

When: The agents' copy of the branch was changed outside Dockingbird, so the agents are paused on it. Nothing is lost; the message says how to look and how to go on.

```text
{repo}: agents are paused. Their copy of {branch} was changed outside Dockingbird
(it was {was}, now {now}). Nothing is lost. This usually means a
Dockingbird bug, or a docker command run by hand.
  See what changed:               dockingbird status --verbose
  To go on from where it is now:  dockingbird sync --accept {now}
```

Next step: dockingbird sync --accept {now}

Exit status: 1 (a problem Dockingbird printed).

### SYNC_COPY_LOCKED

When: The agents' copy of the branch is locked by an update that didn't finish, so nothing was sent. Nothing is lost; trying again in a minute usually works.

```text
{repo}: the agents' copy of {branch} is locked by an unfinished update, so
nothing was sent. Nothing is lost. Run this again in a minute; if it stays
locked: dockingbird status --verbose
```

Next step: dockingbird status --verbose

Exit status: 1 (a problem Dockingbird printed).

### SYNC_COPY_MISSING

When: The agents' copy of the branch is missing, so nothing was sent. Nothing is lost.

```text
{repo}: the agents' copy of {branch} is missing, so nothing was sent.
Nothing is lost. Details: dockingbird status --verbose
```

Next step: dockingbird status --verbose

Exit status: 1 (a problem Dockingbird printed).

### SYNC_COPY_UNCHECKED

When: Dockingbird couldn't check the agents' copy of the branch, so sync stopped. Nothing is lost; trying again in a minute usually works.

```text
{repo}: Dockingbird couldn't check the agents' copy of {branch}, so this
stopped. Nothing is lost. Run this again in a minute; if it stops again:
dockingbird status --verbose
```

Next step: dockingbird status --verbose

Exit status: 1 (a problem Dockingbird printed).

### SYNC_BRANCH_CHANGED

When: Your checkout moved to another branch, or to no branch, while `dockingbird sync` ran. Nothing changed, unless sync had already merged the agents' commits into your branch: that merge stays, so the message doesn't say nothing changed, and a last line says the merge stays. Switch back to the branch and run the command again.

```text
Your checkout moved to another branch while sync ran. Nothing changed.
Switch back to {branch}, then run this again.
```

Or:

```text
Your checkout moved to another branch while sync ran.
Switch back to {branch}, then run this again.
```

Next step: Switch back to {branch}, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### SYNC_NO_COMMON_HISTORY

When: You and the agents both have new commits on this branch, but the two histories have no commit in common, so sync can't merge them. Their commits are kept beside your branch; the message gives the command that looks at them.

```text
{repo} ({branch}) and the agents' copy share no history, so nothing can be merged.
Look first: git log --oneline dockingbird/{branch}
```

Next step: git log --oneline dockingbird/{branch}

Exit status: 1 (a problem Dockingbird printed).

### SYNC_TOOK_TOO_LONG

When: Sync stopped a step that took longer than Dockingbird allows it. When it was asking what the agents have or taking their commits, nothing changed, unless sync had already merged them into your branch: that merge stays, so the message doesn't say nothing changed, and a last line says the merge stays. When it was sending yours, Dockingbird may still have finished it: run the command again, which checks what the agents have before it sends. When it was accepting a commit for `sync --accept`, Dockingbird may or may not have accepted it: run `dockingbird status`, then the command again.

```text
Syncing {repo} ({branch}) took too long, so it stopped. Nothing changed.
Run this again.
```

Or:

```text
Syncing {repo} ({branch}) took too long, so it stopped.
Run this again.
```

Or:

```text
Accepting {commit} for {repo} ({branch}) took too long, so it stopped.
Dockingbird may or may not have accepted it.
To find out: dockingbird status, then run this again.
```

Next step, as the message gives it:

- Run this again.
- dockingbird status, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### SYNC_NO_ANSWER

When: Sync could not get an answer from Dockingbird: the command that asks it did not start. When it was asking what the agents have or taking their commits, nothing changed, unless sync had already merged them into your branch: that merge stays, so the message doesn't say nothing changed, and a last line says the merge stays. When it was sending yours, run the command again, which checks what the agents have before it sends. When it was accepting a commit for `sync --accept`, the commit was not accepted: run the command again.

```text
Dockingbird didn't answer while syncing {repo} ({branch}). Nothing changed.
Run this again.
```

Or:

```text
Dockingbird didn't answer while syncing {repo} ({branch}).
Run this again.
```

Or:

```text
Dockingbird didn't answer while accepting {commit} for {repo} ({branch}).
It wasn't accepted. Run this again.
```

Next step: Run this again.

Exit status: 1 (a problem Dockingbird printed).

### SYNC_BUNDLE_UNREADABLE

When: The agents' commits reached your Mac in a form sync's own checks refused, so it took none of them and changed nothing, unless it had already merged earlier ones into your branch: that merge stays, so the message doesn't say nothing changed, and a last line says the merge stays. Running the command again asks for them afresh.

```text
Dockingbird couldn't read the agents' commits. Nothing changed.
Run this again.
```

Or:

```text
Dockingbird couldn't read the agents' commits.
Run this again.
```

Next step: Run this again.

Exit status: 1 (a problem Dockingbird printed).

### SYNC_DISK_FULL

When: Sync ran out of disk on this Mac while taking the agents' commits: the message names the folder and the free space. Nothing changed, unless sync had already merged earlier commits into your branch: that merge stays, so the message doesn't say nothing changed, and a last line says the merge stays. Free space where the message says, then run the command again.

```text
This Mac's disk has {free} free, too little for the agents' commits at {path}.
Nothing changed.
Free space on this Mac, then run this again.
```

Or:

```text
This Mac's disk has {free} free, too little for the agents' commits at {path}.
Free space on this Mac, then run this again.
```

Or:

```text
This Mac's disk ran out of room at {path} for the agents' commits.
Free space on this Mac, then run this again.
```

Next step: Free space on this Mac, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### SYNC_PUSH_DISK_FULL

When: Sync was sending your commits to the agents, and their disk (Docker's virtual disk) ran out of room for them: the message shows the free space. The agents took none of them. Free space there (in Docker Desktop, Settings, Resources, or with `docker system prune`), then run the command again.

```text
The agents' disk (Docker's) has {free} free, too little to take your commits on {repo} ({branch}).
Nothing was taken. Free some of Docker's disk, or give it more, then run this again.
```

Or:

```text
The agents' disk (Docker's) ran out of room taking your commits on {repo} ({branch}).
Nothing was taken. Free some of Docker's disk, or give it more, then run this again.
```

Next step: Free some of Docker's disk, or give it more, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### ACCEPT_MISMATCH

When: You ran `sync --accept` with a commit other than the one the paused message shows. Nothing changed.

```text
{commit} isn't where the agents' {branch} moved ({now}). Nothing changed.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### ACCEPT_REWRITE_UNSUPPORTED

When: The agents' branch was rewritten outside Dockingbird, and accepting a rewrite isn't supported yet. Nothing changed.

```text
The agents' {branch} was rewritten outside Dockingbird ({now} does not
build on {was}), and accepting a rewrite isn't supported yet. Nothing changed.
Ask the agent to redo its change on top of {was}, then run this again.
```

Next step: Ask the agent to redo its change on top of {was}, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### SYNC_LET_GO_NOT_NEEDED

When: You ran `dockingbird sync --let-go` on a branch that is linked, or that already has the agents' commits, so there is nothing to let go. Plain `dockingbird sync` takes or sends what differs.

```text
{repo} ({branch}): nothing to let go. This branch is linked, or already
carries the agents' commits.
To take or send commits: dockingbird sync
```

Next step: dockingbird sync

Exit status: 1 (a problem Dockingbird printed).

### SYNC_LET_GO_NEEDS_TERMINAL

When: You ran `dockingbird sync --let-go` without a terminal, or with `--json`. Letting go asks first, so nothing was taken or sent; run it on a terminal.

```text
Letting go asks first. Run it on a terminal: dockingbird sync --let-go
```

Next step: dockingbird sync --let-go

Exit status: 1 (a problem Dockingbird printed).

### SYNC_LET_GO_QUESTION

When: You ran `dockingbird sync --let-go` on a branch you made under a deleted branch's name. It lists the commits the agents made there that your branch lacks and asks whether to let them go and make yours the branch. The answer is no unless you type y.

```text
The agents made {count:commit|commits} on {branch} that this branch lacks:
{commits}
Let go of {count:commit|commits} the agents made on {branch} and make yours the branch? [y/N]
```

Or:

```text
The agents made commits on {branch} that this branch lacks.
Let go of the commits the agents made on {branch} and make yours the branch? [y/N]
```

Next step: answer y to go on; anything else is no

Exit status: 1 (a problem Dockingbird printed), unless you go on at its question; then the command ends with its own status.

### SYNC_LET_GO_DECLINED

When: You said no (or pressed Enter or Ctrl-C) when `dockingbird sync --let-go` asked. Nothing was sent or linked, and the agents' commits stay on their branch.

```text
Nothing changed. The agents' commits stay on their {branch}.
To take them instead: dockingbird sync
```

Next step: dockingbird sync

Exit status: 1 (a problem Dockingbird printed).

### SYNC_LET_GO_DONE

When: You said yes to `dockingbird sync --let-go`: your branch is now the agents' branch, and it is linked again. The agents' copies keep the commits you let go, but an agent can't share work built on them until its copy syncs onto your branch.

```text
{repo} ({branch}): let {count} commits go; yours is the branch now.
The agents' copies keep their work.
A copy built on the commits let go can't share until it syncs onto yours.
```

Or:

```text
{repo} ({branch}): let 1 commit go; yours is the branch now.
The agents' copies keep their work.
A copy built on the commit let go can't share until it syncs onto yours.
```

Next step: none; it only informs.

Exit status: 0 (done).

### ACCEPT_NOT_A_COMMIT

When: You gave `sync --accept` something other than a commit id.

```text
dockingbird sync: --accept takes the commit the paused message shows, not '{word}'.
See: dockingbird sync -h
```

Next step: dockingbird sync -h

Exit status: 2 (usage).

### SYNC_LET_GO_WITH_ACCEPT

When: You gave `dockingbird sync` both `--accept` and `--let-go`. They don't go together: use one of them.

```text
dockingbird sync: use --accept COMMIT or --let-go, not both.
See: dockingbird sync -h
```

Next step: dockingbird sync -h

Exit status: 2 (usage).

### SHARE_FINISHED

When: An agent's share was interrupted (for example by a restart), and Dockingbird finished it.

```text
Finished sharing {count} commits that were interrupted.
```

Or:

```text
Finished sharing 1 commit that was interrupted.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SHARE_UNPROVEN

When: An agent's share was interrupted, and Dockingbird can't tell how far it got. Nothing is lost; `status --verbose` shows the details.

```text
{repo} ({branch}): sharing a commit was interrupted, and Dockingbird can't tell
how far it got. Nothing is lost. Details: dockingbird status --verbose
```

Next step: dockingbird status --verbose

Exit status: 0 (done).

### SHARE_RESIDUE

When: An update of the agents' copy of a branch was interrupted and left git lock files there that Dockingbird can't tie to a step it finished, so their work on that branch is paused. Nothing is lost; `status --verbose` shows the details.

```text
{repo} ({branch}): agents are paused. An interrupted update left {count} lock files
in their copy that Dockingbird can't tie to a finished step. Nothing is lost.
Details: dockingbird status --verbose
```

Or:

```text
{repo} ({branch}): agents are paused. An interrupted update left a lock file
in their copy that Dockingbird can't tie to a finished step. Nothing is lost.
Details: dockingbird status --verbose
```

Or:

```text
{repo} ({branch}): agents are paused. An interrupted update left lock files
in their copy that Dockingbird can't tie to a finished step. Nothing is lost.
Details: dockingbird status --verbose
```

Next step: dockingbird status --verbose

Exit status: 0 (done).

## Sign-ins

### SIGNIN_NEEDED

When: The tool isn't signed in. Either there was no terminal to sign in on, or its sign-in screen showed and didn't finish (you quit, or never used the link). The message gives both routes: a sign-in or an API key.

```text
{harness} isn't signed in yet. Sign in first: dockingbird login {tool}
```

Or:

```text
{harness} isn't signed in yet. Run dockingbird {tool} again to sign in.
Or use an API key: dockingbird login {tool} --api-key
```

Next step, as the message gives it:

- dockingbird login {tool}
- dockingbird {tool}

Exit status: 1 (a problem Dockingbird printed).

### SIGNIN_START

When: You ran `dockingbird login claude` or `login codex`: the tool's own sign-in screen follows, and the line says what it will ask.

```text
Signing in to Claude. Open the link it shows, sign in, then paste the code here.
```

Or:

```text
Signing in to Codex. Open the link it shows on this Mac and enter the code.
```

Next step, as the message gives it:

- Open the link it shows, sign in, then paste the code here.
- Open the link it shows on this Mac and enter the code.

Exit status: 0 (done).

### SIGNIN_DONE

When: The sign-in finished, and Dockingbird keeps it.

```text
{harness} is signed in.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SIGNIN_DONE_KEY_REMOVED

When: The sign-in finished. You had an API key saved for the tool, and the last login wins, so the key was removed.

```text
{harness} is signed in. Your saved {harness} API key is removed.
```

Next step: none; it only informs.

Exit status: 0 (done).

### DEVICE_AUTH_DISABLED

When: Codex's sign-in didn't finish. Codex signs in with a device code, which ChatGPT's security settings can turn off; the message says where, and gives the API key route.

```text
Codex isn't signed in yet. Run dockingbird codex again to sign in.
(If device code login is off, turn it on in ChatGPT's security settings.)
Or use an API key: dockingbird login codex --api-key
```

Or:

```text
Codex sign-in didn't finish. Nothing changed. Run dockingbird login codex again.
(If device code login is off, turn it on in ChatGPT's security settings.)
Or use an API key: dockingbird login codex --api-key
```

Next step, as the message gives it:

- dockingbird codex
- Run dockingbird login codex again.

Exit status: 1 (a problem Dockingbird printed).

### SIGNED_OUT

When: You ran `dockingbird logout`: the tool's sign-in and any saved key are gone. When Dockingbird followed this computer's own login of the tool, it stops following it; the login on this computer is unchanged, and `dockingbird login claude --here` (or `codex`) uses it again.

```text
Signed out of {harness}. Dockingbird has no {harness} sign-in or key now.
```

Or:

```text
Dockingbird stopped following this computer's {harness} login
and has no {harness} sign-in or key now.
Your own {harness} login here is unchanged. To use it again:
dockingbird login {tool} --here
```

Next step, as the message gives it:

- none, where the message only informs
- dockingbird login {tool} --here

Exit status: 0 (done).

### LOGOUT_NOT_SIGNED_IN

When: You ran `dockingbird logout` for a tool that had no sign-in and no saved key.

```text
{harness} wasn't signed in. Nothing to do.
```

Next step: none; it only informs.

Exit status: 0 (done).

### LOGOUT_AGENTS_RUNNING

When: You ran `dockingbird logout` while an agent of that tool is running. Signing out would pull its sign-in away, so it waits for you to stop the agent.

```text
{name} is still running. Stop it first: dockingbird stop {name}
```

Or:

```text
{names:and} are still running. Stop them first, by name: dockingbird stop {names:first}
```

Or:

```text
A Claude agent is still running. Stop it first: dockingbird stop
```

Next step, as the message gives it:

- dockingbird stop {name}
- dockingbird stop {names:first}
- dockingbird stop

Exit status: 1 (a problem Dockingbird printed).

### LOGOUT_FAILED

When: Signing out didn't finish, or the saved API key couldn't be removed. Running the command again usually works.

```text
Signing out of {harness} didn't finish.
Run dockingbird logout {tool} again.
```

Or:

```text
Signed out of {harness}, but your saved {harness} API key couldn't be
removed, so it is still used. Run dockingbird logout {tool} again.
```

Next step: Run dockingbird logout {tool} again.

Exit status: 1 (a problem Dockingbird printed).

### LOGIN_AGENTS_RUNNING

When: You ran `dockingbird login` for a tool while one of its agents is running: a Claude agent keeps Claude's sign-in fresh, and a Codex agent could put its own sign-in back, so stop it first.

```text
{name} is still running and keeps Claude's sign-in fresh.
Stop it first: dockingbird stop {name}
```

Or:

```text
{names:and} are still running and keep Claude's sign-in fresh.
Stop them first, by name: dockingbird stop {names:first}
```

Or:

```text
A Claude agent is still running and keeps Claude's sign-in fresh.
Stop it first: dockingbird stop
```

Or:

```text
{name} is still running and could put its own Codex sign-in back.
Stop it first: dockingbird stop {name}
```

Or:

```text
{names:and} are still running and could put their Codex sign-in back.
Stop them first, by name: dockingbird stop {names:first}
```

Next step, as the message gives it:

- dockingbird stop {name}
- dockingbird stop {names:first}
- dockingbird stop

Exit status: 1 (a problem Dockingbird printed).

### LOGIN_NEEDS_TERMINAL

When: You ran `dockingbird login` without a terminal, as in a script. The tool's sign-in needs one; an API key doesn't.

```text
Signing in to {harness} needs a terminal. Run it in one, or save an
API key instead: dockingbird login {tool} --api-key
```

Next step: dockingbird login {tool} --api-key

Exit status: 1 (a problem Dockingbird printed).

### SIGNIN_FAILED

When: The tool's sign-in failed or didn't finish. Nothing changed; the message gives the API key route too.

```text
{harness} sign-in didn't finish. Nothing changed. Run dockingbird login {tool} again.
Or use an API key: dockingbird login {tool} --api-key
```

Next step: Run dockingbird login {tool} again.

Exit status: 1 (a problem Dockingbird printed).

### SIGNIN_NOT_SAVED

When: The sign-in finished, but Dockingbird couldn't keep it. Running `login` again usually works.

```text
{harness} signed in, but Dockingbird couldn't keep the sign-in.
Run dockingbird login {tool} again.
```

Next step: Run dockingbird login {tool} again.

Exit status: 1 (a problem Dockingbird printed).

### KEY_NOT_REMOVED

When: The sign-in finished, but your saved API key couldn't be removed, so the key is still what the tool uses.

```text
{harness} is signed in, but your saved {harness} API key couldn't be
removed, so it is still used. Run dockingbird login {tool} again.
```

Next step: Run dockingbird login {tool} again.

Exit status: 1 (a problem Dockingbird printed).

### API_KEY_NOT_SAVED

When: You ran `dockingbird login ... --api-key`, and Dockingbird couldn't save the key. Nothing changed. When removing what an earlier save left took longer than Dockingbird waits, usually because the computer was busy, the message says so; the next run removes it first again.

```text
Dockingbird couldn't save the key. Nothing changed.
Run dockingbird login {tool} --api-key again.
```

Or:

```text
Dockingbird didn't save the key: removing a container an earlier
save left took longer than {bound}.
Run dockingbird login {tool} --api-key again when this computer is less busy.
```

Next step, as the message gives it:

- Run dockingbird login {tool} --api-key again.
- Run dockingbird login {tool} --api-key again when this computer is less busy.

Exit status: 1 (a problem Dockingbird printed).

### API_KEY_TIMED_OUT

When: You ran `dockingbird login ... --api-key`, and saving the key took longer than Dockingbird waits, usually because the computer was busy, so it may or may not be saved. When Docker couldn't remove the step's container, the message names it.

```text
Saving your {harness} API key took longer than {bound}, so Dockingbird stopped it.
The key may or may not have been saved.
Run dockingbird login {tool} --api-key again when this computer is less busy.
```

Or:

```text
Saving your {harness} API key took longer than {bound}.
Dockingbird couldn't stop its container {container}.
Once it has ended, run dockingbird login {tool} --api-key again.
```

Next step, as the message gives it:

- Run dockingbird login {tool} --api-key again when this computer is less busy.
- Once it has ended, run dockingbird login {tool} --api-key again.

Exit status: 1 (a problem Dockingbird printed).

### API_KEY_PROMPT

When: `dockingbird login ... --api-key` asks for the key. What you paste isn't shown.

```text
Paste your Anthropic API key (hidden):
```

Or:

```text
Paste your OpenAI API key (hidden):
```

Next step: none; it only informs.

Exit status: 0 (done).

### API_KEY_SAVED

When: Dockingbird saved your API key. The tool uses it from now on, in place of any sign-in.

```text
Saved. {harness} will use this key; your {harness} sign-in is not used.
```

Next step: none; it only informs.

Exit status: 0 (done).

### API_KEY_INVALID

When: The API key you pasted was empty or had spaces or control characters, or you pressed Ctrl-C at the question. Nothing was saved.

```text
That API key is empty, or has spaces or control characters. Nothing changed.
```

Or:

```text
No key was pasted. Nothing changed. Run this again and paste the key.
```

Or:

```text
No key was saved. Nothing changed.
```

Next step, as the message gives it:

- none, where the message only informs
- Run this again and paste the key.

Exit status: 1 (a problem Dockingbird printed).

### BASE_URL_INVALID

When: You gave `--base-url` something that isn't an `https://` address. Nothing changed.

```text
--base-url needs an https:// URL, in ASCII with no spaces. Nothing changed.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### BASE_URL_UNSUPPORTED

When: You gave `--base-url` for a tool that can't use one. Both tools can today, so you shouldn't see this.

```text
--base-url works only for Claude for now. Nothing changed.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### LOGIN_TOKEN_ON_STDIN

When: You ran `dockingbird login claude --oauth-token -` or `dockingbird login codex --auth-json -` without piping the value in: it is read from standard input only, never from a terminal, a file or your Mac's own sign-ins.

```text
Copy the token claude setup-token shows, then pipe it in:
pbpaste | dockingbird login claude --oauth-token -
```

Or:

```text
Pipe the file in; nothing is read from a terminal or a path:
cat ~/.codex/auth.json | dockingbird login codex --auth-json -
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### LOGIN_IMPORT_INVALID

When: The token or file you piped in was refused, before anything ran or by the sign-in store's own parser: a token must be one line of printable ASCII within the key's size bound, and a Codex auth.json a Codex sign-in within the sign-in store's size bound. Nothing changed.

```text
That token is empty, or has spaces or control characters. Nothing changed.
```

Or:

```text
That isn't a Codex auth.json Dockingbird can keep. Nothing changed.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### LOGIN_IMPORT_FAILED

When: Dockingbird could not keep the piped token or file for another reason than its content (the store was busy, unreadable or could not be written, or Docker gave no answer); nothing changed.

```text
Dockingbird couldn't keep the {harness} sign-in. Nothing changed.
Run it again; if it keeps failing, dockingbird stop, then try again.
```

Next step: dockingbird stop

Exit status: 1 (a problem Dockingbird printed).

### LOGIN_IMPORTED

When: The piped token or file is in Dockingbird's store, and the tool uses it from now on. The last login wins, so a saved API key goes with it; the line says so only when there was one.

```text
Saved. Claude will use this token.
```

Or:

```text
Saved. Claude will use this token; a saved Claude API key is removed.
```

Or:

```text
Saved. Codex will use this sign-in.
```

Or:

```text
Saved. Codex will use this sign-in; a saved Codex API key is removed.
```

Next step: none; it only informs.

Exit status: 0 (done).

### LOGIN_IMPORT_FORM

When: You gave `login` an import form of the other tool, or two forms at once (`--here` is one of them).

```text
--oauth-token is Claude's.
Copy the token claude setup-token shows, then pipe it in:
pbpaste | dockingbird login claude --oauth-token -
```

Or:

```text
--auth-json is Codex's. Pipe the file in:
cat ~/.codex/auth.json | dockingbird login codex --auth-json -
```

Or:

```text
Give one of --here, --api-key, --oauth-token - and --auth-json -, not two.
```

Next step: none; it only informs.

Exit status: 2 (usage).

### LOGIN_HERE_DONE

When: You ran `dockingbird login claude --here` (or `codex`): Dockingbird keeps a copy of the login this computer's Claude Code or Codex uses, without its refresh token, and follows it from then on. Run it again any time; when nothing changed it says so.

```text
{harness} uses this computer's login now, and Dockingbird follows it.
```

Or:

```text
{harness} uses this computer's login now, and Dockingbird follows it;
a saved {harness} API key is removed.
```

Or:

```text
{harness} already uses this computer's login, and Dockingbird's copy of it
is up to date.
```

Next step: none; it only informs.

Exit status: 0 (done).

### LOGIN_HERE_ADOPTED

When: The first start of a tool Dockingbird had no sign-in or key for found the tool's login on this computer and uses it from now on, as `dockingbird login claude --here` would. `dockingbird logout` stops that.

```text
{harness} uses this computer's login from now on (dockingbird logout {tool} stops that).
```

Next step: dockingbird logout {tool}

Exit status: 0 (done).

### LOGIN_HERE_NOT_FOUND

When: You ran `dockingbird login claude --here` (or `codex`), and this computer has no login of that tool: sign in with Claude Code or Codex here first, or sign in for Dockingbird only with `dockingbird login claude`. When `~/.claude/settings.json` was skipped on the way (a link, or a file others may write, say), the message names it and the rule, since that file may hold your only Claude login: make it a plain file of yours (not a link) that only you can write, readable and under 64 KiB, then run it again. Nothing changed.

```text
There's no {harness} login on this computer to use. Nothing changed.
Sign in with {harness} here first, or sign in for Dockingbird only: dockingbird login {tool}
```

Or:

```text
There's no {harness} login on this computer Dockingbird can use:
~/.claude/settings.json was skipped ({why}) and no other login was found.
Nothing changed.
Make it a plain file of yours (not a link) that only you can write, readable
and under 64 KiB, then: dockingbird login {tool} --here
```

Next step, as the message gives it:

- dockingbird login {tool}
- dockingbird login {tool} --here

Exit status: 1 (a problem Dockingbird printed).

### LOGIN_HERE_EXPIRED

When: You ran `dockingbird login claude --here`, and the login on this computer has expired. Claude Code renews it when you use it here; Dockingbird never does. Nothing changed.

```text
This computer's {harness} login has expired. Nothing changed.
Use {harness} here once so it renews its login, then: dockingbird login {tool} --here
```

Next step: dockingbird login {tool} --here

Exit status: 1 (a problem Dockingbird printed).

### LOGIN_HERE_UNAVAILABLE

When: You ran `dockingbird login claude --here` (or `codex`), and the login on this computer couldn't be read: the Keychain refused or didn't answer in time (macOS may be asking you to allow it), the login file is a link or readable by others, the login has nothing Dockingbird can use, or the shell's `HOME` isn't your home folder (Dockingbird reads your login only from a shell whose `HOME` is your own). Nothing changed.

```text
This computer's Keychain didn't give Dockingbird the {harness} login. Nothing changed.
Run it again, or sign in for Dockingbird only: dockingbird login {tool}
```

Or:

```text
This computer's Keychain didn't answer in time; macOS may be asking
whether security may read the {harness} login. Nothing changed.
Answer it, then: dockingbird login {tool} --here
```

Or:

```text
This computer's {harness} login file isn't one Dockingbird reads: it must be
a file of yours that only you can read, not a link. Nothing changed.
Or sign in for Dockingbird only: dockingbird login {tool}
```

Or:

```text
This computer's {harness} login isn't one Dockingbird can use. Nothing changed.
Sign in with {harness} here again, or sign in for Dockingbird only: dockingbird login {tool}
```

Or:

```text
HOME isn't your home folder, so Dockingbird can't read this computer's
{harness} login from here. Nothing changed.
From a normal shell: dockingbird login {tool} --here.
Or sign in for Dockingbird only: dockingbird login {tool}
```

Next step, as the message gives it:

- dockingbird login {tool}
- dockingbird login {tool} --here

Exit status: 1 (a problem Dockingbird printed).

### LOGIN_HERE_BLOCKED

When: You ran `dockingbird login claude --here` while an agent still keeps Dockingbird's own Claude sign-in fresh. Stop the agent, or sign that sign-in out with `dockingbird logout claude`, then run it again. Nothing changed.

```text
An agent still keeps Dockingbird's own {harness} sign-in fresh,
so it can't be replaced. Nothing changed.
Stop the agent, or sign that sign-in out: dockingbird logout {tool}
```

Next step: dockingbird logout {tool}

Exit status: 1 (a problem Dockingbird printed).

### LOGIN_HERE_GATEWAY_NOT_HTTPS

When: You ran `dockingbird login claude --here`, and Claude Code on this computer signs in with the token set in `~/.claude/settings.json` (its `env` block) through a gateway set there whose address isn't `https://`. Dockingbird sends a token only to an `https://` gateway: point Claude Code at the gateway's `https://` address, then run it again. A first start adopts nothing from such a login, and `status` says so after a change the watcher saw. Nothing changed. The one plain address Dockingbird follows is this computer's own (`http://127.0.0.1:59471`, say, a proxy on this Mac), which agents reach as `host.docker.internal`.

```text
This computer's Claude login goes through {gateway},
and Dockingbird sends a token only to an https:// gateway. Nothing changed.
Point Claude Code here at the gateway's https:// address (ANTHROPIC_BASE_URL
in ~/.claude/settings.json), then: dockingbird login claude --here
```

Next step: dockingbird login claude --here

Exit status: 1 (a problem Dockingbird printed).

### LOGIN_HERE_GATEWAY_UNREACHABLE

When: You ran `dockingbird login claude --here` on a computer that isn't a Mac, and Claude Code here signs in with the token set in `~/.claude/settings.json` (its `env` block) through a gateway on this computer itself (`127.0.0.1`, `localhost` or `[::1]`), which agents reach only through Docker Desktop on a Mac, as `host.docker.internal`. Point Claude Code at an `https://` address agents can reach, then run it again. A first start adopts nothing from such a login, and `status` says so after a change the watcher saw. Nothing changed.

```text
This computer's Claude login goes through {gateway},
this computer's own address, which agents reach only through Docker
Desktop on a Mac. Nothing changed.
Point Claude Code here at an https:// address agents can reach
(ANTHROPIC_BASE_URL in ~/.claude/settings.json), then:
dockingbird login claude --here
```

Next step: dockingbird login claude --here

Exit status: 1 (a problem Dockingbird printed).

### LOGIN_HERE_SETTINGS_SKIPPED

When: You ran `dockingbird login claude --here`, or an agent's first start took this computer's Claude login, and `~/.claude/settings.json` isn't a file Dockingbird reads (a link, as dotfiles setups make; another user's; one the group or others may write; a very large one; or one that can't be read): Dockingbird skipped it, took no token and no gateway from it, and read the login from the Keychain or Claude's login file instead. `status` says so while that lasts. Make it a plain file of yours (not a link) that only you can write, readable and under 64 KiB, for a token or a gateway set there to count.

```text
Dockingbird skipped ~/.claude/settings.json ({why}), so it took no token
and no gateway from it and read Claude's login elsewhere.
```

Or:

```text
Dockingbird skipped ~/.claude/settings.json at its last read of Claude's
login ({why}), so it takes no token and no gateway from it.
```

Next step: none; it only informs.

Exit status: 0 (done).

## Status

### STATUS_NOT_SET_UP

When: You ran `status` (or `sync`, `stop`, `clean`, `logout` or `mcp install`) before Dockingbird was set up. The first `dockingbird claude` sets it up. In a repo whose branch has files the agents don't take, `status` says only that it isn't set up, and the next line says why the start would refuse.

```text
Dockingbird isn't set up yet. cd into a repo, then: dockingbird claude; or, with no repo, sign in first: dockingbird login claude
```

Or:

```text
Dockingbird isn't set up yet. Start here: dockingbird claude
```

Or:

```text
Dockingbird isn't set up yet.
```

Next step, as the message gives it:

- cd into a repo, then: dockingbird claude; or, with no repo, sign in first: dockingbird login claude
- dockingbird claude
- none, where the message only informs

Exit status: 0 (done).

### STATUS_SETTING_UP

When: You ran `status` while another terminal is setting Dockingbird up.

```text
Dockingbird is being set up in another terminal.
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_OFF

When: You ran `status` while Docker or Dockingbird is off, and no agent is working. Your repos and their work are kept; any agent command starts Dockingbird again.

```text
Dockingbird is off, so nothing is working. Your repos and their work are kept.
```

Or:

```text
Dockingbird is off, so nothing is working.
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_NOT_LINKED

When: The last line of `status` while Dockingbird is off and no repo is linked yet, as after saving an API key first. In a repo whose branch has files the agents don't take, it says only that nothing is linked, and the next line says why.

```text
Nothing is linked yet. cd into a repo, then: dockingbird claude
```

Or:

```text
Nothing is linked yet. Start here: dockingbird claude
```

Or:

```text
Nothing is linked yet.
```

Next step, as the message gives it:

- cd into a repo, then: dockingbird claude
- dockingbird claude
- none, where the message only informs

Exit status: 0 (done).

### STATUS_START_HERE

When: The last line of `status` while Dockingbird is off, in a repo with no work kept.

```text
Start one here: dockingbird claude
```

Next step: dockingbird claude

Exit status: 0 (done).

### STATUS_CANNOT_LINK

When: You ran `status` in a repo whose branch isn't linked yet and has files the agents don't take, so a start there would refuse it: the line counts them in place of the step that starts one. `dockingbird claude` lists each one and sets nothing up.

```text
{repo} ({branch}) can't be linked yet: it has {count} files the agents don't take.
See them: dockingbird claude
```

Or:

```text
{repo} ({branch}) can't be linked yet: it has 1 file the agents don't take.
See them: dockingbird claude
```

Next step: dockingbird claude

Exit status: 0 (done).

### STATUS_SIGNED_IN

When: The sign-in line of `status` while Dockingbird is off or Docker answers slowly: which tools are signed in or use an API key, and the command for one that isn't yet.

```text
Signed in to Claude and Codex
```

Or:

```text
Signed in to Claude; Codex not yet: dockingbird codex
```

Or:

```text
Signed in to Codex; Claude not yet: dockingbird claude
```

Or:

```text
Not signed in yet: dockingbird claude
```

Or:

```text
Claude uses an API key, signed in to Codex
```

Or:

```text
Signed in to Claude, Codex uses an API key
```

Or:

```text
Claude and Codex use API keys
```

Or:

```text
Claude uses an API key; Codex not yet: dockingbird codex
```

Or:

```text
Codex uses an API key; Claude not yet: dockingbird claude
```

Next step, as the message gives it:

- none, where the message only informs
- dockingbird codex
- dockingbird claude

Exit status: 0 (done).

### STATUS_HOST_LOGIN

When: A line of `status`: the tools whose login on this computer Dockingbird follows, set by `dockingbird login claude --here` or a first start. When Claude Code here sends its requests through a gateway, the line names it; when that gateway is this computer's own address (a proxy on this Mac, `http://127.0.0.1:59471` say), it also names the address the agents reach it at, `host.docker.internal`, Docker Desktop's name for this Mac seen from a container.

```text
Claude uses this computer's login.
```

Or:

```text
Codex uses this computer's login.
```

Or:

```text
Claude and Codex use this computer's logins.
```

Or:

```text
Claude uses this computer's login through {gateway}.
```

Or:

```text
Claude uses this computer's login through {gateway};
Codex uses this computer's login.
```

Or:

```text
Claude uses this computer's login through {gateway} (agents reach it at
{agent_gateway}).
```

Or:

```text
Claude uses this computer's login through {gateway} (agents reach it at
{agent_gateway}); Codex uses this computer's login.
```

Next step: none; it only informs.

Exit status: 0 (done).

### LOGIN_HERE_GATEWAY_UNFOLLOWED

When: `~/.claude/settings.json` sets a gateway in its `env` block with no token beside it, so Claude's login here is the Keychain's or its login file's, and that gateway isn't one Dockingbird follows with such a login: only a gateway on this Mac itself (`127.0.0.1`, `localhost` or `[::1]`) is, reached by the agents as `host.docker.internal`; a gateway elsewhere, or one on a Linux computer, is left to Claude Code here, and the agents call Anthropic directly. `dockingbird login claude --here`, a first start and `status` say it. To send the agents through that gateway too, give Claude Code here a token in the same `env` block (`claude setup-token`), which Dockingbird follows with its gateway.

```text
Claude Code here sends its requests through {gateway}, which the agents
don't use: beside a Keychain or login-file sign-in, Dockingbird follows a
gateway only on a Mac and only at this computer's own address.
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_HOST_LOGIN_NOT_COPIED

When: A line of `status` after the one that says a tool uses this computer's login: the last read of that login, after it changed on this computer or at a command, made no copy for the agents; how long ago and why. The agents keep the earlier copy until a read succeeds; the log in Dockingbird's folder has the entry.

```text
Dockingbird couldn't update its copy of Claude's login {ago} ago: {why}.
The agents keep the earlier copy.
```

Or:

```text
Dockingbird couldn't update its copy of Codex's login {ago} ago: {why}.
The agents keep the earlier copy.
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_OFF_KEPT

When: The heading of the agents' kept work on the screen `status` shows while Dockingbird is off.

```text
Work kept:
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_HEADER

When: The first line of `status`: Dockingbird's version, signed in to both tools.

```text
Dockingbird {version}, signed in to Claude and Codex
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_SIGNED_IN_ONE

When: The first line of `status` when only one tool, or neither, is signed in, with the command for the other.

```text
Dockingbird {version}, signed in to Claude; Codex not yet: dockingbird codex
```

Or:

```text
Dockingbird {version}, signed in to Codex; Claude not yet: dockingbird claude
```

Or:

```text
Dockingbird {version}, not signed in yet: dockingbird claude
```

Next step, as the message gives it:

- dockingbird codex
- dockingbird claude

Exit status: 0 (done).

### STATUS_USES_KEY

When: The first line of `status` when a tool uses a saved API key.

```text
Dockingbird {version}, Claude uses an API key, signed in to Codex
```

Or:

```text
Dockingbird {version}, signed in to Claude, Codex uses an API key
```

Or:

```text
Dockingbird {version}, Claude uses an API key; Codex not yet: dockingbird codex
```

Or:

```text
Dockingbird {version}, Codex uses an API key; Claude not yet: dockingbird claude
```

Or:

```text
Dockingbird {version}, Claude and Codex use API keys
```

Next step, as the message gives it:

- none, where the message only informs
- dockingbird codex
- dockingbird claude

Exit status: 0 (done).

### STATUS_REPO

When: A repo's heading in `status`: its folder name and branch, and, when the agents have commits you lack there, the command that takes them from where you are (with `git switch` or `cd` first when that branch isn't the one you are on). It says you are behind only when sync would just add their commits; when you have new commits too, it says you both do (sync will merge), and when Dockingbird can't tell, that the agents have new commits. A branch you deleted is named as no longer in your checkout, with a step only when the agents shared commits there that you haven't synced (counted when git can).

If you deleted that branch, the message says `({branch}, no longer in your checkout)` where the forms below say `({branch})`, and its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where they say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

```text
{repo} ({branch})
```

Or:

```text
{repo} ({branch}, no longer in your checkout)
```

Or:

```text
{repo} ({branch})   you are {count:commit|commits} behind: dockingbird sync
```

Or:

```text
{repo} ({branch})   you are {count:commit|commits} behind: git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch})   you are {count:commit|commits} behind: cd {checkout}, then dockingbird sync
```

Or:

```text
{repo} ({branch})   you are {count:commit|commits} behind: cd {checkout}, then git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch})   you are behind: dockingbird sync
```

Or:

```text
{repo} ({branch})   you are behind: git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch})   you are behind: cd {checkout}, then dockingbird sync
```

Or:

```text
{repo} ({branch})   you are behind: cd {checkout}, then git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch})   you and the agents both have new commits: dockingbird sync
```

Or:

```text
{repo} ({branch})   you and the agents both have new commits:
git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch})   you and the agents both have new commits: cd {checkout}, then dockingbird sync
```

Or:

```text
{repo} ({branch})   you and the agents both have new commits:
cd {checkout}, then git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch})   the agents have new commits: dockingbird sync
```

Or:

```text
{repo} ({branch})   the agents have new commits: git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch})   the agents have new commits: cd {checkout}, then dockingbird sync
```

Or:

```text
{repo} ({branch})   the agents have new commits: cd {checkout}, then git switch {branch}, then dockingbird sync
```

Or, if you deleted that branch:

```text
{repo} ({branch}, no longer in your checkout)   you are {count:commit|commits} behind: git switch -c {branch} dockingbird/{branch}, then dockingbird sync
```

Next step, as the message gives it:

- none, where the message only informs
- dockingbird sync
- git switch {branch}, then dockingbird sync
- cd {checkout}, then dockingbird sync
- cd {checkout}, then git switch {branch}, then dockingbird sync

Exit status: 0 (done).

### STATUS_NAME_REUSED

When: A repo's heading in `status` for a branch you made under the name of a branch you deleted, while that branch's agents have commits it doesn't. `dockingbird sync`, or a start, asks whether to carry on from them before it links the branch; the command runs from where you are.

```text
{repo} ({branch})   has a deleted branch's name, so sync asks first: dockingbird sync
```

Or:

```text
{repo} ({branch})   has a deleted branch's name, so sync asks first: git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch})   has a deleted branch's name, so sync asks first: cd {checkout}, then dockingbird sync
```

Or:

```text
{repo} ({branch})   has a deleted branch's name, so sync asks first: cd {checkout}, then git switch {branch}, then dockingbird sync
```

Next step, as the message gives it:

- dockingbird sync
- git switch {branch}, then dockingbird sync
- cd {checkout}, then dockingbird sync
- cd {checkout}, then git switch {branch}, then dockingbird sync

Exit status: 0 (done).

### STATUS_MERGE_IN_PROGRESS

When: Under "Needs your attention": a repo has a merge in progress. Sync and new agents wait until you finish it.

```text
{repo} ({branch}): a merge is in progress with {count} files in conflict ({files}).
Fix them, commit, then dockingbird sync
```

Or:

```text
{repo} ({branch}): a merge is in progress with 1 file in conflict ({files}).
Fix it, commit, then dockingbird sync
```

Or:

```text
{repo} ({branch}): a merge is in progress. Commit it, then dockingbird sync
```

Next step, as the message gives it:

- Fix them, commit, then dockingbird sync
- Fix it, commit, then dockingbird sync
- Commit it, then dockingbird sync

Exit status: 0 (done).

### STATUS_KEPT

When: Under "Needs your attention": an agent stopped with work left in its copy. The line says what the copy has, and gives the command that picks it up from where you are. It says "may" when Dockingbird couldn't count the copy's own commits, usually because the branch moved on since the copy started (another agent shared, or you sent your own commits) or git couldn't read the copy; and after a crash or a restart, when the last count can be older than the agent's last change. Nothing in it is lost: it stays kept, with its files and commits, until you pick it up or `dockingbird clean` removes it. An agent that stopped after sharing everything has no copy left, but its conversation is kept: the line says it can pick up where it left off, with the same command.

If you deleted that branch, the message says `({branch}, no longer in your checkout)` where the forms below say `({branch})`, and its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where they say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

```text
{name} stopped in {repo} ({branch}) with {count:commit|commits} not shared yet.
Pick it up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} ({branch}) with {count:commit|commits} not shared yet.
Pick it up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} ({branch}) with {count:commit|commits} not shared yet.
Pick it up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} ({branch}) with {count:commit|commits} not shared yet.
Pick it up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} ({branch}) with {count:file|files} not committed.
Pick it up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} ({branch}) with {count:file|files} not committed.
Pick it up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} ({branch}) with {count:file|files} not committed.
Pick it up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} ({branch}) with {count:file|files} not committed.
Pick it up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} ({branch}); its copy may hold work.
Pick it up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} ({branch}); its copy may hold work.
Pick it up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} ({branch}); its copy may hold work.
Pick it up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} ({branch}); its copy may hold work.
Pick it up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} crashed in {repo} ({branch}); its copy may hold work.
Pick it up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} crashed in {repo} ({branch}); its copy may hold work.
Pick it up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} crashed in {repo} ({branch}); its copy may hold work.
Pick it up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} crashed in {repo} ({branch}); its copy may hold work.
Pick it up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
A restart stopped {name} in {repo} ({branch}); its copy may hold work.
Pick it up: dockingbird {subcommand} --as {name}
```

Or:

```text
A restart stopped {name} in {repo} ({branch}); its copy may hold work.
Pick it up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
A restart stopped {name} in {repo} ({branch}); its copy may hold work.
Pick it up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
A restart stopped {name} in {repo} ({branch}); its copy may hold work.
Pick it up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} ({branch}); it can pick up where it left off.
Pick it up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} ({branch}); it can pick up where it left off.
Pick it up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} ({branch}); it can pick up where it left off.
Pick it up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} ({branch}); it can pick up where it left off.
Pick it up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped with {count:commit|commits} not shared yet.
Pick it up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped with {count:file|files} not committed.
Pick it up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped; its copy may hold work.
Pick it up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} crashed; its copy may hold work.
Pick it up: dockingbird {subcommand} --as {name}
```

Or:

```text
A restart stopped {name}; its copy may hold work.
Pick it up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped; it can pick up where it left off.
Pick it up: dockingbird {subcommand} --as {name}
```

Or, if you deleted that branch:

```text
{name} stopped in {repo} ({branch}, no longer in your checkout) with {count:commit|commits} not shared yet.
Pick it up: git switch -c {branch} dockingbird/{branch}, then dockingbird {subcommand} --as {name}
```

Next step, as the message gives it:

- dockingbird {subcommand} --as {name}
- git switch {branch}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}

Exit status: 0 (done).

### STATUS_KEPT_REUSED

When: Under "Needs your attention": an agent stopped with work left in its copy on a branch you deleted, and a new branch you made since has that branch's name. The line names the place as the branch you deleted, so the copy is never taken for the new branch's own, and gives the command that picks it up from where you are: it asks first whether the new branch should carry on from that branch's agents' commits, and picks the agent up only if you say yes.

```text
{name} stopped in {repo} (the {branch} you deleted) with {count:commit|commits} not shared yet.
To pick it up, say yes when it asks: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} (the {branch} you deleted) with {count:commit|commits} not shared yet.
To pick it up, say yes when it asks: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} (the {branch} you deleted) with {count:commit|commits} not shared yet.
To pick it up, say yes when it asks: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} (the {branch} you deleted) with {count:commit|commits} not shared yet.
To pick it up, say yes when it asks: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} (the {branch} you deleted) with {count:file|files} not committed.
To pick it up, say yes when it asks: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} (the {branch} you deleted) with {count:file|files} not committed.
To pick it up, say yes when it asks: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} (the {branch} you deleted) with {count:file|files} not committed.
To pick it up, say yes when it asks: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} (the {branch} you deleted) with {count:file|files} not committed.
To pick it up, say yes when it asks: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} (the {branch} you deleted); its copy may hold work.
To pick it up, say yes when it asks: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} (the {branch} you deleted); its copy may hold work.
To pick it up, say yes when it asks: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} (the {branch} you deleted); its copy may hold work.
To pick it up, say yes when it asks: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} (the {branch} you deleted); its copy may hold work.
To pick it up, say yes when it asks: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} crashed in {repo} (the {branch} you deleted); its copy may hold work.
To pick it up, say yes when it asks: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} crashed in {repo} (the {branch} you deleted); its copy may hold work.
To pick it up, say yes when it asks: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} crashed in {repo} (the {branch} you deleted); its copy may hold work.
To pick it up, say yes when it asks: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} crashed in {repo} (the {branch} you deleted); its copy may hold work.
To pick it up, say yes when it asks: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
A restart stopped {name} in {repo} (the {branch} you deleted); its copy may hold work.
To pick it up, say yes when it asks: dockingbird {subcommand} --as {name}
```

Or:

```text
A restart stopped {name} in {repo} (the {branch} you deleted); its copy may hold work.
To pick it up, say yes when it asks: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
A restart stopped {name} in {repo} (the {branch} you deleted); its copy may hold work.
To pick it up, say yes when it asks: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
A restart stopped {name} in {repo} (the {branch} you deleted); its copy may hold work.
To pick it up, say yes when it asks: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} (the {branch} you deleted); it can pick up where it left off.
To pick it up, say yes when it asks: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} (the {branch} you deleted); it can pick up where it left off.
To pick it up, say yes when it asks: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} (the {branch} you deleted); it can pick up where it left off.
To pick it up, say yes when it asks: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} stopped in {repo} (the {branch} you deleted); it can pick up where it left off.
To pick it up, say yes when it asks: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Next step, as the message gives it:

- dockingbird {subcommand} --as {name}
- git switch {branch}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}

Exit status: 0 (done).

### STATUS_KEPT_WORKTREE

When: You ran `dockingbird status NAME` for an agent whose kept copy has a git worktree with commits on no branch, so the copy can't be picked up as it is: a start under that name gets a fresh copy, and the kept one stays as it is. The line names the worktree; finish or remove it in a new agent first. When Dockingbird couldn't read the worktree's name, the line says the copy may have one.

```text
{name}'s kept copy has a worktree ({worktree}) with commits on no branch,
so it can't be picked up as it is: a start makes {name} a fresh copy and this
one stays kept. Finish or remove that worktree in a new agent first.
```

Or:

```text
{name}'s kept copy may have a worktree with commits on no branch
(Dockingbird couldn't read its name), so a start may not pick it up as it is:
it then makes {name} a fresh copy and this one stays kept.
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_OPTIONS_MISMATCH

When: Under "Needs your attention": a running agent's tool reports another model or effort than the one you asked, for example a level its model or your organization does not allow, which the tool lowers without a word. Ask for one it takes with `dockingbird set NAME`.

```text
{name} runs {field} {reported}, not the asked {asked}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_FAILED_NOTE

When: Under "Needs your attention": a running agent's last turn failed, for example because Claude or Codex refused the request (an access or billing problem on the tool's side), with the tool's own error line when it gave one. The agent stays up but did nothing with that message. Fix the cause the error names, then send it the work again with the `dockingbird send` shown: a failed turn leaves the agent running, its next message starts a new turn in the same conversation, and it keeps the files it is working on and its jobs. A newer login reaches the agent between turns. If that turn fails too, stop the agent and pick it up with the command shown, which resumes its conversation but lets go of the files it was working on and its jobs. An agent that signs in with a saved Claude token (`dockingbird login claude --oauth-token -`) whose token stopped working (revoked or expired) keeps that token until it stops, so a send fails the same way: the note then says to make a new token with `claude setup-token`, stop the agent (Dockingbird saves a token only while no Claude agent runs), save the token and pick the agent up, which starts it on the new token. When that token is the one Claude Code uses on this computer, which Dockingbird follows, the note says to renew that login here instead, then stop and pick up the agent.

```text
{name}'s last turn failed: {error}.
Recover it: dockingbird send {name} TEXT
It keeps what it works on and its jobs. If it fails again:
dockingbird stop {name}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name}'s last turn failed: {error}
Recover it: dockingbird send {name} TEXT
It keeps what it works on and its jobs. If it fails again:
dockingbird stop {name}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name}'s last turn failed; its tool gave no error text.
Recover it: dockingbird send {name} TEXT
It keeps what it works on and its jobs. If it fails again:
dockingbird stop {name}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name}'s last turn failed: {error}.
It keeps its Claude token until it stops, so a send fails the same way.
Recover it: claude setup-token, then stop it, save the token and pick it up:
dockingbird stop {name}
pbpaste | dockingbird login claude --oauth-token -
dockingbird {subcommand} --as {name}
```

Or:

```text
{name}'s last turn failed: {error}
It keeps its Claude token until it stops, so a send fails the same way.
Recover it: claude setup-token, then stop it, save the token and pick it up:
dockingbird stop {name}
pbpaste | dockingbird login claude --oauth-token -
dockingbird {subcommand} --as {name}
```

Or:

```text
{name}'s last turn failed; its tool gave no error text.
It keeps its Claude token until it stops, so a send fails the same way.
Recover it: claude setup-token, then stop it, save the token and pick it up:
dockingbird stop {name}
pbpaste | dockingbird login claude --oauth-token -
dockingbird {subcommand} --as {name}
```

Or:

```text
{name}'s last turn failed: {error}.
It keeps its Claude token until it stops, so a send fails the same way.
Recover it: renew Claude's login here, which Dockingbird follows
(run claude here once, or your account tool), then stop it and pick it up:
dockingbird stop {name}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name}'s last turn failed: {error}
It keeps its Claude token until it stops, so a send fails the same way.
Recover it: renew Claude's login here, which Dockingbird follows
(run claude here once, or your account tool), then stop it and pick it up:
dockingbird stop {name}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name}'s last turn failed; its tool gave no error text.
It keeps its Claude token until it stops, so a send fails the same way.
Recover it: renew Claude's login here, which Dockingbird follows
(run claude here once, or your account tool), then stop it and pick it up:
dockingbird stop {name}, then dockingbird {subcommand} --as {name}
```

Next step, as the message gives it:

- dockingbird send {name} TEXT
- claude setup-token
- dockingbird stop {name}, then dockingbird {subcommand} --as {name}

Exit status: 0 (done).

### STATUS_WORKING

When: An agent working in a terminal: the files it is working on, and for how long.

One row of a table; its cells line up with the rows around it.

```text
  {label}   working on {claims}   {options}   {elapsed}
```

Or:

```text
  {label}   working   {options}
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_WAITING

When: An agent waiting for a file another agent is working on.

One row of a table; its cells line up with the rows around it.

```text
  {label}   waiting for {holder} ({file})   {options}   {elapsed}
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_NO_TERMINAL

When: An agent working without a terminal, with the command that reconnects to it. The on-the-bus form: an agent on the message bus has no terminal to reconnect to, so its row ends with the `dockingbird send` that gives it work.

One row of a table; its cells line up with the rows around it.

```text
  {label}   working on {claims}   {options}   no terminal: dockingbird {tool} --as {name}
```

Or:

```text
  {label}   working   {options}   no terminal: dockingbird {tool} --as {name}
```

Or:

```text
  {label}   working on {claims}   {options}   on the bus: dockingbird send {name} TEXT
```

Or:

```text
  {label}   working   {options}   on the bus: dockingbird send {name} TEXT
```

Next step, as the message gives it:

- dockingbird {tool} --as {name}
- dockingbird send {name} TEXT

Exit status: 0 (done).

### STATUS_IDLE

When: An agent that reported on its task (done, declined, or asked you for more information) and has no message still waiting for it, or (the at-prompt form) one whose tool says its turn ended and nothing waits. It keeps running until you stop it with `dockingbird stop NAME`; `done` is its report, not a verified result.

One row of a table; its cells line up with the rows around it.

```text
  {label}   idle, reported done (not verified)   {options}   dockingbird stop {name} ends it
```

Or:

```text
  {label}   idle, declined the task   {options}   dockingbird stop {name} ends it
```

Or:

```text
  {label}   idle, needs more information   {options}   dockingbird stop {name} ends it
```

Or:

```text
  {label}   idle   {options}   dockingbird stop {name} ends it
```

Next step: dockingbird stop {name}

Exit status: 0 (done).

### STATUS_ASKS

When: A running agent asks you something. The row counts what it asked (a choice or a plan its tool put up, the end of a Codex turn at a terminal that takes your next words, a question over the bus): `dockingbird questions` lists them and `dockingbird answer` answers one. Only an open question makes an agent ask: one whose tool waits at its prompt with nothing to answer (Claude says so about a minute after any turn ends) shows idle.

One row of a table; its cells line up with the rows around it.

```text
  {label}   asks you {count:question|questions}   {options}   see them: dockingbird questions
```

Next step: dockingbird questions

Exit status: 0 (done).

### STATUS_FAILED

When: A running agent whose last turn failed: the tool ended the turn with an error (for example, it refused the request over access or billing) and did nothing with the message. The row shows the tool's own error line when it gave one, and the recovery's first step: a `dockingbird send`, which starts a new turn in the same conversation and keeps the files the agent is working on and its jobs. The note under "Needs your attention" gives the stop and pick-up if that turn fails too. `dockingbird wait` and `dockingbird inbox` show the failure too. For an agent whose saved Claude token stopped working, the recovery starts with a new token and the agent's stop instead (`claude setup-token`, then `dockingbird stop`), since a send fails the same way; for a token Dockingbird follows from Claude Code on this computer, you renew that login here first.

One row of a table; its cells line up with the rows around it.

```text
  {label}   failed: {error}.   {options}   Recover it: dockingbird send {name} TEXT
```

Or:

```text
  {label}   failed: {error}   {options}   Recover it: dockingbird send {name} TEXT
```

Or:

```text
  {label}   failed, no error text from its tool.   {options}   Recover it: dockingbird send {name} TEXT
```

Or:

```text
  {label}   failed: {error}.   {options}   Recover it: claude setup-token, then dockingbird stop {name}
```

Or:

```text
  {label}   failed: {error}   {options}   Recover it: claude setup-token, then dockingbird stop {name}
```

Or:

```text
  {label}   failed, no error text from its tool.   {options}   Recover it: claude setup-token, then dockingbird stop {name}
```

Or:

```text
  {label}   failed: {error}.   {options}   Recover it: renew Claude's login here, then dockingbird stop {name}
```

Or:

```text
  {label}   failed: {error}   {options}   Recover it: renew Claude's login here, then dockingbird stop {name}
```

Or:

```text
  {label}   failed, no error text from its tool.   {options}   Recover it: renew Claude's login here, then dockingbird stop {name}
```

Next step, as the message gives it:

- dockingbird send {name} TEXT
- claude setup-token
- dockingbird stop {name}

Exit status: 0 (done).

### STATUS_BUS_LOST

When: An agent's bus server, the program its tool reaches the bus through, ended while the tool still ran. Dockingbird restarts the tool, resuming its conversation when its id is known, and messages you send it wait until the server is back. If it doesn't come back, the agent stops and its starter is told why.

One row of a table; its cells line up with the rows around it.

```text
  {label}   lost its bus server, restarting its tool   {options}   on the bus: dockingbird send {name} TEXT
```

Next step: dockingbird send {name} TEXT

Exit status: 0 (done).

### STATUS_RETRYING

When: A running agent whose last turn ended because Anthropic refused its sign-in, while Dockingbird tries that turn again by itself: a few times, a little longer apart each time, so a sign-in that changed meanwhile can reach the agent. The row says which try this is and how many there are at most. A message you send meanwhile goes to the agent instead of the next try. If the last try fails too, the row shows the failed turn and its recovery.

One row of a table; its cells line up with the rows around it.

```text
  {label}   retrying after a sign-in refusal ({retry} of {retries})   {options}   on the bus: dockingbird send {name} TEXT
```

Next step: dockingbird send {name} TEXT

Exit status: 0 (done).

### STATUS_EGRESS_DEFAULT

When: The line under `dockingbird status`'s first line: what new agents can reach unless a config or `--egress` says otherwise, and the `allow` list of `allowlist`.

```text
Egress for new agents: {mode} ({allow})
```

Or:

```text
Egress for new agents: {mode}
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_STOPPED_NOT_SHARED

When: An agent that stopped with work kept in its copy, with the command that picks it up from where you are.

If you deleted that branch, its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where the forms below say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

One row of a table; its cells line up with the rows around it.

```text
  {label}   stopped, {count:commit|commits} not shared yet: dockingbird {subcommand} --as {name}
```

Or:

```text
  {label}   stopped, {count:file|files} not committed: dockingbird {subcommand} --as {name}
```

Or:

```text
  {label}   stopped, may hold work: dockingbird {subcommand} --as {name}
```

Or:

```text
  {label}   stopped, {count:commit|commits} not shared yet: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
  {label}   stopped, {count:commit|commits} not shared yet: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
  {label}   stopped, {count:commit|commits} not shared yet: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
  {label}   stopped, {count:file|files} not committed: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
  {label}   stopped, {count:file|files} not committed: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
  {label}   stopped, {count:file|files} not committed: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
  {label}   stopped, may hold work: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
  {label}   stopped, may hold work: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
  {label}   stopped, may hold work: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or, if you deleted that branch:

```text
  {label}   stopped, {count:commit|commits} not shared yet: git switch -c {branch} dockingbird/{branch}, then dockingbird {subcommand} --as {name}
```

Next step, as the message gives it:

- dockingbird {subcommand} --as {name}
- git switch {branch}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}

Exit status: 0 (done).

### STATUS_STOPPED_BY_RESTART

When: An agent a restart of Docker or Dockingbird stopped. Its copy may hold work; the line gives the command that picks it up.

If you deleted that branch, its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where the forms below say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

One row of a table; its cells line up with the rows around it.

```text
  {label}   restart stopped it, may hold work: dockingbird {subcommand} --as {name}
```

Or:

```text
  {label}   restart stopped it, may hold work: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
  {label}   restart stopped it, may hold work: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
  {label}   restart stopped it, may hold work: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or, if you deleted that branch:

```text
  {label}   restart stopped it, may hold work: git switch -c {branch} dockingbird/{branch}, then dockingbird {subcommand} --as {name}
```

Next step, as the message gives it:

- dockingbird {subcommand} --as {name}
- git switch {branch}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}

Exit status: 0 (done).

### STATUS_CRASHED_KEPT

When: An agent that crashed: it was killed, most likely because it ran out of memory, or its tool ended on its own while no one had asked it to stop, whatever status it ended with. Its copy may hold work; the line gives the command that picks it up.

If you deleted that branch, its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where the forms below say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

One row of a table; its cells line up with the rows around it.

```text
  {label}   crashed, its copy may hold work: dockingbird {subcommand} --as {name}
```

Or:

```text
  {label}   crashed, its copy may hold work: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
  {label}   crashed, its copy may hold work: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
  {label}   crashed, its copy may hold work: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or, if you deleted that branch:

```text
  {label}   crashed, its copy may hold work: git switch -c {branch} dockingbird/{branch}, then dockingbird {subcommand} --as {name}
```

Next step, as the message gives it:

- dockingbird {subcommand} --as {name}
- git switch {branch}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}

Exit status: 0 (done).

### STATUS_TODAY

When: How many commits the agents shared today, and which agents shared them.

One row of a table; its cells line up with the rows around it.

```text
  today   {count:commit|commits} shared by {names:and}
```

Or:

```text
  today   {count:commit|commits} shared by {names} and agents that ended
```

Or:

```text
  today   {count:commit|commits} shared by agents that ended
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_AGENT

When: The first line of `status NAME`: the agent's tool, repo and branch, and how long it has run or how it stopped. For a copy kept on a branch you deleted, it says the branch is no longer in your checkout, or, when a new branch you made since has its name, that the copy is on the branch you deleted. An agent that works in a scratch folder has no repo or branch, so the line says it works in a scratch folder.

```text
{name} ({harness} {version}) on {repo} ({branch}), running {elapsed}
```

Or:

```text
{name} ({harness}) on {repo} ({branch}), stopped
```

Or:

```text
{name} ({harness}) on {repo} ({branch}), crashed
```

Or:

```text
{name} ({harness}) on {repo} ({branch}), stopped by a restart
```

Or:

```text
{name} ({harness} {version}) in a scratch folder, running {elapsed}
```

Or:

```text
{name} ({harness}) in a scratch folder, stopped
```

Or:

```text
{name} ({harness}) in a scratch folder, crashed
```

Or:

```text
{name} ({harness}) in a scratch folder, stopped by a restart
```

Or:

```text
{name} ({harness}) on {repo} ({branch}, no longer in your checkout), stopped
```

Or:

```text
{name} ({harness}) on {repo} ({branch}, no longer in your checkout), crashed
```

Or:

```text
{name} ({harness}) on {repo} ({branch}, no longer in your checkout), stopped by a restart
```

Or:

```text
{name} ({harness}) on {repo} (the {branch} you deleted), stopped
```

Or:

```text
{name} ({harness}) on {repo} (the {branch} you deleted), crashed
```

Or:

```text
{name} ({harness}) on {repo} (the {branch} you deleted), stopped by a restart
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_WAITING

When: In `status NAME`: a file the agent waits for, which agent has it, and for how long.

One row of a table; its cells line up with the rows around it.

```text
  waiting for   {file} ({holder} has it, {elapsed})
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_WORKING

When: In `status NAME`: the files the agent is working on.

One row of a table; its cells line up with the rows around it.

```text
  working on   {claims}
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_FAILED

When: In `status NAME`: the agent's last turn failed, with the tool's own error line when it gave one (for example, a refused request over access or billing). The agent did nothing with that message; the `recover` row under it says what to do.

One row of a table; its cells line up with the rows around it.

```text
  failed   {error}
```

Or:

```text
  failed   its tool gave no error text
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_BUS_LOST

When: `dockingbird status NAME` shows that the agent's bus server ended and Dockingbird is restarting its tool; messages to it wait until the server is back.

One row of a table; its cells line up with the rows around it.

```text
  bus server   lost, restarting its tool
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_RETRYING

When: In `status NAME`: Anthropic refused the agent's sign-in at the end of its last turn, and Dockingbird tries that turn again by itself; the row says which try this is and how many there are at most.

One row of a table; its cells line up with the rows around it.

```text
  retrying   after a sign-in refusal ({retry} of {retries})
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_SIGNAL

When: In `status NAME` of an agent that crashed: the signal that ended its container when no stop was asked, by its Linux name and number (`SIGUSR1, signal 10` for exit status 138), or by its number alone for one without a name. No stop sent it: something in the container did (a test the agent ran that signalled the container, say). Its copy is kept, and the pick-up under it resumes it.

One row of a table; its cells line up with the rows around it.

```text
  ended by   {signal}, signal {number}
```

Or:

```text
  ended by   signal {number}
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_MODEL

When: In `status NAME`: the model the agent runs with. Plain, the value you asked (in its config, after `--`, or with `dockingbird set`), which the tool confirmed; `asked; not confirmed by its tool yet` before Claude Code's first turn reports it; `asked; Codex reports neither in its stream` for a Codex agent, which never confirms it; `asked; its tool reports only to its terminal` for an agent you work with at a terminal; `asked X, running Y` when the tool runs another model than you asked; `its tool's own` when you asked none.

One row of a table; its cells line up with the rows around it.

```text
  model   {asked}
```

Or:

```text
  model   {asked} (asked; not confirmed by its tool yet)
```

Or:

```text
  model   {asked} (asked; Codex reports neither in its stream)
```

Or:

```text
  model   {asked} (asked; its tool reports only to its terminal)
```

Or:

```text
  model   asked {asked}, running {reported}
```

Or:

```text
  model   {reported} (its tool's own; none asked)
```

Or:

```text
  model   unknown
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_EFFORT

When: In `status NAME`: the effort level the agent runs with, in the same forms as its model row; `unknown` when neither you nor its tool named one, as the model row says too.

One row of a table; its cells line up with the rows around it.

```text
  effort   {asked}
```

Or:

```text
  effort   {asked} (asked; not confirmed by its tool yet)
```

Or:

```text
  effort   {asked} (asked; Codex reports neither in its stream)
```

Or:

```text
  effort   {asked} (asked; its tool reports only to its terminal)
```

Or:

```text
  effort   asked {asked}, running {reported}
```

Or:

```text
  effort   {reported} (its tool's own; none asked)
```

Or:

```text
  effort   unknown
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_CONTEXT

When: In `status NAME`: the context the agent's last turn used, of the point its tool compacts at, both in tokens (41K of 967K). The context comes from the tool's own stream; the point is the one you set with `dockingbird set NAME --compact-at N`, else, for a Claude Code agent whose tool reported a native 1M window, the default its docs name for such a model (about 967K), which the row says is the documented one; `unknown` where Dockingbird has no value, never a guess (a Codex agent's own default; a Claude agent's before its tool reported its window, or for a smaller one; a context no turn reported yet).

One row of a table; its cells line up with the rows around it.

```text
  context   {context} of {compact}
```

Or:

```text
  context   {context} of {compact} (asked; not confirmed by its tool yet)
```

Or:

```text
  context   {context} of {compact} (Claude Code's documented default)
```

Or:

```text
  context   {context} of {compact}, the model's window, which caps the point set
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_LIMITS

When: In `status NAME`: the CPU and memory limits the agent's container started with (`--cpus` and `--memory`, or its config's `[limits]`); there is no row when it has neither.

One row of a table; its cells line up with the rows around it.

```text
  limits   {cpu_limit} cpus, {memory_limit} memory
```

Or:

```text
  limits   {cpu_limit} cpus
```

Or:

```text
  limits   {memory_limit} memory
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_LOCAL_MODEL

When: In `status NAME`: the local model the agent started with, which the config you added named and Docker Model Runner on this Mac serves; there is no row for an agent without one. Dockingbird reads it from what it recorded at the start, without asking Docker.

One row of a table; its cells line up with the rows around it.

```text
  local model   {model}, served by Docker Model Runner on this Mac
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_BROWSER_EXTENSIONS

When: In `status NAME`: the ids of the Chrome extensions the agent's browser started with, as its config names them; there is no row when it names none.

One row of a table; its cells line up with the rows around it.

```text
  extensions   {ids}
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_BROWSER_POLICY

When: In `status NAME`: one row per Chrome policy the agent's browser was given, as Chrome's own policy page showed it when the browser started: applied, not applied with Chrome's words, not on the page, or not read when the page itself could not be read.

One row of a table; its cells line up with the rows around it.

```text
  policy   {name}: applied
```

Or:

```text
  policy   {name}: not applied: {detail}
```

Or:

```text
  policy   {name}: not on Chrome's policy page
```

Or:

```text
  policy   {name}: Chrome's policy page could not be read
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_RESUME_ROW

When: In `status NAME`: how an agent started with `--as NAME` picked up: its own conversation (its tool's saved state restored), or a summary of it when that state was missing or over its bound. Or an older conversation, when its last run saved nothing (it crashed): what that run did is not in it.

One row of a table; its cells line up with the rows around it.

```text
  resumed   picked up its conversation
```

Or:

```text
  resumed   picked up from a summary: its conversation could not be kept
```

Or:

```text
  resumed   picked up an older conversation: its last run saved nothing
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_PENDING_ROW

When: In `status NAME`: the requests waiting in the agent's inbox, the tasks and review requests sent to it that it has not settled yet, how long the oldest has waited and who sent it. Status notes and alerts are not counted, and nothing is shown when nothing waits.

One row of a table; its cells line up with the rows around it.

```text
  inbox   {count:delivery|deliveries} waiting, the oldest {elapsed} from {sender}
```

Or:

```text
  inbox   {count:delivery|deliveries} waiting, the oldest {elapsed}
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_REPORTED

When: In `status NAME`: what the agent itself reported about its task when it acknowledged it. `done` is its report, not a verified result; `dockingbird results NAME` writes what it sent. It may also have declined the task, or asked you for more information.

One row of a table; its cells line up with the rows around it.

```text
  reported   done (not verified)
```

Or:

```text
  reported   declined the task
```

Or:

```text
  reported   needs more information
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_REFUSED

When: In `status NAME`: a share of this agent that Dockingbird refused or has not settled yet, one row each, oldest first: its status and the reason Dockingbird recorded (a stale share was based on a commit that is no longer the branch's head), the commit it sent and the head it was checked against.

One row of a table; its cells line up with the rows around it.

```text
  share   {value} ({reason}): {commit} against head {head}, {ago} ago
```

Or:

```text
  share   {value}: {commit} against head {head}, {ago} ago
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_CONNECTIONS

When: In `status NAME`: the connections the agent's start granted it, by name, from a config you added. The agent fetches and pushes through them; it never sees a key.

One row of a table; its cells line up with the rows around it.

```text
  connections   {names}
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_NOT_SHARED

When: In `status NAME`: how many commits the agent hasn't shared yet.

One row of a table; its cells line up with the rows around it.

```text
  not shared   {count:commit|commits}: {commit} {subject}
```

Or:

```text
  not shared   {count:commit|commits}
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_CHANGED

When: In `status NAME`: files the agent changed and hasn't committed. Unknown when they couldn't be counted: the agent hasn't counted them yet, git status in its copy failed or took too long, or Dockingbird couldn't read the copy.

One row of a table; its cells line up with the rows around it.

```text
  changed   {count:file|files} not committed yet
```

Or:

```text
  changed   1 file not committed yet: {file}
```

Or:

```text
  changed   unknown: the files not committed yet could not be counted
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_COMMIT

When: In `status NAME`: one more commit not shared yet.

One row of a table; its cells line up with the rows around it.

```text
   {commit} {subject}
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_FILE

When: In `status NAME`: one more file not committed.

One row of a table; its cells line up with the rows around it.

```text
   {file}
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_MORE

When: In `status NAME`: how many more commits or files there are past the ones listed.

One row of a table; its cells line up with the rows around it.

```text
   and {count} more
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_COPY

When: In `status NAME`: the agent's kept copy, when Dockingbird can't count what it has, or can't count its commits beside the files it lists. Its files go uncounted after a crash, a kill or a restart; its commits when the branch moved on since the copy started (another agent shared, or you sent your own commits) or git couldn't read the copy. Nothing in it is lost: it stays kept, with its files and commits, until you pick it up or `dockingbird clean` removes it.

One row of a table; its cells line up with the rows around it.

```text
  copy   kept; it may hold work
```

Or:

```text
  copy   kept; it may also hold commits not shared yet
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_ENDED

When: In `status NAME`: the agent stopped after sharing everything, so no copy is kept, but its conversation is: the pick-up under it resumes where it left off.

One row of a table; its cells line up with the rows around it.

```text
  stopped   it can pick up where it left off
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_RECONNECT

When: In `status NAME`: the command that reconnects to the agent, or picks up its kept copy, from where you are. For an agent on the message bus: the `dockingbird send` that gives it work, since it has no terminal to reconnect to. For an agent whose last turn failed: the recovery, a `dockingbird send`, which keeps the files it is working on and its jobs, or else stop it, then pick it up, which resumes its conversation; for one whose saved Claude token stopped working, a new token (`claude setup-token`), the stop, the token saved (`dockingbird login claude --oauth-token -`) and the pick-up, or, for a token Dockingbird follows from Claude Code on this computer, renewing that login here, then the stop and pick-up.

If you deleted that branch, its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where the forms below say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

One row of a table; its cells line up with the rows around it.

```text
  no terminal   dockingbird {tool} --as {name}
```

Or:

```text
  pick it up   dockingbird {subcommand} --as {name}
```

Or:

```text
  pick it up   git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
  pick it up   cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
  pick it up   cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
  on the bus   dockingbird send {name} TEXT
```

Or:

```text
  its screen   send it a task: dockingbird send {name} TEXT, or see it: dockingbird {tool} --as {name}
```

Or:

```text
  recover   dockingbird send {name} TEXT, or dockingbird stop {name}, then dockingbird {subcommand} --as {name}
```

Or:

```text
  recover   claude setup-token, then dockingbird stop {name}, then pbpaste | dockingbird login claude --oauth-token -, then dockingbird {subcommand} --as {name}
```

Or:

```text
  recover   renew Claude's login here, then dockingbird stop {name}, then dockingbird {subcommand} --as {name}
```

Or, if you deleted that branch:

```text
  pick it up   git switch -c {branch} dockingbird/{branch}, then dockingbird {subcommand} --as {name}
```

Next step, as the message gives it:

- dockingbird {tool} --as {name}
- dockingbird {subcommand} --as {name}
- git switch {branch}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
- dockingbird send {name} TEXT
- claude setup-token
- dockingbird stop {name}, then dockingbird {subcommand} --as {name}

Exit status: 0 (done).

### DETAIL_LOG

When: In `status NAME`: where Dockingbird's own log of the agent is (not the tool's output).

One row of a table; its cells line up with the rows around it.

```text
  log   Dockingbird's log of this agent, when it ends: {path}
```

Or:

```text
  log   Dockingbird's log of this agent: {path}
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_DOCKER_SLOW

When: Docker didn't answer in time, so `status` can't see what is working right now. It shows what it last knew.

```text
Docker isn't answering, so Dockingbird can't see what is working right now.
Try again in a moment.
```

Next step: Try again in a moment.

Exit status: 0 (done).

### STATUS_COORDINATOR_STOPPED

When: Under "Needs your attention": Dockingbird stopped while agents still run, so they can't share their work. Any other command starts it again.

```text
Dockingbird stopped, but {name} is still running and can't share its work.
Any other command starts Dockingbird again, for example: dockingbird sync
```

Or:

```text
Dockingbird stopped, but {names:and} are still running and can't
share their work.
Any other command starts Dockingbird again, for example: dockingbird sync
```

Next step: dockingbird sync

Exit status: 0 (done).

### STATUS_VERSIONS_DIFFER

When: `status` while Dockingbird of another version runs with no agent in it. A `dockingbird` older than it lists the work kept as it last knew it, and its other commands stop until you update it; with a newer one, any other command finishes the update. When Dockingbird was installed from a folder on this Mac and its code changed while its version stayed the same, the message says the code changed, and names the version once. When `dockingbird update` staged the newer one, it says Dockingbird switches by itself now and no command is needed, or, when that switch failed, that `dockingbird update` tries again.

```text
Dockingbird {running} is running, and this dockingbird is the older {version}.
This one shows the work kept as it last knew it, which can be out of date.
Use the newer one, or update this one: dockingbird update
```

Or:

```text
Dockingbird {running} is running, and this dockingbird is the newer {version}.
Any other command finishes the update, for example: dockingbird sync
```

Or:

```text
Dockingbird's code changed since it started (both are version {version}).
Any other command finishes the update, for example: dockingbird sync
```

Or:

```text
Dockingbird {running} is running, and this dockingbird is the newer {version}.
Dockingbird switches to {version} by itself now; no command is needed.
```

Or:

```text
Dockingbird's code changed since it started (both are version {version}).
Dockingbird switches to the new code by itself now; no command is needed.
```

Or:

```text
Dockingbird {running} is running, and this dockingbird is the newer {version}.
The switch to {version} didn't work. See why and try again: dockingbird update
```

Next step, as the message gives it:

- dockingbird update
- dockingbird sync
- none, where the message only informs

Exit status: 0 (done).

### STATUS_UPDATE_STAGED

When: `status` after `dockingbird update` installed a new version while agents are working: it names the version and the agents it waits for, and says when it is taking over now. Under "Needs your attention": the record of the staged update can't be read, and `dockingbird update` says what to do.

```text
Dockingbird {new} is installed and takes over when {name} ends.
```

Or:

```text
Dockingbird {new} is installed and takes over when {names:and} end.
```

Or:

```text
Dockingbird {new} is taking over now.
```

Or:

```text
Dockingbird can't read the update staged here:
  {path}
See what to do: dockingbird update
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_NO_AGENTS

When: `status` while no agent is working. In a repo whose branch isn't linked and has files the agents don't take, it says only that, and the next line says why a start would refuse.

```text
No agents are working. Start one: cd into a repo, then dockingbird claude
```

Or:

```text
No agents are working. Start one here: dockingbird claude
```

Or:

```text
No agents are working.
```

Next step, as the message gives it:

- cd into a repo, then dockingbird claude
- dockingbird claude
- none, where the message only informs

Exit status: 0 (done).

### STATUS_START_FAILED

When: Under "Needs your attention": the last start of an agent on this branch stopped because Dockingbird couldn't make the agents' copy of the branch. The row says how long ago, why, and the command that starts it again, with `--as` and the agent's name when you named the agent, so the same agent starts; it goes once a start on the branch gets going.

One row of a table; its cells line up with the rows around it.

```text
  {repo} ({branch})   the last start failed {ago} ago: {why}. Try again: dockingbird {subcommand}
```

Or:

```text
  {repo} ({branch})   the last start failed {ago} ago: {why}. Try again: dockingbird {subcommand} --as {agent}
```

Next step, as the message gives it:

- dockingbird {subcommand}
- dockingbird {subcommand} --as {agent}

Exit status: 0 (done).

### NEEDS_ATTENTION

When: The heading in `status` over what only you can fix.

```text
Needs your attention
```

Next step: none; it only informs.

Exit status: 0 (done).

### NOTHING_NEEDS_YOU

When: The last line of `status` when nothing needs you.

```text
Nothing needs your attention.
```

Next step: none; it only informs.

Exit status: 0 (done).

## Set

### SET_DONE

When: You ran `dockingbird set NAME` with `--model` or `--effort`: the change was stored, and the line says what the agent will run with from its next turn (a turn already running finishes as it was). For a Claude Code agent at a terminal, the change is applied by `dockingbird ui` at its next idle prompt: it types the tool's own `/model`, `/effort` and `/autocompact` there, only into an empty prompt box. While the box has unsent text, it types nothing and says the change waits; it never deletes that text. An agent that asks you something gets nothing typed. `dockingbird status NAME` shows what was asked beside what the tool reports.

```text
{name}: model {model}, effort {effort}; applies from its next turn.
See it: dockingbird status {name}
```

Or:

```text
{name}: model {model}; applies from its next turn.
See it: dockingbird status {name}
```

Or:

```text
{name}: effort {effort}; applies from its next turn.
See it: dockingbird status {name}
```

Or:

```text
{name}: compact at {compact}; applies from its next turn.
See it: dockingbird status {name}
```

Or:

```text
{name}: model {model}, compact at {compact}; applies from its next turn.
See it: dockingbird status {name}
```

Or:

```text
{name}: effort {effort}, compact at {compact}; applies from its next turn.
See it: dockingbird status {name}
```

Or:

```text
{name}: model {model}, effort {effort}, compact at {compact}; applies from its next turn.
See it: dockingbird status {name}
```

Or:

```text
{name}: model {model}, effort {effort};
applied by dockingbird ui at its next idle prompt.
See it: dockingbird status {name}
```

Or:

```text
{name}: model {model};
applied by dockingbird ui at its next idle prompt.
See it: dockingbird status {name}
```

Or:

```text
{name}: effort {effort};
applied by dockingbird ui at its next idle prompt.
See it: dockingbird status {name}
```

Or:

```text
{name}: compact at {compact};
applied by dockingbird ui at its next idle prompt.
See it: dockingbird status {name}
```

Or:

```text
{name}: model {model}, compact at {compact};
applied by dockingbird ui at its next idle prompt.
See it: dockingbird status {name}
```

Or:

```text
{name}: effort {effort}, compact at {compact};
applied by dockingbird ui at its next idle prompt.
See it: dockingbird status {name}
```

Or:

```text
{name}: model {model}, effort {effort}, compact at {compact};
applied by dockingbird ui at its next idle prompt.
See it: dockingbird status {name}
```

Or:

```text
{name}: model {model}, effort {effort};
applied at its next idle prompt.
See it: dockingbird status {name}
```

Or:

```text
{name}: model {model};
applied at its next idle prompt.
See it: dockingbird status {name}
```

Or:

```text
{name}: effort {effort};
applied at its next idle prompt.
See it: dockingbird status {name}
```

Or:

```text
{name}: compact at {compact};
applied at its next idle prompt.
See it: dockingbird status {name}
```

Or:

```text
{name}: model {model}, compact at {compact};
applied at its next idle prompt.
See it: dockingbird status {name}
```

Or:

```text
{name}: effort {effort}, compact at {compact};
applied at its next idle prompt.
See it: dockingbird status {name}
```

Or:

```text
{name}: model {model}, effort {effort}, compact at {compact};
applied at its next idle prompt.
See it: dockingbird status {name}
```

Next step: dockingbird status {name}

Exit status: 0 (done).

### SET_STOP_AFTER_TURN

When: You ran `dockingbird set NAME --stop-after-turn`: the agent finishes the turn it is on, starts no new one and stops itself, its work kept. `dockingbird set NAME --run-turns` takes that back before the turn ends.

```text
{name} stops itself once its running turn ends; it starts no new one.
Take it back: dockingbird set {name} --run-turns
```

Next step: dockingbird set {name} --run-turns

Exit status: 0 (done).

### SET_RUN_TURNS

When: You ran `dockingbird set NAME --run-turns`: the stop after its turn is taken back, and the agent takes turns again. One that already stopped is picked up as any stopped agent is.

```text
{name} takes turns again: no stop after its turn is asked.
See it: dockingbird status {name}
```

Next step: dockingbird status {name}

Exit status: 0 (done).

### SET_STOP_TERMINAL

When: You asked an agent that runs at a terminal to stop after its turn, or to take turns again: it has no turns to stop after, so nothing is stored. `dockingbird stop NAME` stops it.

```text
{name} runs at a terminal, which has no turns to stop after.
Stop it: dockingbird stop {name}
```

Next step: dockingbird stop {name}

Exit status: 1 (a problem Dockingbird printed).

### SET_NOT_RUNNING

When: You ran `dockingbird set` for an agent that isn't running. A change lasts only while the agent runs; when you pick it up again it reads its config, so set the model or effort there, or start it and set them then.

```text
{name} isn't running: nothing to change (a pick-up reads its config).
See: dockingbird status
```

Next step: dockingbird status

Exit status: 1 (a problem Dockingbird printed).

### SET_LOCAL_MODEL

When: You ran `dockingbird set` with `--model` for an agent that runs a local model, which the config you added names and Docker Model Runner on this Mac serves. Its tool can reach no other model there, so nothing was changed. Its effort and compact point can still be set; for another model, name it in that config and start the agent again.

```text
{name} runs the local model {model}, which the config you added names, so its
model can't be changed here: nothing was changed. Name another model in that
config's local_model, then start the agent again.
```

Next step: Name another model in that config's local_model, then start the agent again.

Exit status: 1 (a problem Dockingbird printed).

### SET_CODEX_TERMINAL

When: You ran `dockingbird set` for a Codex agent you work with at a terminal, where Codex takes no typed command for a change. The line names the pick-up that applies it: stop the agent, then pick it up with Codex's own flags after `--`; with `auto` alone, Codex's own default, the plain pick-up.

```text
{name} runs at a terminal, where Codex takes no command for a change:
it applies at its next pick-up. Pick it up with it:
dockingbird stop {name}, then dockingbird {subcommand} --as {name} -- {words}
```

Or:

```text
{name} runs at a terminal, where Codex takes no command for a change:
auto is Codex's own default, which its next pick-up runs with:
dockingbird stop {name}, then dockingbird {subcommand} --as {name}
```

Next step, as the message gives it:

- dockingbird stop {name}, then dockingbird {subcommand} --as {name} -- {words}
- dockingbird stop {name}, then dockingbird {subcommand} --as {name}

Exit status: 1 (a problem Dockingbird printed).

### SET_EFFORT_INVALID

When: You ran `dockingbird set --effort` for a Claude Code agent with a word that isn't one of its levels. Dockingbird refuses it rather than let Claude Code ignore it and run at its default effort.

```text
The effort must be one of: {choices}.
See: dockingbird set -h
```

Next step: dockingbird set -h

Exit status: 2 (usage).

### SET_COMPACT_AT_INVALID

When: You ran `dockingbird set NAME --compact-at` with a value in no form Claude Code's own `/autocompact` takes (`auto` for the tool's own window, a token count, `600k`, `1M`, or `600` for 600 thousand), or outside the agent's range: for a Claude Code agent 100K to 1M, the range its docs give (another value it would clamp or ignore without a word); for a Codex agent any count of tokens, since Codex documents no range. Nothing was changed.

```text
The compact point must be auto, or 100K to 1M tokens in Claude Code's own forms:
600000, 600k, 1M, or 600 for 600 thousand.
See: dockingbird set -h
```

Or:

```text
The compact point must be auto, or a count of tokens in these forms:
600000, 600k, 1M, or 600 for 600 thousand.
See: dockingbird set -h
```

Next step: dockingbird set -h

Exit status: 2 (usage).

### SET_VALUE_INVALID

When: You ran `dockingbird set` with a model or effort Dockingbird can't hand to the tool as one argument: empty, with a control character, longer than the bound, starting with `-`, or (an effort) holding `=`. The line names the rule; type the value as the tool's own option takes it.

```text
The {field} must be printable, at most {count} characters, and not start with -.
See: dockingbird set -h
```

Next step: dockingbird set -h

Exit status: 2 (usage).

## Stop and clean

### STOP_CONFIRM

When: You ran `dockingbird stop` while agents are working, so it asks first. Their work is kept either way.

```text
Stop {name} (working) and turn Dockingbird off?
Its work is kept. [y/N]
```

Or:

```text
Stop {names:and} (both working) and turn Dockingbird off?
Their work is kept. [y/N]
```

Or:

```text
Stop {names:and} (all working) and turn Dockingbird off?
Their work is kept. [y/N]
```

Next step: answer y to go on; anything else is no

Exit status: 1 (a problem Dockingbird printed), unless you go on at its question; then the command ends with its own status.

### STOP_DECLINED

When: You answered no to `stop`'s question.

```text
Nothing stopped.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### STOP_NOT_TRIED

When: You ran `dockingbird stop` with several names, and the stop of one of them was refused or failed, so it did not go on: the line names the agents it did not stop. Fix what the line above it says, then stop those again.

```text
The stop ended before these, so they were not stopped: {names:and}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### STOP_REFUSED_NO_TTY

When: You ran `dockingbird stop` without a terminal, as in a script, while agents work. It stops them only with `--yes`.

```text
Agents are working. To stop them without asking: dockingbird stop --yes
```

Next step: dockingbird stop --yes

Exit status: 1 (a problem Dockingbird printed).

### STOPPED

When: `dockingbird stop` stopped every agent and Dockingbird (or only Dockingbird, when no agent ran), or `dockingbird stop NAME` stopped the one agent you named. Their work is kept; when one agent's copy is kept, the line gives the command that picks it up from where you are, and where the copy is when that is another branch or checkout.

If you deleted that branch, the message says `({branch}, no longer in your checkout)` where the forms below say `({branch})`, and its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where they say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

```text
Stopped {names:and}. Dockingbird is off until you next use it.
```

Or:

```text
Stopped {name}.
```

Or:

```text
Stopped {name}. Its work is kept: dockingbird {subcommand} --as {name}
```

Or:

```text
Stopped {name}. Its work is kept in {repo} ({branch}).
To pick it up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
Stopped {name}. Its work is kept in {repo} ({branch}).
To pick it up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
Stopped {name}. Its work is kept in {repo} ({branch}).
To pick it up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
Stopped Dockingbird. It's off until you next use it.
```

Or, if you deleted that branch:

```text
Stopped {name}. Its work is kept in {repo} ({branch}, no longer in your checkout).
To pick it up: git switch -c {branch} dockingbird/{branch}, then dockingbird {subcommand} --as {name}
```

Next step, as the message gives it:

- none, where the message only informs
- dockingbird {subcommand} --as {name}
- git switch {branch}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}

Exit status: 0 (done).

### STOPPED_UPDATE_NEXT

When: `dockingbird stop` stopped the last agent on the older Dockingbird, so the next start finishes the update. When `dockingbird update` staged the new version, Dockingbird switches to it by itself now; when `stop` stopped Dockingbird too, it stays off after the switch until you next use it.

```text
Stopped {name}. The next start finishes the update to {version}.
```

Or:

```text
Stopped Dockingbird. The next command finishes the update to {version}.
```

Or:

```text
Stopped {name}. Dockingbird now switches to {version} by itself.
```

Or:

```text
Stopped Dockingbird. It switches to {version} now and stays off until you next use it.
```

Next step: none; it only informs.

Exit status: 0 (done).

### STOP_NOT_RUNNING

When: You named an agent with `stop` that isn't running, but has work kept. The line gives the command that picks it up from where you are, and says where the work is kept when that is another branch or checkout.

If you deleted that branch, the message says `({branch}, no longer in your checkout)` where the forms below say `({branch})`, and its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where they say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

```text
{name} isn't running. Its work is kept: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} isn't running. Its work is kept in {repo} ({branch}).
To pick it up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} isn't running. Its work is kept in {repo} ({branch}).
To pick it up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} isn't running. Its work is kept in {repo} ({branch}).
To pick it up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or, if you deleted that branch:

```text
{name} isn't running. Its work is kept in {repo} ({branch}, no longer in your checkout).
To pick it up: git switch -c {branch} dockingbird/{branch}, then dockingbird {subcommand} --as {name}
```

Next step, as the message gives it:

- dockingbird {subcommand} --as {name}
- git switch {branch}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}

Exit status: 0 (done).

### STOP_ALREADY_STOPPED

When: You named an agent with `stop` that is already stopped, with nothing kept but its conversation. Nothing was stopped. The line gives the command that picks it up from where you are.

If you deleted that branch, the message says `({branch}, no longer in your checkout)` where the forms below say `({branch})`, and its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where they say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

```text
{name} is already stopped; it can pick up where it left off.
Pick it up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name} is already stopped in {repo} ({branch}); it can pick up where it left off.
Pick it up: git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} is already stopped in {repo} ({branch}); it can pick up where it left off.
Pick it up: cd {checkout}, then dockingbird {subcommand} --as {name}
```

Or:

```text
{name} is already stopped in {repo} ({branch}); it can pick up where it left off.
Pick it up: cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}
```

Or, if you deleted that branch:

```text
{name} is already stopped in {repo} ({branch}, no longer in your checkout); it can pick up where it left off.
Pick it up: git switch -c {branch} dockingbird/{branch}, then dockingbird {subcommand} --as {name}
```

Next step, as the message gives it:

- dockingbird {subcommand} --as {name}
- git switch {branch}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then dockingbird {subcommand} --as {name}
- cd {checkout}, then git switch {branch}, then dockingbird {subcommand} --as {name}

Exit status: 0 (done).

### NOTHING_RUNNING

When: You ran `dockingbird stop`, and nothing was running.

```text
Nothing is running. Dockingbird is off.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_DONE

When: `dockingbird clean` finished: what it removed, and how much space that freed.

```text
Removed {versions:old version|old versions} and temporary files: {freed} freed.
```

Or:

```text
Removed {copies:copy|copies} ({held:each}), {versions:old version|old versions} and temporary files: {freed} freed.
```

Or:

```text
Removed {copies:copy|copies} ({held:each}) and temporary files: {freed} freed.
```

Or:

```text
Removed temporary files: {freed} freed.
```

Or:

```text
Removed {versions:old version|old versions} and temporary files: under 1 MB freed.
```

Or:

```text
Removed {copies:copy|copies} ({held:each}), {versions:old version|old versions} and temporary files: under 1 MB freed.
```

Or:

```text
Removed {copies:copy|copies} ({held:each}) and temporary files: under 1 MB freed.
```

Or:

```text
Removed temporary files: under 1 MB freed.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_KEPT

When: `dockingbird clean` kept the copies you answered no for; `dockingbird clean NAME` also says so for an agent whose results you answered no for, and keeps that agent whole.

```text
Kept {name}'s copy. Nothing else to clean.
```

Or:

```text
Kept the copies of {names:and}. Nothing else to clean.
```

Or:

```text
Kept {name}'s copy.
```

Or:

```text
Kept the copies of {names:and}.
```

Or:

```text
Kept {name}'s results.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_NAME_DELETED

When: You ran `dockingbird clean NAME` (or pressed `x` on a stopped agent in `dockingbird ui`, then `y`): the agent is gone, with what it left (its kept copy, its results and its history) and how much space that freed. `dockingbird status` no longer lists it, and its name starts a new agent.

```text
Deleted {name}: {held:and}; {freed} freed.
```

Or:

```text
Deleted {name}: {held:and}; under 1 MB freed.
```

Or:

```text
Deleted {name}: {held:and}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_NAME_RUNNING

When: You ran `dockingbird clean NAME` for an agent that is still running. Nothing of it was touched: stop it with `dockingbird stop NAME` first, then delete it.

```text
{name} is running. To delete it, stop it first: dockingbird stop {name}
```

Next step: dockingbird stop {name}

Exit status: 1 (a problem Dockingbird printed).

### CLEAN_NAME_NOTHING

When: You ran `dockingbird clean NAME` for an agent Dockingbird started before, but nothing of it is left to delete.

```text
Nothing to delete: {name} has no kept copy, results or history.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_NAME_NOT_REMOVED

When: `dockingbird clean NAME` could not finish deleting an agent. It goes in order (the kept copy, then the results, then the history) and stops at the step that failed, so what comes after it is kept. Run the same command again.

```text
Could not remove {name}'s copy, so nothing of {name} was deleted.
```

Or:

```text
Could not remove {name}'s results, so its history is kept:
{path}
```

Or:

```text
Could not delete {name}'s history, so dockingbird status still lists it.
Run this again: dockingbird clean {name}
```

Next step, as the message gives it:

- none, where the message only informs
- dockingbird clean {name}

Exit status: 1 (a problem Dockingbird printed).

### CLEAN_NAMES_WITH_ALL

When: You gave `dockingbird clean --all` an agent's name. `--all` removes every agent, so it takes none; to delete one agent, leave out `--all`.

```text
dockingbird {command}: --all removes every agent, so it takes no name.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### NOTHING_TO_CLEAN

When: `dockingbird clean` found nothing to remove.

```text
Nothing to clean.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_ASK_UNSHARED

When: `dockingbird clean` asks before removing a kept copy that has commits not shared yet.

```text
{name} left {count:commit|commits} not shared yet. Remove its copy anyway? [y/N]
```

Or:

```text
{name} left commits not shared yet. Remove its copy anyway? [y/N]
```

Or:

```text
{name} may have left commits not shared yet. Remove its copy anyway? [y/N]
```

Next step: answer y to go on; anything else is no

Exit status: 0 (done).

### CLEAN_KEPT_NO_TERMINAL

When: You ran `dockingbird clean` without a terminal, so it couldn't ask about copies that may hold work, and kept them. `--yes` removes them without asking. With a name, the line names that agent's own command, which deletes it alone.

```text
Kept the copies of {names:and}, which may hold work: there is no terminal to ask.
To remove them without asking: dockingbird clean --yes
```

Or:

```text
Kept {name}'s copy, which may hold work: there is no terminal to ask.
To remove it without asking: dockingbird clean --yes
```

Or:

```text
Kept {name}'s copy, which may hold work: there is no terminal to ask.
To delete it without asking: dockingbird clean {name} --yes
```

Or:

```text
Kept {name}'s results: there is no terminal to ask.
To delete them without asking: dockingbird clean {name} --yes
```

Next step, as the message gives it:

- dockingbird clean --yes
- dockingbird clean {name} --yes

Exit status: 1 (a problem Dockingbird printed).

### CLEAN_ASK_CHANGED

When: `dockingbird clean` asks before removing a kept copy that has files not committed. When Dockingbird couldn't count the copy's commits, it says the copy may hold commits not shared yet too. That happens usually because the branch moved on since the copy started (another agent shared, or you sent your own commits), else because git couldn't read or fully count the copy.

```text
{name} left {count:changed file|changed files} not committed. Remove its copy anyway? [y/N]
```

Or:

```text
{name} left {count:changed file|changed files} not committed, and may have left commits not shared yet.
Remove its copy anyway? [y/N]
```

Next step: answer y to go on; anything else is no

Exit status: 0 (done).

### CLEAN_ASK_CRASHED

When: `dockingbird clean` asks before removing a copy that may hold work Dockingbird couldn't count, such as a crashed agent's.

```text
{name} crashed, and its copy may hold work. Remove it anyway? [y/N]
```

Or:

```text
{name} didn't sign in, and its copy may hold work. Remove it anyway? [y/N]
```

Or:

```text
{name} never started, and its copy may hold work. Remove it anyway? [y/N]
```

Or:

```text
{name} stopped, and its copy may hold work. Remove it anyway? [y/N]
```

Next step: answer y to go on; anything else is no

Exit status: 0 (done).

### CLEAN_ALL_CONFIRM

When: You ran `dockingbird clean --all`. It names everything that would be lost, however long the list (agents working now, kept copies, commits you haven't synced with the command that keeps them), then asks you to type `delete`; your code is never touched.

```text
This removes everything Dockingbird made: every agent and its copy, their
history, and the settings and logs in {home}.
{repos}
Your code is untouched. Type delete to go on:
```

Or:

```text
This removes everything Dockingbird made: every agent and its copy, their
history, {saved}, and the settings and logs in {home}.
{repos}
Your code is untouched. Type delete to go on:
```

Next step: type delete to go on; anything else is no

Exit status: 1 (a problem Dockingbird printed), unless you go on at its question; then the command ends with its own status.

### CLEAN_ALL_DECLINED

When: You didn't type `delete` at `clean --all`'s question.

```text
Nothing removed.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### CLEAN_ALL_UNSYNCED

When: Part of `clean --all`'s question: a repo with commits the agents shared that you haven't synced, with the command that keeps them from where you are. For a branch you deleted, it counts the commits that only Dockingbird keeps, which `clean --all` would remove even if you had synced them before, and it names none when nothing would be lost.

If you deleted that branch, the message says `({branch}, no longer in your checkout)` where the forms below say `({branch})`, and its step makes the branch again first: `git switch -c {branch} dockingbird/{branch}` where they say `git switch {branch}`, or `git switch -c {branch}` when the agents' ref is gone too. The last form below shows one.

```text
{repo} ({branch}): {count} commits the agents shared that you haven't synced.
To keep them: dockingbird sync
```

Or:

```text
{repo} ({branch}): {count} commits the agents shared that you haven't synced.
To keep them: git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch}): {count} commits the agents shared that you haven't synced.
To keep them: cd {checkout}, then dockingbird sync
```

Or:

```text
{repo} ({branch}): {count} commits the agents shared that you haven't synced.
To keep them: cd {checkout}, then git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch}): 1 commit the agents shared that you haven't synced.
To keep it: dockingbird sync
```

Or:

```text
{repo} ({branch}): 1 commit the agents shared that you haven't synced.
To keep it: git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch}): 1 commit the agents shared that you haven't synced.
To keep it: cd {checkout}, then dockingbird sync
```

Or:

```text
{repo} ({branch}): 1 commit the agents shared that you haven't synced.
To keep it: cd {checkout}, then git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch}): the agents may have shared commits you haven't synced.
To keep them: dockingbird sync
```

Or:

```text
{repo} ({branch}): the agents may have shared commits you haven't synced.
To keep them: git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch}): the agents may have shared commits you haven't synced.
To keep them: cd {checkout}, then dockingbird sync
```

Or:

```text
{repo} ({branch}): the agents may have shared commits you haven't synced.
To keep them: cd {checkout}, then git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch}): the agents shared commits you haven't synced.
To keep them: dockingbird sync
```

Or:

```text
{repo} ({branch}): the agents shared commits you haven't synced.
To keep them: git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch}): the agents shared commits you haven't synced.
To keep them: cd {checkout}, then dockingbird sync
```

Or:

```text
{repo} ({branch}): the agents shared commits you haven't synced.
To keep them: cd {checkout}, then git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch}, no longer in your checkout): {count} commits the agents shared are kept only by Dockingbird.
To keep them: git switch -c {branch} dockingbird/{branch}
```

Or:

```text
{repo} ({branch}, no longer in your checkout): {count} commits the agents shared are kept only by Dockingbird.
To keep them: cd {checkout}, then git switch -c {branch} dockingbird/{branch}
```

Or:

```text
{repo} ({branch}, no longer in your checkout): {count} commits the agents shared are kept only by Dockingbird.
To keep them: git switch -c {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch}, no longer in your checkout): {count} commits the agents shared are kept only by Dockingbird.
To keep them: cd {checkout}, then git switch -c {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch}, no longer in your checkout): 1 commit the agents shared is kept only by Dockingbird.
To keep it: git switch -c {branch} dockingbird/{branch}
```

Or:

```text
{repo} ({branch}, no longer in your checkout): 1 commit the agents shared is kept only by Dockingbird.
To keep it: cd {checkout}, then git switch -c {branch} dockingbird/{branch}
```

Or:

```text
{repo} ({branch}, no longer in your checkout): 1 commit the agents shared is kept only by Dockingbird.
To keep it: git switch -c {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch}, no longer in your checkout): 1 commit the agents shared is kept only by Dockingbird.
To keep it: cd {checkout}, then git switch -c {branch}, then dockingbird sync
```

Or, if you deleted that branch:

```text
{repo} ({branch}, no longer in your checkout): {count} commits the agents shared that you haven't synced.
To keep them: git switch -c {branch} dockingbird/{branch}, then dockingbird sync
```

Next step, as the message gives it:

- dockingbird sync
- git switch {branch}, then dockingbird sync
- cd {checkout}, then dockingbird sync
- cd {checkout}, then git switch {branch}, then dockingbird sync
- git switch -c {branch} dockingbird/{branch}
- cd {checkout}, then git switch -c {branch} dockingbird/{branch}
- git switch -c {branch}, then dockingbird sync
- cd {checkout}, then git switch -c {branch}, then dockingbird sync

Exit status: 0 (done).

### CLEAN_ALL_NAME_REUSED

When: Part of `clean --all`'s question: a branch you made under the name of a branch you deleted, whose agents' commits only Dockingbird keeps, so `clean --all` would remove them. To keep them, run `dockingbird sync` and answer yes when it asks.

```text
{repo} ({branch}) has a deleted branch's name.
{count} commits that branch's agents shared are kept only by Dockingbird.
To keep them, say yes when sync asks: dockingbird sync
```

Or:

```text
{repo} ({branch}) has a deleted branch's name.
{count} commits that branch's agents shared are kept only by Dockingbird.
To keep them, say yes when sync asks: git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch}) has a deleted branch's name.
{count} commits that branch's agents shared are kept only by Dockingbird.
To keep them, say yes when sync asks: cd {checkout}, then dockingbird sync
```

Or:

```text
{repo} ({branch}) has a deleted branch's name.
{count} commits that branch's agents shared are kept only by Dockingbird.
To keep them, say yes when sync asks: cd {checkout}, then git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch}) has a deleted branch's name.
1 commit that branch's agents shared is kept only by Dockingbird.
To keep it, say yes when sync asks: dockingbird sync
```

Or:

```text
{repo} ({branch}) has a deleted branch's name.
1 commit that branch's agents shared is kept only by Dockingbird.
To keep it, say yes when sync asks: git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch}) has a deleted branch's name.
1 commit that branch's agents shared is kept only by Dockingbird.
To keep it, say yes when sync asks: cd {checkout}, then dockingbird sync
```

Or:

```text
{repo} ({branch}) has a deleted branch's name.
1 commit that branch's agents shared is kept only by Dockingbird.
To keep it, say yes when sync asks: cd {checkout}, then git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch}) has a deleted branch's name.
Commits that branch's agents shared are kept only by Dockingbird.
To keep them, say yes when sync asks: dockingbird sync
```

Or:

```text
{repo} ({branch}) has a deleted branch's name.
Commits that branch's agents shared are kept only by Dockingbird.
To keep them, say yes when sync asks: git switch {branch}, then dockingbird sync
```

Or:

```text
{repo} ({branch}) has a deleted branch's name.
Commits that branch's agents shared are kept only by Dockingbird.
To keep them, say yes when sync asks: cd {checkout}, then dockingbird sync
```

Or:

```text
{repo} ({branch}) has a deleted branch's name.
Commits that branch's agents shared are kept only by Dockingbird.
To keep them, say yes when sync asks: cd {checkout}, then git switch {branch}, then dockingbird sync
```

Next step, as the message gives it:

- dockingbird sync
- git switch {branch}, then dockingbird sync
- cd {checkout}, then dockingbird sync
- cd {checkout}, then git switch {branch}, then dockingbird sync

Exit status: 0 (done).

### CLEAN_ALL_WORKING

When: Part of `clean --all`'s question: an agent that is working now and would be stopped.

```text
{name} is working now: it will be stopped and its copy removed.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_ALL_KEPT

When: Part of `clean --all`'s question: an agent that stopped with its work kept, and what its copy has when Dockingbird counted it. Typing `delete` removes that copy too. It says "work kept", with no count, when Dockingbird couldn't count the copy's commits: usually because the branch moved on since the copy started (another agent shared, or you sent your own commits), or because git couldn't read or fully count the copy.

```text
{name} stopped with {count:commit|commits} not shared yet: its copy will be removed.
```

Or:

```text
{name} stopped with {count:file|files} not committed: its copy will be removed.
```

Or:

```text
{name} stopped with work kept: its copy will be removed.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_ALL_STATE_UNREAD

When: Part of `clean --all`'s question when Dockingbird can't read its `state.json` whole: it is over its size limit, or a link, a folder or a file Dockingbird can't open. `clean --all` removes it unread with the rest. What only that file records can't be listed: your saved sign-ins and keys, the kept copies Docker doesn't show, and which tools `dockingbird mcp install` connected. The line names each tool's own command that removes Dockingbird from it.

```text
Dockingbird's state file is {size_bytes:byte|bytes}, past its limit of {limit_bytes:byte|bytes},
so it goes unread: the saved sign-ins and keys and any other kept copies
it records can't be listed, and go too. A tool connected with mcp install
may still list Dockingbird after; to remove it:
claude mcp remove --scope user dockingbird, or codex mcp remove dockingbird
```

Or:

```text
Dockingbird's state file is a link, a folder or a file it can't open,
so it goes unread: the saved sign-ins and keys and any other kept copies
it records can't be listed, and go too. A tool connected with mcp install
may still list Dockingbird after; to remove it:
claude mcp remove --scope user dockingbird, or codex mcp remove dockingbird
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_ALL_STATE_REMOVED

When: `clean --all` removed a `state.json` Dockingbird couldn't read whole, without reading it, with your saved sign-ins and keys and the kept copies it recorded. It didn't disconnect any tool `dockingbird mcp install` connected, since only that file says which; the line names each tool's own command that does.

```text
Removed Dockingbird's state file unread: it was {size_bytes:byte|bytes}, past its
limit of {limit_bytes:byte|bytes}. The saved sign-ins and keys and the kept
copies it recorded went too.
A tool connected with mcp install may still list Dockingbird; to remove it:
claude mcp remove --scope user dockingbird, or codex mcp remove dockingbird
```

Or:

```text
Removed Dockingbird's state file unread: it was a link, a folder or a file
Dockingbird can't open. The saved sign-ins and keys and the kept copies it
recorded went too.
A tool connected with mcp install may still list Dockingbird; to remove it:
claude mcp remove --scope user dockingbird, or codex mcp remove dockingbird
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_ALL_STOPPED

When: `clean --all --yes` stopped agents that were working, and removed their copies.

```text
Stopped {names:and}, which were working, and removed their copies.
```

Or:

```text
Stopped {name}, which was working, and removed its copy.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_ALL_INSTRUCTIONS

When: Part of `clean --all`'s question: your own rules for the agents, which go too.

```text
Your own rules for the agents go too: {path}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_ALL_PINS

When: Part of `clean --all`'s question: your `versions.toml`, the file that chooses which version each tool runs, which goes too (`--yes` keeps it).

```text
Your tool versions file goes too: {path}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_ALL_NEEDS_TERMINAL

When: You ran `dockingbird clean --all` without a terminal. It removes everything only with `--yes`.

```text
Removing everything asks you to type delete, and there is no terminal.
To remove everything without asking: dockingbird clean --all --yes
```

Next step: dockingbird clean --all --yes

Exit status: 1 (a problem Dockingbird printed).

### CLEAN_ALL_INCOMPLETE

When: `clean --all` couldn't remove everything. What is left is still Dockingbird's, so running it again finishes the job.

```text
Dockingbird couldn't remove everything it made. The rest is still there.
Run dockingbird clean --all again.
```

Next step: Run dockingbird clean --all again.

Exit status: 1 (a problem Dockingbird printed).

### CLEAN_ALL_HOME_REFUSED

When: `DOCKINGBIRD_HOME` points at a folder Dockingbird didn't set up, or at your home folder or one above it, so `clean --all` removes nothing.

```text
{home} has no Dockingbird settings, so clean --all removes nothing.
Point DOCKINGBIRD_HOME at the folder Dockingbird set up, then run this again.
```

Or:

```text
{home} is your home folder or one above it, so clean --all removes nothing.
Point DOCKINGBIRD_HOME at the folder Dockingbird set up, then run this again.
```

Next step: Point DOCKINGBIRD_HOME at the folder Dockingbird set up, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### CLEAN_ALL_LINK_LEFT

When: `clean --all` couldn't remove a repo's Dockingbird link: your git couldn't change it, or the branch's name is one Dockingbird won't pass to git. The link does nothing on its own.

```text
Left the Dockingbird link on {repo} ({branch}): your git couldn't change {path}.
The link does nothing on its own.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_ALL_REFS_LEFT

When: `clean --all` couldn't remove the agents' refs (`dockingbird/...`) from a repo. The message gives the command that removes one.

```text
Left the agents' refs in {repo}: your git couldn't remove them.
Remove one yourself: git branch -dr dockingbird/{branch}
```

Next step: git branch -dr dockingbird/{branch}

Exit status: 0 (done).

### CLEAN_ALL_IMAGE_LEFT

When: `clean --all` couldn't remove one of the things Dockingbird made in Docker, because something else in Docker is built on it or uses it.

```text
Left {tag} in Docker:
something else in Docker is built on it or uses it, so Docker won't remove it.
Remove that first if you no longer want it, then run this again.
```

Or:

```text
Left {tag} in Docker:
your {holder} is built on it, so Docker won't remove it.
Remove {holder} first if you no longer want it, then run this again.
```

Or:

```text
Left {tag} in Docker:
your container {holder} uses it, so Docker won't remove it.
Remove {holder} first if you no longer want it, then run this again.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_ALL_PARENTS_UNREAD

When: `clean --all` asked Docker what else is built on each version of Dockingbird, and Docker didn't answer, so it tried to remove them all. If something else is built on one, Docker keeps it, and the lines after name it.

```text
Docker didn't say what else is built on each version of Dockingbird,
so this run tried to remove them all.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_SIZES_UNREAD

When: `clean` or `clean --all` removed versions of Dockingbird whose size Docker didn't give, or `clean`, `clean NAME` or `clean --all` removed copies or files whose size Dockingbird couldn't read, so the space it says it freed doesn't count them.

```text
Docker didn't say how big the removed versions of Dockingbird were,
so the space freed leaves them out.
```

Or:

```text
Dockingbird couldn't read the size of {copies:removed copy|removed copies},
so the space freed leaves that out.
```

Or:

```text
Dockingbird couldn't read the size of some files it removed,
so the space freed leaves them out.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_RESULTS_LEFT

When: `clean` removed an agent's copy, but couldn't remove the agent's results that were to go with it; they are still in the folder the message names, which you can remove yourself.

```text
Could not remove {name}'s results; they are kept in:
{path}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_ALL_RULES_KEPT

When: `clean --all --yes` kept your own rules for the agents; delete the folder yourself if you no longer want them.

```text
Kept your own rules for the agents: {path}
Delete that folder yourself if you no longer want them.
```

Next step: Delete that folder yourself if you no longer want them.

Exit status: 0 (done).

### CLEAN_ALL_VAULTS_KEPT

When: `clean --all` kept your `vaults` folder, where the stores of your vault connections live (it removes only an empty one); delete the folder yourself if you no longer want them.

```text
Kept the stores of your vault connections: {path}
Delete that folder yourself if you no longer want them.
```

Next step: Delete that folder yourself if you no longer want them.

Exit status: 0 (done).

### CLEAN_ALL_LISTING

When: With `--verbose` only: after `clean --all`, how many of Dockingbird's Docker objects each listing still shows.

```text
{listing}: {count:entry|entries} left
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_ALL_DONE

When: `clean --all` finished: everything Dockingbird made is gone, and how much space that freed.

```text
Removed everything Dockingbird made ({freed}). Your code is untouched.
To remove the command too: uv tool uninstall dockingbird
```

Or:

```text
Removed everything Dockingbird made (under 1 MB). Your code is untouched.
To remove the command too: uv tool uninstall dockingbird
```

Or:

```text
Removed everything Dockingbird made ({freed}). Your code is untouched.
Kept the empty folder {folder}, so the next start works.
To remove the command too: uv tool uninstall dockingbird
```

Or:

```text
Removed everything Dockingbird made (under 1 MB). Your code is untouched.
Kept the empty folder {folder}, so the next start works.
To remove the command too: uv tool uninstall dockingbird
```

Next step: uv tool uninstall dockingbird

Exit status: 0 (done).

## Other

### MORE_ROW

When: Ends a list cut short: how many more there are. The list of what `clean --all` would remove is never cut.

One row of a table; its cells line up with the rows around it.

```text
  and {count} more
```

Next step: none; it only informs.

Exit status: 0 (done).

## Connections: what agents fetch and push through Dockingbird

### CONNECT_ARGUMENTS_REQUIRED

When: You ran `dockingbird connect` without the GitHub repo, the database or the folder and the name it needs, or without a reviewed JSON file, or with both the GitHub repo and the reviewed file, or with `--database` or `--folder` and another of the forms, or with both `--agent` and `--key`, or with `--folder` and `--to`: a folder reaches an agent only when the agent starts, so connect it without `--to` and name it in the agent's config. The message shows what to type.

```text
Inside the repo, use dockingbird connect NAME --github OWNER/REPO,
or dockingbird connect --config FILE.
```

Or:

```text
Use either --github OWNER/REPO or --config FILE with dockingbird connect,
not both.
```

Or:

```text
Use either --agent or --key PATH with dockingbird connect,
not both.
```

Or:

```text
Use only one of these with dockingbird connect:
--folder PATH, --github OWNER/REPO, --config FILE, --database URL,
--service FILE, --browser BROWSER or --vault gopass.
```

Or:

```text
A folder reaches an agent only when it starts.
Connect it without --to, and name it in a config.
```

Next step, as the message gives it:

- dockingbird connect NAME --github OWNER/REPO
- none, where the message only informs

Exit status: 2 (usage).

### CONNECTED_REGISTERED

When: You ran `dockingbird connect` with a reviewed JSON file and no `--to`: the connection is added, granted to no one, and a config you add with `dockingbird config add` may name it; its agents get it when they start.

```text
Saved {name}.
A config you add with dockingbird config add may name it in its connections.
```

Next step: none; it only informs.

Exit status: 0 (done).

### REVOKE_ARGUMENTS_REQUIRED

When: You ran `dockingbird revoke` without both the connection name and target agent name. The message shows the complete command.

```text
Use dockingbird revoke NAME --to AGENT.
```

Next step: none; it only informs.

Exit status: 2 (usage).

### CONNECTION_CONNECT_DONE

When: `dockingbird connect` with a reviewed JSON file and `--to` granted the named connection to that active agent, until the displayed expiry. The agent can fetch and push through it until then.

```text
Connected {name} to {other} until {value}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECTION_LIST_EMPTY

When: `dockingbird connections` found no enabled connections. The message gives the command that connects a GitHub repo, run inside its checkout.

```text
No connections are enabled. Connect a GitHub repo from inside its checkout:
dockingbird connect NAME --github OWNER/REPO
```

Next step: dockingbird connect NAME --github OWNER/REPO

Exit status: 0 (done).

### CONNECTION_LIST_CONNECTION

When: In `dockingbird connections`: the friendly name of one enabled reviewed connection.

```text
{name}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECTION_LIST_OPERATION

When: Under a connection in `dockingbird connections`: one permitted operation from its reviewed catalog.

```text
  Permitted operation: {value}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECTION_LIST_RESOURCE

When: Under a connection in `dockingbird connections`: one permitted resource alias from its reviewed catalog.

```text
  Resource: {label}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECTION_LIST_AGENT

When: Under a connection in `dockingbird connections`: a recorded grant's verified agent name, state and expiration time.

```text
  Agent: {other}; {kind}; until {value}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECTION_LIST_AGENT_OPERATION

When: Under an agent grant in `dockingbird connections`: one operation that grant permits. Each operation is shown separately.

```text
    {other}: operation {value}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECTION_LIST_AGENT_RESOURCE

When: Under an agent grant in `dockingbird connections`: one resource alias that grant permits. Each resource is shown separately.

```text
    {other}: resource {label}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECTION_LIST_UNRESOLVED_AGENT

When: `dockingbird connections` found a recorded grant whose previous agent's name cannot be verified. It shows the state and expiry without borrowing another agent's name.

```text
  Previous or unresolved agent: {kind}; until {value}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECTION_LIST_UNRESOLVED_OPERATION

When: Under a previous or unresolved agent in `dockingbird connections`: one permitted operation from its recorded grant.

```text
    Operation: {value}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECTION_LIST_UNRESOLVED_RESOURCE

When: Under a previous or unresolved agent in `dockingbird connections`: one permitted resource alias from its recorded grant.

```text
    Resource: {label}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECTION_REVOKE_DONE

When: `dockingbird revoke` confirmed revocation of the selected active agent's grant for the named connection.

```text
Revoked {other}'s access to {name}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECTION_DISCONNECT_DONE

When: `dockingbird disconnect` confirmed that the named connection is disabled and removed Dockingbird's copy of its key. Your own key files are left as they are.

```text
Disconnected {name}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECTION_INVALID_NAME

When: A connection or agent name contains characters Dockingbird does not accept, or is too long. Use its existing lowercase name, made from letters, digits and hyphens.

```text
Use a connection or agent name made of lowercase letters, digits and hyphens.
```

Next step: none; it only informs.

Exit status: 2 (usage).

### CONNECTION_INVALID_UNTIL

When: The `--until` value is not an ISO timestamp with a timezone, or its expiration has already been reached. No grant was confirmed.

```text
Use --until with a future ISO timestamp that includes a timezone.
```

Next step: none; it only informs.

Exit status: 2 (usage).

### CONNECTION_INVALID_CONFIG

When: `dockingbird connect` could not accept the reviewed JSON catalog. When it names the catalog file's path, the file itself was refused: it is missing, not a plain file of your own that only you can read, or reached through a link (on a Mac, `/tmp` is `/private/tmp`); give its real path. When the message names a field of the catalog (a remote, a branch or a port, say), that field is the one to fix; the message never shows what it says. For a key file, a `known_hosts` file, an API resource's `env_file`, or a provider's `adc_file`, `config_dir` or `config_file`, the catalog must give the real, absolute path of a file (for `config_dir`, a folder) of your own: not a relative path, one with `..` in it, or a link. When it says the catalog, or an entry of its resources or of a resource's projection, has a key Dockingbird doesn't know, a key of that JSON object (for a resource, its configuration too) is misspelled or doesn't belong there; the message never shows it.

```text
The owner catalog is invalid.
Review the JSON catalog before connecting.
```

Or:

```text
Dockingbird can't use the catalog file at {path}: it must be there, a file
of your own that only you can read, with no link in its path.
Give its real path (on a Mac, /tmp is /private/tmp), then run this again.
```

Or:

```text
The catalog's {field} isn't one Dockingbird can use as written.
Fix it in the JSON catalog, then run this again.
```

Or:

```text
The catalog's {field} must be the real, absolute path of a file
of your own, not a link.
Fix it in the JSON catalog, then run this again.
```

Or:

```text
The catalog's {field} must be the real, absolute path of a folder
of your own, not a link.
Fix it in the JSON catalog, then run this again.
```

Or:

```text
An entry of the catalog's {field} has a key Dockingbird doesn't know.
Fix it in the JSON catalog, then run this again.
```

Or:

```text
The catalog has a key Dockingbird doesn't know.
Fix it in the JSON catalog, then run this again.
```

Next step, as the message gives it:

- none, where the message only informs
- Give its real path (on a Mac, /tmp is /private/tmp), then run this again.
- Fix it in the JSON catalog, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### CONNECTION_CONFIG_CHANGED

When: A reviewed catalog or saved configuration differs from the policy the named connection was added with, or you ran `dockingbird connect` again for a connection with another repo, branch or key file. Its settings never change silently: disconnect it, then connect it again.

```text
The named connection has a different catalog.
Disconnect it before reviewing a new connection.
```

Or:

```text
{name} is already connected with different settings.
To use these instead: dockingbird disconnect {name}
Then run this again.
```

Next step, as the message gives it:

- none, where the message only informs
- dockingbird disconnect {name}

Exit status: 1 (a problem Dockingbird printed).

### CONNECTION_STORE_FAILED

When: Dockingbird could not safely store or read the private configuration for a connection. Check the ownership and permissions of its own home folder.

```text
Could not store or read private connection configuration.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### CONNECTION_FILE_KEPT

When: `dockingbird connect` was refused after it had saved the connection's file under Dockingbird's folder, and that file could not be removed again. Nothing was connected. Delete the file the message names, or `dockingbird clean --all` removes it.

```text
Dockingbird couldn't remove the connection file it had saved at {where};
nothing was connected. Delete it, or run dockingbird clean --all.
```

Next step: dockingbird clean --all

Exit status: 1 (a problem Dockingbird printed).

### CONNECTION_UNKNOWN_CONNECTION

When: You named a connection that is not currently enabled, or you started a config you added that names one. `dockingbird connections` lists the names available now; no agent was started.

```text
No enabled connection has that name. Run dockingbird connections.
```

Or:

```text
No enabled connection is named {name}, so no agent was started.
See: dockingbird connections
```

Next step, as the message gives it:

- none, where the message only informs
- dockingbird connections

Exit status: 1 (a problem Dockingbird printed).

### CONNECTION_AMBIGUOUS_CONNECTION

When: More than one enabled connection has the same friendly name. Dockingbird refuses to choose one for you.

```text
That connection name is ambiguous. Resolve it before making changes.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### CONNECTION_UNKNOWN_AGENT

When: No active agent has the requested name. `dockingbird status` shows which agents are working now.

```text
No active agent has that name. Check dockingbird status.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### CONNECTION_AMBIGUOUS_AGENT

When: More than one active agent has the requested name. Dockingbird refuses to choose one for the access change.

```text
More than one active agent has that name. Check dockingbird status.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### CONNECTION_SESSION_CHANGED

When: The active agent with the requested name changed before its grant or revocation was sent. Dockingbird did not choose the newer agent; check `dockingbird status` before proceeding.

```text
The selected agent changed. Check dockingbird status.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### CONNECTION_UNKNOWN_GRANT

When: You asked to revoke access, but the active agent with that name has no unrevoked grant for that connection. A grant for an earlier agent with the same name is not selected.

```text
The active agent with that name has no unrevoked grant for this connection.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### CONNECTION_INVALID_STATE

When: Dockingbird could not verify complete, consistent connection and agent information, or could not verify the returned access change. It did not report the change as successful.

```text
Could not verify complete, consistent owner state.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### CONNECTION_NATIVE_FAILED

When: Dockingbird could not read or confirm the requested owner access change. It does not automatically retry; check `dockingbird connections` because a change may already have happened.

```text
Could not read or confirm the owner change.
Check dockingbird connections before proceeding.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### CONNECT_GITHUB_DONE

When: `dockingbird connect NAME --github OWNER/REPO` connected the repo and the branch you are on, with a copy of the key your own ssh uses for GitHub, kept in Dockingbird without its passphrase until you disconnect, or, with `--agent`, with your Mac's ssh-agent, which Docker Desktop forwards into Dockingbird, and no copy of any key. The agents of a config whose `connections` list names it fetch and push that branch through Dockingbird; the line names the GitHub account the key signed in as.

```text
Connected {name}: {repo} ({branch}) over SSH as {author}, with a copy of
{where} (no passphrase) kept in Dockingbird until you disconnect.
A config that names it: connections = ["{name}"]
```

Or:

```text
Connected {name}: {repo} ({branch}) over SSH, with a copy of
{where} (no passphrase) kept in Dockingbird until you disconnect.
A config that names it: connections = ["{name}"]
```

Or:

```text
Connected {name}: {repo} ({branch}) over SSH as {author}, with your Mac's
ssh-agent; no key is copied.
A config that names it: connections = ["{name}"]
```

Or:

```text
Connected {name}: {repo} ({branch}) over SSH, with your Mac's
ssh-agent; no key is copied.
A config that names it: connections = ["{name}"]
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECT_NOT_IN_REPO

When: You ran `dockingbird connect NAME --github OWNER/REPO` outside a git checkout, or with `--branch` naming a branch Dockingbird hasn't copied yet. A connection is for the repo and branch you run it in, and connect copies the branch you are on first: switch to that branch and run it again.

```text
Run this inside the repo the connection is for: cd into it, then run it again.
```

Or:

```text
Dockingbird hasn't copied {repo} ({branch}) yet.
On that branch, this copies it first. Switch to it, then run this again:
git switch {branch}
```

Next step, as the message gives it:

- none, where the message only informs
- git switch {branch}

Exit status: 1 (a problem Dockingbird printed).

### CONNECT_GITHUB_INVALID

When: The value after `--github` isn't a repo's owner and name as GitHub shows them, such as `zeus-fyi/myapp`: two parts of letters, digits, hyphens, underscores and dots, joined by one slash.

```text
Use --github OWNER/REPO: the repo's owner and name as GitHub shows them,
such as zeus-fyi/myapp.
```

Next step: none; it only informs.

Exit status: 2 (usage).

### CONNECT_KEY_UNREADABLE

When: The key file `--key` names (or one a reviewed catalog names) is missing, is a link, a folder or a pipe, can be read by someone else, is inside Dockingbird's own folder, or isn't text. Dockingbird shows nothing of its content.

```text
Dockingbird can't use the file at {path}: it must be a file of your own
that only you can read, not a link, and not inside Dockingbird's own
folder.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### CONNECT_KNOWN_HOSTS_UNREADABLE

When: The host-key file `--known-hosts` names (or one a reviewed catalog names) is missing, is a link, a folder or a pipe, can be changed by someone else, is inside Dockingbird's own folder, or isn't text. Anyone may read it, as anyone may read ssh's own file of host keys; Dockingbird shows nothing of its content.

```text
Dockingbird can't use the host-key file at {path}: it must be a file of your own
that no one else can write, not a link, and not inside Dockingbird's own folder.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### CONNECT_NO_KEY

When: You ran `dockingbird connect NAME --github OWNER/REPO` without `--key`, and none of the key files your own ssh would use for GitHub exists as a file of yours, or none of those is a private key Dockingbird can copy. Name one with `--key PATH`, or make a deploy key for the repo.

```text
No SSH key for GitHub was found: ssh -G github.com names none that
exists under ~/.ssh.
Name one: dockingbird connect {name} --github {target} --key PATH.
Or make a deploy key:
ssh-keygen -t ed25519 -N '' -f ~/.ssh/dockingbird_{name}, add its .pub to
the repo as a deploy key with write access, then --key
~/.ssh/dockingbird_{name}
```

Next step: dockingbird connect {name} --github {target} --key PATH

Exit status: 1 (a problem Dockingbird printed).

### CONNECT_PASSPHRASE

When: The key has a passphrase. `ssh-keygen` asks for it on your terminal and makes Dockingbird's copy without one; Dockingbird never reads, keeps or logs the passphrase, and your own key file stays as it is.

```text
{where} has a passphrase. Enter it once, for ssh-keygen to make
Dockingbird's copy without one (Dockingbird never sees it):
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECT_PASSPHRASE_WRONG

When: `ssh-keygen` couldn't unlock the key with the passphrase you typed, or you stopped it. Nothing was saved; run the command again, or make a deploy key for the repo.

```text
That passphrase didn't unlock {where}. Run this again.
If you don't remember it, make a deploy key:
ssh-keygen -t ed25519 -N '' -f ~/.ssh/dockingbird_{name}, add its .pub to
the repo as a deploy key with write access, then --key
~/.ssh/dockingbird_{name}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### CONNECT_PASSPHRASE_NEEDS_TERMINAL

When: The key has a passphrase, and the command runs without a terminal where `ssh-keygen` could ask for it. Run it in a terminal.

```text
{where} has a passphrase, so run this in a terminal, where ssh-keygen can ask for it.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### CONNECT_KEY_HARDWARE

When: The key lives on a security key, or is a kind Dockingbird's SSH doesn't take, so there is nothing Dockingbird can copy. A deploy key made for the repo works instead.

```text
{where} lives on a security key, which Dockingbird can't copy.
Make a deploy key:
ssh-keygen -t ed25519 -N '' -f ~/.ssh/dockingbird_{name}, add its .pub to
the repo as a deploy key with write access, then --key
~/.ssh/dockingbird_{name}
```

Or:

```text
{where} is a kind of key Dockingbird can't copy.
Make a deploy key:
ssh-keygen -t ed25519 -N '' -f ~/.ssh/dockingbird_{name}, add its .pub to
the repo as a deploy key with write access, then --key
~/.ssh/dockingbird_{name}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### CONNECT_KEY_INVALID

When: The file `--key` names (or one a reviewed catalog names) isn't a private SSH key, such as the key's `.pub` file or another text, so Dockingbird asks no passphrase and saves nothing. Name the private key file, the one without `.pub`.

```text
{where} isn't a private SSH key Dockingbird can read.
Name the private key file, not its .pub, then run this again.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### CONNECT_KNOWN_HOSTS_REQUIRED

When: The connection's SSH host isn't one whose keys Dockingbird knows, so it needs a file of that host's keys: `--known-hosts PATH`, or the same setting in the reviewed catalog.

```text
Dockingbird doesn't know this SSH host's keys: name a known_hosts file
with --known-hosts PATH, or set known_hosts in the catalog, then run this again.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### CONNECT_KEY_REFUSED

When: GitHub refused the key; without `--key`, Dockingbird tried each key your own ssh would use for GitHub, and the message names every one GitHub refused. A key's public half, the file with `.pub` after its name, must be in your GitHub account's SSH keys, or added to the repo as a deploy key with write access; or name another key file with `--key PATH`. Nothing was saved.

```text
GitHub didn't accept {where}.
Is its .pub in your GitHub account (Settings, SSH and GPG keys), or added
to the repo as a deploy key with write access?
To use another key file: dockingbird connect {name} --github {target} --key PATH
```

Next step: dockingbird connect {name} --github {target} --key PATH

Exit status: 1 (a problem Dockingbird printed).

### CONNECT_GITHUB_UNREACHABLE

When: Dockingbird's check couldn't reach GitHub from this computer, or got an answer it doesn't know, within its time limit. Nothing was saved.

```text
GitHub couldn't be reached from this Mac. Check your connection, then run this again.
```

Next step: Check your connection, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### CONNECT_HOST_KEY_MISMATCH

When: GitHub answered with an SSH host key Dockingbird doesn't hold, so no key was offered and nothing was saved. A newer Dockingbird may hold GitHub's new key: `dockingbird update`. When you named a file with `--known-hosts`, the key isn't in that file: run the command again without `--known-hosts`, or put GitHub's current key in the file.

```text
GitHub's SSH host key isn't the one Dockingbird knows.
Update Dockingbird: dockingbird update
```

Or:

```text
GitHub's SSH host key isn't in {where}, the file you named with --known-hosts.
Run this again without --known-hosts to use the keys Dockingbird knows,
or put GitHub's current key in it.
```

Next step, as the message gives it:

- dockingbird update
- Run this again without --known-hosts to use the keys Dockingbird knows, or put GitHub's current key in it.

Exit status: 1 (a problem Dockingbird printed).

### CONNECT_KEY_CHANGED

When: You ran `dockingbird connect` again, and the key file it names now has a different key than the copy Dockingbird keeps, such as a key made again at the same path. Dockingbird keeps the copy it has; to use the new key, disconnect the connection, then connect it again. For a database, you ran `dockingbird connect NAME --database URL --password` again with a password other than the one Dockingbird keeps for the role, such as a new one after you changed it on the server: Dockingbird keeps the one it has, so the agents' queries still use it. Disconnect the connection, then connect it again with `--password`. For a vault, you ran `dockingbird connect NAME --vault gopass` again with the same logins and a passphrase other than the one Dockingbird keeps for its store, such as a new one after you changed it in gopass: Dockingbird keeps the one it has. Disconnect the connection, then connect it again.

```text
{name} already keeps a different key for {where}.
To use the one there now: dockingbird disconnect {name}
Then run this again.
```

Or:

```text
{name} already keeps a password for {value}.
To use the one you typed: dockingbird disconnect {name}
Then run this again with --password.
```

Or:

```text
{name} already keeps a passphrase for the store {store}.
To use the one you typed: dockingbird disconnect {name}
Then run this again.
```

Next step: dockingbird disconnect {name}

Exit status: 1 (a problem Dockingbird printed).

### CONNECT_NO_AGENT

When: You ran `dockingbird connect NAME --github OWNER/REPO --agent` in a shell that names no ssh-agent Dockingbird can use: none at all, no socket of yours, or a path with a space or a character ssh would read as its own. Load your key into your agent with `ssh-add`, or copy a key file with `--key PATH` instead. Nothing was saved.

```text
No ssh-agent is running for this shell, so Dockingbird can't use your GitHub
key with --agent.
Load it: ssh-add --apple-use-keychain ~/.ssh/id_ed25519, then run this again.
Or copy a key file instead: dockingbird connect {name} --github {target} --key PATH
```

Next step: ssh-add --apple-use-keychain ~/.ssh/id_ed25519

Exit status: 1 (a problem Dockingbird printed).

### CONNECT_AGENT_REFUSED

When: With `--agent`, Dockingbird's check offered GitHub the keys of your shell's ssh-agent, and GitHub accepted none of them: the agent has no key, or none that your GitHub account knows. `ssh-add -l` lists the keys it has; load your GitHub key with `ssh-add`. Nothing was saved.

```text
GitHub didn't accept a key from your ssh-agent
(ssh-add -l lists the keys it has).
Load your GitHub key: ssh-add --apple-use-keychain ~/.ssh/id_ed25519
Then run this again.
```

Next step: ssh-add --apple-use-keychain ~/.ssh/id_ed25519

Exit status: 1 (a problem Dockingbird printed).

### CONNECT_AGENT_NO_DESKTOP

When: You ran `dockingbird connect` with `--agent`, and this Docker is not Docker Desktop: only Docker Desktop forwards your Mac's ssh-agent into Dockingbird. Copy a key file with `--key PATH` instead. Nothing was checked or saved.

```text
Only Docker Desktop can forward your ssh-agent into Dockingbird, and this
Docker isn't Docker Desktop.
Copy a key file instead: dockingbird connect {name} --github {target} --key PATH
```

Next step: dockingbird connect {name} --github {target} --key PATH

Exit status: 1 (a problem Dockingbird printed).

### COORDINATOR_RESHAPING

When: A connection that uses your Mac's ssh-agent was added, or the last one was disconnected, while no agent ran, so Dockingbird restarted to take Docker Desktop's forwarded ssh-agent, or to give it back.

```text
Restarting Dockingbird to use your Mac's ssh-agent ... done
```

Or:

```text
Restarting Dockingbird to use your Mac's ssh-agent ...
```

Or:

```text
Restarting Dockingbird without your Mac's ssh-agent ... done
```

Or:

```text
Restarting Dockingbird without your Mac's ssh-agent ...
```

Next step: none; it only informs.

Exit status: 0 (done).

### COORDINATOR_RESHAPE_LATER

When: A connection that uses your Mac's ssh-agent was added, or the last one was disconnected, while agents run. Dockingbird isn't restarted under them: it takes the ssh-agent, or gives it back, at its next start. When the agents are done, `dockingbird stop`, then any dockingbird command.

```text
Dockingbird will use your Mac's ssh-agent after its next start.
When the agents are done: dockingbird stop, then any dockingbird command
```

Or:

```text
Dockingbird will stop using your Mac's ssh-agent after its next start.
When the agents are done: dockingbird stop, then any dockingbird command
```

Next step: dockingbird stop

Exit status: 0 (done).

### CONNECT_AGENT_UNREACHABLE

When: The connection is saved, and the ssh-agent Docker Desktop forwards answers nothing. Docker Desktop opened from the Dock or Spotlight has no ssh-agent of its own; quit it and open it from a terminal (`open -a Docker`), so it takes the terminal's, then run any dockingbird command. Until then the connection's requests fail.

```text
Docker Desktop can't reach your Mac's ssh-agent, so agents can't use it yet.
Quit Docker Desktop, open it from a terminal: open -a Docker
Then run any dockingbird command.
```

Next step: open -a Docker

Exit status: 0 (done).

### CONNECT_AGENT_EMPTY

When: The connection is saved, and the ssh-agent Docker Desktop forwards has no key to offer, so its requests fail until you load your GitHub key with `ssh-add`. A terminal with an agent of its own, such as one inside tmux, may have the key while Docker Desktop's agent does not.

```text
The ssh-agent Docker Desktop reaches has no key, so agents can't use it yet.
Load your GitHub key: ssh-add --apple-use-keychain ~/.ssh/id_ed25519
Then run any dockingbird command.
```

Next step: ssh-add --apple-use-keychain ~/.ssh/id_ed25519

Exit status: 0 (done).

### COORDINATOR_AGENT_SOCKET_MISSING

When: Dockingbird started, and Docker had no ssh-agent socket for it, so it started without your Mac's ssh-agent: this Docker is not Docker Desktop, or Docker Desktop lost its socket. The command went on; the connections that use the ssh-agent fail until Docker Desktop has one again. Restart Docker Desktop, or disconnect such a connection and connect it again without `--agent`.

```text
Docker has no ssh-agent socket to give Dockingbird, which started without
your Mac's ssh-agent; the connections that use it will fail until it has one.
Is this Docker Desktop?
Else: dockingbird disconnect NAME, then connect it again without --agent
```

Next step: dockingbird disconnect NAME

Exit status: 0 (done).

### CONNECTION_RELEASED

When: `dockingbird connections --release` recorded the push whose result was unknown as failed, after you checked the branch on GitHub. The next push needs a fresh fetch first.

```text
Released the push to {repo} whose result was unknown.
The next push starts with a fresh fetch.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECTION_NOTHING_UNRESOLVED

When: `dockingbird connections --release` found no push whose result is unknown, so there is nothing to release.

```text
No push is waiting to be released.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECTION_LIST_SSH

When: Under a connection in `dockingbird connections`: what its agents may do through it, fetch, push or both, with which repo and branch.

```text
  Fetch and push {repo} ({branch})
```

Or:

```text
  Fetch {repo} ({branch})
```

Or:

```text
  Push {repo} ({branch})
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_CONNECTIONS

When: In `status`, after the sign-in line, while connections exist: the heading `Connections` and a row under it for each one.

```text
Connections
{rows}
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_CONNECTION_ROW

When: In `status`, under `Connections`: one connection by name, with the repo or server it reaches and the key its copy was made from, the key's path whole (a path too long for the row goes on a line of its own, never cut), or `your Mac's ssh-agent` for one that uses it (`ssh-agent at the next start` while Dockingbird waits to restart for it). A folder of this Mac shows its path, read-only; a database its server, port and name and the role its queries run as, read-only; a service the path of its program.

One row of a table; its cells line up with the rows around it.

```text
  {name}   {target}
```

Or:

```text
  {name}   {target}, a copy of {path}
```

Or:

```text
  {name}   {target}, your Mac's ssh-agent
```

Or:

```text
  {name}   {target}, ssh-agent at the next start
```

Or:

```text
  {name}   folder {path}, read-only
```

Or:

```text
  {name}   database {target} as {value}, read-only
```

Or:

```text
  {name}   service {path}
```

Or:

```text
  {name}   browser {target}
```

Or:

```text
  {name}   gopass vault {target}, {count:login|logins}: {aliases}
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_CONNECTION_LAST

When: In `status NAME`, after its connections: the agent's newest request through them, a fetch or a push of the connected repo, a query of a database or a run of a service, and whether it waits, runs, is done, was cancelled, failed or ended with an unknown result, with how long ago. A push with nothing new to push (the host already has its commit) says so, not that it failed. A service's request waits until you run `dockingbird serve` with the connection's name. A failure says why, in one of these words, where `{host}` is GitHub for a GitHub repo and the server's own name for another: `{host}'s {branch} is ahead: merge it, share, push; fetch again if it moved` (the branch has commits the agents haven't shared: an agent merges its newest fetch of the branch into its work and shares it, then pushes; when the branch moved since that fetch, it fetches again first), `{host} already has this commit`, `a fetch must come first`, `its known_hosts has another key (or none); fix it, disconnect, connect again` (the server's key changed, or the file never had it: put its current key in the known_hosts file, run `dockingbird disconnect NAME`, then connect it again with that file) (for a GitHub repo, `GitHub's SSH host key isn't the one Dockingbird knows: dockingbird update`), `{host} refused the key; add its .pub there with write access` (for a GitHub repo, `GitHub refused the key; add its .pub as a deploy key with write access`), `{host} couldn't be reached`, `{host} refused the request`, `the connections' relay isn't running; run any dockingbird command`, `an answer was too large to read`, `it took too long`, `Dockingbird stopped while it ran`, `another push hasn't finished`, `the agent had ended`, `its access was revoked`, `the connection changed; start the agent again`, `the connection has no key; connect it again`, `Dockingbird couldn't read {host}'s answer; check its {branch} yourself`, `Dockingbird's own checks refused it before anything was sent`, `git failed on Dockingbird's side before anything was sent`, `Docker's disk was full; free some of it, or give it more` or `your Mac's ssh-agent isn't reachable; dockingbird stop, then any command`; for a connection on your Mac's ssh-agent, a refused key reads `{host} refused your ssh-agent's keys; load the right key with ssh-add`. A database's or a service's request says why in one of these: `the role can write, so Dockingbird won't use it; connect a read-only role`, `the database refused the statement; only one read that returns rows runs`, `the query ran past its time limit`, `the result is over its size limit`, `the database couldn't be reached from Dockingbird`, `the database refused the role's password; connect again`, `the request's parameters don't fit the connection`, `dockingbird serve stopped before the result came back`, `the program ended with an error; its output is in the agent's log folder`, `the program ran past the service's time limit`, `the service's checkout isn't at its pinned commit`, `the service's program isn't where it was connected`, `the runner was too slow to start it; it takes the next request`, `the arguments don't fit the service's declaration` or `the database allows prepared transactions, so Dockingbird won't use it`. A browser's request says why in one of these: `the browser's remote control is off; dockingbird serve names the switch`, `the browser, or macOS, didn't allow the connection`, `the browser couldn't be reached`, `the browser isn't installed`, `Firefox isn't installed`, `Firefox couldn't be reached`, `Firefox is open on your profile but can't be lent; quit it, then ask again`, `Firefox has no default profile; open Firefox once`, `the agent's container had stopped` or `the browser relay couldn't start in the agent's container`. A sign-in to a site, typed from a vault connection, says why in one of these: `no browser is lent to this agent right now; open one first`, `the page isn't on the login's site, so nothing was typed`, `the named field isn't a password field, so nothing was typed`, `the page has no code field by that name, so nothing was typed`, `the page has no username field by that name, so nothing was typed; check it`, `the page has no sign-in button by that name, so nothing was typed; check it`, `the vault has no entry, or no time-based code, for that login`, `the stored password has a control or formatting character Dockingbird won't type`, `the vault couldn't be read; check its store and its passphrase`, `the site didn't accept the sign-in; the field was cleared`, `sign-ins run only in a temporary profile: open a browser with profile temporary`, `that login's second factor is a counter (HOTP); use a time-based code`, `the browser's input was refused, so nothing was typed; the serve window says why` (the Mac refused the typing itself, a window in front of the browser or its tab gone; the serve window names what and where), `another window came in front while typing, so typing stopped; nothing was sent` (a window rose over the browser while the host typed, or a field read back other than what was typed; what was typed was cleared, and the agent may ask again once the desktop is quiet) or `the agent let the browser go before the result came back` (the agent released the browser while its sign-in was typed; what was typed was cleared).

One row of a table; its cells line up with the rows around it.

```text
  last request   {value} {repo} queued ({ago} ago)
```

Or:

```text
  last request   {value} {repo} waits for dockingbird serve {name} ({ago} ago)
```

Or:

```text
  last request   {value} {repo} running (asked {ago} ago)
```

Or:

```text
  last request   {value} {repo} done ({ago} ago)
```

Or:

```text
  last request   {value} {repo} cancelled ({ago} ago)
```

Or:

```text
  last request   {value} {repo} ended with an unknown result ({ago} ago)
```

Or:

```text
  last request   {value} {repo} failed ({ago} ago)
```

Or:

```text
  last request   {value} {repo} failed: {detail} ({ago} ago)
```

Or:

```text
  last request   {value} {repo}: nothing new to push; {detail} ({ago} ago)
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_PUSH_UNRESOLVED

When: Under "Needs your attention" in `status`: an agent's push stopped midway, and Dockingbird couldn't tell from the server, GitHub for a GitHub repo, whether it landed. No other push runs until you check the branch there and run `dockingbird connections --release`.

```text
{name}'s push to {repo} ended with an unknown result and the branch
moved meanwhile.
Check it on {host}, then: dockingbird connections --release
```

Or:

```text
A push ended with an unknown result and its branch moved meanwhile.
Check it on {host}, then: dockingbird connections --release
```

Next step: dockingbird connections --release

Exit status: 0 (done).

### RELAY_START_FAILED

When: A command started Dockingbird while a connection exists, and Docker refused to start the small container that carries the connections' SSH traffic to their hosts. The command went on; agents can't fetch or push through a connection until that container runs, which the next dockingbird command tries again.

```text
The connections' relay couldn't start, so agents can't fetch or push
until it does. Check Docker Desktop, then run any dockingbird command.
```

Next step: Check Docker Desktop, then run any dockingbird command.

Exit status: 0 (done).

## Configs, trust and the agents' own commands

### HELP_CONFIG_COMMAND

When: You ran `dockingbird -h` in a repo whose `.dockingbird/` folder, or a config you added with `dockingbird config add`, gives agents a command of its own. Each row names the command, its summary and the file it comes from.

One row of a table; its cells line up with the rows around it.

```text
  {command}  {summary}  ({file})
```

Or:

```text
  {command}  ({file})
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONFIG_PROBLEM_ROW

When: You ran `dockingbird -h` or `dockingbird config list`, and a config, one of its settings or one of its commands does not apply: the file is not valid (the row names the setting that failed, never its value, and says why in the words `dockingbird config add` uses when it refuses a file), a setting is ignored there, a setting of this repo's own config is off because the repo isn't trusted on this Mac (you marked it with `dockingbird trust --off`, or it has no mark while `config.toml` in Dockingbird's folder says `trust = "untrusted"`) and applies once you run `dockingbird trust` in it, a command is in two configs, this repo's own config replaces an added one, two commands are marked as the default, or Dockingbird can't read its own list of the configs you added (the row names that file). Fix the file, run `dockingbird trust` for a repo you trust, run `dockingbird config add` again for one you added, or move the list the row names aside and add each config again: moving it aside makes Dockingbird forget the list, not the copies.

One row of a table; its cells line up with the rows around it.

```text
  {file}: invalid ({key}: {cause})
```

Or:

```text
  {file}: more than {count} configs, so none applies
```

Or:

```text
  {file}: {key} is ignored here
```

Or:

```text
  {file}: {key} applies after dockingbird trust
```

Or:

```text
  {file}: {key} works only in a config you add with dockingbird config add
```

Or:

```text
  {file}: {key} is in another config too, so neither runs
```

Or:

```text
  {file}: {key} is replaced here by this repo's own
```

Or:

```text
  {file}: {key} is one of two defaults, so neither applies
```

Or:

```text
  {path}: Dockingbird can't read its list of added configs; move it aside
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONFIG_READ_FAILED

When: Dockingbird could not read the configs (this repo's `.dockingbird/` folder, or the ones you added), so their commands are not available. Dockingbird's own commands still work, and the command you ran goes on; `dockingbird config list` stops here.

```text
Could not read the configs, so their commands are not available.
```

Next step: none; it only informs.

Exit status: 0 (done) or 1 (a problem Dockingbird printed), as "When:" says.

### CONFIG_REGISTERED

When: You ran `dockingbird config add` with a config of a new name. Its commands now work in every repo, and the line names the connections it may use, if any.

```text
Registered {name}: dockingbird {command} "task"
```

Or:

```text
Registered {name}: dockingbird {command} "task" (connections: {names})
```

Or:

```text
Registered {name}. Its commands are {commands:and}.
```

Or:

```text
Registered {name}. Its commands are {commands:and}
(connections: {names}).
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONFIG_REPLACED

When: You ran `dockingbird config add` with a config of a name you added before: Dockingbird's copy is replaced. Agents already running keep the config they started with.

```text
Replaced {name} (was {digest})
```

Or:

```text
Replaced {name} (was {digest}; connections: {names})
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONFIG_EXTENSION_PACKED

When: You ran `dockingbird config add` with a config whose Chrome extensions include a folder: Dockingbird packed it as a Chrome extension, signed with a key it keeps for that folder, so the folder keeps its id. The line names the folder, its id, the version its `manifest.json` gives and the packed file's size. Agents started from now on get it; editing the folder changes nothing until you add the config again.

```text
Packed {folder} as Chrome extension {id}, version {version} ({size_bytes:byte|bytes})
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONFIG_EXTENSION_OWN_KEY

When: You ran `dockingbird config add`, and a folder among the config's Chrome extensions has a `key` in its `manifest.json`. Dockingbird signs the extension with its own key for that folder, so Chrome gives it the id the line names, not the one that key would give.

```text
{folder}'s manifest.json names its own key; Chrome uses Dockingbird's, so its id is {id}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONFIG_EXTENSION_HIDDEN

When: You ran `dockingbird config add`, and a folder among the config's Chrome extensions has files or folders whose names start with a dot. They are left out of the packed extension; the line counts them.

```text
Left out {count:hidden file or folder|hidden files or folders} of {folder} (names starting with a dot)
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONFIG_LIST_ROW

When: You ran `dockingbird config list`. Each row is one config: where it comes from (this repo or one you added), its commands, the copy agents work in, how they run, the connections it may use and the start of its fingerprint.

One row of a table; its cells line up with the rows around it.

```text
  {name}  {scope}  {commands}  {workspace}  {mode}  {connections}  {digest}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONFIG_LIST_SUMMARY_ROW

When: You ran `dockingbird config list`, and the config on the row above has a `summary`: its one line, shown under its row. A config without one has no such line.

One row of a table; its cells line up with the rows around it.

```text
    {summary}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONFIG_LIST_EMPTY

When: You ran `dockingbird config list`, and neither this repo nor Dockingbird has a config yet.

```text
No configs yet. Put one in this repo's .dockingbird/ folder,
or add one: dockingbird config add PATH
```

Next step: dockingbird config add PATH

Exit status: 0 (done).

### CONFIG_REMOVED

When: You ran `dockingbird config remove`: Dockingbird's copy of that config is gone, and its commands with it.

```text
Removed {name}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONFIG_NOT_REGISTERED

When: You ran `dockingbird config remove` with a name no config you added has. `dockingbird config list` shows the names.

```text
No config named {name} was added. See: dockingbird config list
```

Next step: dockingbird config list

Exit status: 1 (a problem Dockingbird printed).

### CONFIG_INVALID_FILE

When: `dockingbird config add` or `dockingbird config remove` refused the file or the name you gave, or a start refused its config: the line names the setting that failed, never its value, and says why in one of these words: `has a key Dockingbird doesn't know` (the setting named has a key that isn't one of Dockingbird's), `the wrong type`, `not an allowed value`, `not a flag it takes (Claude: --effort, --fallback-model, --max-turns, --model; Codex: --model, -c, -m)` (a tool argument in a flag's place that the tool doesn't take here), `empty`, `too long`, `too many`, `out of range`, `has an unprintable character`, `has a secret in it`, `not a valid name`, `a name Dockingbird keeps`, `repeated`, `cannot go with another key here` (two settings that can't be used together, for example the `full` set of `tools` in a config that works in a `scratch` folder), `not an allowed path`, `not a file Dockingbird can read safely`, `missing`, `too large`, `not UTF-8 text`, `not well formed` (a config that isn't valid TOML), `only for a config you added`, `a repository's config cannot ask for a browser, its extensions or its policy; set them on a config you added` (a `browser`, its extensions or its policy in a checkout's own config), `a repository's config cannot ask for a local model; set it on a config you added` (a local model in a checkout's own config), `not a Chrome Web Store link, a 32-letter extension id or a folder path starting with / or ~/` (an extension the browser can't be given), `its signing key under configs/.extension-keys can't be read; remove it and add the config again for a new id` (the key Dockingbird keeps for a folder extension is damaged), `can't be read` (a file the config names), or `refused by the check` (a refusal that gave no reason). A config must be a regular `.toml` file of yours outside Dockingbird's folder, and a name is lowercase letters, digits and dashes. A config runs in its own `mode` and `harness` only, so `--terminal` or `--harness` can't change them.

```text
{file}: invalid ({key}: {cause})
Fix that, then run this again.
```

Next step: Fix that, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### CONFIG_INDEX_UNREADABLE

When: You ran `dockingbird config add` or `dockingbird config remove`, and Dockingbird can't read its list of the configs you added: `configs/index.json`, in Dockingbird's folder, is damaged, was written by another version of Dockingbird, is too large, is not text, or is a link or another user's file. The line names the file. Move it aside (rename it, for example to `index.json.damaged`), then run the command again. Moving it aside makes Dockingbird forget the list, not your configs: each config's copy stays in the `configs` folder, and `dockingbird config add` with a config's file puts it on the list again and replaces its copy. `dockingbird config list` and `dockingbird -h` name the same file in a row until you do.

```text
Dockingbird can't read its list of added configs:
  {path}
Move it aside, then run this again.
```

Next step: Move it aside, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### CONFIG_INDEX_FULL

When: You ran `dockingbird config add` with a config whose name isn't added yet, and Dockingbird already has as many added configs as it keeps; the line says how many. Remove one you don't use with `dockingbird config remove NAME`, then add this one again. A config whose name is already added is replaced, never refused for this.

```text
Dockingbird already has {count:added config|added configs}, the most it can keep.
Remove one first: dockingbird config remove NAME
```

Next step: dockingbird config remove NAME

Exit status: 1 (a problem Dockingbird printed).

### TRUSTED

When: You ran `dockingbird trust` in a repo: Dockingbird marks the repo trusted on your Mac, whatever `config.toml`'s `trust` line says, removing the mark `dockingbird trust --off` left, if any, and the repo's own settings, hooks and MCP servers load in agents started there.

```text
Trusted {path}. This checkout's own settings, hooks and MCP servers
load in agents started here.
```

Next step: none; it only informs.

Exit status: 0 (done).

### TRUST_PIN_UNPROVEN

When: After `dockingbird trust`, for each tool whose sign-in Dockingbird has not yet proven safe from a repo's own settings: that tool keeps them off for now, trusted or not.

```text
Claude Code keeps them off for now: Dockingbird has not yet proven
they can't redirect its sign-in.
```

Or:

```text
Codex keeps them off for now: Dockingbird has not yet proven
they can't redirect its sign-in.
```

Next step: none; it only informs.

Exit status: 0 (done).

### TRUST_FORGOTTEN

When: You ran `dockingbird trust --off` (or `--forget`, the same): Dockingbird marks the repo untrusted, on your Mac only, and its own settings, hooks and MCP servers stay off in agents started there until you run `dockingbird trust` in it.

```text
Not trusted: {path}. Its own settings, hooks and MCP servers stay off
in agents started here.
```

Next step: none; it only informs.

Exit status: 0 (done).

### TRUST_NOT_A_CHECKOUT

When: You ran `dockingbird trust` outside a git repo, or named a folder that is not in one, so nothing was recorded.

```text
{path} is not in a git repo, so there is nothing to trust.
Run it in your repo, or name it: dockingbird trust PATH
```

Next step: dockingbird trust PATH

Exit status: 1 (a problem Dockingbird printed).

### TRUST_CONFIG_INVALID

When: You started an agent, or ran `dockingbird -h` or `dockingbird config list` in a repo, and `config.toml` in Dockingbird's folder can't be read as written: its `trust` line, which sets whether a repo you haven't marked is trusted, is something other than `"trusted"` or `"untrusted"`, or the file isn't TOML, or it isn't a plain file of yours Dockingbird can read (a link, which Dockingbird never follows there, a folder, a file too large or not UTF-8). Dockingbird never guesses which you meant: the start stops before anything runs, and the help and the list say it and go on without this repo's own configs. Fix the line or the file, or remove it: with no `trust` line, every repo is trusted unless you marked it with `dockingbird trust --off`, and `dockingbird trust` marks one trusted whatever the line says.

```text
{path}: trust must be "trusted" or "untrusted".
No agent starts until it is fixed.
Fix the line, or remove it: then every repo is trusted unless you mark it.
```

Or:

```text
{path} isn't TOML, so Dockingbird can't read its trust line,
trust = "trusted" or trust = "untrusted".
No agent starts until it is fixed.
Fix the file, or move it aside: then every repo is trusted unless you mark it.
```

Or:

```text
{path} isn't a regular file of yours, or is too large or not UTF-8,
so Dockingbird can't read its trust line.
No agent starts until it is fixed.
Make it a plain file of yours (a link won't do), or move it aside.
```

Next step, as the message gives it:

- Fix the line, or remove it: then every repo is trusted unless you mark it.
- Fix the file, or move it aside: then every repo is trusted unless you mark it.
- Make it a plain file of yours (a link won't do), or move it aside.

Exit status: 0 (done) or 1 (a problem Dockingbird printed), as "When:" says.

### START_USING_DEFAULT

When: You ran `dockingbird start` without a command, in a repo whose `.dockingbird/` folder marks one command as its default: that command runs, and the line names it and its file.

```text
Using {command} from {file} for this checkout
```

Next step: none; it only informs.

Exit status: 0 (done).

### START_COMMAND_UNKNOWN

When: You named a command no config here gives. The message lists the commands you can start here; `dockingbird config list` shows every config and what it gives. When you continued an agent by name and its own command is the one missing (its config was removed), the agent waits: add the config again with `dockingbird config add`, then continue it by that command.

```text
No command named {command} here. The commands here are {commands:and}.
See: dockingbird config list
```

Or:

```text
No command named {command} here, and none is available here.
See: dockingbird config list
```

Or:

```text
No command named {command} here, so {name} can't be continued until a config
gives {command} again. The commands here are {commands:and}.
See: dockingbird config list
```

Or:

```text
No command named {command} here, and none is available here, so {name} can't
be continued until a config gives {command} again.
See: dockingbird config list
```

Next step: dockingbird config list

Exit status: 1 (a problem Dockingbird printed).

### START_NO_SIGNIN_BUS

When: You started an agent without a terminal for a tool that isn't signed in and has no API key saved: nobody would see its sign-in, so nothing was started. Sign in once with `dockingbird login`. When `~/.claude/settings.json` was skipped on the way (a link, or a file others may write, say), the message names it and the rule, since that file may hold your only Claude login: make it a plain file of yours (not a link) that only you can write, readable and under 64 KiB.

```text
{harness} isn't signed in, so nothing was started.
An agent without a terminal can't sign in. Sign in first: dockingbird login {tool}
```

Or:

```text
{harness} isn't signed in, so nothing was started: ~/.claude/settings.json was
skipped ({why}) and no other login was found.
An agent without a terminal can't sign in. Make it a plain file of yours
(not a link) that only you can write, readable and under 64 KiB, or sign in
first: dockingbird login {tool}
```

Next step: dockingbird login {tool}

Exit status: 1 (a problem Dockingbird printed).

### START_LOGIN_HERE_EXPIRED

When: You started an agent of a tool whose login on this computer Dockingbird follows, and that login has expired here. Use the tool on this computer once, so it renews its login, then start again; `dockingbird login claude --here` reads it again at once.

```text
{harness}'s login on this computer expired and Dockingbird could not
renew it, so nothing was started.
Run {harness} here once (or your account tool), then try again.
To read its login again now: dockingbird login {tool} --here
To sign in separately: dockingbird logout {tool}, then dockingbird login {tool}
```

Next step: dockingbird login {tool} --here

Exit status: 1 (a problem Dockingbird printed).

### START_LOGIN_HERE_GONE

When: You started an agent of a tool whose login on this computer Dockingbird follows, and you are no longer signed in to that tool here. Sign in to it on this computer again, or sign in for Dockingbird only with `dockingbird logout claude` then `dockingbird login claude`.

```text
{harness} is no longer signed in on this computer, so nothing was started.
Run {harness} here once (or your account tool), then try again.
To read its login again now: dockingbird login {tool} --here
To sign in separately: dockingbird logout {tool}, then dockingbird login {tool}
```

Next step: dockingbird login {tool}

Exit status: 1 (a problem Dockingbird printed).

### START_GATEWAY_UNREACHABLE

When: You started a Claude agent in the `models` or `allowlist` egress mode while Claude's login on this computer goes through a gateway on this Mac itself (`http://127.0.0.1:59471`, say, a proxy of yours). In those modes an agent reaches only its own proxy, which admits no address of this computer, so the start stopped before making anything rather than fail its first turn. Start with `--egress full` (the agent then reaches the gateway as `host.docker.internal`), or point Claude Code here at an `https://` address agents can reach.

```text
Claude's login on this computer goes through {gateway},
this computer's own address, which an agent in the {mode} egress mode can't
reach (its proxy admits no address of this computer), so nothing was started.
Point Claude Code here at an https:// address agents can reach, or start
with --egress full.
```

Next step: Point Claude Code here at an https:// address agents can reach, or start with --egress full.

Exit status: 1 (a problem Dockingbird printed).

### HARNESS_ARG_STREAM_REFUSED

When: You passed an argument after `--` that Dockingbird refuses: one it sets itself for an agent without a terminal, or the hook-trust bypass, which would let a repo's hooks run unchecked. Nothing was started. When you picked an agent up with `--as NAME` and typed no arguments, the refused one came from that agent's last start, which a pick-up runs again; arguments you give after `--` replace all of that start's.

```text
Dockingbird sets {option} itself for an agent without a terminal,
so nothing was started.
```

Or:

```text
{option} would let a repo's hooks run unchecked, so nothing was started.
```

Or:

```text
{option} came from {name}'s last start, and Dockingbird sets it itself for an
agent without a terminal, so nothing was started. Words you give after --
replace all of that start's.
```

Or:

```text
{option} came from {name}'s last start, and it would let a repo's hooks run
unchecked, so nothing was started. Words you give after -- replace all of
that start's.
```

Next step: none; it only informs.

Exit status: 2 (usage).

### HARNESS_ARG_LOCAL_MODEL

When: You started an agent of a config that names a local model and passed an argument after `--` that would change the model the tool asks for (`--model`, `-m` or `--fallback-model`) or, for Codex, where it sends its requests (`--oss`, `--ignore-user-config`, `--profile`, or a `-c` that sets its base URL). Docker Model Runner serves only the model the config names, so nothing was started: start it without that argument, or name another model in the config. When you picked an agent up with `--as NAME` and typed no arguments, the argument came from that agent's last start; arguments you give after `--` replace all of that start's.

```text
{option} would change the model the tool asks for, or where it asks, and
this config's agents run the local model {model}, so nothing was started.
Start it without {option}.
```

Or:

```text
{option} came from {name}'s last start, and it would change the model the
tool asks for, or where it asks, while this config's agents run the local
model {model}, so nothing was started.
Words you give after -- replace all of that start's.
```

Next step, as the message gives it:

- Start it without {option}.
- Words you give after -- replace all of that start's.

Exit status: 2 (usage).

### START_ARGS_NOT_KEPT

When: You started an agent with arguments after `--`, and keeping them for its next pick-up would take Dockingbird's `state.json` past the size it reads, so they were left out of it. The agent runs with them now; when you pick it up again with `--as NAME`, give them again after `--`, or it runs without them.

```text
{name}'s arguments after -- weren't kept: they would take state.json past {limit},
so its next pick-up runs without them unless you give them again.
```

Next step: none; it only informs.

Exit status: 0 (done) or 1 (a problem Dockingbird printed), as "When:" says.

### REPO_SETTINGS_OFF

When: You started an agent in a repo that isn't trusted on this Mac (one you marked with `dockingbird trust --off`, or one with no mark while `config.toml` in Dockingbird's folder says `trust = "untrusted"`; every other repo is trusted), or a command whose config leaves `repo_settings` off: the repo's own settings, hooks and MCP servers don't load in it. In a repo that isn't trusted, `dockingbird trust` turns them back on where the tool's sign-in is proven safe from them. For a command whose config leaves them off, `repo_settings = true` in that config does; `dockingbird trust` alone doesn't.

```text
Repository settings, hooks and MCP servers are off here
(dockingbird trust turns them on).
```

Or:

```text
Repository settings, hooks and MCP servers are off here.
```

Or:

```text
Repository settings, hooks and MCP servers are off for this command:
its config leaves them off (repo_settings = true in that config turns them on).
```

Next step, as the message gives it:

- dockingbird trust
- none, where the message only informs

Exit status: 0 (done).

### START_PROJECT_CONNECTIONS

When: You started a config from a repo's own `.dockingbird/` folder that names connections: only a config you add may name them, so a repo you cloned can't reach your credentials. Nothing was started; add it with `dockingbird config add` if you trust it.

```text
{file} names connections, which only a config you add may name,
so nothing was started.
Add it first: dockingbird config add {config_path}
```

Next step: dockingbird config add {config_path}

Exit status: 1 (a problem Dockingbird printed).

### START_PROJECT_VERSION

When: You started a config from a repo's own `.dockingbird/` folder that sets `version`, at its top level or in one of its commands: only a config you add may pin the tool's version, so a repo you cloned can't choose what runs. Nothing was started; add it with `dockingbird config add` if you trust it.

```text
{file} sets version, which only a config you add may set,
so nothing was started.
Add it first: dockingbird config add {config_path}
```

Next step: dockingbird config add {config_path}

Exit status: 1 (a problem Dockingbird printed).

### START_PROJECT_RULES_REPLACED

When: You started Codex in a repo you trusted whose own `.codex/config.toml` sets Codex's developer-instructions key, the one the agent's Dockingbird rules travel in, so the repo would replace them. Nothing was started: remove the key, or run with the repo's settings off with `dockingbird trust --off`. The same line shows when that file can't be read (a link, too large, not TOML).

```text
{file} sets developer_instructions, which replaces the agent's
Dockingbird rules in a trusted checkout, so nothing was started.
Remove the key, or run untrusted: dockingbird trust --off
```

Or:

```text
{file} can't be checked for developer_instructions (a link, too
large or not TOML), so nothing was started in this trusted checkout.
Fix the file, or run untrusted: dockingbird trust --off
```

Next step: dockingbird trust --off

Exit status: 2 (usage).

### INSTRUCTION_FILE_REFUSED

When: You started an agent with `--agent-md` or `--claude-md` (or picked up one that started with it), and the file is missing, a link, not a regular file, larger than the limit, not UTF-8, or has a Dockingbird credential. Nothing was started.

```text
{path} can't be used for {option}, so nothing was started.
Give a regular UTF-8 text file of at most {limit}, with no
Dockingbird credential in it.
```

Or:

```text
{path}, the file {name} started with for {option}, can't be read now, so nothing was started.
Put it back at that path, or start a new agent with --new.
```

Next step, as the message gives it:

- Give a regular UTF-8 text file of at most {limit}, with no Dockingbird credential in it.
- Put it back at that path, or start a new agent with --new.

Exit status: 1 (a problem Dockingbird printed).

### INSTRUCTION_FILE_UNREAD

When: You started an agent with `--agent-md` or `--claude-md` where its tool would not read that file at startup: a scratch folder, Codex with `--claude-md`, a config's command whose repo settings don't load for Claude (its `repo_settings` is off, or the checkout isn't trusted), or Codex in a trusted checkout whose branch has `AGENTS.override.md`. Nothing was started.

```text
A scratch folder has no repo copy, so {option} can't be used there; nothing was started.
Start it in a repo, or attach the file to its task with --file.
```

Or:

```text
Codex doesn't read CLAUDE.md at startup, so --claude-md can't be used with
Codex; nothing was started.
Give Codex the file with --agent-md PATH instead.
```

Or:

```text
Claude reads no {file} here: the repo's own settings never load for it in
this Dockingbird, so {option} can't be used; nothing was started.
Attach the file to its task with --file instead.
```

Or:

```text
Claude reads no {file} for this command: its config's repo settings don't
load here (repo_settings is off, or the checkout isn't trusted on this Mac),
so {option} can't be used; nothing was started.
Set repo_settings = true in that config and trust the checkout, or start it
with dockingbird claude.
```

Or:

```text
This trusted checkout has AGENTS.override.md, which Codex reads instead of
AGENTS.md, so --agent-md can't be used; nothing was started.
Remove it from the branch, or run
untrusted: dockingbird trust --off (dockingbird trust turns trust back on)
```

Next step, as the message gives it:

- none, where the message only informs
- dockingbird trust --off

Exit status: 2 (usage).

### INSTRUCTION_FILE_CARRIED

When: You picked up an agent with `--as`, and it started with `--agent-md` or `--claude-md`: an agent keeps its instruction files for its whole life, so this start reads the same file again from the same path.

```text
{name} starts again with {option} {path}, as it has since its first start.
```

Next step: none; it only informs.

Exit status: 0 (done).

### INSTRUCTION_FILE_FIXED

When: You picked up or reconnected to an agent with `--as` and gave `--agent-md` or `--claude-md` another file than the one it started with, or a file it started without. An agent keeps its instruction files for its whole life; a new agent (`--new`) can use another.

```text
{name} was started with {path} as its {file} and keeps it for its whole
life, so {option} {given} can't be used for it; nothing was started.
To use another file, start a new agent: run the same command with --new
instead of --as {name}.
```

Or:

```text
{name} was started with the repo's own {file} and keeps it for its whole
life, so {option} {given} can't be used for it; nothing was started.
To use your file, start a new agent: run the same command with --new
instead of --as {name}.
```

Next step, as the message gives it:

- To use another file, start a new agent: run the same command with --new instead of --as {name}.
- To use your file, start a new agent: run the same command with --new instead of --as {name}.

Exit status: 2 (usage).

### INSTRUCTION_FILE_SAVED

When: A new agent's start found that an earlier agent had changed the AGENTS.md or CLAUDE.md that `--agent-md` or `--claude-md` gave it. Dockingbird saved the changed file to its agent logs folder, then put the repo's own file back; nothing was lost and nothing reached the repo.

```text
{name}'s copy held changes to the {file} an earlier agent was given. They are
saved in {path}, and the repo's own {file} is back in its copy.
```

Or:

```text
{name}'s copy held changes to the {file} an earlier agent was given, and the
repo's own {file} is back in its copy; the changed file couldn't be copied to
this Mac and stays in the agent's log inside Dockingbird.
```

Next step: none; it only informs.

Exit status: 0 (done).

### AGENT_COPY_PREPARING

When: You started an agent without a terminal: Dockingbird gets the agent ready and prepares its copy of the repo. The line shows while it runs, then how long it took.

```text
Preparing the agent's copy ... done ({elapsed})
```

Or:

```text
Preparing the agent's copy ...
```

Next step: none; it only informs.

Exit status: 0 (done).

### AGENT_CONTAINER_STARTING

When: You started an agent without a terminal: Dockingbird makes its container and starts it. The line shows while it starts, then how long it took.

```text
Starting the agent's container ... done ({elapsed})
```

Or:

```text
Starting the agent's container ...
```

Next step: none; it only informs.

Exit status: 0 (done).

### AGENT_TASK_SENDING

When: You started an agent with a task: Dockingbird sends the task as the thread's first message. The line shows while it is sent, then how long it took.

```text
Sending the task ... done ({elapsed})
```

Or:

```text
Sending the task ...
```

Next step: none; it only informs.

Exit status: 0 (done).

### AGENT_STARTED_BUS

When: You started an agent without a terminal: it works on its task, which opened the thread the line names, and the command returned. `dockingbird wait` shows what it sends you.

```text
{name} started on {repo} ({branch}).
Thread {thread}. Watch: dockingbird wait {name}
```

Or:

```text
{name} started in a scratch folder.
Thread {thread}. Watch: dockingbird wait {name}
```

Next step: dockingbird wait {name}

Exit status: 0 (done).

### START_STREAM_FORM

When: You started an agent without a terminal, for a tool whose agents run with a screen of their own, but the start gave the tool words of its own (after `--`, or its config's own tool arguments) that only a run without a screen takes. So this agent runs without a screen: `dockingbird send` reaches it as before, and `dockingbird claude --as NAME` has no screen to show.

```text
{name} runs without a screen: its arguments are for a run without one.
```

Next step: none; it only informs.

Exit status: 0 (done).

### START_NO_SCREEN_TRUST

When: You started an agent without a terminal, for a tool whose agents run with a screen of their own, in a repo you marked untrusted (`dockingbird trust --off`), with a config that leaves the repo's own settings off, or in a scratch folder, whose repo settings are always off. There its tool would first ask whether to trust the folder, which Dockingbird never answers, so this agent runs without a screen: `dockingbird send` reaches it as before.

```text
{name} runs without a screen: its tool would ask whether to trust this folder.
```

Next step: none; it only informs.

Exit status: 0 (done).

### AGENT_STARTED_IDLE

When: You started an agent without a terminal and without a task: it waits for its first message, which `dockingbird send` gives it.

```text
{name} started on {repo} ({branch}), idle.
Send it a task: dockingbird send {name} TEXT
```

Or:

```text
{name} started in a scratch folder, idle.
Send it a task: dockingbird send {name} TEXT
```

Next step: dockingbird send {name} TEXT

Exit status: 0 (done).

### AGENT_STARTED_TASK_REFUSED

When: You started an agent without a terminal and with a task, and Dockingbird refused the task once the agent was running: the agent runs without it, and the refusal follows. `dockingbird send` gives it a task; `dockingbird stop` stops it.

```text
{name} started on {repo} ({branch}) and runs without its task: Dockingbird refused it.
Send it a task: dockingbird send {name} TEXT
Or stop it: dockingbird stop {name}
```

Or:

```text
{name} started in a scratch folder and runs without its task: Dockingbird refused it.
Send it a task: dockingbird send {name} TEXT
Or stop it: dockingbird stop {name}
```

Next step: dockingbird send {name} TEXT

Exit status: 0 (done).

### AGENT_STARTED_AGAIN

When: You started an agent without a terminal with `--as` and the name of one that ended, and sent it no task: it picks up what waited for that agent, which `dockingbird wait` shows.

```text
{name} started on {repo} ({branch}).
Watch: dockingbird wait {name}
```

Or:

```text
{name} started in a scratch folder.
Watch: dockingbird wait {name}
```

Next step: dockingbird wait {name}

Exit status: 0 (done).

### START_TAKEN_OVER

When: You started an agent with `--as` and the name of one whose last start was killed after its copy was made and before its container ran (a `kill`, a closed terminal), or while its copy was being made. Nothing else was starting it, so Dockingbird closed that start and this one goes on: it picks up where that agent left off.

```text
{name}'s earlier start never ran its container; Dockingbird closed it.
```

Next step: none; it only informs.

Exit status: 0 (done).

### AGENT_CONTINUED

When: You started an agent with `--as` and the name of one that ended: it picks up where that agent left off, and what waited for it is delivered to it. `dockingbird status NAME` says whether its conversation was kept. With `dockingbird claude` or `codex`, the line says the setup it goes on in: as its config's agent at this terminal, or at this terminal reading the messages that wait for it.

```text
{name} picks up where it left off.
```

Or:

```text
{name} picks up where it left off, as a {config_command} agent at this terminal.
```

Or:

```text
{name} picks up where it left off at this terminal;
the messages waiting for it reach it when you type.
```

Next step: none; it only informs.

Exit status: 0 (done).

### NAMES_EXHAUSTED

When: You started an agent without `--as`, and every numbered name of its tool or command has been used in this installation: a number is never given twice. Nothing was started; name the agent yourself with `--as`, or start the numbering again with `dockingbird clean --all`, which removes everything Dockingbird made.

```text
Every {stem}-<n> name is taken in this installation, so none was started.
Name it yourself: dockingbird {subcommand} --as NAME.
Or start the numbering again: dockingbird clean --all
(removes everything Dockingbird made)
```

Next step: dockingbird {subcommand} --as NAME

Exit status: 1 (a problem Dockingbird printed).

### START_COPY_FAILED

When: You started an agent, and Dockingbird couldn't make the agents' copy of your branch for it, so nothing was started. The line says why, in one of these words: `the clone of the agents' copy failed or ran out of time`, `its folder in Dockingbird couldn't be made`, `its kept copy couldn't be resumed`, or `Dockingbird no longer lists this repo for it`; and it gives the command that starts it again, with `--as` and the agent's name when you named the agent, so the same agent starts. With `--verbose` it also names the error's code and reason and, for a clone, whether it ran out of time or how git ended; Dockingbird's log, `dockingbird.log` in its `logs` folder, keeps the same words. `dockingbird status` shows it under "Needs your attention" until a start on that branch gets going.

```text
{name}'s copy of {repo} ({branch}) couldn't be made: {why}.
Try again: dockingbird {subcommand}
```

Or:

```text
{name}'s copy of {repo} ({branch}) couldn't be made: {why}.
Try again: dockingbird {subcommand} --as {agent}
```

Next step, as the message gives it:

- dockingbird {subcommand}
- dockingbird {subcommand} --as {agent}

Exit status: 1 (a problem Dockingbird printed).

### START_AGENT_ENDED

When: Your harness retried a start it had already made, and that agent ran and ended before the retry reached it. Nothing new was started; its results are kept.

```text
{name} started on an earlier try and has already ended.
Its results are kept: dockingbird results {name}
```

Next step: dockingbird results {name}

Exit status: 1 (a problem Dockingbird printed).

### START_RETRY_EXHAUSTED

When: Your harness retried a start several times, and each time Dockingbird's answer was lost and the agent it had begun to start was already gone. Nothing was started; check Docker, then start again.

```text
This start lost Dockingbird's answer {attempts:time|times} in a row.
Check Docker (dockingbird status), then start again.
```

Next step: dockingbird status

Exit status: 1 (a problem Dockingbird printed).

### INBOX_ROW_UNKNOWN

When: You gave a row number no message in your inbox has now, or your inbox is empty. A message keeps the number `dockingbird inbox` or `dockingbird wait` first showed it with while it waits, on any page; the id `dockingbird --json inbox` shows always works.

```text
Row {index} names no message in your inbox now; use the id shown by dockingbird inbox
```

Next step: dockingbird inbox

Exit status: 1 (a problem Dockingbird printed).

### INBOX_ROW_RESOLVED

When: You gave a row number of your inbox instead of an id. The line says which message the row was when the command read it, before it acts on it.

```text
{command} {index} -> {value}
```

Next step: none; it only informs.

Exit status: 0 (done).

### DELIVERY_EXCEEDS_LINE

When: An agent asked to read a message, and not even the shortest page of it fits in one answer of the agent's tools (they are given a most characters an answer may have). Nothing was read, so the message waits as it was. The line names what does not fit, the message's subject or the rest of it, and how long an answer it needs; an agent whose answers may be that long can read it.

```text
Even the shortest page of this message is too long for this agent's answers.
Reading it takes answers of {needed_chars} characters; this agent's are at most {line_chars}.
An agent whose answers may be that long can read it.
```

Or:

```text
This message's subject is too long for this agent's answers.
Reading it takes answers of {needed_chars} characters; this agent's are at most {line_chars}.
An agent whose answers may be that long can read it.
```

Next step: An agent whose answers may be that long can read it.

Exit status: 1 (a problem Dockingbird printed).

### SEND_AMBIGUOUS

When: You sent an agent a plain message while two or more of its questions to you are still unanswered, so Dockingbird can't tell which one it answers. Nothing was sent; say which with `--reply-to` and the question's row in `dockingbird inbox` (an inbox row, not its number in `dockingbird questions`), or answer it by that number with `dockingbird answer`.

```text
{name} asked {count:question|questions} you haven't answered, so this message could answer any of them.
Say which with --reply-to and its inbox row, not its question number;
the inbox rows are from: dockingbird inbox
```

Next step: dockingbird inbox

Exit status: 1 (a problem Dockingbird printed).

### SEND_REPLY_ANOTHER_AGENT

When: You replied with `--reply-to` to a message in your inbox that is another agent's question, not one of the agent you sent to: the words would have answered the other agent. Nothing was sent. Send them to the agent the line names with the same `--reply-to`, or find the question you meant in `dockingbird inbox`.

```text
The message you reply to is {agent}'s question, not {name}'s, so nothing was sent.
To answer it, send to {agent} with the same --reply-to.
{name}'s own questions are in: dockingbird inbox
```

Next step: dockingbird inbox

Exit status: 1 (a problem Dockingbird printed).

### SEND_NOT_ON_BUS

When: You sent a message to an agent that runs in a terminal without the bus's read tool: Dockingbird's default environment, or a config whose tool set lacks it. It could never read the message, and nothing was sent. `dockingbird start` starts an agent on the bus, which can read it. The same line, in its start form, refuses a `dockingbird start` with a task that would run in a terminal (with `--terminal`, or a config whose mode is terminal) without that tool: the agent could never read the task, so nothing was started.

```text
{name} runs in a terminal with no bus tools, so it can't read messages.
Start one on the bus: dockingbird start
```

Or:

```text
{harness} would run in a terminal with no bus tools, so it couldn't
read the task, and nothing was started.
Start it on the bus: dockingbird start
```

Next step: dockingbird start

Exit status: 1 (a problem Dockingbird printed).

### SEND_PAYLOAD_INVALID

When: `dockingbird send --kind KIND --payload JSON` with a payload larger than the bound: nothing was sent; give the kind's fields as one JSON object. The shape form: the payload is not one JSON object, nests deeper than the bound, repeats a key or has a decimal number, and nothing was sent either.

```text
--payload must be one JSON object of at most {count:byte|bytes}.
Try: dockingbird send NAME TEXT --kind status --payload '{"phase":"..."}'
```

Or:

```text
--payload must be one JSON object, at most {depth:level|levels} deep,
with no key twice and no decimal number.
Try: dockingbird send NAME TEXT --kind status --payload '{"phase":"..."}'
```

Next step: dockingbird send NAME TEXT --kind status --payload '{"phase":"..."}'

Exit status: 2 (usage).

### FILE_REPEATED

When: You attached the same file twice with `--file`, or two files with the same name and the same text: Dockingbird keeps such a file once, and a message can't carry it twice. Nothing was sent or started; attach each file once.

```text
{path} is attached twice (the same name and text), so nothing was sent.
Attach each file once, then run this again.
```

Next step: Attach each file once, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### FILE_REFUSED

When: A file you attached with `--file` is missing, a link, not a regular file, too large, not UTF-8 text, or named with characters an attachment's name can't hold. Nothing was sent.

```text
{path} can't be attached, so nothing was sent.
Attach a regular UTF-8 text file of at most {limit} whose name, before its
suffix, is lowercase letters, digits and -.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### RESULTS_FULL

When: Saving an agent's results would take its results folder past its limit, so that file was not saved; `--to` saves into a folder of your own, whatever is already in it. After `dockingbird read`, the file is one the agent attached to that message: make room in the folder and read the message again.

```text
{file} was not saved: the results folder of {name} would pass {limit}.
Save it in a folder of your own: dockingbird results {name} --to DIR
```

Or:

```text
{file} was not saved: the results folder of {name} would pass {limit}.
Make room in it, then read the message again: dockingbird read {delivery_id}
```

Next step, as the message gives it:

- dockingbird results {name} --to DIR
- dockingbird read {delivery_id}

Exit status: 1 (a problem Dockingbird printed).

### RESULTS_TAKEN

When: Saving an agent's results found that file's name already taken in the folder by something else: a link, a folder, a file with other content, or the same name in other letter case. Dockingbird left it as it is and saved nothing there. After `dockingbird read`, the file is one the agent attached to that message: move the other thing away and read the message again.

```text
{file} was not saved: {folder} has something else under that name.
Save it in another folder: dockingbird results {name} --to DIR
```

Or:

```text
{file} was not saved: {folder} has something else under that name.
Move that away, then read the message again: dockingbird read {delivery_id}
```

Next step, as the message gives it:

- dockingbird results {name} --to DIR
- dockingbird read {delivery_id}

Exit status: 1 (a problem Dockingbird printed).

### RESULTS_COPY_OWN

When: You copied an agent's results into a folder of your own with `--to`. Those copies are yours: `dockingbird clean` never removes them.

```text
The copy in {where} is yours, outside dockingbird clean.
```

Next step: none; it only informs.

Exit status: 0 (done).

### RESULTS_TO_INVALID

When: You gave `--to` a folder that doesn't exist, isn't a folder, or is inside Dockingbird's own folder. Nothing was copied.

```text
{path} is not a folder outside {home}.
Give --to a folder that exists, outside Dockingbird's own folder.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### NATIVE_REFUSED

When: Dockingbird refused a message, inbox, artifact or results request, or a start or its task, and the line names its code and reason, and the field it refused when it names one. Check `dockingbird status` and the names, ids and text you gave. The payload forms: `dockingbird send --kind KIND` with a `--payload` (or none) that lacks a key the kind requires, has a key the kind does not take, or has a value the kind refuses; nothing was sent, the line names the field and the keys, and the step is the same send with the kind's example payload. An unexpected error with a system error behind it names that error instead of a reason, for example `EIO`; `ENOSPC` means the agents' disk (Docker's) is full: free some of Docker's disk, or give it more (in Docker Desktop: Settings, Resources), then run it again.

```text
Dockingbird refused it: {code} ({reason}).
See: dockingbird status
```

Or:

```text
Dockingbird refused it: {code}.
See: dockingbird status
```

Or:

```text
Dockingbird refused it: {code} ({errno}).
See: dockingbird status
```

Or:

```text
The agents' disk (Docker's) ran out of room ({errno}).
Free some of Docker's disk, or give it more, then run this again.
```

Or:

```text
Dockingbird refused it: {code} ({reason}) at {field}.
See: dockingbird status
```

Or:

```text
Dockingbird refused it: {code} at {field}.
See: dockingbird status
```

Or:

```text
Dockingbird refused it: {code} ({reason}) at {field}.
Missing: {missing}.
Every kind's keys: dockingbird send -h
Try: dockingbird send NAME TEXT --kind {kind} --payload '{example}'
```

Or:

```text
Dockingbird refused it: {code} ({reason}) at {field}.
The keys there: {allowed}.
Every kind's keys: dockingbird send -h
Try: dockingbird send NAME TEXT --kind {kind} --payload '{example}'
```

Or:

```text
Dockingbird refused it: {code} ({reason}) at {field}.
Every kind's keys: dockingbird send -h
Try: dockingbird send NAME TEXT --kind {kind} --payload '{example}'
```

Next step, as the message gives it:

- dockingbird status
- Free some of Docker's disk, or give it more, then run this again.
- dockingbird send NAME TEXT --kind {kind} --payload '{example}'

Exit status: 1 (a problem Dockingbird printed).

### SEND_TEXT_CONTROL

When: You sent a text with a control character a message can't carry, such as the escape in a terminal's colour codes, or a NUL. Nothing was sent: remove it and send again. A tab, or an invisible mark such as a right-to-left override, is no problem: the message keeps it, and its subject, made from the text's first line, shows a space there.

```text
The text has a control character a message can't carry (an escape, say).
Remove it, then run this again.
```

Next step: Remove it, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### MCP_CONNECTED

When: You ran `dockingbird mcp install` and it connected Dockingbird's tools to Claude Code or Codex with the tool's own `mcp add`, and recorded it; the line shows how to undo it. The by-hand form: `--connected NAME` recorded a connection you made yourself.

```text
Connected Dockingbird's tools to Claude Code: {path}
To undo: claude mcp remove --scope user dockingbird
```

Or:

```text
Connected Dockingbird's tools to Codex: {path}
To undo: codex mcp remove dockingbird
```

Or:

```text
Recorded {name} as connected to Dockingbird's tools by hand.
```

Next step: none; it only informs.

Exit status: 0 (done).

### MCP_ALREADY_CONNECTED

When: You ran `dockingbird mcp install` (or its `--check`) and the tool already has Dockingbird's tools, or you gave `--connected` a name already recorded. Nothing was changed.

```text
Claude Code already has Dockingbird's tools; nothing changed.
```

Or:

```text
Codex already has Dockingbird's tools; nothing changed.
```

Or:

```text
{name} is already recorded as connected; nothing changed.
```

Next step: none; it only informs.

Exit status: 0 (done).

### MCP_CONNECT_FAILED

When: You ran `dockingbird mcp install` and the tool's own `mcp add` failed or didn't answer, so nothing was recorded. What the tool printed is not shown; the message gives the command to run yourself, then the one that records it. With a `DOCKINGBIRD_HOME` that is not the default, that command passes it, on a second line after a `\`, so copy both lines.

```text
Claude Code didn't take Dockingbird's tools: {path}
Connect them yourself, then record it:
  claude mcp add --scope user dockingbird -- dockingbird mcp
  dockingbird mcp install --connected claude
```

Or:

```text
Codex didn't take Dockingbird's tools: {path}
Connect them yourself, then record it:
  codex mcp add dockingbird -- dockingbird mcp
  dockingbird mcp install --connected codex
```

Or:

```text
Claude Code didn't take Dockingbird's tools: {path}
Connect them yourself, then record it:
  claude mcp add --scope user dockingbird \
    --env DOCKINGBIRD_HOME={shell_home} -- dockingbird mcp
  dockingbird mcp install --connected claude
```

Or:

```text
Codex didn't take Dockingbird's tools: {path}
Connect them yourself, then record it:
  codex mcp add dockingbird \
    --env DOCKINGBIRD_HOME={shell_home} -- dockingbird mcp
  dockingbird mcp install --connected codex
```

Next step, as the message gives it:

- claude mcp add --scope user dockingbird -- dockingbird mcp
- codex mcp add dockingbird -- dockingbird mcp
- claude mcp add --scope user dockingbird --env DOCKINGBIRD_HOME={shell_home} -- dockingbird mcp
- codex mcp add dockingbird --env DOCKINGBIRD_HOME={shell_home} -- dockingbird mcp

Exit status: 1 (a problem Dockingbird printed).

### MCP_NOT_FOUND

When: You ran `dockingbird mcp install` and no `claude` or `codex` program it can run is on your `PATH`. The message shows Dockingbird's server definition, `{"command": "dockingbird", "args": ["mcp"]}`, to add to any other tool by hand; with a `DOCKINGBIRD_HOME` that isn't the default, it adds `"env": {"DOCKINGBIRD_HOME": ...}`, so the server reaches that folder.

```text
No claude or codex program on your PATH could be used, so nothing was connected.
For another tool, add Dockingbird's server (stdio) to its MCP settings:
  {definition}
Then record it: dockingbird mcp install --connected NAME
```

Next step: dockingbird mcp install --connected NAME

Exit status: 1 (a problem Dockingbird printed).

### MCP_SHOW

When: You ran `dockingbird mcp install --show`: the server definition, `{"command": "dockingbird", "args": ["mcp"]}` (stdio), to add to a tool's MCP settings yourself; with a `DOCKINGBIRD_HOME` that isn't the default, it adds `"env": {"DOCKINGBIRD_HOME": ...}`. Nothing was connected.

```text
Dockingbird's MCP server (stdio), for any tool's MCP settings:
  {definition}
Once you've added it, record it: dockingbird mcp install --connected NAME
```

Next step: dockingbird mcp install --connected NAME

Exit status: 0 (done).

### HARNESS_PATH_REFUSED

When: `dockingbird mcp install` found a `claude` or `codex` it won't run: in a `PATH` folder that isn't a full path, inside Dockingbird's own folder, or not a regular program file. It looks on through the rest of your `PATH`.

```text
Skipped, as its PATH folder isn't a full path:
  {path}
```

Or:

```text
Skipped, as it is inside Dockingbird's own folder:
  {path}
```

Or:

```text
Skipped, as it isn't a regular program file:
  {path}
```

Next step: none; it only informs.

Exit status: 0 (done).

### MCP_CHECKED

When: You ran `dockingbird mcp install --check`: a connection it recorded is gone from the tool, no `claude` or `codex` program on your `PATH` could be used now, or it was made by hand for another tool, which can't be checked; or nothing is recorded yet.

```text
Claude Code no longer has Dockingbird's tools.
Connect them again: dockingbird mcp install
```

Or:

```text
Codex no longer has Dockingbird's tools.
Connect them again: dockingbird mcp install
```

Or:

```text
No claude program on your PATH could be used, so Claude Code wasn't checked.
```

Or:

```text
No codex program on your PATH could be used, so Codex wasn't checked.
```

Or:

```text
{name} was connected by hand, so Dockingbird can't check it.
```

Or:

```text
No connection is recorded yet. To connect: dockingbird mcp install
```

Next step, as the message gives it:

- dockingbird mcp install
- none, where the message only informs

Exit status: 0 (done).

### STATE_FILE_UNREADABLE

When: `dockingbird mcp install` can't read Dockingbird's `state.json`: it is damaged, too large or not a plain file. Rather than write over it, it recorded nothing: with no `Connected` line before it, no tool was asked; after one (the file changed while that tool connected), that tool stays connected but unrecorded, and no other tool was asked.

```text
Dockingbird can't read its state file:
  {path}
Move it aside, then run this again.
```

Next step: Move it aside, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### INBOX_ROW

When: You ran `dockingbird inbox`: each row is one message waiting for you, in the inbox's order (priority, then age), with the number it got when you first saw it, here or from `dockingbird wait`; it keeps that number while it waits, and the numbers start at 1 again once your inbox is empty. `dockingbird read` takes the number or the id. The operator form: Dockingbird itself sent it.

One row of a table; its cells line up with the rows around it.

```text
  {index}  {name}  {kind}  {priority}  {subject}  {ago} ago
```

Or:

```text
  {index}  Dockingbird  {kind}  {priority}  {subject}  {ago} ago
```

Next step: none; it only informs.

Exit status: 0 (done).

### AGENT_INBOX_ROW

When: You ran `dockingbird inbox NAME` to read what the other agents (and you) sent that agent: one line per message waiting in its inbox, with the `dockingbird read` command that reads it.

One row of a table; its cells line up with the rows around it.

```text
  {name}  {kind}  {priority}  {subject}  {ago} ago  dockingbird read {delivery_id}
```

Or:

```text
  Dockingbird  {kind}  {priority}  {subject}  {ago} ago  dockingbird read {delivery_id}
```

Next step: none; it only informs.

Exit status: 0 (done).

### AGENT_INBOX_EMPTY

When: You ran `dockingbird inbox NAME` and no message is waiting in that agent's inbox.

```text
Nothing is waiting in {name}'s inbox.
```

Next step: none; it only informs.

Exit status: 0 (done).

### AGENT_INBOX_MORE

When: You ran `dockingbird inbox NAME` and that agent's inbox has more messages than one page shows. The page lists them in the order the agent gets them: the most urgent first and, at each priority, the oldest first, so the messages past it are newer or lower in priority. `dockingbird inbox NAME --all` lists them all.

```text
{count} more after these, newer or lower in priority: dockingbird inbox {name} --all
```

Next step: none; it only informs.

Exit status: 0 (done).

### INBOX_EMPTY

When: You ran `dockingbird inbox` and no message is waiting for you. With `--priority` or `--questions`, no waiting message matches them; others may wait, which `dockingbird inbox` lists.

```text
Nothing is waiting in your inbox.
```

Or:

```text
Nothing waiting in your inbox matches {options}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### INBOX_MORE

When: Your inbox has more messages than one page shows. The page lists the most urgent first and, at each priority, the newest first, so the messages past it are older or lower in priority. `dockingbird inbox --all` lists them all, each with its row number; a message keeps its number while it waits, on any page. With `--priority` or `--questions` it counts only the messages that match and names the same options with `--all`.

```text
{count} more, older or lower in priority: dockingbird inbox --all
```

Or:

```text
{count} more, older or lower in priority: dockingbird inbox {options} --all
```

Or:

```text
{count} more, older: dockingbird inbox {options} --all
```

Next step: none; it only informs.

Exit status: 0 (done).

### SEARCH_ROW

When: You ran `dockingbird search TEXT`: one line per message whose subject or body has every word of TEXT, the newest first, in every thread of your agents: who sent it, its kind, its subject and how long ago. With `--json` each line carries the message's id and its thread's.

One row of a table; its cells line up with the rows around it.

```text
  {name}  {kind}  {subject}  {ago} ago
```

Or:

```text
  Dockingbird  {kind}  {subject}  {ago} ago
```

Next step: none; it only informs.

Exit status: 0 (done).

### SEARCH_EMPTY

When: You ran `dockingbird search TEXT`, and no message has every word of TEXT. Try fewer words, or other ones.

```text
No message has those words.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SEARCH_MORE

When: You ran `dockingbird search TEXT`, and more messages have its words than one page shows. Add words to narrow it.

```text
More messages match than one page shows; add words to narrow it.
```

Next step: none; it only informs.

Exit status: 0 (done).

### INBOX_PAGE_MORE

When: You ran `dockingbird inbox --page N` and later pages hold more messages: how many, and the command that shows the next page, with the same `--priority` or `--questions` you gave.

```text
{count} more after this page, older or lower in priority: dockingbird inbox {options}
```

Or:

```text
{count} more after this page, older: dockingbird inbox {options}
```

Next step: none; it only informs.

Exit status: 0 (done).

### INBOX_PAGE_EMPTY

When: You ran `dockingbird inbox --page N` for a page past the last one: nothing is on it, and the message says how many pages your inbox (or the messages that match your `--priority` or `--questions`) fills.

```text
Page {index} of your inbox is empty; it has {count:page|pages}.
```

Or:

```text
Page {index} is empty; what matches {options} fills {count:page|pages}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### INBOX_PAGE_ZERO

When: You ran `dockingbird inbox --page 0`. Pages count from 1, the page `dockingbird inbox` shows; nothing ran.

```text
dockingbird {command}: --page counts from 1.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### INBOX_NAME_OPTION

When: You ran `dockingbird inbox NAME` with an option that only works on your own inbox: `--priority`, `--questions`, `--page` or `--clear`. Nothing ran; an agent's inbox takes only `--all`.

```text
dockingbird {command}: {option} works only on your own inbox; inbox NAME takes only {options}.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### INBOX_SWARM_INVALID

When: You gave `dockingbird inbox` or `dockingbird read` a `--swarm` value with an item that isn't a swarm's name (lowercase letters, digits and `-`, up to 63 characters), or an empty one, as two commas in a row or one at the end make. Nothing ran; `dockingbird swarm list` shows this home's swarms.

```text
dockingbird {command}: --swarm takes swarm names, lowercase letters, digits
and -, up to 63 characters, separated by commas, not '{value}'.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### INBOX_ENGINE_INVALID

When: You gave `dockingbird inbox` or `dockingbird read` an `--engine` value with an item that isn't a workload's id: a UUID in lower case, as `dockingbird swarm list --json` shows it. Nothing ran.

```text
dockingbird {command}: --engine takes workload ids, UUIDs, separated by
commas, not '{value}'.
See: dockingbird {command} -h
```

Next step: dockingbird {command} -h

Exit status: 2 (usage).

### INBOX_ROW_NOT_OWNED

When: You read a message with `--swarm`, `--engine` or `--no-swarm`, and by this home's swarm record its sender is outside them: on a home that others share too, one of their agents sent it. Nothing was read or marked, so it stays in the inbox for its own reader; `dockingbird read ROW --keep` shows it without settling it.

```text
Message {row} is from {name} of swarm {swarm}, not of {options};
it stays in your inbox for its reader.
Look at it without settling it: dockingbird read {row} --keep
```

Or:

```text
Message {row} is from {name}, in no swarm of this home, not of {options};
it stays in your inbox for its reader.
Look at it without settling it: dockingbird read {row} --keep
```

Or:

```text
Message {row} is from Dockingbird, in no swarm, not of {options};
it stays in your inbox.
Look at it without settling it: dockingbird read {row} --keep
```

Next step: dockingbird read {row} --keep

Exit status: 1 (a problem Dockingbird printed).

### INBOX_CLEAR_UNSCOPED

When: You ran `dockingbird inbox --clear` with no `--swarm`, `--engine` or `--no-swarm` on a home whose swarm record has two or more swarms, such as a fleet engine home that others share: one clear would settle everyone's stopped agents' notices at once. Nothing ran; name the swarms whose stopped agents you clear, or all of them, as the line shows.

```text
dockingbird inbox: this home's agents are in {count} swarms ({swarm_names});
--clear needs whose rows to clear: --swarm NAME[,NAME], --engine ID[,ID]
or --no-swarm (agents in no swarm).
All of them: dockingbird inbox --clear --swarm {swarm_names} --no-swarm
```

Next step: dockingbird inbox --clear --swarm {swarm_names} --no-swarm

Exit status: 2 (usage).

### INBOX_ROWS_NOT_KEPT

When: Your inbox has so many open messages that their row numbers would take Dockingbird's `state.json` past the size it reads, so the numbers shown last for this command only. The rows are still listed, the newest first; read one by the id `dockingbird --json inbox` shows, or answer some to bring the count down.

```text
Row numbers for your {count} open messages would take state.json past {limit},
so they last for this command only; ids always work.
```

Next step: none; it only informs.

Exit status: 0 (done).

### INBOX_CLEARED_ROW

When: You ran `dockingbird inbox --clear`: one row for each item it cleared that an agent that has stopped left you, with the agent, the kind, `read` for a notice it marked read or `closed` for a question it closed, and the id that still reads it.

One row of a table; its cells line up with the rows around it.

```text
  {name}  {kind}  read  {value}
```

Or:

```text
  {name}  {kind}  closed  {value}
```

Next step: none; it only informs.

Exit status: 0 (done).

### INBOX_CLEARED

When: You ran `dockingbird inbox --clear` and it cleared what agents that have stopped left you: their notices are marked read and their open questions closed. Nothing is deleted: `dockingbird read ID` still reads each message.

```text
Cleared {count:item|items} that stopped agents left; each message still reads by its id.
```

Next step: none; it only informs.

Exit status: 0 (done).

### INBOX_CLEAR_NOTHING

When: You ran `dockingbird inbox --clear` and no agent that has stopped left a notice or an open question in your inbox, so nothing changed.

```text
Nothing to clear: no stopped agent left a notice or an open question.
```

Next step: none; it only informs.

Exit status: 0 (done).

### INBOX_CLEAR_LEFT

When: You ran `dockingbird inbox --clear` and agents that have stopped left messages that ask you to act: a task, a review request or work handed over. They stay in your inbox; `dockingbird inbox --all` lists them.

```text
Left {count:message|messages} from stopped agents that ask you to act: dockingbird inbox --all
```

Next step: none; it only informs.

Exit status: 0 (done).

### QUESTION_ROW

When: You ran `dockingbird questions`: each row is one question an agent is asking you, with the number it got when you first saw it (kept until it is answered), who asks, what kind of question it is, its text, its options numbered, and how long ago. The typed form: the question takes any text. `dockingbird answer` takes the number or the id.

One row of a table; its cells line up with the rows around it.

```text
  {index}  {name}  {kind}  {subject}  {choices}  {ago} ago
```

Or:

```text
  {index}  {name}  {kind}  {subject}  any text  {ago} ago
```

Next step: none; it only informs.

Exit status: 0 (done).

### QUESTIONS_EMPTY

When: You ran `dockingbird questions` and no agent is waiting for an answer.

```text
No agent is waiting for your answer.
```

Next step: none; it only informs.

Exit status: 0 (done).

### QUESTIONS_MORE

When: More questions are open than one page shows; a question after the page gets its row once earlier ones are answered.

```text
{count} more after these; they get rows once earlier ones are answered.
```

Next step: none; it only informs.

Exit status: 0 (done).

### QUESTION_ROW_UNKNOWN

When: You gave `dockingbird questions` or `dockingbird answer` a row number no open question has: a question keeps its number until it is answered, and the id `dockingbird --json questions` shows always works.

```text
Row {index} is not an open question; the rows are from: dockingbird questions
```

Next step: dockingbird questions

Exit status: 1 (a problem Dockingbird printed).

### QUESTION_HEADER

When: You ran `dockingbird questions ROW`: who asks, what kind of question it is and which tool; its text and options follow. The replied form: you answered it; the on-screen form: it was answered in the tool's own dialog on the agent's screen; the replied-by form names who else did (a rule, a helper agent); the dropped form: it was withdrawn, since its agent moved on or ended.

```text
{name} asks ({kind}, {tool}):
```

Or:

```text
{name} asked ({kind}, {tool}); answered by you:
```

Or:

```text
{name} asked ({kind}, {tool}); answered by {value}:
```

Or:

```text
{name} asked ({kind}, {tool}); answered on its screen:
```

Or:

```text
{name} asked ({kind}, {tool}); withdrawn:
```

Next step: none; it only informs.

Exit status: 0 (done).

### QUESTION_OPTION_ROW

When: One option of the question shown: its number, which `dockingbird answer --option N` takes, its label and, in the described form, what the tool says about it.

One row of a table; its cells line up with the rows around it.

```text
  {index}  {label}
```

Or:

```text
  {index}  {label}  {line}
```

Next step: none; it only informs.

Exit status: 0 (done).

### QUESTION_ANSWER_HINT

When: The last line of a question shown whole: the command that answers it, by an option's number or, in the typed form, in words.

```text
Pick one: dockingbird answer {value} --option N
```

Or:

```text
Answer it: dockingbird answer {value} TEXT
```

Next step, as the message gives it:

- dockingbird answer {value} --option N
- dockingbird answer {value} TEXT

Exit status: 0 (done).

### ANSWERED

When: You ran `dockingbird answer` and the answer was recorded for the agent. The on-screen form: the agent works at a terminal, so its tool shows its own dialog on its screen, where you pick it with the arrow keys and Enter; `dockingbird ui` opens that screen from the agent's row. The sent-on form: a Codex agent on the bus takes your words as its next turn. The at-prompt form: a Codex agent at a terminal takes them typed at its prompt; you type them there, in its screen, which `dockingbird ui` opens from the agent's row.

```text
{name}'s question {value} answered by you: {said}
```

Or:

```text
{name}'s question {value} answered by you: {said}
{name}'s screen shows it: pick it there with the arrows and Enter.
dockingbird ui opens that screen from the agent's row.
```

Or:

```text
{name}'s question {value} answered by you: {said}
Sent to {name} as its next turn.
```

Or:

```text
{name}'s question {value} answered by you: {said}
{name}'s prompt takes it: type it there, then Enter.
dockingbird ui opens that screen from the agent's row.
```

Next step: none; it only informs.

Exit status: 0 (done).

### ANSWER_NEEDS_ONE

When: You ran `dockingbird answer` without an option number or an answer, or with both; give one of them.

```text
answer needs the option's number (--option N) or the answer's text
```

Or:

```text
answer takes --option N or the answer's text, not both
```

Next step: none; it only informs.

Exit status: 2 (usage).

### ANSWER_OPTION_UNKNOWN

When: You picked an option number the question does not have; the line says how many options it has.

```text
Question {value} has {count:option|options}; --option {option} names none of them.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### ANSWERED_NOT_SENT

When: You answered a Codex agent's turn end on the bus; the answer was recorded, but sending it as the agent's next turn failed (the line quotes why; the lost form: the docker call behind the send gave no answer, and `--verbose` shows its detail). Send the words with `dockingbird send NAME TEXT`; a second `dockingbird answer` would be refused, the question being closed.

```text
{name}'s question {value} answered by you: {said}
The words did not reach {name}: {line}
Send them: dockingbird send {name} TEXT
```

Or:

```text
{name}'s question {value} answered by you: {said}
The words did not reach {name}: the send got no answer from Docker ({reason}).
Send them: dockingbird send {name} TEXT
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### ANSWER_ONE_LINE

When: You answered a question of an agent at a terminal with a text that has a line break, a tab or another control character; `dockingbird ui` types the answer into the tool's dialog, where a line break ends it early and a tab moves to another question, so write it on one line. Nothing was answered.

```text
{name}'s screen takes the answer as typed: one line, no tab.
A line break ends the answer early; a tab moves to another question.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### PLAN_OPTION

When: A plan question's two options: `dockingbird answer ROW --option 1` approves the plan, `--option 2` sends it back for more planning, and `dockingbird answer ROW TEXT` sends it back with your words.

```text
approve the plan
```

Or:

```text
keep planning
```

Next step: none; it only informs.

Exit status: 0 (done).

### READ_HEADER

When: You ran `dockingbird read`: the message's kind, sender, priority and subject. Its body follows, every control character escaped, then the files it names. The operator form: Dockingbird itself sent it.

```text
{kind} from {name}, {priority}: {subject}
```

Or:

```text
{kind} from Dockingbird, {priority}: {subject}
```

Next step: none; it only informs.

Exit status: 0 (done).

### READ_BODY_LINE

When: You ran `dockingbird --json read`: each envelope carries a piece of the message's body, in order, so the agent's text never stands outside an envelope.

```text
{line}
```

Next step: none; it only informs.

Exit status: 0 (done).

### BODY_ARTIFACT_ROW

When: The message you read names a file an agent attached: its name, type, size and id. `dockingbird results` saves the files of the agent's task thread.

One row of a table; its cells line up with the rows around it.

```text
  {file}  {media}  {value}
```

Next step: none; it only informs.

Exit status: 0 (done).

### SENT

When: You ran `dockingbird send` and the message went; the line shows its id. The ended form: the agent has stopped, so the message waits until you continue it with the command the line names: the agent's own command for an agent of a config, and `dockingbird start --as NAME` for one of the default environment, whose own terminal can't read messages. The not-running form: the agent's start began but no container of it runs (that start stopped before its container ran), so the message waits until it starts; the command the line names starts it. The still-starting form: another command is starting the agent right now, and the message reaches it once its container runs.

```text
Sent {kind} to {name} (message {value}).
```

Or:

```text
Sent {kind} to {name} (message {value}).
{name} has ended; it gets this when you continue it: dockingbird {subcommand} --as {name}
```

Or:

```text
Sent {kind} to {name} (message {value}).
{name} isn't running yet; it gets this once it starts: dockingbird {subcommand} --as {name}
```

Or:

```text
Sent {kind} to {name} (message {value}).
{name} is still starting; it gets this once its container runs.
```

Next step, as the message gives it:

- none, where the message only informs
- dockingbird {subcommand} --as {name}

Exit status: 0 (done).

### WITHDRAWN

When: You ran `dockingbird send --withdraw`: the message's deliveries that no agent had taken yet are withdrawn. The cancel form: an agent had accepted it, so its work is asked to stop, and the delivery stays accepted until the agent settles it.

```text
Withdrew message {value}.
```

Or:

```text
Withdrew message {value}. An agent had accepted it, so its work is asked to stop.
```

Next step: none; it only informs.

Exit status: 0 (done).

### WAIT_DELIVERY

When: You ran `dockingbird wait` and a message you hadn't seen yet was waiting, or arrived while it waited, wherever it sorts in your inbox. The line gives its row number for `dockingbird read`, and no later wait shows it again. The operator form: Dockingbird itself sent it.

```text
{kind} from {name}: {subject}
Read it: dockingbird read {index}
```

Or:

```text
{kind} from Dockingbird: {subject}
Read it: dockingbird read {index}
```

Next step: dockingbird read {index}

Exit status: 0 (done).

### WAIT_TIMED_OUT

When: You ran `dockingbird wait` and no message you hadn't seen arrived before its time ran out. Run it again to keep waiting. The unread form: messages still wait in your inbox.

```text
Nothing arrived in {elapsed}.
```

Or:

```text
Nothing new in {elapsed}. {count:message waits|messages wait} in your inbox: dockingbird inbox
```

Next step, as the message gives it:

- none, where the message only informs
- dockingbird inbox

Exit status: 0 (done).

### RESULTS_WRITTEN

When: You ran `dockingbird results`: each line is one file it saved from the agent's task thread, with the file's type. After `dockingbird read`, each line is a file the agent attached to that message. The saved-before form: the folder held that file already; the copy form: the copy in your `--to` folder.

```text
{media}
{where}
```

Or:

```text
{media}, saved before
{where}
```

Or:

```text
{media}, your copy
{where}
```

Next step: none; it only informs.

Exit status: 0 (done).

### RESULTS_NONE

When: You ran `dockingbird results` and the agent's task thread has no attached files yet.

```text
{name}'s task thread has no artifacts yet.
```

Next step: none; it only informs.

Exit status: 0 (done).

### RESULTS_NO_THREAD

When: You ran `dockingbird results` for an agent this Mac started without a task, or did not start, so no task thread is recorded for it. Nothing was saved; `dockingbird read` shows the files a message names.

```text
No task thread is recorded for {name}, so nothing was saved.
Artifacts of other threads are reached with dockingbird read
```

Next step: dockingbird read

Exit status: 1 (a problem Dockingbird printed).

### NEEDS_YOU_ROW

When: `dockingbird status` shows each question an agent asked you that is still open, first on the screen: every one `dockingbird questions` lists, of every kind. `dockingbird questions N` shows it whole, by the row number it was first shown with, there or by `dockingbird status`, and `dockingbird answer N` answers it. A question from an agent that ended is marked so.

One row of a table; its cells line up with the rows around it.

```text
  {name} asks  {subject}  dockingbird questions {value}
```

Or:

```text
  {name} asks (ended)  {subject}  dockingbird questions {value}
```

Next step: dockingbird questions {value}

Exit status: 0 (done).

### MANUAL_WAKE_ROW

When: `dockingbird status` shows an agent running in a terminal with messages waiting for it: nothing starts its next turn but your typing, so type anything in its terminal.

One row of a table; its cells line up with the rows around it.

```text
  {name}  {count:delivery|deliveries} waiting  manual wake required: type anything in its terminal
```

Next step: none; it only informs.

Exit status: 0 (done).

### WAITING_ENDED_ROW

When: `dockingbird status` shows an agent that has ended while messages were still waiting for it, after the questions: how many wait, what the first of them is (its kind and subject; after `dockingbird stop` in the middle of a task, that is the task the agent was working on), and the command that continues the agent, which hands it them. Nothing delivers them until you run it. The unnamed form shows when the inbox's row carries no kind or subject text.

One row of a table; its cells line up with the rows around it.

```text
  {name}  {count:delivery|deliveries} waiting for it, and it has ended: {kind}, "{subject}"  pick it up: dockingbird {subcommand} --as {name}
```

Or:

```text
  {name}  {count:delivery|deliveries} waiting for it, and it has ended; the first is {kind}, "{subject}"  pick it up: dockingbird {subcommand} --as {name}
```

Or:

```text
  {name}  {count:delivery|deliveries} waiting for it, and it has ended  pick it up: dockingbird {subcommand} --as {name}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_RESULTS_QUESTION

When: You ran `dockingbird clean` and an ended agent left both a copy and results. The results go with the copy, so the question about the copy covers both; the empty form asks about a copy that has nothing else. `dockingbird clean NAME` asks about an agent's results alone when no copy of it is left.

```text
{name}'s results go with its copy: {path}
```

Or:

```text
{name}'s copy is empty, and its results are in {path}
Remove both? [y/N]
```

Or:

```text
{name}'s results are in {path}
Remove them? [y/N]
```

Next step, as the message gives it:

- none, where the message only informs
- answer y to go on; anything else is no

Exit status: 0 (done).

### CLEAN_ALL_RESULTS

When: You ran `dockingbird clean --all`: its question names the agents whose results it removes. Copies you made with `results --to` are yours and stay.

```text
The results of {names:and} go too: {path}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_ALL_CONFIGS

When: You ran `dockingbird clean --all`: its question names the configs you added with `dockingbird config add`, which it removes. A repo's own `.dockingbird/` folder is never touched.

```text
Your added configs go too: {names:and}
```

Next step: none; it only informs.

Exit status: 0 (done).

### MCP_DISCONNECTED

When: You ran `dockingbird clean --all` and it disconnected a harness `dockingbird mcp install` had connected, with the harness's own remove command.

```text
Disconnected {harness} from Dockingbird.
```

Next step: none; it only informs.

Exit status: 0 (done).

### MCP_CONNECTED_BY_HAND

When: You ran `dockingbird clean --all` with a harness you had connected yourself (`dockingbird mcp install --connected`). Dockingbird changed none of that harness's settings, so it leaves them; the line names the remove command if you want it gone.

```text
You connected {harness} yourself; Dockingbird changed none of its settings.
Remove it yourself if you want:
{undo}
```

Next step: none; it only informs.

Exit status: 0 (done).

### MCP_DISCONNECT_FAILED

When: You ran `dockingbird clean --all` and a harness's remove command failed, or the program is gone. Run the command the line shows yourself.

```text
{harness} could not be disconnected from Dockingbird. Run this yourself:
{undo}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

## Every Dockingbird home on this computer

### HOMES_ROW

When: You ran `dockingbird homes`: each line is a Dockingbird home on this computer (each `DOCKINGBIRD_HOME`, the default one included), its folder, whether its Dockingbird runs, and its version. A home "not readable from here" would be started or updated by a command there; a home whose folder is gone, or whose logs folder is not its own, has no folder to show.

```text
{home} ({profile}): Dockingbird {coordinator}, version {version}
```

Or:

```text
{home} ({profile}): Dockingbird {coordinator}, version {version}, this home
```

Or:

```text
{home} ({profile}): Dockingbird {coordinator}, version {version}, not readable from here
```

Or:

```text
{profile}: its home is gone, or its logs folder is not its own
```

Next step: none; it only informs.

Exit status: 0 (done).

## Swarm inspection

### INSPECT_CAPABILITIES

When: You ran `dockingbird inspect capabilities`, the first read the Dockingbird GUI's Swarms tab makes: the line says what this Dockingbird can show there. With `--json` the GUI reads the same facts.

```text
Inspection is supported: homes, agents, who may message whom, and settings.
```

Next step: none; it only informs.

Exit status: 0 (done).

### INSPECT_INSTANCES

When: You ran `dockingbird inspect instances`: one entry per Dockingbird home on this computer, as `dockingbird homes` lists them, each with whether its Dockingbird runs (`running`), is stopped, runs another version than this one (`unreadable`) or has lost its folder (`gone`), and how many of its agents run.

```text
{instances:Dockingbird home|Dockingbird homes} on this computer.
```

Next step: none; it only informs.

Exit status: 0 (done).

### INSPECT_SWARM

When: You ran `dockingbird inspect swarm`: this home's agents and, for every pair of them, whether one may message the other, decided as a real send is decided; nothing is sent. The line counts the agents and the swarms they were started into; with `--swarm NAME`, only that swarm's agents and the pairs among them. With Dockingbird not set up or off, the line `status` prints for that state comes instead.

```text
{agents:agent|agents} in {swarms:swarm|swarms} of this home, {decisions:decision|decisions} on who may message whom.
```

Or:

```text
{agents:agent|agents} of {swarm}, {decisions:decision|decisions} on who may message whom.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SWARM_UNKNOWN

When: You ran `dockingbird inspect swarm --swarm NAME` and no agent of this home is in a swarm of that name: none was started with `--swarm NAME`, or each has left it. Nothing of the home is shown.

```text
No swarm named {swarm} in this home.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### SWARM_NAME_INVALID

When: You gave `--swarm` a name no swarm can have. A swarm's name follows the rule of an agent's name: lowercase letters, digits and `-`, a letter or a digit first.

```text
{swarm} can't be a swarm's name; use lowercase letters, digits and -.
```

Next step: none; it only informs.

Exit status: 2 (usage).

### INSPECT_CONFIG

When: You ran `dockingbird inspect config`: alone, this home's own settings; with `--agent NAME`, the settings that agent runs with, its model and effort, its limits, its tool versions and the names of its environment variables. An environment value that is not a tool's is never shown. A name of no agent is refused as `status NAME` refuses it.

```text
Settings of {name}: {variables:environment variable|environment variables}.
```

Or:

```text
Settings of this home.
```

Next step: none; it only informs.

Exit status: 0 (done).

### INSPECT_SECRET_REFUSED

When: You ran `dockingbird inspect config --agent NAME` and the agent's settings hold a secret, so Dockingbird shows none of them rather than part. Take the secret out of the agent's config, or leave those settings unread.

```text
{name}'s settings hold a secret, so none of them are shown.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

## The swarm command

### SWARM_ROW

When: You ran `dockingbird swarm list`: one line per swarm of this home, with how many agents are in it and whether you made it (`hand`) or the fleet runs it (`engine`). With `--json`, each member's role and the members that review and test its work come too.

```text
{swarm}: {agents:agent|agents} ({source})
```

Next step: none; it only informs.

Exit status: 0 (done).

### SWARM_NONE

When: You ran `dockingbird swarm list` and no agent of this home is in a swarm: none was started with `--swarm`, or each one left its swarm. `dockingbird start --swarm NAME` starts an agent in one, and `dockingbird swarm add` puts an agent there.

```text
No swarm in this home: dockingbird start --swarm NAME labels one.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SWARM_ADDED

When: You ran `dockingbird swarm add NAME --swarm SWARM`: the agent is now in that swarm, with the role you gave, and out of any swarm it was in before. Only this home's record changed: the agent wasn't started, stopped or told.

```text
{name} joined {swarm} as {role}.
```

Or:

```text
{name} joined {swarm}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SWARM_REMOVED

When: You ran `dockingbird swarm remove NAME`: the agent is in no swarm now, and no member is reviewed or tested by it any more. The agent itself keeps running; `dockingbird stop NAME` stops it.

```text
{name} left {swarm}; it keeps running: dockingbird stop {name} stops it.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SWARM_ROLE_SET

When: You ran `dockingbird swarm role NAME --role ROLE`: the agent's role in its swarm is the one you gave. Only this home's record changed.

```text
{name} is now {role} in {swarm}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SWARM_ASSIGNED

When: You ran `dockingbird swarm assign NAME`: the line names the members that review and test the agent's work now, `none` where none does. Only this home's record changed: no agent was told.

```text
{name} in {swarm}: reviewer {reviewer}, tester {tester}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SWARM_NOT_A_MEMBER

When: You ran `dockingbird swarm remove`, `role` or `assign` for an agent that is in no swarm, so there was nothing to change. Put it in one first with `dockingbird swarm add NAME --swarm SWARM`.

```text
{name} is in no swarm. Put it in one: dockingbird swarm add {name} --swarm NAME
```

Next step: dockingbird swarm add {name} --swarm NAME

Exit status: 1 (a problem Dockingbird printed).

### SWARM_ENGINE_OWNED

When: You tried to change a swarm the fleet runs with `dockingbird swarm`. The fleet keeps its own list of who is in it and tells its agents of every change, so change it with the `dockingbird fleet` command the line names. An agent's role there is the one the fleet started it for: retire it and add one of the other role.

```text
The fleet runs {swarm}, so {name} changes there: dockingbird fleet retire|replace|assign {id} {name}
```

Or:

```text
The fleet runs {swarm}, and {name}'s role there is its package's: dockingbird fleet retire {id} {name}, then fleet add {id} ROLE
```

Next step, as the message gives it:

- dockingbird fleet retire\|replace\|assign {id} {name}
- dockingbird fleet retire {id} {name}, then fleet add {id} ROLE

Exit status: 1 (a problem Dockingbird printed).

### SWARM_ASSIGNEE_IS_SELF

When: You ran `dockingbird swarm assign NAME` and named the agent itself as its own reviewer or tester. Name another member of its swarm.

```text
In {swarm}, {name} can't review or test its own work.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### SWARM_ASSIGNEE_NOT_A_MEMBER

When: You ran `dockingbird swarm assign NAME` and named a reviewer or tester that is not in the agent's swarm. Put that agent in the swarm first with `dockingbird swarm add`, or name a member.

```text
{name} is not in {swarm}: an agent's reviewer and tester are members of its swarm.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### SWARM_NEEDS_SWARM

When: You ran `dockingbird swarm add NAME` without `--swarm SWARM`, the swarm to put the agent in. Nothing changed.

```text
dockingbird swarm add needs --swarm SWARM, the swarm to put it in.
See: dockingbird swarm -h
```

Next step: dockingbird swarm -h

Exit status: 2 (usage).

### SWARM_NEEDS_ROLE

When: You ran `dockingbird swarm role NAME` without `--role ROLE`, the agent's new role. Nothing changed.

```text
dockingbird swarm role needs --role ROLE, the agent's new role.
See: dockingbird swarm -h
```

Next step: dockingbird swarm -h

Exit status: 2 (usage).

### SWARM_ROLE_INVALID

When: You gave `--role` a word that can't be a role: a role is lowercase letters, digits and `-`, as an agent's name is. Nothing changed.

```text
dockingbird swarm: '{role}' can't be a role; use lowercase letters, digits and -.
See: dockingbird swarm -h
```

Next step: dockingbird swarm -h

Exit status: 2 (usage).

### SWARM_ASSIGN_NEEDS_OPTION

When: You ran `dockingbird swarm assign NAME` with none of `--reviewer`, `--tester`, `--no-reviewer` and `--no-tester`, so there was nothing to change.

```text
dockingbird swarm assign needs --reviewer, --tester or their --no- forms.
See: dockingbird swarm -h
```

Next step: dockingbird swarm -h

Exit status: 2 (usage).

### SWARM_ASSIGN_CONFLICT

When: You gave `dockingbird swarm assign` a reviewer and `--no-reviewer`, or a tester and `--no-tester`, at once. Give one of the two.

```text
dockingbird swarm assign: use either {option} NAME or {other}, not both.
See: dockingbird swarm -h
```

Next step: dockingbird swarm -h

Exit status: 2 (usage).

### SWARM_ASSIGNEE_INVALID

When: You gave `--reviewer` or `--tester` a word that can't be an agent's name: a name is lowercase letters, digits and `-`. Nothing changed.

```text
dockingbird swarm: '{name}' can't be a name; use lowercase letters, digits and -.
See: dockingbird swarm -h
```

Next step: dockingbird swarm -h

Exit status: 2 (usage).

### SWARM_ENGINE_INVALID

When: `dockingbird swarm` was given an `--engine` value that is not the id of a fleet workload. The fleet's own worker gives that option; you never need to type it.

```text
dockingbird swarm: --engine takes the id of a fleet workload.
```

Next step: none; it only informs.

Exit status: 2 (usage).

## The Dockingbird GUI

### UI_NOT_A_TERMINAL

When: You ran `dockingbird ui` where it has no terminal to draw on: in a pipe, from a script, or with `--json`. The Dockingbird GUI it opens draws on the terminal and reads your keys and mouse there, so it needs a Terminal window. Run it there.

```text
dockingbird ui needs a terminal: run it in Terminal, not in a pipe or a script.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### UI_STOP_WITH_INSTALL

When: You ran `dockingbird ui stop` with `--install`. One stops the GUI's server, the other installs the GUI: run them one at a time.

```text
dockingbird ui: stop and --install don't go together; give one.
See: dockingbird ui -h
```

Next step: dockingbird ui -h

Exit status: 2 (usage).

### GUI_MISSING

When: You ran `dockingbird ui`, and the Dockingbird GUI it opens isn't on this computer: there's no `dockingbird-gui` in the `bin` folder in Dockingbird's folder, where `dockingbird ui --install` puts it, nor in a folder of your `PATH`. Install it with `dockingbird ui --install`. When the line names a file instead, you set the variable that picks the GUI's file, and nothing is at its path: fix the path, or unset the variable to use the installed GUI.

```text
The Dockingbird GUI isn't installed.
Install it: dockingbird ui --install
```

Or:

```text
There's no Dockingbird GUI at {path}, which DOCKINGBIRD_GUI names.
Unset it to use the installed one: unset DOCKINGBIRD_GUI
```

Next step, as the message gives it:

- dockingbird ui --install
- unset DOCKINGBIRD_GUI

Exit status: 1 (a problem Dockingbird printed).

### GUI_SESSION_EMPTY

When: You ran `dockingbird ui` or `dockingbird ui stop` with the variable that names where the GUI runs set, but empty. That variable is for development and tests: it names another place for the GUI than the one every home shares. Unset it, or give it a name.

```text
DOCKINGBIRD_GUI_SESSION is set but empty, so it names nothing to run the GUI in.
Unset it to use the GUI's own: unset DOCKINGBIRD_GUI_SESSION
```

Next step: unset DOCKINGBIRD_GUI_SESSION

Exit status: 1 (a problem Dockingbird printed).

### GUI_PREVIOUS_OPENED

When: You ran `dockingbird ui`, and two GUIs run on this computer: the one you had before Dockingbird 0.4.4, and the one 0.4.4 started beside it under a name of its own. `dockingbird ui` opens the one from before, with its tabs, from every folder. The other keeps running, with whatever runs in its tabs, until you end it with the line's last command; the line's third command opens it. When the line says it could not be checked, run `dockingbird --verbose ui` to see why.

```text
The GUI opens as you had it before Dockingbird 0.4.4, with its tabs.
The GUI 0.4.4 started still runs beside it, with what runs in its tabs.
To open that one: env DOCKINGBIRD_GUI_SESSION=dockingbird dockingbird ui
To end it: env DOCKINGBIRD_GUI_SESSION=dockingbird dockingbird ui stop
```

Or:

```text
The GUI opens as you had it before Dockingbird 0.4.4, with its tabs.
The GUI 0.4.4 started may still run beside it: that could not be checked.
To open that one: env DOCKINGBIRD_GUI_SESSION=dockingbird dockingbird ui
To end it: env DOCKINGBIRD_GUI_SESSION=dockingbird dockingbird ui stop
```

Next step: none; it only informs.

Exit status: 0 (done).

### GUI_NOT_EXECUTABLE

When: You ran `dockingbird ui`, and the file it found for the Dockingbird GUI can't be run: it isn't a program file you may run, or it didn't start, as a program built for another kind of computer doesn't. `dockingbird ui --install` puts a good copy in its place; run the command with `--verbose` to see why.

```text
The Dockingbird GUI at {path} can't be run.
Install it again: dockingbird ui --install
```

Next step: dockingbird ui --install

Exit status: 1 (a problem Dockingbird printed).

### GUI_WRONG_VERSION

When: You ran `dockingbird ui`, and the Dockingbird GUI it found is another version than the one this Dockingbird works with, or didn't say its version when asked. The line names both versions and the file; `dockingbird ui --install` installs the version it needs.

```text
The Dockingbird GUI at {path} is {version}, and this Dockingbird needs {wanted}.
Install that one: dockingbird ui --install
```

Or:

```text
The program at {path} didn't give its Dockingbird GUI version,
and this Dockingbird needs {wanted}.
Install that one: dockingbird ui --install
```

Next step: dockingbird ui --install

Exit status: 1 (a problem Dockingbird printed).

### GUI_INSTALLING

When: You ran `dockingbird ui --install`, or `dockingbird update` found no dockingbird-gui installed, or one at another version than the one this Dockingbird expects. Dockingbird is getting that version from the zeus-fyi/dockingbird-gui repository with your own git and SSH key. With none installed, `dockingbird update` gets it only once Dockingbird is set up, and never on a computer this Dockingbird pins no dockingbird-gui build for.

```text
Getting dockingbird-gui {version} from zeus-fyi/dockingbird-gui ...
```

Next step: none; it only informs.

Exit status: 0 (done).

### GUI_INSTALLED

When: The dockingbird-gui Dockingbird got matched the checksum it expects, and it is now installed in the `bin` folder of your Dockingbird home, in place of the one before, with a link to it beside `dockingbird` on your `PATH`, so `dockingbird-gui` is a command too (run bare, it opens its own default view, not this home's: use `dockingbird ui`). `dockingbird ui` opens it. The form without the `PATH` line made no link; the one-line form comes from `dockingbird update`, which made the link again.

```text
Installed dockingbird-gui {version}:
  {path}
  On your PATH: {link}
Open it: dockingbird ui
```

Or:

```text
Installed dockingbird-gui {version}:
  {path}
Open it: dockingbird ui
```

Or:

```text
dockingbird-gui {version} is on your PATH now:
  {link}
```

Next step, as the message gives it:

- dockingbird ui
- none, where the message only informs

Exit status: 0 (done).

### GUI_LINK_IN_THE_WAY

When: You ran `dockingbird ui --install`, and where Dockingbird links dockingbird-gui beside `dockingbird` there is already a file that isn't its link, such as a build of your own. Dockingbird left it as it is, so the dockingbird-gui your `PATH` finds may not be the one it installed; `dockingbird ui` runs the installed one. Remove the file and run the install again to get the link.

```text
Dockingbird left this as it is, since it didn't make it:
  {link}
The dockingbird-gui your PATH finds may not be the one installed;
dockingbird ui runs the installed one.
```

Next step: none; it only informs.

Exit status: 0 (done).

### GUI_LINK_REFUSED

When: You ran `dockingbird ui --install` or `dockingbird update`, and the folder `dockingbird` is in refused the link to dockingbird-gui. The GUI is installed all the same and `dockingbird ui` runs it; run the command with `--verbose` to see why.

```text
Dockingbird couldn't put dockingbird-gui on your PATH here:
  {link}
dockingbird ui runs it all the same.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CLEAN_GUI_LINK_LEFT

When: You ran `dockingbird clean --all`, and where `dockingbird ui --install` puts the link to dockingbird-gui, beside `dockingbird` on your `PATH`, there is a file or a link to something else, such as a build of your own. Dockingbird left it as it is; delete it yourself if you don't want it. The other form says the link is Dockingbird's own but its folder refused to remove it; run the command with `--verbose` to see why, and delete the link yourself.

```text
Kept {link}: it isn't the link to the GUI this Dockingbird installed.
```

Or:

```text
Dockingbird couldn't remove its link to the GUI, so it stays:
  {link}
```

Next step: none; it only informs.

Exit status: 0 (done).

### GUI_CHECKSUM_MISMATCH

When: The dockingbird-gui file Dockingbird got doesn't have the SHA-256 checksum this Dockingbird expects for that version: the release was replaced by another build, or the file is damaged. Nothing was installed, and the dockingbird-gui you had stays. The line shows both checksums, to compare with the release's `SHA256SUMS`.

```text
The dockingbird-gui {version} download isn't the build this Dockingbird pins:
  {pinned}  pinned
  {downloaded}  downloaded
Nothing was installed, and the dockingbird-gui you had stays.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### GUI_PLATFORM_UNSUPPORTED

When: You ran `dockingbird ui --install` on a computer dockingbird-gui has no build for: it is built for Macs with Apple silicon and for Linux on arm64. The line names this computer's system and processor. Its other form says this Dockingbird has no checksum for that version's build of this computer yet, so it installs nothing it can't check.

```text
dockingbird-gui has no build for {platform}.
It runs on Apple silicon Macs and arm64 Linux.
```

Or:

```text
Dockingbird pins dockingbird-gui {version}.
Its {platform} build has no checksum yet.
Dockingbird installs nothing it can't check.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### GUI_FETCH_FAILED

When: Getting dockingbird-gui failed, so nothing was installed and the one you had stays. Usually git couldn't read the private zeus-fyi/dockingbird-gui repository over SSH (the line shows git's own words, such as a refused key), or that version has no release there. Other forms say git isn't on your `PATH` or couldn't start, that no answer came in time, or that the answer was larger than Dockingbird reads.

```text
Dockingbird couldn't get dockingbird-gui {version}.
git said:
  {said}
Check that your git can read this repository:
  git@github.com:zeus-fyi/dockingbird-gui.git
Then run dockingbird ui --install again.
```

Or:

```text
Dockingbird couldn't get dockingbird-gui {version}.
It needs git, and git isn't on your PATH or doesn't start.
Install git, then run dockingbird ui --install again.
```

Or:

```text
Dockingbird couldn't get dockingbird-gui {version}.
No answer came within {elapsed} from:
  git@github.com:zeus-fyi/dockingbird-gui.git
Check the network, then run dockingbird ui --install again.
```

Or:

```text
Dockingbird couldn't get dockingbird-gui {version}.
git's answer was over {limit}.
That is more than Dockingbird reads.
Nothing was installed.
```

Next step, as the message gives it:

- dockingbird ui --install
- none, where the message only informs

Exit status: 1 (a problem Dockingbird printed).

### COMPLETION_INSTALLED

When: You ran `dockingbird completion --install`: Dockingbird wrote the completion script for your shell into its own folder and added the line that loads it to your shell's startup file (`~/.zshrc`, `~/.bashrc`, or fish's `~/.config/fish/conf.d/dockingbird.fish`). Open a new terminal to use it. The one-line form comes from `dockingbird update`, which rewrote an installed script for the version it installed.

```text
Installed tab completion for {shell}:
  {path}
  {rc} sources it
Open a new terminal.
```

Or:

```text
Updated tab completion for {shell}:
  {path}
```

Next step: none; it only informs.

Exit status: 0 (done).

### COMPLETION_ALREADY

When: You ran `dockingbird completion --install` again: your startup file already loads the script, so nothing was added to it, and the script was written again for this version.

```text
Tab completion for {shell} was installed already; its script is current:
  {path}
  {rc} sources it
```

Next step: none; it only informs.

Exit status: 0 (done).

### COMPLETION_SHELL_UNKNOWN

When: You ran `dockingbird completion --install` without naming a shell, and the `SHELL` variable names a shell Dockingbird has no completion for, or isn't set. Name `zsh`, `bash` or `fish` after `--install`. Nothing was written.

```text
dockingbird completion --install can't tell which shell to complete:
SHELL is {shell}, and Dockingbird completes zsh, bash and fish.
Name one: dockingbird completion --install zsh
```

Or:

```text
dockingbird completion --install can't tell which shell to complete:
SHELL isn't set.
Name one: dockingbird completion --install zsh
```

Next step: dockingbird completion --install zsh

Exit status: 2 (usage).

### COMPLETION_RC_REFUSED

When: You ran `dockingbird completion --install`, and Dockingbird couldn't read or write your shell's startup file: the system refused it, it isn't a regular file, or it is very large; run the command with `--verbose` to see why. The script was written and the startup file is unchanged. The other form says `HOME` isn't set, so there is no startup file to name.

```text
Dockingbird couldn't add the line that loads tab completion to {rc}.
Make the file writable, then run dockingbird completion --install again.
```

Or:

```text
Dockingbird couldn't find your startup file: HOME isn't set.
Set it, then run dockingbird completion --install again.
```

Next step, as the message gives it:

- Make the file writable, then run dockingbird completion --install again.
- Set it, then run dockingbird completion --install again.

Exit status: 1 (a problem Dockingbird printed).

## Host resource connections

### CONNECTION_LIST_FOLDER

When: Under a connection in `dockingbird connections`: a folder of this Mac its agents read, by its path. They can read it and never write there.

```text
  Read-only: {path}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECTION_LIST_DATABASE

When: Under a connection in `dockingbird connections`: a database its agents query, by its server, port and name, with the role the queries run as. They read rows and never write.

```text
  Query {target} as {value}, read-only
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECTION_LIST_SERVICE

When: Under a connection in `dockingbird connections`: a service, a program of this Mac you declared, by its path, and the first digits of the commit its checkout must be at when you pinned one.

```text
  Run {path}
```

Or:

```text
  Run at commit {value}: {path}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECTION_LIST_BROWSER

When: Under a connection, `dockingbird connections` shows a browser of this Mac that its agents control: its word, and that it runs in your own profile or a temporary one, as the agent's request picks.

```text
  Control {target} on this Mac, in your own profile or a temporary one
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECTION_LIST_VAULT

When: Under a connection in `dockingbird connections`: a gopass vault, with how many logins it has and their names. No site, username, password or code is shown.

```text
  {name}: gopass vault, {count:login|logins}: {aliases}
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECTION_LIST_REQUEST

When: In `dockingbird connections NAME`, after its agents: the connection's newest requests, newest first, each with the agent that asked, what it asked (a fetch, a push, a query or a run), whether it waits, runs, is done, was cancelled, failed (with why, in the words `dockingbird status NAME` uses), found nothing new to push, or ended with an unknown result, and how long ago. `Older requests aren't shown.` ends a list that has more.

```text
  {other}: {value} {kind} ({ago} ago)
```

Or:

```text
  {other}: {value} failed: {detail} ({ago} ago)
```

Or:

```text
  {other}: {value}: nothing new to push; {detail} ({ago} ago)
```

Or:

```text
  Older requests aren't shown.
```

Next step: none; it only informs.

Exit status: 0 (done).

### STATUS_SERVICE_WAITING

When: Under "Needs your attention" in `status`: an agent asked a service to run, and the request waits until you start its runner with `dockingbird serve` and the connection's name.

```text
{name}'s request to {connection} waits for its runner.
Start it: dockingbird serve {connection}
```

Or:

```text
A request to {connection} waits for its runner.
Start it: dockingbird serve {connection}
```

Next step: dockingbird serve {connection}

Exit status: 0 (done).

### CONNECT_DATABASE_DONE

When: `dockingbird connect NAME --database URL` connected a database: Dockingbird opened it as the role from its own side, found that the role can't write and that the server allows no prepared transactions, and kept the connection. The agents of a config whose `connections` list names it run one read-only SQL statement at a time through Dockingbird and read the rows from a file; none sees the database or its password. The line names the database as server, port and name, and the role.

```text
Connected {name}: {target} as {value}, read-only, checked from Dockingbird.
Agents of a config that names it query it through Dockingbird;
none sees the database.
A config that names it: connections = ["{name}"]
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECT_DATABASE_INVALID

When: The URL after `--database` isn't one Dockingbird takes. It is `postgres://ROLE@HOST:PORT/DATABASE`: the server's host name in lowercase, a port (PostgreSQL's own when you leave it out), the database name, and no password, query or fragment. A password in the URL is never shown again: leave it out and add `--password`, and Dockingbird asks for it, hidden. The role and the database must be plain PostgreSQL names. Nothing was saved.

```text
Use --database with a URL of the form postgres://ROLE@HOST:PORT/DATABASE:
the role, the server's host name, its port (PostgreSQL's own when left out) and
the database name, with no password, query or fragment.
```

Or:

```text
Don't put the password in the URL: your shell's history would keep it.
Leave it out and add --password; Dockingbird asks for it, hidden.
dockingbird connect NAME --database URL --password
```

Or:

```text
The role and the database name must be plain PostgreSQL names.
Use lowercase letters, digits and _, not starting with a digit,
at most {count} characters.
```

Next step, as the message gives it:

- none, where the message only informs
- dockingbird connect NAME --database URL --password

Exit status: 2 (usage).

### CONNECT_DATABASE_REFUSED

When: `dockingbird connect --database` checked the database from Dockingbird's own side and refused it; the connection was removed again and nothing is kept. One line shows the cause. The role can write: itself, or through a role it can switch to (a superuser, a role that can create roles or databases, replicate or bypass row security, a role that can write, one that reads or writes the server's files, runs its programs, ends other connections or runs maintenance, or a member of any of them), or it owns a table or the database, or has the MAINTAIN right on a table, or it may call the function that writes a message into the server's log of changes; the message shows the commands that make a read-only role that is a member of none of those, owns no table, has no MAINTAIN right and is not the database's owner. On PostgreSQL 16 and earlier that function has no fourth parameter, so name its two forms without it in the REVOKE line. Or Dockingbird couldn't reach the server: is it listening for connections from Docker, and does its list of allowed hosts let them in? The same line shows when the server took longer than a query's time limit to answer the check, as a busy server may: run the command again once it answers. Or the server asks for a password none was given for. Or it refused the role, its password or the database name, which PostgreSQL doesn't tell apart. Or it allows prepared transactions, which a query could leave behind: set their maximum to 0 in its configuration and restart it.

```text
The role {value} can write to {target}, so Dockingbird won't give it to agents.
Make a read-only role: CREATE ROLE reader LOGIN;
GRANT CONNECT ON DATABASE {name} TO reader;
GRANT USAGE ON SCHEMA public TO reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;
REVOKE EXECUTE ON FUNCTION
  pg_catalog.pg_logical_emit_message(
    boolean, text, text, boolean),
  pg_catalog.pg_logical_emit_message(
    boolean, text, bytea, boolean)
FROM PUBLIC;
Then run this again with reader.
```

Or:

```text
Dockingbird couldn't reach {target} from its container.
Is the server listening for connections from Docker (listen_addresses,
pg_hba.conf)? Then run this again.
```

Or:

```text
{target} asks for a password for {value}.
Run this again with --password.
```

Or:

```text
{target} refused the role, its password or the database name.
Check the three, then run this again with --password.
```

Or:

```text
{target} allows prepared transactions, which a query could
leave behind, so Dockingbird won't use it.
Set max_prepared_transactions = 0 in postgresql.conf, restart the server,
then run this again.
```

Next step, as the message gives it:

- Then run this again with reader.
- Then run this again.
- Run this again with --password.
- Check the three, then run this again with --password.
- Set max_prepared_transactions = 0 in postgresql.conf, restart the server, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### CONNECT_DATABASE_PASSWORD

When: You ran `dockingbird connect --database` with `--password` at a terminal: Dockingbird asks for the role's password there, and it isn't shown as you type. Without a terminal it reads the password from what you pipe in.

```text
Password for {value} (hidden):
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECT_DATABASE_PASSWORD_SHORT

When: The password you gave `--password` is empty (Enter or Ctrl-D at the hidden question, or nothing piped in), or isn't text Dockingbird can send (not valid text, with a NUL character, or too long). Nothing was saved; run the command again and give the role's password, or give the role another one.

```text
A database password cannot be empty.
Run this again with --password and give the role's password.
```

Or:

```text
Dockingbird can't send that password: it must be text of at most {limit},
with no NUL character.
Give the role another one, then run this again with --password.
```

Next step, as the message gives it:

- Run this again with --password and give the role's password.
- Give the role another one, then run this again with --password.

Exit status: 2 (usage).

### CONNECT_FOLDER_DONE

When: You ran `dockingbird connect NAME --folder PATH`. The folder is connected: from their next start, the agents of a config that names it read it at `/dockingbird/folders/NAME`, read-only, and can't write, rename or delete there, unless the config gives them write access: a `[folders]` table with `NAME = "write"` mounts it read-write. Reads there aren't logged; the grant to each agent is. Nothing to do.

```text
Connected {name}: agents of a config that names it read it, read-only unless
the config gives them write access, at /dockingbird/folders/{name}.
On this Mac it is {path}.
Reads there aren't logged; the grant is.
A config that names it: connections = ["{name}"]
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECT_FOLDER_INVALID

When: You ran `dockingbird connect NAME --folder PATH` with a path Dockingbird can't connect: it isn't a folder or isn't there; it is a link (connect the folder it points at); it is the whole disk; it is Dockingbird's own folder or inside it; its path has a character a mount can't take (a comma, a quote, a backslash or an equals sign: rename the folder); its path is longer than a connected folder's may be; or you can't open it for reading (no read permission on it for you, or a privacy-protected folder such as Desktop or Documents when the terminal has no Full Disk Access), so Dockingbird can't check its real name. Nothing was connected. Give the folder's own path, or read access to it, and run the command again.

```text
{path} isn't a folder.
```

Or:

```text
{path} is a link; connect the folder it points at.
```

Or:

```text
Connect a folder, not the whole disk.
```

Or:

```text
{path} is Dockingbird's own folder; connect another.
```

Or:

```text
{path} has a character Docker can't take in a mount path:
a comma, a quote, a backslash or an equals sign.
Rename it, then run this again.
```

Or:

```text
{path} is longer than {count} characters, the most a connected
folder's path may have.
```

Or:

```text
{path} can't be opened for reading by this user,
so its real name can't be checked.
Give this user read access to it (or Full Disk Access
to the terminal), then run this again.
```

Next step, as the message gives it:

- none, where the message only informs
- Rename it, then run this again.
- Give this user read access to it (or Full Disk Access to the terminal), then run this again.

Exit status: 2 (usage).

### START_FOLDER_MISSING

When: You started an agent of a config that names a folder connection, and the folder isn't where it was when you connected it: it was moved, renamed (a change of its case counts), deleted, or replaced by a file or a link; or you can't open it for reading any more. Nothing was started. Connect the folder again with `dockingbird connect NAME --folder PATH`, or take the connection away with `dockingbird disconnect NAME`.

```text
{name} names the folder {path}, which isn't there any more, or isn't a folder.
Connect it again, or disconnect it: dockingbird disconnect {name}
```

Next step: dockingbird disconnect {name}

Exit status: 1 (a problem Dockingbird printed).

### START_FOLDER_NOT_A_FOLDER

When: You started an agent of a config whose `[folders]` table names a connection that has no folder (a GitHub repository, a database, a service or a browser), so its entry can't set any folder's access. Nothing was started. Remove the connection from `[folders]` in the config (it stays in `connections`), then run the command again.

```text
{name} isn't a folder connection, so [folders] can't set its access.
Remove {name} from [folders] in the config.
```

Next step: Remove {name} from \[folders\] in the config.

Exit status: 1 (a problem Dockingbird printed).

### START_FOLDER_NOT_SHARED

When: You started an agent of a config that names a folder connection, and Docker Desktop refused to give the agent the folder: it is outside the folders Docker Desktop shares (by default /Users, /Volumes, /private and /tmp). Nothing was started. In Docker Desktop open Settings > Resources > File sharing, add the folder or one above it, apply, then run the command again.

```text
Docker Desktop isn't sharing {path}, so no agent can read it.
Add it in Docker Desktop > Settings > Resources > File sharing,
then run this again.
```

Next step: Add it in Docker Desktop > Settings > Resources > File sharing, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### CONNECTION_REVOKE_STOPPED

When: You ran `dockingbird revoke NAME --to AGENT` for a folder connection. The agent's access is revoked and the agent was stopped: a folder reaches an agent as a mount, which can't be taken away while the agent runs. Continue the agent with the command shown; it gets the folders its config names when it starts again.

```text
Revoked {agent}'s access to {name} and stopped {agent}: a folder can't be
taken away from a running agent.
Continue it: dockingbird {subcommand} --as {agent}
```

Next step: dockingbird {subcommand} --as {agent}

Exit status: 0 (done).

### CONNECTION_DISCONNECT_STOPPED

When: You ran `dockingbird disconnect NAME` for a folder connection that running agents were given. The connection is disconnected and those agents were stopped: a folder reaches an agent as a mount, which can't be taken away while the agent runs. Continue each with `dockingbird start --as AGENT`, or with its own command.

```text
Disconnected {name} and stopped {names:and}: a folder can't be taken away
from a running agent.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECT_SERVICE_DONE

When: `dockingbird connect NAME --service FILE` connected a program of this Mac. The TOML file declares its path, the checkout it is in and the commit that checkout must be at, its time limit, its words and the arguments an agent may fill in. An agent of a config whose `connections` list names it asks for a run, and the run happens here, as you, with exactly the declared words, while `dockingbird serve NAME` runs in a terminal. The line names the program, with ~ for your home folder.

```text
Connected {name}: agents of a config that names it run {path} here, as you,
with the arguments it declares, when you run dockingbird serve {name}.
A config that names it: connections = ["{name}"]
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECT_BROWSER_DONE

When: `dockingbird connect NAME --browser chrome`, `--browser firefox` or `--browser safari` connected that browser on this Mac. An agent of a config whose `connections` list names it asks to use the browser, in your own profile in that browser (your logins and open windows) or in a temporary profile made for that use, and it happens here, as you, while `dockingbird serve NAME` runs in a terminal. Your own Chrome profile needs remote debugging on once, at chrome://inspect/#remote-debugging, and Chrome asks you to allow each use. Your own Firefox profile needs Firefox quit before the first request: `serve` then starts Firefox on it with remote control on and leaves it open for you. Your own Safari needs Safari's Developer setting Allow JavaScript from Apple Events on, and macOS asks once whether your terminal may control Safari; a temporary Safari profile needs Allow Remote Automation on once (Safari > Settings > Developer).

```text
Connected {name}: agents of a config that names it control {target} on this Mac,
in your own profile or a temporary one, when you run dockingbird serve {name}.
A config that names it: connections = ["{name}"]
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECT_BROWSER_UNSUPPORTED

When: The word after `--browser`, or the browser a catalog file names under `connect --config`, isn't a browser Dockingbird controls, and nothing was saved. `chrome`, `firefox` and `safari` are the browsers Dockingbird controls; any other word isn't a browser Dockingbird knows. Run the command again with `--browser chrome`, `--browser firefox` or `--browser safari`. `dockingbird serve NAME` says the same, and serves nothing, when the connection you gave it names such a browser.

```text
{word} isn't a browser Dockingbird controls.
Use dockingbird connect NAME --browser chrome, firefox or safari.
```

Next step: dockingbird connect NAME --browser chrome

Exit status: 1 (a problem Dockingbird printed).

### CONNECT_VAULT_DONE

When: You ran `dockingbird connect NAME --vault gopass` with one or more `--login ALIAS ORIGIN USERNAME`, and Dockingbird saved the connection: the gopass store's folder under its own `vaults` folder, each login's name, site and username, and the vault's passphrase, which no agent ever sees. Agents of a config that names the connection may then ask Dockingbird to sign in to those sites in a browser `dockingbird serve` lends them: Dockingbird types the password, or the current time-based code of a login given with `--totp`, into the page itself, and the agent is told only whether it worked. The last line is the line that adds it to a config.

```text
Connected {name}: a gopass vault with {count:login|logins}.
Configs that name {name} may sign in to those sites.
Add it to a config: connections = ["{name}"].
```

Next step: Add it to a config: connections = \["{name}"\].

Exit status: 0 (done).

### CONNECT_VAULT_INVALID

When: You ran `dockingbird connect NAME --vault`, and one of its words was refused before the passphrase was asked for; nothing was saved. The line names which: a manager other than `gopass`; a store that isn't a real folder under Dockingbird's `vaults` folder (a missing folder, a link, or a file in its place is refused), and the line adds that the folder must hold the whole home that `gopass setup --crypto age --storage fs` filled; a login name that isn't lowercase letters, digits and hyphens (the line numbers the `--login` words from 1 in the order given and names the refused one by its number, never the name typed); a site that isn't an origin such as `https://example.com` or `https://example.com:8443`, with no path or anything else after it (the line names its login, never the site's text); a username that is empty or has a control character (the line names its login, never the username); two `--login` words with the same name (the line names it); a `--totp` that names none of the `--login` names; or no `--login` at all.

```text
{word} isn't a password manager Dockingbird uses. Use --vault gopass.
```

Or:

```text
The store {store} isn't a folder under {folder} (a link or a file in its place is refused).
It must hold the whole home that gopass setup --crypto age --storage fs filled.
```

Or:

```text
Login {position}'s alias isn't a name of up to {count} characters
(lowercase letters, digits, dashes).
```

Or:

```text
The site for {alias} isn't an origin: use https://host or https://host:port,
nothing after it.
```

Or:

```text
The username for {alias} is empty or has a control character.
```

Or:

```text
--totp names a login that isn't one of --login's names.
```

Or:

```text
Give at least one --login ALIAS ORIGIN USERNAME.
```

Or:

```text
Give each --login its own alias; {alias} is given more than once.
```

Next step, as the message gives it:

- Use --vault gopass.
- none, where the message only informs
- Give at least one --login ALIAS ORIGIN USERNAME.
- Give each --login its own alias; {alias} is given more than once.

Exit status: 2 (usage).

### CONNECT_VAULT_PASSPHRASE

When: You ran `dockingbird connect NAME --vault gopass` at a terminal, and every word was accepted: Dockingbird asks for the gopass store's passphrase there, and it isn't shown as you type. Without a terminal it reads the passphrase from what you pipe in.

```text
Passphrase for the gopass store {store} (hidden):
```

Next step: none; it only informs.

Exit status: 0 (done).

### CONNECT_VAULT_PASSPHRASE_SHORT

When: The vault's passphrase that `dockingbird connect NAME --vault` asked for was refused, and nothing was saved: it was empty (Enter or Ctrl-D at the hidden question, or nothing piped in), or it isn't text Dockingbird can keep: UTF-8 with no NUL character, no longer than the size the line names. Nothing of it is shown.

```text
The vault's passphrase is empty. Type it at the question, or pipe it in.
```

Or:

```text
The passphrase isn't text Dockingbird can keep (UTF-8 without NUL, at most {limit}).
```

Next step, as the message gives it:

- Type it at the question, or pipe it in.
- none, where the message only informs

Exit status: 2 (usage).

### CONNECT_SERVICE_INVALID

When: Dockingbird refused the service file after `--service`, and nothing was saved. One line names what to fix and never shows what the file says: the file itself (a file of your own that only you can read, at most the size the line names, with no link in its path and outside Dockingbird's own folder), a file that isn't TOML, a key it doesn't know, or the key that is wrong: the program, the checkout, the commit, the time limit, argv, the arguments, an argument's name or one of an argument's own keys. Paths start with / or ~. The checkout must be the top folder of a git checkout that has a commit.

```text
Dockingbird can't use the service file at {path}: it must be there,
a file of your own that only you can read, at most {count:byte|bytes},
with no link in its path.
Give its real path (on a Mac, /tmp is /private/tmp), then run this again.
```

Or:

```text
The service file at {path} isn't TOML Dockingbird can read.
Fix it in the service file, then run this again.
```

Or:

```text
The service file has a key Dockingbird doesn't know. Its keys are program,
checkout, commit, timeout_s, argv and an [arguments.NAME] table for each
argument, with type, minimum, maximum, choices and max_chars.
Fix it in the service file, then run this again.
```

Or:

```text
The service file's program must be the absolute path of the program to run,
inside its checkout when it names one.
Fix it in the service file, then run this again.
```

Or:

```text
The service file's checkout must be the absolute path of the top folder
of the git checkout the program is in; a commit needs one.
Fix it in the service file, then run this again.
```

Or:

```text
The service file's commit must be the full id git rev-parse HEAD prints
in its checkout; a checkout needs one.
Fix it in the service file, then run this again.
```

Or:

```text
The service file's timeout_s must be the program's time limit in whole
seconds, from one up to {count}.
Fix it in the service file, then run this again.
```

Or:

```text
The service file's argv must be a list of at most {count:word|words}:
fixed words, {NAME} for each argument's value and {output} once,
each placeholder a whole word.
Fix it in the service file, then run this again.
```

Or:

```text
The service file's arguments must be its [arguments.NAME] tables,
at most {count}.
Fix it in the service file, then run this again.
```

Or:

```text
An argument's name in the service file must be made of lowercase letters,
digits and hyphens, and not output.
Fix it in the service file, then run this again.
```

Or:

```text
The service file's argument {name} can't be used as written: check its {field}.
An int argument takes minimum and maximum, a choice takes choices (words
that don't start with -), and a text may take max_chars.
Fix it in the service file, then run this again.
```

Next step, as the message gives it:

- Give its real path (on a Mac, /tmp is /private/tmp), then run this again.
- Fix it in the service file, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### CONNECT_SERVICE_CHECKOUT_MOVED

When: The checkout your service file names isn't at the commit the file names: its HEAD moved since you wrote the file. Nothing was saved. Check that commit out there, or put the commit it is at in the service file (`git rev-parse HEAD` in the checkout prints it), then run the command again.

```text
{path} isn't at commit {value}, which the service file names.
Check that commit out there, or name the commit it is at in the service file,
then run this again.
```

Next step: Check that commit out there, or name the commit it is at in the service file, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### SERVE_READY

When: `dockingbird serve NAME` serves the program you connected with `dockingbird connect NAME --service FILE`. Each request an agent makes runs here, as you, one at a time, with only the words the service file declares, while this terminal stays open. Press Ctrl-C to stop: a request then waits until you serve it again, and `dockingbird status` says so. With `--once` it runs the request waiting now, if there is one, and stops.

```text
Serving {name}: agents' requests to it run here, as you, one at a time.
Ctrl-C stops it.
```

Or:

```text
Serving {name}: agents' requests to it open {target} here, as you, one at a time.
Ctrl-C stops it.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_BROWSER_OPEN

When: `dockingbird serve NAME` opened the browser the line names (Chrome, Firefox or Safari) for the agent the line names, in the profile its request picked: `own` is your own profile in that browser (its logins and open windows), `temporary` a fresh profile made for this use. The agent keeps the browser until it lets it go, its container ends, the browser closes, the time limit passes or you press Ctrl-C; the next line says how it ended.

```text
{target} is open for {other} ({value} profile) until {other} lets it go,
its container ends, or Ctrl-C.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_BROWSER_CONSENT

When: An agent asked to use your own Chrome profile. Chrome shows a dialog asking whether to allow remote debugging: click Allow within the time the line names, and the agent gets the browser; otherwise the request is refused and the agent is told Chrome didn't allow it.

```text
Chrome asks whether to allow remote debugging for {name}: click Allow
within {count:second|seconds}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_BROWSER_NOT_ENABLED

When: An agent asked to use your own Chrome profile, but Chrome's remote debugging is off, so the request was refused and `dockingbird serve` keeps serving. Once, in Chrome, open chrome://inspect/#remote-debugging and turn remote debugging on; the agent's next request then works (Chrome asks you to allow each use).

```text
Chrome's remote debugging is off, so {other}'s request to {name} was refused.
In Chrome, open chrome://inspect/#remote-debugging and turn it on.
The next request then works.
```

Next step: In Chrome, open chrome://inspect/#remote-debugging and turn it on.

Exit status: 0 (done).

### SERVE_BROWSER_MISSING

When: You gave `dockingbird serve` a browser connection, but Google Chrome isn't installed at the path the line names, so nothing can be served. Install Chrome there, then run the command again.

```text
Google Chrome isn't installed at {path}, so {name} can't be served.
Install Chrome, then run this again.
```

Next step: Install Chrome, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### SERVE_BROWSER_MAC_ONLY

When: You gave `dockingbird serve` a browser connection on a computer that isn't a Mac. Dockingbird lends Chrome, Firefox and Safari from a Mac only, so nothing was opened or served here.

```text
Browsers are lent from a Mac, and this computer isn't one, so {name} can't be served.
Lend the browser from a Mac that runs Dockingbird.
```

Next step: Lend the browser from a Mac that runs Dockingbird.

Exit status: 1 (a problem Dockingbird printed).

### SERVE_BROWSER_RELAY_FAILED

When: An agent asked to use the browser the line names and `dockingbird serve` opened it, but the relay that carries the agent's commands into its container ended at once, with the status the line names and, when it wrote anything, its last words; the request was refused and `dockingbird serve` keeps serving. The usual cause is an agent whose container was made by an older Dockingbird, before it had the relay: stop the agent, run `dockingbird update`, then start the agent again.

```text
The browser relay in {other}'s container ended with status {count} before {other} could use {target},
so {other}'s request to {name} was refused. It said: {detail}
```

Or:

```text
The browser relay in {other}'s container ended with status {count} before {other} could use {target},
saying nothing, so {other}'s request to {name} was refused.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_BROWSER_UNREACHABLE

When: An agent asked to use Chrome on a temporary profile, and `dockingbird serve` started a Chrome of its own for it, but Chrome didn't start or didn't answer within the wait, so the request was refused and `dockingbird serve` keeps serving. Chrome's own output goes to a file in the folder made for it, removed with the folder, never to this terminal; the line says its last line, when it wrote one, which usually names the cause. Check that Google Chrome opens on this Mac and that the disk has room, then let the agent ask again.

```text
The Chrome started for {other} on a temporary profile didn't answer,
so {other}'s request to {name} was refused. It said: {detail}
```

Or:

```text
The Chrome started for {other} on a temporary profile didn't answer
and wrote nothing, so {other}'s request to {name} was refused.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_BROWSER_GROUP_LEFT

When: `dockingbird serve` ended a Chrome it started for an agent on a temporary profile, after the agent let the browser go or when that Chrome didn't start, and part of it kept running after it waited for it: a Chrome process stuck in macOS can do this. The line names the process group that is left and the command that ends it.

```text
Part of the Chrome started for {name} on a temporary profile kept running after
Dockingbird ended it, in process group {pid}. End it:
kill -KILL -- -{pid}
```

Next step: kill -KILL -- -{pid}

Exit status: 1 (a problem Dockingbird printed).

### SERVE_BROWSER_ACCESSIBILITY

When: `dockingbird serve` of a browser connection started and found that its own process may not post mouse and keyboard events: macOS's Accessibility switch is off for it, so an agent's clicks, keys, scrolls and drags in the browser are refused (in words, to the agent and here) until it is on. The line names the program macOS checks: the app you started `dockingbird serve` from (Terminal, iTerm), or, when an agent app such as Codex started it as its own responsible process, `dockingbird serve` itself, which no app's switch covers; when no app started it at all (a shell no app opened, a login over ssh), the line says so instead of naming one. Turn the switch on in System Settings > Privacy & Security > Accessibility for the app named, reopen that app, and start `dockingbird serve` from it; when the line says to use Terminal, start `dockingbird serve` from Terminal with Terminal turned on. Serving goes on meanwhile.

```text
Real mouse and keyboard input for {name} needs Accessibility for {tool}, the app
dockingbird serve was started from: System Settings > Privacy & Security >
Accessibility. Turn {tool} on there and reopen it, then run this again; until
then an agent's clicks and keys are refused, and serving goes on.
```

Or:

```text
Real mouse and keyboard input for {name} needs Accessibility, and macOS checks
dockingbird serve itself: {tool} started it as its own responsible process, so
no app's switch covers it. Start dockingbird serve from Terminal with Terminal
turned on in System Settings > Privacy & Security > Accessibility, and reopen
Terminal after turning the switch on; until then an agent's clicks and keys are
refused, and serving goes on.
```

Or:

```text
Real mouse and keyboard input for {name} needs Accessibility, and no app
started dockingbird serve, so no app's switch covers it. Start
dockingbird serve from Terminal with Terminal turned on in System Settings >
Privacy & Security > Accessibility, and reopen Terminal after turning the
switch on; until then an agent's clicks and keys are refused, and serving
goes on.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_BROWSER_SCREEN_RECORDING

When: `dockingbird serve` of a Safari connection started and found that its own process may not capture the screen: macOS's Screen Recording switch is off for it, so an agent's screenshot of your own Safari (taken with `screencapture`) is refused until it is on; Chrome's, Firefox's and a temporary Safari's screenshots come from the browser and need no switch, so a Chrome or Firefox connection never asks for it or says this. The line names the program macOS checks, as the Accessibility line does. Turn the switch on in System Settings > Privacy & Security > Screen & System Audio Recording for the app named, reopen that app, and start `dockingbird serve` from it. Serving goes on meanwhile.

```text
A screenshot of your own Safari for {name} needs Screen Recording for {tool},
the app dockingbird serve was started from: System Settings > Privacy &
Security > Screen & System Audio Recording. Turn {tool} on there and reopen
it, then run this again; until then an agent's screenshot of your Safari is
refused, and serving goes on.
```

Or:

```text
A screenshot of your own Safari for {name} needs Screen Recording; macOS checks
dockingbird serve itself: {tool} started it as its own responsible process, so
no app's switch covers it. Start dockingbird serve from Terminal with Terminal
turned on in System Settings > Privacy & Security > Screen & System Audio
Recording and reopen Terminal after turning the switch on; until then an
agent's screenshot of your Safari is refused, and serving goes on.
```

Or:

```text
A screenshot of your own Safari for {name} needs Screen Recording, and no app
started dockingbird serve, so no app's switch covers it. Start
dockingbird serve from Terminal with Terminal turned on in System Settings >
Privacy & Security > Screen & System Audio Recording, and reopen Terminal
after turning the switch on; until then an agent's screenshot of your Safari
is refused, and serving goes on.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_BROWSER_INPUT

When: An agent clicked, typed, pressed a key, scrolled, hovered or dragged in the lent browser, and `dockingbird serve` moved the pointer and keyboard like a person: along a curved path of the points named, over the milliseconds named, with pauses before a press and between keys. `OS input` means real mouse and keyboard events on this Mac; `protocol input along the path` means the browser's own input events played along the same path and timing (a browser without a window on screen, or Safari driven through WebDriver, whose automation window takes no real input). Nothing to do: the line is the record of what the agent did.

```text
{other} {detail} in {target} for {name} ({value}): {count:point|points} over {ms} ms.
```

Or:

```text
{other} {detail} in {target} for {name} ({value}) over {ms} ms.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_BROWSER_INPUT_REFUSED

When: An agent's click, key, text, scroll or drag in the lent browser was not posted, and the agent was told the same reason: the Accessibility switch is off for the program named (turn it on and reopen that app); another app's window is in front of the browser at the point (bring the browser forward, or move the other window); the browser has no window on screen; the point lies outside the page's viewport or the viewport's place cannot be told (a sidebar or panel open, a zoom outside the range); a key no Mac has; or the fail-safe stopped it because the pointer was in a corner of the screen, which is your way to stop an input by hand. In your own Safari, where the page itself reports the numbers, the page's viewport did not fit the content area `dockingbird serve` measured through Accessibility, the page was pinch-zoomed, or that measurement failed (the line then says why: often the page has no web content area yet, so it may still be loading; try again). Nothing was sent to the page in its place.

```text
{other}'s input to {target} for {name} was refused: {detail}
```

Or:

```text
{other}'s input to {target} for {name} was refused: {target}'s content area
could not be measured through Accessibility ({detail}), so the page's own
numbers were not trusted.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_BROWSER_RELEASE_FAILED

When: An agent's use of a browser that `dockingbird serve` lent ended (the agent let the browser go or left, its time ran out, or serve was stopped), and serve let go of the mouse buttons and keys the agent's clicks and typing still held down on this Mac, but some of them could not be let go: the message says how many and why the first one failed (the fail-safe among the reasons: the pointer in a corner of the screen). Or serve was still typing a sign-in for the agent when it ended, past the time it waits for one, so it let none of them go beside that typing. Or serve was still playing one of the agent's clicks or keys when it ended, past the time it waits for one, so it lets them go only once that one stops. Press and release any mouse button or key that still seems held, so it is not left down under your hands.

```text
{other}'s use of {target} for {name} ended, but Dockingbird couldn't let go of every
mouse button and key {other}'s input held: {count:release|releases} failed, the first: {detail}.
Press and release any mouse button or key that still seems held.
```

Or:

```text
{other}'s use of {target} for {name} ended while a sign-in was still being typed,
so Dockingbird let go of no mouse button or key {other}'s input held.
Press and release any mouse button or key that still seems held.
```

Or:

```text
{other}'s use of {target} for {name} ended while its input was still playing,
so Dockingbird lets go of what that input held only once it stops.
Press and release any mouse button or key that still seems held.
```

Next step: Press and release any mouse button or key that still seems held.

Exit status: 1 (a problem Dockingbird printed).

### SERVE_BROWSER_MESSAGES_DROPPED

When: An agent's use of a browser that `dockingbird serve` lent ended while messages the agent had sent were still waiting to be taken: serve dropped them, so nothing in them was clicked or typed on this Mac (a sign-in among them was never started) or sent to the browser. Nothing to do; the agent can ask for the browser again.

```text
{other}'s use of {target} for {name} ended with {count:message|messages} not yet taken,
so Dockingbird dropped what was left: nothing more was played, typed or sent.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### SERVE_BROWSER_SCREENSHOT_REFUSED

When: An agent asked for a screenshot of your own Safari and `screencapture` could not take it, and the agent was told the same reason: macOS's Screen Recording switch is off for the program named. Turn it on in System Settings > Privacy & Security > Screen & System Audio Recording for that app, reopen it, and start `dockingbird serve` from it again.

```text
{other}'s screenshot of your {target} for {name} was refused: {detail}
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_BROWSER_LOGIN

When: An agent asked Dockingbird to sign in to a site in the browser `dockingbird serve` lends it, and `serve` typed the login's password, with its username when the agent named a field for it, or its current time-based code, into the page, and the site took it. The line names the agent, the site, the login by its name and how the typing went, as an input line does. It never shows the username, the password or the code, and Dockingbird tells the agent none of them.

```text
{other} signed in to {origin} as {login} for {name}: {typing}
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_BROWSER_LOGIN_REFUSED

When: An agent's sign-in to a site in the lent browser was refused, or the site didn't accept it, and the agent was told the same reason: no browser was lent to it; the page isn't on the login's site, the named field isn't a password field, or the page has no code field, username field or sign-in button by that name, so nothing was typed; the vault has no entry, or no time-based code, for that login, or couldn't be read; the stored password has a character Dockingbird won't type; the browser isn't on a temporary profile; the login's second factor is a counter (HOTP), not a time-based code; the site didn't accept the sign-in, and the field was cleared; the Mac refused the typing itself (a window in front of the browser, its tab gone or not focused), and this line's words say what and where; another window came in front while the host typed, so the typing stopped and nothing was sent (the agent may ask again once the desktop is quiet); or the agent let the browser go before the result came back, and what was typed was cleared. No password or code reached the agent.

```text
{other}'s sign-in to {origin} for {name} was refused: {refusal}
```

Next step: none; it only informs.

Exit status: 0 (done).

### BROWSER_DISPLAY_MISSING

When: An agent clicked or typed in its browser (Chrome in its own container beside the agent's), and that container's real mouse and keyboard input had no X display named to post to, so the input was refused and the agent was told the same words. Nothing was sent to the page in its place.

```text
The agent's browser has no X display named,
so its real mouse and keyboard input was refused.
```

Next step: none; it only informs.

Exit status: 0 (done).

### BROWSER_DISPLAY_UNREACHABLE

When: An agent clicked or typed in its browser (Chrome in its own container beside the agent's), and the X display that container's real mouse and keyboard input posts to didn't answer: no display server runs under the name shown, it refused the connection, or the name is no display's. The input was refused and the agent was told the same words, with the display's own reason. Nothing was sent to the page in its place.

```text
The agent's browser can't reach its X display {value} ({detail}),
so its real mouse and keyboard input was refused.
```

Next step: none; it only informs.

Exit status: 0 (done).

### BROWSER_DISPLAY_STOPPED

When: An agent clicked or typed in its browser (Chrome in its own container beside the agent's), and the X display that container's real mouse and keyboard input was posting to stopped answering partway: it did not answer within its time, so the display server is gone or hung, or it refused a mouse or keyboard event it was sent. The input was refused and the agent was told the same words, with the reason. What was sent before that point may have reached the page.

```text
The X display {value} of the agent's browser stopped answering
({detail}),
so its real mouse and keyboard input was refused.
```

Next step: none; it only informs.

Exit status: 0 (done).

### BROWSER_XAUTHORITY_MISSING

When: An agent clicked or typed in its browser (Chrome in its own container beside the agent's), and the X display's authority file, its X cookie, named in the message (the file `XAUTHORITY` names, or `.Xauthority` in that container's home) was missing or could not be read, so the real mouse and keyboard input never started: the input was refused and the agent was told the same words. Dockingbird never makes that file on its own.

```text
The agent's browser can't read its X cookie file,
{path} ({detail}),
so its real mouse and keyboard input was refused.
```

Next step: none; it only informs.

Exit status: 0 (done).

### BROWSER_SECCOMP_FILE_FAILED

When: You ran a command whose config asks for a browser (`browser = "chrome"`), and Dockingbird couldn't write the file that tells Docker which system calls the browser's container may make, under `seccomp/` in Dockingbird's folder: the disk is full or read-only, the folder is a link or another user's, or the copy Dockingbird ships doesn't match its own record of it. Nothing was started. The line names the file and the system's reason.

```text
Dockingbird couldn't write {path}, the browser's seccomp profile
({detail}),
so nothing was started.
Check that path and its disk, then run this again.
```

Next step: Check that path and its disk, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### BROWSER_DISPLAY_FAILED

When: An agent's browser was starting in its own container beside the agent's, and one of the programs that make its screen (the virtual display, its keyboard layout, its window manager, the viewer's server or the display's key tool) didn't come up: the message names the program and the last line it wrote, if any. The browser didn't start, and the agent's browser tools will say the browser is unavailable.

```text
The agent's browser didn't start: its screen's {tool} didn't come up.
It said: {detail}
```

Or:

```text
The agent's browser didn't start: its screen's {tool} didn't come up,
saying nothing.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### BROWSER_NO_WINDOW

When: An agent's browser was starting in its own container, and Chrome showed no window on its screen within the time the message names, or showed its window and then didn't answer the connection the agent's browser tools use, for the reason the message gives: the message gives the last line Chrome wrote, if any. Chrome and its screen were stopped, and the agent's browser tools will say the browser is unavailable.

```text
The agent's browser showed no window within {count:second|seconds}, so it was stopped.
It said: {detail}
```

Or:

```text
The agent's browser showed no window within {count:second|seconds}, so it was stopped,
saying nothing.
```

Or:

```text
The agent's browser showed its window, but {error}, so it was stopped.
It said: {detail}
```

Or:

```text
The agent's browser showed its window, but {error}, so it was stopped,
saying nothing.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### BROWSER_EXTENSIONS_NOT_RUNNING

When: An agent's browser was starting in its own container with the Chrome extensions its config names, and the ones the message names did not start within the time it gives. Chrome and its screen were stopped, so the start failed; check the extension's folder or link, then add the config again.

```text
{count:extension|extensions} did not start within {seconds:second|seconds}: {extensions}; so the agent's browser was stopped.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### BROWSER_EXPECTED_MALFORMED

When: An agent's browser was starting in its own container, and the policy files Dockingbird copied into it were not as it wrote them: not owned by root, writable by others, or not in their form. The browser was stopped before it waited for any extension, so the start failed.

```text
The browser's policy files are not as Dockingbird wrote them ({detail}),
so the agent's browser was stopped.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### BROWSER_POLICY_TAB_OPEN

When: An agent's browser read Chrome's own policy page in a tab of its own when it started, and could not close that tab. The browser goes on; the tab stays open beside the agent's own.

```text
Chrome's policy page could not be closed ({detail}); it stays open as a tab
in the agent's browser.
```

Next step: none; it only informs.

Exit status: 0 (done) or 1 (a problem Dockingbird printed), as "When:" says.

### BROWSER_EXITED

When: An agent's browser (Chrome in its own container beside the agent's) stopped while the agent was using it, or could not be started: the message says how it ended and the last line it wrote, if any. The agent's next browser call was refused with the same words, and the browser's container stops.

```text
The agent's browser stopped with status {status}, so the agent's call was refused.
It said: {detail}
```

Or:

```text
The agent's browser stopped with status {status}, so the agent's call was refused,
saying nothing.
```

Or:

```text
The agent's browser closed its connection, so the agent's call was refused.
```

Or:

```text
The agent's browser could not be started: {detail}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### BROWSER_INPUT_RELEASE_FAILED

When: An agent's browser (Chrome in its own container beside the agent's) let go of the mouse buttons and keys the agent's clicks and typing still held down, because the agent's browser tools left or the browser stopped, and some of them could not be let go: the message says how many and why the first one failed. Nothing waits for an answer then, so it is said in the browser's log only.

```text
The agent's browser could not let go of everything the agent's input held
when the agent left or the browser stopped: {count:release|releases} failed, the first: {detail}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### BROWSER_PROXY_MALFORMED

When: An agent's browser container was given a network proxy address that doesn't start with `http://`, the one form Dockingbird writes, so the browser could not be told where to send its traffic and was not started. Nothing was sent without the proxy.

```text
The agent's browser can't use its network proxy: {name} is {value},
not an http:// address, so the browser wasn't started.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### BROWSER_VNC_UNAVAILABLE

When: You asked to watch an agent's browser, and the browser's container could not open the view: the password file the browser's screen writes at its start is missing, or the viewer's server refused the connection. The message names which. Nothing is shown.

```text
The agent's browser can't be watched: {detail}.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### BROWSER_VNC_VIEWER

When: A line of the viewer server's own log inside an agent's browser container, which you read when watching the browser goes wrong: your viewer connected, signed in, left or was turned away, or sent its clipboard, which isn't passed to the agent's browser.

```text
A viewer connected to the agent's browser screen from {host}:{port}.
```

Or:

```text
A viewer signed in to the agent's browser screen from {host}:{port}.
```

Or:

```text
A viewer left the agent's browser screen ({host}:{port}).
```

Or:

```text
A viewer was turned away from the agent's browser screen ({host}:{port}): {reason}
```

Or:

```text
A viewer's clipboard text ({count:byte|bytes}) from {host}:{port} was not passed to the agent's browser.
```

Or:

```text
A key a viewer pressed ({host}:{port}, keysym {number}) wasn't pressed in the agent's browser:
{reason}
```

Next step: none; it only informs.

Exit status: 0 (done).

### BROWSER_VNC_REFUSAL

When: Your viewer was turned away while watching an agent's browser, and this says why: a wrong password, or something the viewer sent or asked for that the browser's screen doesn't take. A viewer that shows a reason shows these words.

```text
the password was wrong.
```

Or:

```text
it doesn't speak the VNC protocol, version 3 (its first bytes were {detail}).
```

Or:

```text
it chose sign-in type {number}, which isn't offered.
```

Or:

```text
it sent message type {number}, which the VNC protocol doesn't have.
```

Or:

```text
it asked for colour-map pixels, which the screen doesn't send.
```

Or:

```text
it asked for {number} bits a pixel; the screen sends 8, 16 or 32.
```

Or:

```text
it asked for a colour channel with the maximum {number};
the screen sends one less than a power of two, from 1 to 255.
```

Or:

```text
it asked for a colour channel past the pixel's {number} bits.
```

Next step: none; it only informs.

Exit status: 0 (done).

### BROWSER_VNC_SERVER

When: The server that shows an agent's browser screen to your viewer stopped: its screen lacks something it needs or is not the kind of screen it reads, or it lost the screen. The browser goes on working for the agent, but watching it fails until the agent's browser starts again.

```text
The agent's browser can't be watched: its screen's viewer server stopped.
It said: {detail}
```

Or:

```text
The agent's browser can't be watched: its screen's viewer server stopped,
saying nothing.
```

Or:

```text
The agent's browser can't be watched: its screen has no {name}
extension, which the viewer server needs.
```

Or:

```text
The agent's browser can't be watched: the viewer server lost its screen ({detail}).
```

Or:

```text
The agent's browser can't be watched: its screen is depth {depth} at {bits}
bits a pixel, colour masks {masks}, byte order {order}, not the 24-bit
TrueColor screen the viewer server reads.
```

Or:

```text
The agent's browser can't be watched: its screen's setup does not list its
own pixel format or visual.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### BROWSER_SOCKET_FAILED

When: An agent's browser started in its own container, but the place where the agent's browser tools connect to it (a folder both containers share) isn't the browser's own private folder, or the connection point there could not be made: the message names the folder's owner and mode, or the system's reason. The browser was stopped rather than listen anywhere else.

```text
The agent's browser can't listen for the agent at {path} ({detail}),
so it was stopped.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### BROWSER_SOLVE_OUTCOME

When: A page in an agent's browser tab showed a challenge (a reCAPTCHA, an hCaptcha, a Cloudflare check or a captcha form), and the browser's container handed the tab to the solver you set up on this Mac. The agent's pending browser action waited for the solve and its answer carries this line: the challenge was solved, the solver gave it up, no solver was set up or the solver lacks its settings, the solver could not run, or it gave no answer in time. The agent goes on with the page as it is.

```text
The challenge in the agent's browser tab was solved.
```

Or:

```text
The challenge in the agent's browser tab was not solved: {detail}
```

Or:

```text
The agent's browser has no solver ({detail}), so its challenge was not solved.
```

Or:

```text
The solver could not run on the challenge in the agent's browser tab: {detail}
```

Or:

```text
The solver gave no answer on the challenge in the agent's browser tab within {seconds:second|seconds}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### BROWSER_SOLVE_VARIABLE_MALFORMED

When: An agent's browser container was given a solve setting other than `on`, the one value Dockingbird writes when a solver file names a runner, so the browser was not started. Nothing was solved.

```text
The agent's browser can't take a solver: {name} is {value}, not on,
so the browser wasn't started.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### BROWSER_SOLVER_FILE_MALFORMED

When: You started an agent whose config asks for a browser, and the solver file in your Dockingbird home (`browser-solver.json`) is there but isn't a command: a JSON object whose `command` is a list of words, the first an absolute path. The agent was not started. Fix the file, or remove it to start browsers with no solver.

```text
The solver file {path} isn't a command ({detail}), so the agent
wasn't started.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### BROWSER_SOLVER_CHANNEL_FAILED

When: The solve watcher of an agent's browser could not reach what a solve needs, and its log carries this line. Either the browser's container could not open the channel for the next challenge (the browser was started without a solver, or its service is gone), and the watcher ended: the agent's browser runs on with no solver. Or one connection of your solver to the browser could not be bridged (the browser is gone, or docker could not be started): that connection was closed and the solve went on to its outcome. Or the outcome of a solve could not be handed back, the channel being gone by then: the agent's browser was told the solve failed, and the watcher went on to the next challenge.

```text
The agent's browser can't hand its challenge to a solver: {detail}.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### BROWSER_SOLVE_WATCH

When: The log of the solve watcher that runs beside an agent's browser (in your Dockingbird home's `logs` folder): a solve begun on a tab, how it ended, and the watcher's own end when the browser's container no longer answers it (the browser was stopped, or its service refused). Nothing to do unless a solve you expected ended otherwise than solved: the line says why.

```text
Solving the challenge in the agent's browser tab {target} ...
```

Or:

```text
The solve in the agent's browser tab {target} ended: {detail}
```

Or:

```text
The agent's browser's solve channel ended with status {status},
so no more of its challenges are solved.
```

Next step: none; it only informs.

Exit status: 0 (done).

### BROWSER_SOLVE_INPUT_RELEASED

When: In the log of an agent's browser container (`docker logs`): your solver's input connection to the browser ended (it closed, its solve ended, or the browser stopped) while the clicks and keys it sent still held a mouse button or a key down, and the browser let them go. When a release failed, the line says how many and why; the others were still let go.

```text
The solver's input connection ended holding {buttons:button|buttons} and {keys:key|keys};
the service released them.
```

Or:

```text
The solver's input connection ended holding {buttons:button|buttons} and {keys:key|keys};
the service released them, and {failed} of the releases failed,
the first: {detail}
```

Next step: none; it only informs.

Exit status: 0 (done).

### BROWSER_SOLVE_INPUT_CUT

When: In the log of an agent's browser container (`docker logs`): the browser refused a click or key of your solver, and the word in brackets says why (for example `viewer-active` while you were using the browser through `dockingbird watch`, `fail-safe` with the pointer in a screen corner, or `session-ended` when the browser was stopping). Since it may have stopped part way, the browser let go of every mouse button and key the solver held. When a release failed, the line says how many and why.

```text
The solver's input frame was refused ({word}) and may have left input held;
the service released {buttons:button|buttons} and {keys:key|keys}.
```

Or:

```text
The solver's input frame was refused ({word}) and may have left input held;
the service released {buttons:button|buttons} and {keys:key|keys}, and {failed} of the releases failed,
the first: {detail}
```

Next step: none; it only informs.

Exit status: 0 (done).

### BROWSER_IMAGE_BUILDING

When: You started an agent whose config asks for a browser (`browser = "chrome"`), and the browser wasn't built yet for this version of Dockingbird: Dockingbird builds it once, before the browser starts. The line shows while it builds, then how long it took. When the output goes to a pipe or a file, the line prints at once and a "still building the browser" line follows once a minute while it runs.

```text
Building the agent's browser ... done ({elapsed})
```

Or:

```text
Building the agent's browser ...
```

Or:

```text
Building the agent's browser: waking Docker ...
```

Or:

```text
Building the agent's browser: no progress for {quiet}
```

Or:

```text
  still building the browser: step {index} of {count}, {elapsed} so far
```

Or:

```text
  still building the browser: step {index} of {count}, no output for {quiet}
```

Or:

```text
  still building the browser: waking Docker ...
```

Or:

```text
  still building the browser: preparing the build, {elapsed} so far
```

Next step: none; it only informs.

Exit status: 0 (done).

### BROWSER_SIDECAR_STARTING

When: You started an agent without a terminal whose config asks for a browser: Dockingbird starts the browser in its own container beside the agent's and waits until it says it is ready. The line shows while it starts, then how long it took.

```text
Starting the agent's browser ... done ({elapsed})
```

Or:

```text
Starting the agent's browser ...
```

Next step: none; it only informs.

Exit status: 0 (done).

### BROWSER_SIDECAR_FAILED

When: You started an agent whose config asks for a browser, and the browser's container didn't start or didn't say it was ready in time. Everything the start made was removed. The message shows the browser's last lines, or what Docker said when it printed none.

```text
{name}'s browser didn't start, so nothing was started. Its last lines:
{entries}
Run this again.
```

Or:

```text
{name}'s browser didn't start, so nothing was started. Docker said:
  {said}
Run this again.
```

Next step: Run this again.

Exit status: 1 (a problem Dockingbird printed).

### BROWSER_LOG_ROW

When: One line of an agent's browser's log, under the message that says the browser didn't start.

One row of a table; its cells line up with the rows around it.

```text
  > {line}
```

Or:

```text
    {line}
```

Next step: none; it only informs.

Exit status: 0 (done).

### BROWSER_STORE_NO_EGRESS

When: You started an agent whose config installs Chrome Web Store extensions in its browser, with egress `none`. Chrome downloads those extensions from Google at each start, which an agent with no network can't reach, so nothing was started. Start with egress `allowlist`, `models` or `full`, or remove the store entries.

```text
Config {name} installs Chrome Web Store extensions, which come from Google's
update hosts, and this start's egress is none.
Start with egress allowlist, models or full, or remove the store entries from
the config and add it again.
```

Next step: Start with egress allowlist, models or full, or remove the store entries from the config and add it again.

Exit status: 1 (a problem Dockingbird printed).

### BROWSER_PACKS_UNREADABLE

When: You started an agent whose config names a folder extension, and the packed copy `dockingbird config add` stored for it could not be read, or the config was replaced or removed while the start read it. Nothing was started; add the config again, or start again.

```text
The packed extensions of config {name} can't be read.
Run dockingbird config add on its file again.
```

Or:

```text
Config {name} was replaced or removed while this start read it.
Start again.
```

Next step, as the message gives it:

- Run dockingbird config add on its file again.
- Start again.

Exit status: 1 (a problem Dockingbird printed).

### BROWSER_HOSTS_ADDED

When: You started an agent whose config installs Chrome Web Store extensions, with egress `allowlist` or `models`: its proxy admits Google's two update hosts the extensions come from. The browser shares the agent's proxy, so the agent can reach them too.

```text
{name}'s proxy admits clients2.google.com and clients2.googleusercontent.com
for its browser's Chrome Web Store extensions; the agent can reach them too.
```

Next step: none; it only informs.

Exit status: 0 (done) or 1 (a problem Dockingbird printed), as "When:" says.

### BROWSER_POLICY_NOT_APPLIED

When: You started an agent whose config gives its browser Chrome policies, and Chrome's own policy page showed some of them with an error or not at all, or could not be read. The agent runs; `dockingbird status NAME` shows each policy's state.

```text
Chrome did not apply {count:policy|policies} for {name}: {policies}.
dockingbird status {name} shows why.
```

Or:

```text
Chrome's policy page could not be read for {name}, so {count:policy|policies} may not apply: {policies}.
```

Next step, as the message gives it:

- dockingbird status {name}
- none, where the message only informs

Exit status: 0 (done) or 1 (a problem Dockingbird printed), as "When:" says.

### WATCH_NO_BROWSER

When: You ran `dockingbird watch NAME` and the agent has no browser running in a container: there is no such agent, its config asks for no browser, or its browser's container has stopped (the message names its state). Nothing is opened. An agent whose config asks for a browser has one while it runs.

```text
{name} has no browser to watch.
```

Or:

```text
{name} has no browser to watch: its browser's container isn't running ({state}).
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### WATCH_OPEN

When: You ran `dockingbird watch NAME`. The line is the address of the agent's browser screen on this Mac, which takes your viewer's connections, from this Mac alone, one at a time, for as long as the watch runs (Screen Sharing connects once to ask you for the password and again to sign in), and the warning that goes with it: whatever you type or paste into that browser, the agent can read from the page. Your VNC viewer opens on the address unless you gave `--no-open`; then open it yourself.

```text
Opening {name}'s browser, vnc://127.0.0.1:{port}, in your VNC viewer.
Anything you type or paste into this browser is visible to the agent {name},
which reads the page. Sign in to nothing you would not hand it.
```

Or:

```text
Open vnc://127.0.0.1:{port} in a VNC viewer to see {name}'s browser.
Anything you type or paste into this browser is visible to the agent {name},
which reads the page. Sign in to nothing you would not hand it.
```

Next step: none; it only informs.

Exit status: 0 (done).

### WATCH_PASSWORD

When: Your viewer connected to the agent's browser screen, and this is the password it asks for. It is the browser's own, set when its container started, so it is the same for every watch of that browser; it is printed once per watch, however many times the viewer connects.

```text
VNC password: {password}
```

Next step: none; it only informs.

Exit status: 0 (done).

### WATCH_ENDED

When: You closed the viewer of the agent's browser and it did not connect again within a moment (Screen Sharing connects again at once when it signs in or after its connection dropped, so the watch waits for that), or you pressed Ctrl-C where `dockingbird watch` ran. The agent's browser runs on; run `dockingbird watch NAME` again to see it again.

```text
Stopped watching {name}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### WATCH_FAILED

When: You ran `dockingbird watch NAME` and the agent's browser screen could not be shown: the bridge in the browser's container refused (the quoted line is its own, or Docker's), or this Mac could not open a port for your viewer or start Docker for the connection (the message says which, with the system's reason).

```text
{name}'s browser can't be watched. Its bridge said:
  {said}
```

Or:

```text
{name}'s browser can't be watched: {detail}.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### WATCH_OPEN_FAILED

When: You ran `dockingbird watch NAME` and macOS's `open` could not start your VNC viewer on the address, or exited with a status. The watch goes on: open the printed address in a VNC viewer (Screen Sharing) yourself. The command exits as the watch ends: 0 once you closed the viewer or pressed Ctrl-C, 1 after a failure it printed.

```text
Your VNC viewer couldn't be opened ({detail}).
Open vnc://127.0.0.1:{port} in one yourself.
```

Next step: Open vnc://127.0.0.1:{port} in one yourself.

Exit status: 0 (done) or 1 (a problem Dockingbird printed), as "When:" says.

### SERVE_SAFARI_CONSENT

When: An agent asked to use your own Safari. The first time, macOS asks whether the app running `dockingbird serve` (your terminal) may control Safari: click OK within the time the line names, and the agent gets Safari; otherwise the request is refused and the agent is told Safari didn't allow it. Once allowed, macOS remembers it (System Settings > Privacy & Security > Automation), and the line is only a reminder.

```text
If macOS asks whether this app may control Safari for {name}, click OK
within {count:second|seconds}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_SAFARI_NOT_ENABLED

When: An agent asked for Safari on a temporary profile, but Safari's remote automation is off, so the request was refused and `dockingbird serve` keeps serving. Once, in Safari, open Settings > Advanced and turn on Show features for web developers, then Settings > Developer and turn on Allow Remote Automation (or run `safaridriver --enable` in a terminal, which asks for your password); the agent's next request then works. Safari opens the agent's pages in an automation window of its own, apart from your browsing, your logins and your history.

```text
Safari's remote automation is off, so {other}'s request to {name} was refused.
In Safari, open Settings > Developer and turn on Allow Remote Automation.
Settings > Advanced > Show features for web developers shows that tab.
The next request then works.
```

Next step: In Safari, open Settings > Developer and turn on Allow Remote Automation.

Exit status: 0 (done).

### SERVE_SAFARI_JAVASCRIPT_OFF

When: An agent asked to use your own Safari, with your logins and open tabs, but Safari's Developer setting Allow JavaScript from Apple Events is off, so the request was refused and `dockingbird serve` keeps serving. Once, in Safari, open Settings > Developer (Settings > Advanced > Show features for web developers shows that tab) and turn it on; the agent's next request then works.

```text
Safari doesn't take JavaScript from Apple Events, so {other}'s request to {name}
for your own Safari was refused.
In Safari, open Settings > Developer and turn on Allow JavaScript from Apple
Events. The next request then works.
```

Next step: In Safari, open Settings > Developer and turn on Allow JavaScript from Apple Events.

Exit status: 0 (done).

### SERVE_SAFARI_DENIED

When: An agent asked to use your own Safari, but macOS didn't let the app running `dockingbird serve` control Safari: you clicked Don't Allow, now or before, or didn't answer within the time the consent line named, so the request was refused and `dockingbird serve` keeps serving. In System Settings > Privacy & Security > Automation, allow that app (your terminal) to control Safari, then let the agent ask again.

```text
macOS didn't let this app control Safari, or its question went unanswered,
so {other}'s request to {name} was refused.
In System Settings > Privacy & Security > Automation, allow this app
to control Safari. Then let {other} ask again.
```

Next step: In System Settings > Privacy & Security > Automation, allow this app to control Safari.

Exit status: 0 (done).

### SERVE_SAFARI_MISSING

When: You gave `dockingbird serve` a Safari connection, but Safari's automation program, safaridriver, isn't at the path the line names, so nothing can be served. It comes with Safari on every Mac since macOS 10.13; update macOS, then run the command again.

```text
Safari's automation program isn't at {path}, so {name} can't be served.
It comes with Safari on a Mac. Update macOS, then run this again.
```

Next step: Update macOS, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### SERVE_SAFARI_UNREACHABLE

When: An agent asked for Safari and `dockingbird serve` couldn't reach it: on a temporary profile the driver didn't start, didn't answer within the wait or refused to open Safari for another reason than its remote automation switch; on your own profile Safari gave no answer to an Apple Event within its time, or osascript couldn't run. The line says the driver's or osascript's own words, when there were any; the request was refused and `dockingbird serve` keeps serving. Check that Safari opens on this Mac, then let the agent ask again. When the line says Safari still keeps the automation of an earlier request, that request was cut short while Safari was busy and Safari keeps its orange automation window: quit Safari and open it again, then let the agent ask again; don't close that window by hand, closing it can crash Safari.

```text
Safari didn't answer, so {other}'s request to {name} was refused. It said: {detail}
```

Or:

```text
Safari didn't answer and said nothing, so {other}'s request to {name} was refused.
```

Or:

```text
Safari didn't answer within {count:second|seconds} and said nothing in that time,
so {other}'s request to {name} was refused.
```

Or:

```text
Safari's driver wasn't ready within {count:second|seconds} and said nothing in that time,
so {other}'s request to {name} was refused.
```

Or:

```text
Safari's driver stopped each of the {count} times it was started,
so {other}'s request to {name} was refused. It said: {detail}
```

Or:

```text
Safari's driver stopped each of the {count} times it was started and said nothing,
so {other}'s request to {name} was refused.
```

Or:

```text
Safari's driver answered with more than {size},
so {other}'s request to {name} was refused.
```

Or:

```text
The connection to Safari's driver failed before it answered,
so {other}'s request to {name} was refused: {detail}
```

Or:

```text
Safari still keeps the automation of an earlier request that was cut short,
so {other}'s request to {name} was refused.
Quit Safari and open it again, then let {other} ask again. Don't close the
orange automation window: closing it can crash Safari.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_SAFARI_REFUSED

When: An agent asked to use your own Safari, and Safari answered an Apple Event of the request's start with an error, for another reason than macOS's permission or the JavaScript setting, so the request was refused and `dockingbird serve` keeps serving. The line says Safari's own words, as osascript gave them. Check that Safari opens on this Mac and shows its windows, then let the agent ask again.

```text
Safari refused {other}'s request to {name}. It said: {detail}
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_SAFARI_CLOSED

When: An agent asked to use your own Safari while Safari wasn't open, and `dockingbird serve` couldn't open it: macOS's `open` failed, or Safari still wasn't running when the request's start sent it an Apple Event, so the request was refused and `dockingbird serve` keeps serving. The line says the words `open` or osascript gave. Open Safari, then let the agent ask again.

```text
Safari isn't open and Dockingbird couldn't open it,
so {other}'s request to {name} was refused. It said: {detail}
Open Safari, then let {other} ask again.
```

Next step: Open Safari, then let {other} ask again.

Exit status: 0 (done).

### SERVE_SAFARI_NOT_DELETED

When: An agent's request used a temporary Safari profile, and when the request ended Safari's driver didn't end its automation: it gave no answer within the time `dockingbird serve` waits, or refused, and the line says its words when there were any. Dockingbird ended the driver but never quits Safari, which may keep the request's orange automation window and would then refuse the next temporary request: quit Safari and open it again before then. Don't close that window by hand, closing it can crash Safari. `dockingbird serve` keeps serving.

```text
Safari's driver didn't end the automation of {other}'s request to {name}.
If Safari still shows its orange automation window, quit Safari and open it
again before the next request. Don't close that window: closing it can crash
Safari.
The error was: {detail}
```

Or:

```text
Safari's driver gave no answer within {count} seconds when asked to end
the automation of {other}'s request to {name}.
If Safari still shows its orange automation window, quit Safari and open it
again before the next request. Don't close that window: closing it can crash
Safari.
```

Or:

```text
Safari's driver didn't end the automation of {other}'s request to {name}
and said nothing.
If Safari still shows its orange automation window, quit Safari and open it
again before the next request. Don't close that window: closing it can crash
Safari.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_FIREFOX_MISSING

When: You gave `dockingbird serve` a Firefox connection, but Firefox isn't installed at the path the line names, so nothing can be served. Install Firefox there, then run the command again.

```text
Firefox isn't installed at {path}, so {name} can't be served.
Install Firefox, then run this again.
```

Next step: Install Firefox, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### SERVE_FIREFOX_RUNNING

When: An agent asked to use your own Firefox profile, and a Firefox is running on it that Dockingbird can't lend: one you opened yourself (Firefox takes remote control only when started with it), or one whose one remote connection is stuck from an earlier use. The request was refused and `dockingbird serve` keeps serving. Quit Firefox; the agent's next request then starts Firefox on your profile with remote control on, later requests use that Firefox, and Dockingbird closes it when `dockingbird serve` stops.

```text
Firefox is open on your profile but can't be lent (no remote control,
or an earlier use that got stuck), so {other}'s request to {name} was refused.
Quit Firefox; the next request starts it with remote control on
and Dockingbird closes it when serving stops.
```

Next step: Quit Firefox; the next request starts it with remote control on and Dockingbird closes it when serving stops.

Exit status: 0 (done).

### SERVE_FIREFOX_NO_PROFILE

When: An agent asked to use your own Firefox profile, but Firefox's `profiles.ini` in the folder the line names is missing or names no default profile (Firefox has never run as you), so the request was refused and `dockingbird serve` keeps serving. Open Firefox once, which makes the profile.

```text
Firefox has no default profile in {path},
so {other}'s request to {name} (own profile) was refused.
Open Firefox once to make one.
```

Next step: Open Firefox once to make one.

Exit status: 0 (done).

### SERVE_FIREFOX_UNREACHABLE

When: An agent asked to use Firefox, and `dockingbird serve` started a Firefox for it (on a temporary profile, or on your own profile while no Firefox ran), but Firefox didn't start, didn't write its remote endpoint or didn't answer within the wait, so the request was refused and `dockingbird serve` keeps serving. Firefox's own output goes to a file in the folder made for that request, removed with it, never to this terminal; the line says its last line, when it wrote one, which usually names the cause. Check that Firefox opens on this Mac and that the disk has room, then let the agent ask again.

```text
The Firefox started for {other} ({value} profile) didn't answer,
so {other}'s request to {name} was refused. It said: {detail}
```

Or:

```text
The Firefox started for {other} ({value} profile) didn't answer
and wrote nothing, so {other}'s request to {name} was refused.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_FIREFOX_STARTED

When: An agent asked to use your own Firefox profile while no Firefox ran, so `dockingbird serve` started Firefox on your profile with remote control on, for that agent's request. It stays open afterwards: later requests use the same Firefox; when a request ends, the tabs the agent opened and the pages those tabs opened are closed, and your own tabs stay, those you open while a request runs too (a page opened from one of your tabs is yours). Dockingbird closes this Firefox when `dockingbird serve` stops (Ctrl-C, its terminal closed, or `--once` done), so nothing is left listening for remote control. You can use it meanwhile, and quitting it yourself is fine: the next request starts it again.

```text
Firefox was started on your profile with remote control on, for {other}'s
request to {name}; it stays open for later requests, and Dockingbird
closes it when serving stops.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_FIREFOX_CLOSED

When: An agent's request used your own Firefox profile, and the Firefox `dockingbird serve` had started lost its remote connection while the request ran (the agent ended it, Firefox sent a message larger than Dockingbird accepts, or Firefox dropped it). When the request ended, Firefox refused the new connection Dockingbird makes to keep that Firefox's one remote connection its own: another program had taken it meanwhile, or Firefox had not let the old one go in time. Dockingbird closed that Firefox at once rather than leave it listening for remote control it no longer had; `dockingbird serve` keeps serving, and the agent's next request starts Firefox on your profile again. A Firefox that quits by itself during the request (the agent closed it, or you quit it) gets no such line.

```text
The Firefox started on your profile lost its remote connection during
{other}'s request to {name} and refused a new one, so Dockingbird closed it;
the next request starts it again.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_BROWSER_FOLDER_FAILED

When: An agent asked to use a browser, and `dockingbird serve` couldn't make the folder that request needs in Dockingbird's own `tmp` folder (the path the line names: the browser's own output goes there, and a temporary profile lives there), so the request was refused and `dockingbird serve` keeps serving. A folder of that name may be left from an earlier `dockingbird serve` that stopped short, or the disk may be full or read-only. Check the path and the disk, then let the agent ask again.

```text
Dockingbird couldn't make {path}, the folder for {other}'s use of {name},
so the request was refused.
Check that path and its disk, then let the agent ask again.
```

Next step: Check that path and its disk, then let the agent ask again.

Exit status: 0 (done).

### SERVE_RAN

When: `dockingbird serve` took one request of the agent the line names. It ran and was done, with how long it took; it ran and ended with the program's own status, and its output is in the agent's log folder all the same; it was refused, with the reason: the checkout isn't at its commit, the program isn't where it was connected or others can change it, the arguments don't fit the service file, the request waited too long to start, the program ran past its time limit, its output was over the size limit, or you stopped `dockingbird serve` (Ctrl-C, or its terminal closed); or its result didn't reach Dockingbird.

```text
Ran {name} for {other}: done in {elapsed}.
```

Or:

```text
Ran {name} for {other}: ended with status {count} in {elapsed};
its output is in {other}'s log folder.
```

Or:

```text
Refused {other}'s request to {name}: {detail}.
```

Or:

```text
Ran {name} for {other}, but its result didn't reach Dockingbird.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_STOPPED

When: You pressed Ctrl-C where `dockingbird serve` ran, closed its terminal, or ended it. A program it was running was stopped and its request refused. New requests wait until you run `dockingbird serve NAME` again.

```text
Stopped serving {name}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### SERVE_NOT_A_SERVICE

When: You gave `dockingbird serve` the name of a connection that isn't a service: a GitHub repo, a folder, a database or a cloud account. Only a program you connected with `dockingbird connect NAME --service FILE` can be served; `dockingbird connections` lists your connections.

```text
{name} is a connection of kind {kind}, not a service.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### SERVE_CHECKOUT_MOVED

When: The checkout the service runs from isn't at the commit it was connected with: its HEAD moved since `dockingbird connect NAME --service FILE`. Nothing ran. Check that commit out there, or connect the service again at the commit it is at.

```text
{path} isn't at the commit {name} was connected with ({value}).
Check it out, or connect the service again.
```

Next step: Check it out, or connect the service again.

Exit status: 1 (a problem Dockingbird printed).

### SERVE_COORDINATOR_GONE

When: Dockingbird stopped while `dockingbird serve` waited for requests; `serve` never starts it again itself, so your stop stands. Requests wait until you run `dockingbird serve NAME` again.

```text
Dockingbird stopped, so serving {name} stopped too.
Run this again.
```

Next step: Run this again.

Exit status: 1 (a problem Dockingbird printed).

### SERVE_CHECKOUT_UNREAD

When: After a run, git couldn't read the service's checkout to tell whether the program changed it, so the result tells the agent the checkout has changes.

```text
Dockingbird couldn't read {path} with git after {name} ran,
so the result says the checkout has changes.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### SERVE_OUTPUT_UNREAD

When: After a run, Dockingbird couldn't read a file the program wrote in its output folder, so it sent the agent no result, and the request ended as stopped.

```text
Dockingbird couldn't read the files {name} wrote, so it sent no result.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### SERVE_FOLDER_LEFT

When: Dockingbird couldn't remove the folder a run used, after the run (a program can make its files hard to remove), or the folder a temporary Chrome profile used, after the agent let the browser go (a download can do the same). Delete the folder the line names.

```text
Dockingbird couldn't remove {path}, a folder of a run of {name}.
Delete it.
```

Next step: Delete it.

Exit status: 1 (a problem Dockingbird printed).

### SERVE_FOLDER_FAILED

When: Dockingbird couldn't make the folder a run needs in its own `tmp` folder, so it refused the request and stopped serving. Check that the folder is yours and the disk has space, then run `dockingbird serve NAME` again.

```text
Dockingbird couldn't make a folder in {path} for a run of {name},
so it refused the request and stopped serving.
Check that folder, then run this again.
```

Next step: Check that folder, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### SERVE_VAULT_FOLDER_FAILED

When: Dockingbird couldn't make its `vaults` folder, where the stores of your vault connections live, or found a link, a file or another user's folder in its place, so the command stopped. Check the path the line names and its disk, then run the command again.

```text
Dockingbird couldn't make its vaults folder {folder}.
Check that path and its disk.
```

Next step: Check that path and its disk.

Exit status: 1 (a problem Dockingbird printed).

## Harbor jobs

### HARBOR_PIN_INVALID

When: You ran `dockingbird harbor` with a `--harbor-commit` that isn't a full commit, or in a task repository whose `.github/workflows/validate-harbor.yml` names a Harbor commit that isn't one, or can't be read safely. Nothing ran; the line says where the commit came from, never what it was.

```text
The Harbor commit from {source} isn't a full commit (40 lowercase hex characters).
Fix it, or give one with --harbor-commit SHA.
```

Or:

```text
Harbor's commit wasn't read: {source} is too large.
Fix it, or give one with --harbor-commit SHA.
```

Or:

```text
Harbor's commit wasn't read: {source} is a link or not a regular file.
Fix it, or give one with --harbor-commit SHA.
```

Or:

```text
Harbor's commit wasn't read: {source} isn't UTF-8 text.
Fix it, or give one with --harbor-commit SHA.
```

Next step: Fix it, or give one with --harbor-commit SHA.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_PIN

When: You ran `dockingbird harbor run`, `baseline`, `check` or `version`: the Harbor commit it uses, and whether it came from `--harbor-commit`, from the task repository's CI workflow or from Dockingbird's own pin.

```text
Harbor {commit} (Dockingbird's default)
```

Or:

```text
Harbor {commit} (the repository's CI pin)
```

Or:

```text
Harbor {commit} (--harbor-commit)
```

Next step: none; it only informs.

Exit status: 0 (done).

### HARBOR_PIN_NOT_FOUND

When: Dockingbird cloned Harbor to install a commit, and Harbor's repository has no such commit. Nothing of the install was kept; check the commit, or give another with `--harbor-commit`.

```text
Harbor's repository has no commit {commit} (Dockingbird's default).
Check it, or give another one with --harbor-commit SHA.
```

Or:

```text
Harbor's repository has no commit {commit} (the repository's CI pin).
Check it, or give another one with --harbor-commit SHA.
```

Or:

```text
Harbor's repository has no commit {commit} (--harbor-commit).
Check it, or give another one with --harbor-commit SHA.
```

Next step: Check it, or give another one with --harbor-commit SHA.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_INSTALLING

When: A `dockingbird harbor` command needed a Harbor commit that isn't installed yet, and installs it, once per commit: the clone, the packages of Harbor's own lock file, then the checks. Another command installing the same commit is waited for.

```text
Installing Harbor {commit}, once for this commit ... done
```

Or:

```text
Installing Harbor {commit}, once for this commit: {step} ...
```

Or:

```text
Installing Harbor {commit}: waiting for another install of it ...
```

Next step: none; it only informs.

Exit status: 0 (done).

### HARBOR_OUTPUT_LINE

When: One of the last lines a failed step of Harbor's install printed, or one mise printed while it read or installed a repo's tool versions (under a failure's message, and each as it comes when you start with `--verbose`), shown with any control character escaped.

```text
  {printed}
```

Next step: none; it only informs.

Exit status: 0 (done).

### HARBOR_INSTALL_FAILED

When: A step of Harbor's install failed, ran past the install's time bound, or couldn't run (uv missing from your PATH, for one), or the commit's lock couldn't be used: it has a package with no wheel for this computer (the install builds none), or it can't be read. The step's last lines are shown; the commit's install folder was removed, so the next command starts over.

```text
Harbor {commit} wasn't installed: {step} failed with exit status {status}. It printed:
{output}
Nothing of it was kept: run the command again to start over.
```

Or:

```text
Harbor {commit} wasn't installed: {step} failed with exit status {status}.
Nothing of it was kept: run the command again to start over.
```

Or:

```text
Harbor {commit} wasn't installed: {step} was still running when the install's {elapsed} were up.
Nothing of it was kept: run the command again to start over.
```

Or:

```text
Harbor {commit} wasn't installed: {step} couldn't run to its end.
Nothing of it was kept: run the command again to start over.
```

Or:

```text
Harbor can't be installed: uv isn't on your PATH.
Install uv (docs.astral.sh/uv), then run the command again.
```

Or:

```text
Harbor {commit} wasn't installed: it says it is {line}, not {version}.
Give another commit with --harbor-commit SHA.
```

Or:

```text
Harbor {commit} wasn't installed: its lock has {package} {version},
which has no wheel for Python {python} on {platform},
and the install builds no package.
Give another commit with --harbor-commit SHA.
```

Or:

```text
Harbor {commit} wasn't installed: the lock Dockingbird carries
for it isn't the one it was released with.
Install Dockingbird again, then run the command again.
```

Or:

```text
Harbor {commit} wasn't installed: its uv.lock is missing,
too large or not a lock Dockingbird can read.
Give another commit with --harbor-commit SHA.
```

Next step, as the message gives it:

- Nothing of it was kept: run the command again to start over.
- Install uv (docs.astral.sh/uv), then run the command again.
- Give another commit with --harbor-commit SHA.
- Install Dockingbird again, then run the command again.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_COMMIT_UNTESTED

When: Harbor was installed at a commit whose private APIs differ from those Dockingbird's Harbor plugin was tested on. Jobs with the oracle and nop agents run as usual.

```text
Dockingbird's Harbor plugin wasn't tested with Harbor {commit}:
its check found other private APIs; oracle and nop jobs run as usual.
```

Next step: none; it only informs.

Exit status: 0 (done).

### HARBOR_VERSION

When: You ran `dockingbird harbor version`: whether the Harbor commit in use is installed, and the folder it is (or will be) installed in.

```text
Not installed yet: the first harbor command that needs it installs it in {folder}
```

Or:

```text
Installed in {folder}
```

Or:

```text
Installed in {folder}, but Dockingbird's plugin wasn't tested with it
```

Next step: none; it only informs.

Exit status: 0 (done).

### HARBOR_NOT_A_TASK

When: You ran `dockingbird harbor run` or `baseline` in a folder, or named one with `-p`, that has no `task.toml`, so it isn't a Harbor task. Nothing ran.

```text
This isn't a Harbor task: there is no task.toml in {folder}
Run the command in a task's folder, or name one with -p DIR.
```

Next step: Run the command in a task's folder, or name one with -p DIR.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_TASK_INVALID

When: The task's `task.toml` couldn't be used: it is too large, a link, not UTF-8 or not TOML, or a setting Dockingbird reads (the task's name, which Harbor takes only as org/name, its operating system, its timeouts, resources or network modes) isn't of the kind Harbor takes, or its count of cpus or of memory is below zero or more than Docker can take, so no job with it would run anywhere. Nothing ran; the line names the setting, never its value.

```text
This task's task.toml can't be used: its {key} isn't what Harbor takes there.
Fix task.toml, then run the command again.
```

Or:

```text
This task's task.toml wasn't read: it is too large.
Fix task.toml, then run the command again.
```

Or:

```text
This task's task.toml wasn't read: it is a link or not a regular file.
Fix task.toml, then run the command again.
```

Or:

```text
This task's task.toml wasn't read: it isn't UTF-8 text.
Fix task.toml, then run the command again.
```

Or:

```text
This task's task.toml wasn't read: it isn't TOML Dockingbird can read.
Fix task.toml, then run the command again.
```

Next step: Fix task.toml, then run the command again.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_TASK_UNSUPPORTED

When: The task's `task.toml` has steps, or sets its operating system to Windows. Dockingbird runs Harbor tasks of one step on Linux, as the platform's local checks do; run any other with Harbor itself. Nothing ran.

```text
This task's task.toml sets {key}, which Dockingbird doesn't run Harbor tasks
with: it runs single-step Linux tasks, as the platform's local checks do.
Run this task with Harbor itself, outside Dockingbird.
```

Next step: Run this task with Harbor itself, outside Dockingbird.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_NETWORK_POLICY_REFUSED

When: The task's `task.toml` asks, in its `[environment]`, `[agent]`, `[verifier]` or `[verifier.environment]` section, for a network other than public, or turns the internet off. Dockingbird runs Harbor tasks on the public network, as the platform does, and refuses the others before anything runs.

```text
This task's [{section}] sets its network to {mode}; Dockingbird runs
Harbor tasks only on the public network, the platform's default.
Remove that setting from task.toml to run the task as the platform does.
```

Next step: Remove that setting from task.toml to run the task as the platform does.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_TASK_LAYOUT

When: You ran `dockingbird harbor run` or `baseline` on a task folder that Harbor wouldn't run as one task: its `environment` folder, its `instruction.md` or its `tests/test.sh` is missing or is a link, it has an `environment/.env`, which compose would read on this Mac, its `environment/Dockerfile` is a link leading outside that folder, or a `Dockerfile.rego` lies beside it, which Docker's build would read on this Mac as a build policy, or a folder inside it has another `task.toml`, which Harbor would run instead. When the task's verifier runs in a container of its own, built from its `tests` folder, a link in its place, a `.env` in it, a `Dockerfile` in it that is a link leading outside it, or a `Dockerfile.rego` beside that Dockerfile, is refused the same way. Nothing ran.

```text
This task has no {item}, so Harbor wouldn't run it as one task.
Add it, then run the command again.
```

Or:

```text
This task's {item} is a link, which Dockingbird doesn't follow in a task.
Make it a real file or folder, then run the command again.
```

Or:

```text
This task has another task.toml in a sub-folder, so Harbor
would run that task, not this one.
Run the command in that task's own folder, or remove the inner task.toml.
```

Or:

```text
This task has {item}, which compose would read on this Mac
before any container.
Remove it; put the task's variables under [environment] env in task.toml.
```

Or:

```text
This task has {item}, which Docker's build would read on this Mac as a build policy.
Remove it, then run the command again.
```

Next step, as the message gives it:

- Add it, then run the command again.
- Make it a real file or folder, then run the command again.
- Run the command in that task's own folder, or remove the inner task.toml.
- Remove it; put the task's variables under \[environment\] env in task.toml.
- Remove it, then run the command again.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_COMPOSE_REFUSED

When: A compose file of the job (the task's `environment/docker-compose.yaml`, the `tests/docker-compose.yaml` of a verifier that runs in a container of its own, or one you gave with `--extra-docker-compose`) sets something Dockingbird doesn't run: a key outside the ones that keep the task's containers to themselves (`ports`, `volumes` or `privileged`, for example), a build folder outside the file's own folder, a build's Dockerfile that is a link leading outside the file's own folder, or a `.rego` file beside it, the host's or another container's network, a network Dockingbird didn't make, a label of Dockingbird's or compose's, or a build path or label that compose would interpolate (`$`). Nothing ran; the line names where, never the value.

```text
{file} sets {key}, which Dockingbird doesn't allow in a Harbor task.
Remove or change it, then run the command again.
```

Next step: Remove or change it, then run the command again.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_COMPOSE_INVALID

When: A compose file of the job (the task's, the verifier's own or one you gave) couldn't be checked: it is too large, missing, a link, not UTF-8 or not one YAML document, it uses a YAML alias or a YAML tag, it nests deeper than a compose file does, or has something other than what a compose file has where Dockingbird reads it. Nothing ran; the line never shows what the file has.

```text
{file} wasn't read: it is too large.
Fix that file, then run the command again.
```

Or:

```text
{file} wasn't read: it is missing, a link or not a regular file.
Fix that file, then run the command again.
```

Or:

```text
{file} wasn't read: it isn't UTF-8 text.
Fix that file, then run the command again.
```

Or:

```text
{file} isn't one YAML document Dockingbird can read.
Fix that file, then run the command again.
```

Or:

```text
{file} uses a YAML alias, which Dockingbird doesn't read.
Write the aliased value out in full, then run the command again.
```

Or:

```text
{file} uses a YAML tag, which Dockingbird doesn't read.
Write the value without its tag, then run the command again.
```

Or:

```text
{file} can't be checked: what's at {key} isn't what a compose
file has there.
Fix that file, then run the command again.
```

Or:

```text
{file} nests deeper than {count} levels, more than a compose file does.
Flatten it, then run the command again.
```

Next step, as the message gives it:

- Fix that file, then run the command again.
- Write the aliased value out in full, then run the command again.
- Write the value without its tag, then run the command again.
- Flatten it, then run the command again.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_AGENT_UNSUPPORTED

When: You gave `dockingbird harbor run` an agent with `-a` that Dockingbird doesn't run: it runs Harbor's oracle, nop and claude-code agents, since any other needs a key in its environment, which Dockingbird never hands Harbor that way. Nothing ran.

```text
Dockingbird doesn't run Harbor's {agent} agent: it runs {choices}.
Name one of them with -a NAME, or leave -a out to run oracle.
```

Next step: Name one of them with -a NAME, or leave -a out to run oracle.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_ENVIRONMENT_UNSUPPORTED

When: You gave `dockingbird harbor run` an environment with `-e` other than docker. Dockingbird runs Harbor jobs in Docker on this Mac, in its own environment, which labels the job's containers so they are removed afterwards. Nothing ran.

```text
Dockingbird runs Harbor jobs in Docker on this Mac, not in {environment}.
Leave -e out, or give -e docker.
```

Next step: Leave -e out, or give -e docker.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_OPTION_REFUSED

When: You gave `dockingbird harbor run` an option Dockingbird doesn't pass on to Harbor, and nothing ran. Dockingbird passes only the options of Harbor's `run` it knows, and refuses by name the ones that mount folders of this Mac into the task's container (`--mounts`, `--mounts-json`) or replace the environment Dockingbird runs jobs in (`--environment-import-path`); the ones that would run a task or a dataset it hasn't checked (a job config, a dataset, another task or a repository); `--env-file`, which would change the environment it gives Harbor; the ones that change the classes Harbor runs the job with (a plugin, a verifier, a simulated user, environment keywords); the ones that send the job to Harbor Hub or Hugging Face; `--override-gpus` and `--override-tpu`, which would give the container a device of this computer; `--ae` or `--ve` with a key, token, password or other credential in the variable's name, which would land on a command line and in the trial's logs (save it with `dockingbird login` instead); and any option it doesn't know at this Harbor commit. `baseline`, which runs oracle then nop and names both jobs itself, also refuses `-a`, `--agent-import-path` and `--job-name`, and a `-k` that isn't a whole number of one or more. Both `run` and `baseline` also refuse `-k`, `-n`, `--n-concurrent-agents` or `-r` over the count the message names, and more `-m` models than that: a job that big wouldn't finish on this Mac (give a smaller number, or leave the option out). Both also refuse an option that takes a value when it is the last word and no value follows it (`--skill` alone, say): the message names the option as you typed it, and a value after an equals sign, even an empty one (`--skill=`), counts as given. Give the option a value, or leave it out.

```text
Dockingbird doesn't pass {option} to Harbor: it would mount
folders of this Mac into the task's container.
Run the job without it.
```

Or:

```text
Dockingbird doesn't pass {option} to Harbor: it would replace
the environment Dockingbird runs Harbor jobs in.
Run the job without it.
```

Or:

```text
Dockingbird doesn't pass {option} to Harbor: it would run a task
or a dataset Dockingbird hasn't checked.
Run the job without it.
```

Or:

```text
Dockingbird doesn't pass {option} to Harbor: it would change the
environment Dockingbird gives Harbor.
Run the job without it.
```

Or:

```text
Dockingbird doesn't pass {option} to Harbor: it would change the
classes Harbor runs the job with.
Run the job without it.
```

Or:

```text
Dockingbird doesn't pass {option} to Harbor: it would send the
job to Harbor Hub or Hugging Face.
Run the job without it.
```

Or:

```text
Dockingbird doesn't pass {option} to Harbor: it would give the
task's container a device of this computer, which the compose
policy refuses.
Run the job without it.
```

Or:

```text
Dockingbird doesn't pass {option} with a credential in it: it
would land on a command line and in the trial's logs.
Save the credential with dockingbird login, and leave it out of the words.
```

Or:

```text
Dockingbird doesn't know {option} as a harbor run option at this
Harbor commit.
Dockingbird passes only options it knows; see harbor run --help at this commit.
```

Or:

```text
baseline runs oracle then nop and names both jobs itself: it takes no {option}.
Leave it out, or use harbor run.
```

Or:

```text
baseline takes -k as a whole number of attempts, 1 or more.
Give -k N, or leave it out for one attempt.
```

Or:

```text
Dockingbird doesn't pass {option} over {count} to Harbor: a job
that big wouldn't finish on this Mac.
Give it a number up to {count}, or leave it out.
```

Or:

```text
Dockingbird doesn't pass more than {count} models (-m) to
Harbor: a job that big wouldn't finish on this Mac.
Give at most {count} models.
```

Or:

```text
{option} takes a value, and none followed it.
Give it one, or leave it out.
```

Next step, as the message gives it:

- Run the job without it.
- Save the credential with dockingbird login, and leave it out of the words.
- Dockingbird passes only options it knows; see harbor run --help at this commit.
- Leave it out, or use harbor run.
- Give -k N, or leave it out for one attempt.
- Give it a number up to {count}, or leave it out.
- Give at most {count} models.
- Give it one, or leave it out.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_JOB_NAME_INVALID

When: You gave `dockingbird harbor run` a `--job-name` that isn't a job name: lowercase letters, digits and hyphens, starting with a letter or digit, up to the length the message names. Nothing ran.

```text
That --job-name can't be used: a job name is up to {count} lowercase
letters, digits and hyphens, and starts with a letter or digit.
Give another one with --job-name NAME, or leave it out.
```

Next step: Give another one with --job-name NAME, or leave it out.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_RUNNING

When: You ran `dockingbird harbor run` or `baseline`: the job's folder is made and Harbor is about to start. The line names the job, its agent and the folder its results go to; Harbor's own live display follows on the terminal.

```text
Running Harbor job {job} ({agent}): Harbor's own display follows.
Its results go to {folder}
```

Next step: none; it only informs.

Exit status: 0 (done).

### HARBOR_JOB_DONE

When: A job of `dockingbird harbor run` or `baseline` ended: one row for each trial that finished (its name, its agent, its reward, how long it ran and, if it failed, the kind of error), then the job's folder. When a trial hit an error or left no readable result, the message says so and the command exits 1, though Harbor itself exits 0 after such a job. After a Ctrl-C the message says the job was interrupted.

```text
Job {job} ran {count:trial|trials}:
{trials}
Results: {folder}
```

Or:

```text
Job {job} ran {count:trial|trials}; {errors:trial hit|trials hit} an error:
{trials}
Results: {folder}
Read the exception.txt in each errored trial's folder.
```

Or:

```text
Job {job} was interrupted; {count:trial|trials} finished:
{trials}
Results: {folder}
```

Next step, as the message gives it:

- none, where the message only informs
- Read the exception.txt in each errored trial's folder.

Exit status: 0 (done) or 1 (a problem Dockingbird printed), as "When:" says.

### HARBOR_TRIAL_ROW

When: One trial of a Harbor job, in the lists `harbor run`, `baseline` and `harbor results` print: its name, its agent, the reward it earned (`-` when it has none), how long it ran and, when it failed, the kind of error. A trial with no readable result shows `no result`. Whatever the trial's files hold is shown with control characters escaped.

One row of a table; its cells line up with the rows around it.

```text
  {trial}  {agent}  reward {reward}  {elapsed}
```

Or:

```text
  {trial}  {agent}  reward {reward}  {elapsed}  stopped
```

Or:

```text
  {trial}  {agent}  reward {reward}
```

Or:

```text
  {trial}  {agent}  reward {reward}  stopped
```

Or:

```text
  {trial}  no result
```

Next step: none; it only informs.

Exit status: 0 (done).

### HARBOR_LEFTOVERS_REMOVED

When: A Harbor job ended and Dockingbird cleaned up after it: the Docker images the job built are removed, each by its exact id; an image a running container still uses stays; and the containers, networks and volumes the job left behind, if any, are removed too. A later Harbor command that finds what a job left when it ended without cleaning up (it crashed or was killed) says so the same way, naming the job; when what it found belongs to no job it can name, the message says only that a Harbor job ended without cleaning up.

```text
Removed {images:image|images} the job built.
```

Or:

```text
Removed {images:image|images} the job built; {in_use:image|images} in use by a container stayed.
```

Or:

```text
Removed {images:image|images} the job built, and {swept:leftover|leftovers} it left behind.
```

Or:

```text
Removed {images:image|images} the job built, and {swept:leftover|leftovers} it left behind;
{in_use:image|images} in use by a container stayed.
```

Or:

```text
Removed {swept:leftover|leftovers} of Harbor job {job}, which ended without cleaning up.
```

Or:

```text
Removed {swept:leftover|leftovers} of a Harbor job that ended without cleaning up.
```

Next step: none; it only informs.

Exit status: 0 (done).

### HARBOR_IMAGES_NOT_MADE

When: A Harbor job ended, and Docker held images that weren't there when it started but that the job didn't make: another program's or another Dockingbird folder's, a base image the job's task pulled, or another job's. Dockingbird removes only what the job built, so these stay; remove one yourself with `docker image rm` if you no longer need it.

```text
Kept {not_made:image|images} that appeared while the job ran: not made by it.
```

Next step: none; it only informs.

Exit status: 0 (done).

### HARBOR_IMAGE_KEPT

When: Docker refused to remove an image a Harbor job built, for a reason other than a container using it. The message gives Docker's own words and the command that removes the image by hand; nothing else is affected. A later `dockingbird harbor clean` that cannot remove an image says it the same way.

```text
An image the job built couldn't be removed; docker said: {detail}
Remove it yourself: docker image rm {image}
```

Or:

```text
An image a Harbor job built couldn't be removed; docker said: {detail}
Remove it yourself: docker image rm {image}
```

Next step: docker image rm {image}

Exit status: 0 (done).

### HARBOR_BASELINE_OK

When: You ran `dockingbird harbor baseline`: the task's oracle run scored 1 on every attempt and its nop run scored 0, so the task's checks pass.

```text
Both baselines pass: oracle scored 1 and nop scored 0 on every attempt.
```

Next step: none; it only informs.

Exit status: 0 (done).

### HARBOR_BASELINE_FAILED

When: You ran `dockingbird harbor baseline` and it found a problem with the task: a trial that scored other than 1 for the oracle or 0 for nop, shown with the last lines its verifier printed; a trial that hit an error, with the last lines of its output; a trial with no result; a job that didn't run the task Dockingbird checked; or a job that ended with a failing status before a verdict. The command exits 1.

```text
Baseline failed: {trial} ({agent}) scored {reward}, not {wanted}. Its verifier printed:
{output}
Fix the task, then run the command again.
```

Or:

```text
Baseline failed: {trial} ({agent}) scored {reward}, not {wanted}.
Fix the task, then run the command again.
```

Or:

```text
Baseline failed: {trial} ({agent}) hit an error (stopped). Its last lines:
{output}
Fix the task, then run the command again.
```

Or:

```text
Baseline failed: {trial} ({agent}) hit an error (stopped).
Fix the task, then run the command again.
```

Or:

```text
Baseline failed: {trial} ({agent}) left no result.
Fix the task, then run the command again.
```

Or:

```text
Baseline failed: the {agent} job didn't run the task as checked.
Fix the task, then run the command again.
```

Or:

```text
Baseline failed: the {agent} job ended with status {status} before a verdict.
Read Harbor's lines above, then run the command again.
```

Next step, as the message gives it:

- Fix the task, then run the command again.
- Read Harbor's lines above, then run the command again.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_JOB_UNEXPECTED

When: A Harbor job ended and what it left doesn't match what Dockingbird started: Harbor wrote no result for the job, the job ran another task than the one Dockingbird checked, or it ran another number of trials than were planned. The rows still print and the command exits 1.

```text
Job {job} ended without a result.json, so Harbor didn't finish it.
Read {folder} for what Harbor wrote.
```

Or:

```text
Job {job} ran another task than the one Dockingbird checked.
Run the command again; if it repeats, report it:
https://github.com/zeus-fyi/dockingbird/issues
```

Or:

```text
Job {job} ran {found:trial|trials} where {expected:was|were} planned.
Run the command again; if it repeats, report it:
https://github.com/zeus-fyi/dockingbird/issues
```

Next step, as the message gives it:

- Read {folder} for what Harbor wrote.
- https://github.com/zeus-fyi/dockingbird/issues

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_RESOURCES_OVER_VM

When: The task asks for more cpus or more memory than Docker's virtual machine has. Harbor runs the job anyway; the message gives the option that fits the task to the machine.

```text
This task asks for {cpus:cpu|cpus}; Docker's VM has {vm_cpus:cpu|cpus}.
Harbor runs it anyway. To fit the VM, pass --override-cpus {vm_cpus}.
```

Or:

```text
This task asks for {memory} MB of memory; Docker's VM has {vm_memory} MB.
Harbor runs it anyway. To fit the VM, pass --override-memory-mb {vm_memory}.
```

Next step, as the message gives it:

- To fit the VM, pass --override-cpus {vm_cpus}.
- To fit the VM, pass --override-memory-mb {vm_memory}.

Exit status: 0 (done).

### HARBOR_COMPOSE_MISSING

When: You ran a `dockingbird harbor` command that runs a job, and Docker has no compose plugin, which Harbor needs. Nothing ran. Docker Desktop includes it.

```text
Docker's compose plugin isn't available, and Harbor needs it.
Install Docker Desktop (it includes compose), then run the command again.
```

Next step: Install Docker Desktop (it includes compose), then run the command again.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_DOCKER_FAILED

When: A docker command a `dockingbird harbor` command runs failed; the message gives the command and Docker's own words. Before a job starts, nothing ran; when the command that failed was the image listing made once the job's folder exists, that folder stays, empty (under `--json`, with an empty log), as it does when Dockingbird's own record of the job can't be written: `dockingbird harbor clean` removes it when it is under Dockingbird's own jobs folder, and one under a `-o` folder of yours is yours to remove. After a job ran, the listing that finds the images and leftovers to clean up failed, so some may remain: the job's own files are complete, the command exits 1, and `dockingbird harbor clean` removes what is left. `dockingbird harbor clean` can fail the same way while cleaning up, after it removed some leftovers.

```text
docker {command} failed, so nothing ran. Docker said: {detail}
Check Docker Desktop, then run the command again.
```

Or:

```text
docker {command} failed after the job ran, so its images or leftovers may remain.
Docker said: {detail}
Check Docker Desktop, then run: dockingbird harbor clean
```

Or:

```text
docker {command} failed while cleaning up, so some leftovers may remain. Docker said: {detail}
Check Docker Desktop, then run the command again.
```

Next step, as the message gives it:

- Check Docker Desktop, then run the command again.
- dockingbird harbor clean

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_JOB_RUNNING

When: You ran `dockingbird harbor run` or `baseline` with a job name that another `dockingbird harbor` command is still running. Nothing was made and nothing ran.

```text
Job {job} is still running (another dockingbird harbor command started it).
Wait for it, or give another --job-name.
```

Next step: Wait for it, or give another --job-name.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_PROGRAM_MISSING

When: You ran `dockingbird harbor run` or `baseline`, and the Harbor that Dockingbird installed can no longer be started: its folder was changed or broken after the install. Harbor never ran, so nothing ran, and the job's record is ended. The message names the Harbor commit, the folder and what the system said; remove that folder, then run the command again, and Dockingbird installs Harbor again.

```text
Harbor {commit}'s program couldn't be started from {folder}: {detail}
Remove that folder, then run the command again: Harbor is installed again.
```

Next step: Remove that folder, then run the command again: Harbor is installed again.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_JOBS_DIR_MISSING

When: You gave `dockingbird harbor run` or `baseline` a `-o` folder that isn't there, or isn't a folder. Nothing ran: Harbor would make the whole path wherever you can write, and Dockingbird makes no folder outside its own for you. Create the folder, or leave `-o` out to use Dockingbird's own jobs folder.

```text
The jobs folder {folder} isn't there, so nothing ran.
Create it, or leave -o out to use Dockingbird's own jobs folder.
```

Next step: Create it, or leave -o out to use Dockingbird's own jobs folder.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_RECORD_FAILED

When: Dockingbird's own record of a Harbor job (`dockingbird.json` in the job's folder) couldn't be written, or under `--json` its log (`dockingbird.log`) couldn't be opened, or the job's folder itself couldn't be made; the message names the folder and what the system said, and the command exits 1. When it fails before the job starts, nothing ran; the folder that was made stays, empty (under `--json`, with an empty log): `dockingbird harbor clean` removes it when it is under Dockingbird's own jobs folder, and one under a `-o` folder of yours is yours to remove; when the folder itself couldn't be made, nothing is there. When it fails at the end, the job ran and was cleaned up and its rows were printed, but `dockingbird harbor jobs` shows it as stopped; `dockingbird harbor results` still reads Harbor's own files.

```text
Job {job} ran, but its record couldn't be written in {folder}: {detail}
Check the folder, then: dockingbird harbor results {job}
```

Or:

```text
Dockingbird couldn't write in job {job}'s folder {folder}, so nothing ran: {detail}
Its folder stays: fix the cause, then run the command again.
```

Or:

```text
Job {job}'s folder {folder} couldn't be made, so nothing ran: {detail}
Fix the cause, then run the command again.
```

Next step, as the message gives it:

- dockingbird harbor results {job}
- Its folder stays: fix the cause, then run the command again.
- Fix the cause, then run the command again.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_SIGNIN_TOO_SHORT

When: You ran `dockingbird harbor run -a claude-code` with no saved Claude key or token, and the Claude sign-in on this Mac isn't known to last the whole trial. Claude Code in a trial never picks up a sign-in that renews while it runs, so the sign-in must outlast the task's agent timeout, its build timeout, Harbor's setup and a margin, for every wave of its attempts (`-k` attempts, `-n` at a time, each retried `-r` times), with the verifier's timeout and a retry's wait between one run and the next; the message says how long it has and how long the trial needs (or that the trial needs a little more than the sign-in has, when the two would read alike), or that the trial would need it for longer than the bound the message names, or that the task sets no agent timeout, or that a timeout multiplier you gave leaves it no finite time bound, or that the sign-in names no expiry. Nothing ran. Save a long-lived token (`claude setup-token`, then `dockingbird login claude --oauth-token -`) and trials use it.

```text
Your Claude sign-in on this Mac is good for {has}, and this trial needs {needs}.
Save a long-lived token: claude setup-token, then dockingbird login claude --oauth-token -
```

Or:

```text
Your Claude sign-in on this Mac is good for {has}, and this trial
needs a little more than that.
Save a long-lived token: claude setup-token, then dockingbird login claude --oauth-token -
```

Or:

```text
This trial would need your Claude sign-in for more than
{longest}, so no sign-in is known to cover it.
Save a long-lived token: claude setup-token, then dockingbird login claude --oauth-token -
```

Or:

```text
This task sets no finite [agent] timeout_sec, so no sign-in is
known to cover it.
Save a long-lived token: claude setup-token, then dockingbird login claude --oauth-token -
```

Or:

```text
With a timeout multiplier you gave, this trial has no finite
time bound, so no sign-in is known to cover it.
Save a long-lived token: claude setup-token, then dockingbird login claude --oauth-token -
```

Or:

```text
Your Claude sign-in on this Mac has no expiry Dockingbird can
read, so it isn't known to cover this trial.
Save a long-lived token: claude setup-token, then dockingbird login claude --oauth-token -
```

Next step: Save a long-lived token: claude setup-token, then dockingbird login claude --oauth-token -

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_NO_SIGNIN

When: You ran `dockingbird harbor run -a claude-code`, and Dockingbird has neither a saved Claude key or token nor a Claude sign-in to give the trial. Nothing ran. Save a long-lived token (`claude setup-token`, then `dockingbird login claude --oauth-token -`) and run it again.

```text
No Claude sign-in or saved key is stored, so a claude-code trial can't run.
Save a long-lived token: claude setup-token, then dockingbird login claude --oauth-token -
```

Next step: Save a long-lived token: claude setup-token, then dockingbird login claude --oauth-token -

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_COMMIT_UNTESTED_AGENT

When: You ran `dockingbird harbor run -a claude-code` on a Harbor commit that Dockingbird's plugin wasn't tested with, taken from the task repository's pin or Dockingbird's default: the claude-code agent relies on parts of Harbor that may differ there, so it doesn't run. Nothing ran; oracle and nop still run on that commit. To run it anyway, name the commit yourself with `--harbor-commit`.

```text
Dockingbird's Harbor plugin wasn't tested with Harbor {commit}, so a
claude-code trial doesn't run on it.
To run it anyway, name that commit yourself with --harbor-commit SHA.
```

Next step: To run it anyway, name that commit yourself with --harbor-commit SHA.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_LEND_FAILED

When: You ran `dockingbird harbor run -a claude-code`, and Dockingbird couldn't get the Claude sign-in or key for the trial: its store refused, Docker failed, or the answer couldn't be read. Nothing ran; the message gives what was said, never the sign-in itself. When the sign-in's pipe is what failed, the job's folder was made already and stays, with its record ended: `dockingbird harbor clean` removes it when it is under Dockingbird's own jobs folder, and one under a `-o` folder of yours is yours to remove. Check `dockingbird status`, then run the command again.

```text
Dockingbird couldn't get your Claude sign-in for the trial. It said: {detail}
Run dockingbird status, then run the command again.
```

Next step: Run dockingbird status, then run the command again.

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_JOBS

When: You ran `dockingbird harbor jobs`: the Harbor jobs on this Mac, newest first, one row each.

```text
Harbor jobs in {folder}:
{jobs}
```

Next step: none; it only informs.

Exit status: 0 (done).

### HARBOR_JOBS_ROW

When: One job of the list `dockingbird harbor jobs` prints: its name, its task, its agent, whether it is running, done or stopped, how long ago it started and the rewards of its trials. A job folder Dockingbird has no record of (one Harbor made without it) shows only its name and state.

One row of a table; its cells line up with the rows around it.

```text
  {job}  {task}  {agent}  {state}  {ago} ago  {rewards}
```

Or:

```text
  {job}  {state}
```

Next step: none; it only informs.

Exit status: 0 (done).

### HARBOR_NO_JOBS

When: You ran `dockingbird harbor jobs` and no Harbor job has run on this Mac yet, or `dockingbird harbor clean` removed them.

```text
No Harbor jobs yet.
Run one: dockingbird harbor baseline
```

Next step: dockingbird harbor baseline

Exit status: 0 (done).

### HARBOR_JOB_UNKNOWN

When: You ran `dockingbird harbor results` with a name that is no Harbor job on this Mac. The word you typed is shown with control characters escaped.

```text
No Harbor job is named {job}.
See: dockingbird harbor jobs
```

Next step: dockingbird harbor jobs

Exit status: 1 (a problem Dockingbird printed).

### HARBOR_JOB_RESULTS

When: You ran `dockingbird harbor results` for one job: its state, one row for each trial it ran, and its folder.

```text
Job {job} ({state}), {count:trial|trials}:
{trials}
Folder: {folder}
```

Next step: none; it only informs.

Exit status: 0 (done).

### HARBOR_CLEAN_QUESTION

When: You ran `dockingbird harbor clean` on a terminal, without `--yes`: the job folders it would remove (with `--all`, Harbor itself too), each with its size, and the question whether to remove them. Anything but yes keeps them. A job that is still running is named as staying.

```text
These Harbor jobs go:
{jobs}
Remove them? [y/N]
```

Or:

```text
These Harbor jobs and Harbor itself ({size}) go:
{jobs}
Remove them? [y/N]
```

Or:

```text
Harbor itself ({size}) goes; there are no job folders.
Remove it? [y/N]
```

Next step: answer y to go on; anything else is no

Exit status: 0 (done).

### HARBOR_CLEAN_ROW

When: One job folder of the question `dockingbird harbor clean` asks: its name, its size and its state; a job that is still running is named as staying.

```text
{job} ({size}, {state})
```

Or:

```text
{job} ({size}) is running and stays
```

Next step: none; it only informs.

Exit status: 0 (done).

### HARBOR_CLEANED

When: You ran `dockingbird harbor clean` and it removed something: the job folders and the space they freed, what earlier jobs left in Docker (containers, networks, volumes, and what the jobs built), and, with `--all`, Harbor itself.

```text
Removed {count:Harbor job|Harbor jobs} ({freed}).
```

Or:

```text
Removed {count:Harbor job|Harbor jobs} ({freed}) and {swept:leftover|leftovers}.
```

Or:

```text
Removed {count:Harbor job|Harbor jobs} ({freed}) and Harbor itself.
```

Or:

```text
Removed {count:Harbor job|Harbor jobs} ({freed}), {swept:leftover|leftovers} and Harbor itself.
```

Or:

```text
Removed {swept:leftover|leftovers} of earlier Harbor jobs.
```

Or:

```text
Removed {swept:leftover|leftovers} of earlier Harbor jobs and Harbor itself ({freed}).
```

Or:

```text
Removed Harbor itself ({freed}).
```

Next step: none; it only informs.

Exit status: 0 (done).

### HARBOR_SIZES_UNREAD

When: `dockingbird harbor clean` couldn't read the size of some files in a Harbor job's folder or Harbor's install, so the sizes it shows leave them out.

```text
Dockingbird couldn't read the size of some of Harbor's files,
so the sizes shown leave them out.
```

Next step: none; it only informs.

Exit status: 0 (done).

### HARBOR_CLEAN_LEFT

When: `dockingbird harbor clean` couldn't remove a Harbor job's folder, Harbor itself with `--all`, Harbor's cache, something in Harbor's tmp folder or a job's lock file; it is still where the message says, and you can remove it yourself.

```text
Could not remove Harbor job {job}; its folder is kept:
{path}
```

Or:

```text
Could not remove Harbor itself; it is kept in:
{path}
```

Or:

```text
Could not remove Harbor's cache; it is kept in:
{path}
```

Or:

```text
Could not remove an entry of Harbor's tmp; it is kept:
{path}
```

Or:

```text
Could not remove Harbor job {job}'s lock file; it is kept:
{path}
```

Next step: none; it only informs.

Exit status: 0 (done).

### HARBOR_NOTHING_TO_CLEAN

When: You ran `dockingbird harbor clean` and there was no job folder, no leftover and nothing else of Harbor's to remove.

```text
Nothing of Harbor's to clean.
```

Next step: none; it only informs.

Exit status: 0 (done).

### HARBOR_CLEAN_KEPT

When: You ran `dockingbird harbor clean` and some of it was kept. The job folders, and with `--all` Harbor itself when it was among what the question offered, either because there is no terminal to ask on and no `--yes`, or because you answered anything but yes: the command exits 1, and the message gives the space kept in all and, without a terminal, the command that removes it. Or the jobs that are still running, including one that started while the question was open, and with `--all` Harbor itself, which they run from: the command exits 0. Or Harbor itself, because another `dockingbird harbor` command started installing it while the question was open: the command exits 0.

```text
Kept {count:job folder|job folders} ({size}): there is no terminal to ask on.
To remove them without a question: dockingbird harbor clean --yes
```

Or:

```text
Kept {count:job folder|job folders} and Harbor itself ({size}): there is no terminal to ask on.
To remove them without a question: dockingbird harbor clean --all --yes
```

Or:

```text
Kept Harbor itself ({size}): there is no terminal to ask on.
To remove it without a question: dockingbird harbor clean --all --yes
```

Or:

```text
Kept {count:job folder|job folders} ({size}).
```

Or:

```text
Kept {count:job folder|job folders} and Harbor itself ({size}).
```

Or:

```text
Kept Harbor itself ({size}).
```

Or:

```text
Kept {names:and}, still running, and Harbor itself with them.
```

Or:

```text
Kept {names:and}, still running.
```

Or:

```text
Kept Harbor itself: another dockingbird harbor command is installing it.
```

Next step, as the message gives it:

- dockingbird harbor clean --yes
- dockingbird harbor clean --all --yes
- none, where the message only informs

Exit status: 0 (done) or 1 (a problem Dockingbird printed), as "When:" says.

### CLEAN_ALL_HARBOR

When: You ran `dockingbird clean --all`, which asks before it removes anything, and Harbor's folder (its jobs and its install) is among what goes, with its size (at least that size when some of its files couldn't be read). A Harbor job that is still running is named too: it is stopped with the rest.

```text
Harbor's jobs and its install go too: {path} ({size})
```

Or:

```text
Harbor's jobs and its install go too: {path} (at least {size}; some files couldn't be read)
```

Or:

```text
Harbor job {job} is still running; it will be stopped with the rest
```

Next step: none; it only informs.

Exit status: 0 (done).

## The fleet probe

### FLEET_PROBE

When: You ran `dockingbird fleet probe` on a Mac. It reads this Mac's cores and memory, its load against its line, its CPU, memory, swap and GPU, Docker's VM, containers and networks, then how much CPU and memory each category of the load uses, with how many containers or processes it counted. A figure it couldn't read says `unread`. It starts, stops and changes nothing; with `--json` it prints every figure by name on one line, for scripts.

```text
This Mac: {cores:core|cores}, {host_memory} of memory.
Load: {load_one}, {load_five}, {load_fifteen} (line {load_line}).
CPU busy: {cpu_busy}, idle cores: {idle_cores}.
Memory free: {memory_free}, compressed: {compressed}.
Swap used: {swap_used} of {swap_total}.
GPU busy: {gpu_busy}.
Docker cpus: {docker_cpus}, memory: {docker_memory}.
Docker VM resident: {docker_resident}.
Containers running: {running_containers}, in all: {all_containers}.
Networks: {all_networks}.
By category (CPU in % of a core, memory, count):
{categories}
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_PROBE_CATEGORY

When: One row of the load by category that `dockingbird fleet probe` prints: the category, its CPU in percent of one core (400% is four cores), the memory it uses and how many containers or processes it counted. A category with nothing in it shows 0.

One row of a table; its cells line up with the rows around it.

```text
  {category}  {cpu}  {memory_used}  {count}
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_PROBE_UNREAD

When: `dockingbird fleet probe` couldn't read part of what it reads, so it names each such part and why: Docker isn't there or didn't answer, a command took too long or printed too much, a command's output had another shape than the probe reads, the Mac has no graphics accelerator to read, or a command failed. The rest of the screen is what it did read, and the command still ends 0.

```text
Not read: {parts:and}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_PROBE_NOT_MACOS

When: You ran `dockingbird fleet probe` on a computer that isn't a Mac. It reads the programs of macOS only, so it stops before it runs anything.

```text
The fleet probe reads macOS only, not {system}.
Run it on a Mac.
```

Next step: Run it on a Mac.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_PROBE_NO_SYSCTL

When: You ran `dockingbird fleet probe` and the first thing it reads, this Mac's cores, memory, load and swap from `sysctl`, failed: it took too long, printed too much or something the probe doesn't read, or failed outright. Without the cores no other figure has its scale, so the probe stops; the word in parentheses says which.

```text
Couldn't read this Mac's sysctl ({reason}).
The probe has nothing to report.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

## The fleet's home read

### FLEET_HOME

When: You ran `dockingbird fleet read-home`. It reads the Dockingbird home it runs under (the one `DOCKINGBIRD_HOME` names, else the default one) through that home's own `dockingbird status` and, only when Dockingbird is ready there, `dockingbird inbox --all`, then prints the home's folder, its version and whether it is ready, how many agents it has and how many are in each state, what waits in its inbox, and its open questions with the oldest one's age. A figure it couldn't read says `unread`. It starts and stops nothing itself; with `--json` it prints the whole reading on one line, for scripts: every agent with its tool, state, model and effort, and every inbox row.

```text
Home: {home}
Dockingbird {version}, {readiness}.
Agents: {agents}.
{states}
Waiting in the inbox: {inbox_open}.
Open questions: {questions_open}, the oldest: {oldest}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_HOME_STATE

When: One row of the agents by state that `dockingbird fleet read-home` prints: a state, such as working, idle or stopped, and how many of the home's agents are in it. A state no agent is in has no row.

One row of a table; its cells line up with the rows around it.

```text
  {state}  {count}
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_HOME_UNREAD

When: `dockingbird fleet read-home` couldn't read part of the home, so it names each such part and why: it reads the inbox only while Dockingbird is ready in that home (`not-ready`), and a read that took too long, printed too much or something read-home doesn't read, or failed, says so. The rest of the screen is what it did read, and the command still ends 0.

```text
Not read from this home: {parts:and}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_HOME_NO_STATUS

When: You ran `dockingbird fleet read-home` and the first thing it reads, the home's own `dockingbird status`, failed: it took too long, printed too much or something read-home doesn't read, or failed outright, or the program the home records (`program`, written by each start and update) is not an executable file of yours that nobody else can write (`program-invalid`), so nothing ran. The agents and whether the home is ready come from it, so read-home stops without reading the inbox; the word in parentheses says which.

```text
Couldn't read this home's status ({reason}).
Without it there is nothing to report.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_HOME_NO_DISK

When: You ran `dockingbird fleet read-home` with `--disk`. Only `dockingbird fleet probe` reads Docker's disk use, so read-home stops before it reads anything.

```text
dockingbird fleet: --disk is the probe's option, not read-home's.
See: dockingbird fleet -h
```

Next step: dockingbird fleet -h

Exit status: 2 (usage).

## The fleet's metrics

### FLEET_SCRAPE

When: You ran `dockingbird fleet scrape --json`. It reads the Dockingbird home it runs under through that home's own `dockingbird status`, as `dockingbird fleet read-home` does, and renders each running agent's figures in the Prometheus text format, the same text the agent's container serves, under labels that name the home, the agent, its run and its tool. The line names the home, how many agents it has and how many it rendered; the JSON carries every agent with its labels, or none for an agent that isn't running, and the text a line each. Without `--json` the screen is that text alone.

```text
Home: {home}
Agents: {agents}, {rendered} with metrics.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_SCRAPE_NO_STATUS

When: You ran `dockingbird fleet scrape` and it had nothing to render: the home's own `dockingbird status` took too long, printed too much or something scrape doesn't read, or failed outright, or Dockingbird isn't ready in that home (`not-ready`: the home isn't set up, or Dockingbird there is off, of another version or slow to answer), so no agent's figures are current, or the program the home records (`program`, written by each start and update) is not an executable file of yours that nobody else can write (`program-invalid`), so nothing ran. The word in parentheses says which; nothing is printed on stdout.

```text
Couldn't read this home's agents ({reason}).
Without them there are no metrics to print.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_SCRAPE_NO_DISK

When: You ran `dockingbird fleet scrape` with `--disk`. Only `dockingbird fleet probe` reads Docker's disk use, so scrape stops before it reads anything.

```text
dockingbird fleet: --disk is the probe's option, not scrape's.
See: dockingbird fleet -h
```

Next step: dockingbird fleet -h

Exit status: 2 (usage).

## Every agent on every host

### FLEET_HOSTS_ROW

When: One line of `dockingbird fleet hosts` for each host `hosts.toml` in your Dockingbird folder names, in the file's order: its name, how it is reached (`ssh` or `gcloud`) and the ssh destination or the VM. `dockingbird fleet agents --host NAME` reads that host's agents.

```text
{host}: {route} {target}
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_HOSTS_NONE

When: You ran `dockingbird fleet hosts` and `hosts.toml` in your Dockingbird folder names no host, or isn't there, so `dockingbird fleet agents` reads `local`, this computer, alone. `dockingbird fleet hosts set NAME --ssh DEST` adds another host once it answers, or `--gcloud VM --zone ZONE --project PROJECT` in place of `--ssh` for a Compute Engine VM.

```text
No other host is set in {path}.
Add one: dockingbird fleet hosts set NAME --ssh DEST
```

Next step: dockingbird fleet hosts set NAME --ssh DEST

Exit status: 0 (done).

### FLEET_HOSTS_FILE_INVALID

When: `hosts.toml` in your Dockingbird folder, which names the other hosts `dockingbird fleet` reads, has a mistake: a value that isn't right or is missing, a key it doesn't take, a host with both `ssh` and `gcloud` or neither, two hosts with one name, a host named `local`, the name every fleet line gives this computer, text that isn't TOML, or a link, a folder or a file that isn't yours in its place. The message names the file and, where it can, the place, such as `host[2].ssh`, never a value. No host is read until it is fixed. `dockingbird fleet hosts set` refuses the same way, writing nothing, when the entry it would write breaks one of these rules.

```text
{path}: {key} isn't right.
Fix it, then run: dockingbird fleet hosts
```

Or:

```text
{path}: {key} is missing.
Fix it, then run: dockingbird fleet hosts
```

Or:

```text
{path} has a key that isn't host or home.
Fix it, then run: dockingbird fleet hosts
```

Or:

```text
{path}: {key} needs one of ssh and gcloud, and only one.
Fix it, then run: dockingbird fleet hosts
```

Or:

```text
{path}: {key} is another host's name too.
Fix it, then run: dockingbird fleet hosts
```

Or:

```text
{path}: {key} is local, this computer's own name.
Fix it, then run: dockingbird fleet hosts
```

Or:

```text
{path} isn't TOML Dockingbird can read.
Fix it, then run: dockingbird fleet hosts
```

Or:

```text
{path} isn't a regular file of yours, or is too large to read.
Fix it, then run: dockingbird fleet hosts
```

Or:

```text
{path} is a folder, not a hosts file.
Fix it, then run: dockingbird fleet hosts
```

Next step: dockingbird fleet hosts

Exit status: 1 (a problem Dockingbird printed).

### FLEET_HOST_UNKNOWN

When: You gave `dockingbird fleet agents` or `dockingbird fleet attach` a `--host` that `hosts.toml` in your Dockingbird folder doesn't name, or `dockingbird fleet hosts rename` or `forget` a name it doesn't have. `dockingbird fleet hosts` lists the hosts it names, which shows a mistyped name; `dockingbird fleet hosts set NAME --ssh DEST` adds a host it lacks.

```text
No host named {host} in {path}.
See: dockingbird fleet hosts
Add it: dockingbird fleet hosts set {host} --ssh DEST
```

Next step: dockingbird fleet hosts set {host} --ssh DEST

Exit status: 2 (usage).

### FLEET_OPTION_NOT_HERE

When: You gave a `dockingbird fleet` action an option that belongs to another one: `--disk` is the probe's, `--host` is for `agents` and `attach`, `--container` for `attach`, and `attach` takes no `--json`. Nothing is read.

```text
dockingbird fleet: {option} is not an option of {action}.
See: dockingbird fleet -h
```

Next step: dockingbird fleet -h

Exit status: 2 (usage).

### FLEET_HOST_ROW

When: The first line of `dockingbird fleet agents`: how many agents run on `local`, this computer, or on the host `--host` names, and in how many Dockingbird homes, read from that computer's Docker whatever Dockingbird version each home runs. `dockingbird fleet hosts set` adds a host and shows its lines the same way.

```text
{host}: {agents:agent|agents} running in {homes:home|homes}
```

Or:

```text
local: {agents:agent|agents} running in {homes:home|homes}
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_HOME_ROW

When: One Dockingbird home that `dockingbird fleet agents` found on the host: its folder, or `folder not known` when Docker doesn't show it, its version, whether it is running, and how many of its agents run.

```text
  {home} ({profile}): Dockingbird {version}, {coordinator}, {agents_running:agent|agents} running
```

Or:

```text
  {profile}: folder not known, Dockingbird {version}, {coordinator}, {agents_running:agent|agents} running
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_AGENT_ROW

When: One agent that `dockingbird fleet agents` found running on the host: its name, `bus` or `terminal`, and whether it has a screen to open; an agent with no screen opens as its log with a line to send it a message.

```text
    {name}  {mode}  no screen  {activity}
```

Or:

```text
    {name}  {mode}  screen  {activity}
```

Or:

```text
    {name}  {mode}  no screen  {activity} {questions}
```

Or:

```text
    {name}  {mode}  screen  {activity} {questions}
```

Or:

```text
    {name}  {mode}  no screen  unknown: {activity_reason}
```

Or:

```text
    {name}  {mode}  screen  unknown: {activity_reason}
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_ROWS_SKIPPED

When: `dockingbird fleet agents`, or `dockingbird fleet hosts set` as it adds a host, found rows in the host's Docker listing that it couldn't read, such as a container of another shape or an agent that stopped while it read, and says how many; the host is `local` for this computer. The rest of what it printed is what it could read.

```text
{skipped:row|rows} of {host}'s Docker listing could not be read.
```

Or:

```text
{skipped:row|rows} of local's Docker listing could not be read.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_HOST_NOT_READ

When: `dockingbird fleet agents` couldn't read the host, or `local`, this computer's own Docker: ssh or gcloud couldn't reach it, its Docker failed or took too long, it printed something else than Docker's listings, or this computer has no Docker or no `gcloud`. The line ends with the error that ssh, gcloud or Docker printed, or a word that says which. `dockingbird fleet hosts set` reads a host the same way before it adds it, and saves nothing when it can't.

```text
Couldn't read {host}: {detail}
```

Or:

```text
Couldn't read local's Docker: {detail}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_HOSTS_SET

When: You ran `dockingbird fleet hosts set` and the host answered: its Docker and its Dockingbird homes were read and shown as `dockingbird fleet agents --host NAME` shows them, and its entry was written at the end of `hosts.toml` in your Dockingbird folder. A comment in a file you wrote by hand is lost on the first write; its hosts and homes are kept.

```text
{host}: {route} {target}, saved in {path}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_HOSTS_UPDATED

When: You ran `dockingbird fleet hosts set` with a name `hosts.toml` already gives a host, and the host answered: its route is replaced, and its `[[host.home]]` tables, its place in the file and a gcloud program you named for it by hand while it stays on gcloud are kept. Moving it to `--ssh` drops that program with the other gcloud settings.

```text
{host}: {route} {target}, updated in {path}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_HOSTS_RENAMED

When: You ran `dockingbird fleet hosts rename OLD NEW`: the host's entry in `hosts.toml` is now under the new name, with its homes and its place in the file. Swarm definitions and fleet pool records that name the old name are not changed; change them where they name it.

```text
{old} is now {host} in {path}.
Swarm definitions and pool records that name {old} are not changed.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_HOSTS_FORGOTTEN

When: You ran `dockingbird fleet hosts forget NAME`: the host's entry and its homes are removed from `hosts.toml` in your Dockingbird folder, and every other entry is kept as it was. Nothing on the host itself changes.

```text
{host} is forgotten: its entry is removed from {path}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_HOSTS_NAME_INVALID

When: You gave `dockingbird fleet hosts set` or `dockingbird fleet hosts rename` a name a host can't have: a host's name is lowercase letters, digits and dashes, starting with a letter or a digit, at most as many characters as the message says, so every fleet line shows it whole. Nothing was read or written.

```text
{word} isn't a host name: lowercase letters, digits and dashes,
at most {count} characters.
```

Next step: none; it only informs.

Exit status: 2 (usage).

### FLEET_HOSTS_LOCAL_FIXED

When: You gave `dockingbird fleet hosts set` or `dockingbird fleet hosts rename` the name `local` for a host of `hosts.toml`, or `dockingbird fleet hosts add` the name `local` for a fleet pool host. `local` is every computer's own name in the fleet's lines, so no other host may take it. Nothing was read or written.

```text
local is this computer's own name: pick another for the host in {path}.
```

Or:

```text
local is this computer's own name: pick another for the pool host.
```

Next step: none; it only informs.

Exit status: 2 (usage).

### FLEET_HOSTS_NAME_TAKEN

When: You ran `dockingbird fleet hosts rename OLD NEW` with a new name `hosts.toml` already gives a host, or the old name itself. Pick a name no host of the file has; nothing was written.

```text
{name} is already a host in {path}.
```

Next step: none; it only informs.

Exit status: 2 (usage).

### FLEET_HOSTS_IN_USE

When: You ran `dockingbird fleet hosts rename` or `forget` for a host that the fleet pool your Dockingbird folder's `fleet.toml` connects to still lists. A host has one name in your hosts file and in the pool, so drain it and remove it from the pool first, then rename or forget it here. Nothing was written.

```text
{host} is in the fleet pool: drain and remove it there first.
See: dockingbird fleet hosts drain {host}
```

Next step: dockingbird fleet hosts drain {host}

Exit status: 1 (a problem Dockingbird printed).

### FLEET_HOSTS_ROUTE_NEEDED

When: You ran `dockingbird fleet hosts set` without one way to reach the host: give `--ssh` with a destination your own ssh reaches, or `--gcloud` with a Compute Engine VM's name and its `--zone` and `--project`, and not both. Nothing was read or written.

```text
dockingbird fleet hosts set needs one route: --ssh DEST, or --gcloud VM
with --zone ZONE and --project PROJECT.
See: dockingbird fleet -h
```

Or:

```text
dockingbird fleet hosts set --gcloud VM needs --zone ZONE and --project PROJECT.
See: dockingbird fleet -h
```

Next step: dockingbird fleet -h

Exit status: 2 (usage).

### FLEET_HOSTS_BUSY

When: Another `dockingbird fleet hosts set`, `rename` or `forget`, from a terminal or the GUI, was changing `hosts.toml` in your Dockingbird folder at the same moment, so this one stopped before it wrote anything. Run it again.

```text
Another dockingbird command is changing {path}. Try again.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_HOSTS_NOT_REACHED

When: You ran `dockingbird fleet hosts set` and Dockingbird couldn't read the host through the route you gave, with the read `dockingbird fleet agents --host NAME` makes: ssh or gcloud couldn't reach it, it gave no answer in time, its Docker didn't answer as Docker does, or this computer has no `gcloud`. Nothing was saved. The message ends with the error that ssh, gcloud or Docker printed, and over ssh or gcloud gives the command to try the host yourself.

```text
Couldn't reach {host} over ssh {target}: {detail}
Nothing was saved. Try it yourself first: ssh {target} docker version
If Docker is installed there but that login's PATH lacks it, add --path PATH
(and --docker-host URL for Docker Desktop's socket), then run this again.
```

Or:

```text
Couldn't reach {host}, the Compute Engine VM {target}: {detail}
Nothing was saved. Try it yourself first, with the VM's --zone and --project:
gcloud compute ssh {target} -- docker version
A stopped VM must be started first.
```

Or:

```text
No gcloud on this computer to reach {host} with: {detail}
Nothing was saved. Install the Google Cloud SDK, or name its gcloud in
{path} as gcloud_program, then run this again.
```

Or:

```text
{host} ({route} {target}) gave no answer in time: {detail}
Nothing was saved. Check that it is up and reachable, then run this again.
```

Or:

```text
{host} ({route} {target}) answered, but not as a Docker host would: {detail}
Nothing was saved. Check Docker on {host} yourself, then run this again.
```

Next step, as the message gives it:

- ssh {target} docker version
- gcloud compute ssh {target} -- docker version
- none, where the message only informs

Exit status: 1 (a problem Dockingbird printed).

### REMOTE_HOME_NEEDS_HOST

When: You gave `--home` to `dockingbird inspect`, `status` or `swarm` without `--host`. A home's folder names a home on another computer, so the command needs that computer's name from `hosts.toml` too.

```text
dockingbird {command}: --home PATH names a home on another host: give --host NAME too.
See: dockingbird fleet hosts
```

Next step: dockingbird fleet hosts

Exit status: 2 (usage).

### REMOTE_HOME_INVALID

When: You gave `--home` a word that isn't a folder's full path, such as a relative path, an empty one, one with a control character or one too long. Give the home's folder as `dockingbird fleet agents --host NAME` lists it.

```text
dockingbird {command}: --home takes the home's absolute folder path,
as dockingbird fleet agents --host prints it; {home} is not one.
```

Next step: none; it only informs.

Exit status: 2 (usage).

### REMOTE_HOST_NOT_READ

When: You ran `dockingbird inspect`, `status` or `swarm` with `--host`, and that computer gave no answer Dockingbird can show: ssh or gcloud couldn't reach it, the command took too long or printed too much, it failed there without saying why, or it printed something else than Dockingbird's answer. The line ends with the error that ssh, gcloud or that computer printed, or a word that says which.

```text
Couldn't reach {host} to run Dockingbird: {detail}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### REMOTE_NO_PROGRAM

When: You ran a command with `--host`, and that computer has no `dockingbird` where its shell looks. Put Dockingbird on that computer's `PATH`, or name the home's own program in `hosts.toml` with a `[[host.home]]` table.

```text
No Dockingbird program on {host} ({program}): put it on that host's PATH,
or name the home's program in a [[host.home]] table of {path}.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### REMOTE_OLDER

When: You ran a command with `--host`, and the Dockingbird on that computer doesn't know the command, its action or one of its options: it is older than this one. Update it there; the line ends with what it said.

```text
The Dockingbird on {host} ({program}) does not know this command: update it there. It said: {detail}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### REMOTE_ROWS_SKIPPED

When: A command you ran with `--host` answered with lines that a newer Dockingbird on that computer wrote and this one can't show. The rest of its answer is shown; update this Dockingbird to see them.

```text
{host}: {skipped:row|rows} of a newer Dockingbird not shown; update this one.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_ATTACH_NO_CONTAINER

When: You ran `dockingbird fleet attach` without `--container`. It opens one agent by its container's full id, which `dockingbird fleet agents` lists.

```text
dockingbird fleet attach needs --container ID.
See: dockingbird fleet agents
```

Next step: dockingbird fleet agents

Exit status: 2 (usage).

### FLEET_ATTACH_BAD_CONTAINER

When: You gave `dockingbird fleet attach` a `--container` that isn't a container's full id, 64 letters and digits as `dockingbird fleet agents --json` lists it. Nothing is read.

```text
dockingbird fleet attach: {container} is not a container id.
See: dockingbird fleet agents
```

Next step: dockingbird fleet agents

Exit status: 2 (usage).

### FLEET_ATTACH_NOT_A_TERMINAL

When: `dockingbird fleet attach` ran without a terminal: its input or output went to a file or a pipe. It shows the agent's screen, or its log with a line to type into, so it needs one; the GUI runs it in a pane of its own when you click the agent.

```text
dockingbird fleet attach needs a terminal: run it in Terminal,
or click the agent in the GUI.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_ATTACH_GONE

When: `dockingbird fleet attach` read the host and no agent runs in that container any more: it ended or was stopped since the list was read. Nothing is opened, and nothing is sent to it.

```text
No agent runs in container {short} on {host} now.
```

Or:

```text
No agent runs in container {short} on this computer now.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_ATTACHING

When: `dockingbird fleet attach` opens the agent's own screen, on its own host, through Docker's attach. Ctrl-\] then Ctrl-\\ leaves it running; the agent goes on either way.

```text
Opening {name} on {host}. Ctrl-] then Ctrl-\ leaves it running.
```

Or:

```text
Opening {name} on this computer. Ctrl-] then Ctrl-\ leaves it running.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_ATTACH_FAILED

When: `dockingbird fleet attach` couldn't start the program that opens the agent: Docker, `ssh` or `gcloud`, or the home's own `dockingbird` that sends a message. The line ends with the system's words.

```text
Couldn't start {program}: {reason}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_FOLLOWING

When: `dockingbird fleet attach`, or a click in the GUI, opened an agent that has no screen, such as a bus agent of a home before Dockingbird 0.4.4: you see its log as it grows, and each line you type and send with Enter goes to the agent as a message. Ctrl-C closes the view; the agent goes on.

```text
{name} has no screen: this is its log as it grows.
Type a message and press Enter to send it to {name}. Ctrl-C closes this view.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_FOLLOW_ENDED

When: The log of the agent you opened with `dockingbird fleet attach` ended. When it says the agent no longer runs, its container stopped. When it says the log stopped, the agent may still run: the connection to its host closed, or Docker failed, and the line ends with the error that ssh, gcloud or Docker printed. Open the agent again to follow its log; a line you type is sent only if the agent still runs.

```text
{name}'s log ended: it no longer runs.
```

Or:

```text
{name}'s log stopped: {detail}
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_SEND_EMPTY

When: You pressed Enter on an empty line in the view of an agent with no screen. Nothing is sent; type a message first.

```text
Nothing to send: type a message, then press Enter.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_SEND_NO_PROGRAM

When: A message you type in the view of an agent with no screen is sent by that home's own `dockingbird`, which `hosts.toml` in your Dockingbird folder must name: a `[[host.home]]` under the agent's host with the home's `path` and its `program`, or a `[[home]]` for a home on this computer. Add it; the next line you type uses it.

```text
Can't send from here: {path} names no program for {home}.
Add that home's own dockingbird under its host as [[host.home]] with
path and program, or as [[home]] on this computer.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_SEND_NO_HOME

When: Docker doesn't show the folder of this agent's home: that home's Dockingbird no longer runs there, or the folder Docker shows isn't that home's. So `dockingbird fleet attach` can't name that home's own `dockingbird` to send your message with, and nothing is sent.

```text
Can't send from here: {name}'s home folder is not known.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_SENT

When: The line you typed in the view of an agent with no screen went to the agent, through its home's own `dockingbird send`.

```text
Sent to {name}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_SEND_FAILED

When: The home's own `dockingbird send` didn't take the line you typed, or didn't answer in time. The line ends with the error it, `ssh` or `gcloud` printed. Nothing is sent again by itself: type the line again to send it.

```text
The send to {name} did not go through: {detail}
```

Or:

```text
The send to {name} gave no answer in time.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_SEND_NOT_TEXT

When: A line you typed in the view of an agent with no screen is not text in your terminal's encoding: some of it was typed or pasted in another one, such as Latin-1 on a UTF-8 terminal. It is not sent, and the view goes on: type the line again in your terminal's encoding.

```text
Not sent: that line is not {encoding} text.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_VIEW_NOT_WRITTEN

When: You closed the view of an agent with no screen, and its log was stopped, but the last of what the view had to show could not be written where its output or its error output goes, such as a file on a full disk. The line ends with the system's words. A closed pane is not this: nothing is there to show anything to. Make room where the output goes, or send it elsewhere, and open the agent again.

```text
{name}'s view could not write its output: {detail}
```

Or:

```text
{name}'s view could not write its error output: {detail}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_VIEW_NOT_READ

When: The view of an agent with no screen could not read the terminal you type in, for a reason other than a closed pane, so it stopped the agent's log and closed. The line ends with the system's words. The agent goes on: open it again from a terminal that works.

```text
{name}'s view could not read its input: {detail}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_OPTION_NEEDED

When: You ran a `dockingbird fleet` scheduler action without an option it cannot do without: `hold` needs `--reason`, `set` needs `--priority`, and `hosts add` needs `--os`, `--cores`, `--memory` and `--line`. Nothing is read; `dockingbird fleet -h` shows each action's options.

```text
dockingbird fleet: {action} needs {option}.
See: dockingbird fleet -h
```

Next step: dockingbird fleet -h

Exit status: 2 (usage).

### FLEET_CONFIG_INVALID

When: A `dockingbird fleet` scheduler action reads `fleet.toml` in your Dockingbird folder first: the fleet database's `host` and the `role` you connect as, with an optional `port`, `database`, `password` and `project` (the project the owner's own leases count against). It isn't there, isn't a file only you can read, isn't TOML, or has a key that is missing, unknown or wrong; the message names the key, never its value. Fix the file and run the command again.

```text
{path}: {key} isn't right.
Fix it, then run the command again.
```

Or:

```text
{path} isn't there: it names the fleet database and your role.
Fix it, then run the command again.
```

Or:

```text
{path}: {key} is missing.
Fix it, then run the command again.
```

Or:

```text
{path}: {key} isn't one of its keys.
Fix it, then run the command again.
```

Or:

```text
{path} isn't TOML Dockingbird can read.
Fix it, then run the command again.
```

Or:

```text
{path} isn't a file only you can read, or is too large to read.
Fix it, then run the command again.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_DB_UNREACHABLE

When: The fleet database `fleet.toml` names did not answer a `dockingbird fleet` action in time, refused the connection before asking for the password, dropped it, or ended it while restarting or too busy: the computer it runs on may be asleep or restarting, or its access rules may not list this computer. The line names the role tried and why the connection failed. Nothing changed, and the command ends 69. Run it again once the database answers.

```text
The fleet database at {host} did not answer within {seconds} s.
```

Or:

```text
The fleet database at {host} did not answer {role} within {seconds} s: {error}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_DB_REFUSED

When: The fleet database `fleet.toml` names answered a `dockingbird fleet` action and refused it: it turned down the login of the role `fleet.toml` names (a wrong password, or a role or database it doesn't have), or answered with an error code once connected. Nothing changed, `fleet run` didn't run its command, and the command ends 78. Correct `fleet.toml`, or the database's roles, and run it again.

```text
refused: the fleet database at {host} turned down the login of {role} (fleet.toml): {error}
```

Or:

```text
refused: the fleet database at {host} answered {role} (fleet.toml) with error {code}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_NOT_PERMITTED

When: The fleet database refused what you asked as the role `fleet.toml` names: a project's role queues and controls its own workloads, and only the fleet's owner changes hosts, lines or policies. Nothing changed.

```text
refused: {role} is not allowed to do this
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_REFUSED

When: A `dockingbird fleet` action refused a value: a swarm definition's field and the rule it breaks, or an option of `fleet hosts add` or `fleet hosts policy` (a gate line, a share above what the host's Docker has, an agent cap above the most a home takes). Nothing changed; fix the value and run the command again.

```text
refused: {field}: {rule}
```

Or:

```text
refused: {field}: above Docker's {millicores} millicores
```

Or:

```text
refused: {field}: above Docker's {mib} MiB
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_NOT_FOUND

When: You named a workload or a host the fleet database doesn't show your role: no such id or name, or a workload of another project, which your role cannot see. `dockingbird fleet queue` lists what it sees.

```text
refused: no workload {id}
```

Or:

```text
refused: no host {id}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_NOT_NOW

When: You asked a control of a workload in a state it doesn't apply to, such as pausing one that isn't running. The message names the states it applies to. Nothing changed.

```text
refused: {id} is {state}; {action} applies to {allowed}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_DONE_NEVER_STARTED

When: You asked `dockingbird fleet done` to end a swarm that is admitted, or interrupted, before any of its agents started: there is no team to end. Nothing changed; `dockingbird fleet cancel` ends it.

```text
refused: {id} is {state} and no agent of it ever started; cancel applies
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_DONE_HOST_NOT_LIVE

When: You asked `dockingbird fleet done` to end an interrupted swarm whose host is stale, stopped or no longer in the pool: nothing there can stop its agents after their running turns. Nothing changed; `done` applies while the host is live, and `dockingbird fleet cancel` ends the swarm now.

```text
refused: {id} is interrupted and its host {host} is {liveness};
done applies while the host is live; cancel ends it now
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_DONE_OTHER_HOLD

When: You asked `dockingbird fleet done` to end a held swarm whose hold is not the one for no agents (yours, or a start the fleet refused): it is not a team that lost its agents. Nothing changed; `dockingbird fleet cancel` applies.

```text
refused: {id} is held ({reason}); done applies to a hold for no agents; cancel applies
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_LEASE_CANCEL_ONLY

When: You asked a lease, a command `dockingbird fleet run` runs under its reservation, to pause, hold, resume or end as a team does; a lease takes `cancel` only, which interrupts its command. Nothing changed.

```text
refused: {id} is a lease; cancel applies
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_FILE_UNREADABLE

When: The swarm definition you gave the fleet is at a path that isn't a file you can read. Nothing was queued.

```text
refused: not a file you can read: {path}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_HOST_STILL_HAS

When: You asked `dockingbird fleet hosts remove` to take out a host that a workload is still reserved on or pinned to; the message names them. Cancel them, or let them end, then remove the host.

```text
refused: {host} still has {names}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_SUBMITTED

When: The fleet queued your swarm: its id, and its place in the queue, which the fleet admits by priority, then age. When your project queued the same key before, the answer is that first swarm and its state, and nothing new is queued.

```text
{id} pending, position {position}
```

Or:

```text
{id} {state}: the same key came before
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_STATE_NOW

When: A control of a workload took effect: the state it entered, and the agents still working, each of which stops after its running turn, never during it.

```text
{id} {state}
```

Or:

```text
{id} {state}; still working: {names}
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_RETIRE_DONE

When: `dockingbird fleet retire` asked an agent of a running swarm to retire: it stops once its running turn ends, never during it, and its share goes back to the pool; one that never started retires at once.

```text
{id} running: {name} retires once its running turn ends
```

Or:

```text
{id} running: {name} retires once its running turn ends; still working: {names}
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_RETIRE_REFUSED

When: `dockingbird fleet retire` or `fleet replace` refused before changing anything: the swarm is not running, it has no agent of that name, the agent neither runs nor waits to start, or retiring it would take its role below its minimum. Check the name with `dockingbird fleet queue`.

```text
refused: {name}: {field}: {rule}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_ADD_DONE

When: `dockingbird fleet add` added agents to a running swarm under their role's next names; each starts, is briefed and is named to the others once its host has room for it.

```text
{id} running: added {names}; each starts once its host has room
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_REPLACE_DONE

When: `dockingbird fleet replace` asked an agent to stop once its running turn ends and start again by its name, its conversation kept; with `--fresh`, a new agent of its role takes its place under the next name.

```text
{id} running: {name} starts again once its running turn ends
```

Or:

```text
{id} running: {name} retires once its running turn ends, and {new} starts in its place
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_ASSIGN_DONE

When: `dockingbird fleet assign` set who reviews and who tests an agent of a running swarm; an option you left out kept its agent. At its next check, the swarm's host tells the agent and the agents you moved its work from and to.

```text
{id}: {name} is reviewed by {reviewer} and tested by {tester};
its host tells {name} and the agents it moved from and to at its next tick.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_ASSIGN_REFUSED

When: `dockingbird fleet assign` refused before changing anything: the swarm is not running, it has no agent of that name, or the reviewer or tester you named is no agent of the swarm, has retired or is retiring, died, or is the agent itself. Check the names with `dockingbird fleet queue`.

```text
refused: assignment of {name}: {field}: {rule}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_PRUNE_DONE

When: `dockingbird fleet prune` queued one prune job for a done or cancelled swarm: its host's worker deletes each of its agents whose container has stopped, and never a running one.

```text
Queued the prune of {id} as job {job_id}.
Its host's worker deletes each of its agents whose container has stopped.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_PRUNE_REFUSED

When: `dockingbird fleet prune` refused before changing anything: `--merged` was not a full commit id, or the workload is not a swarm, is not done or cancelled, or never ran.

```text
refused: prune of {id}: {field}: {rule}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_PRIORITY_NOW

When: `dockingbird fleet set --priority` changed a workload's priority; it keeps its place by age, and its next admission uses the new priority.

```text
{id} priority {priority}
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_WHY_STATE

When: `dockingbird fleet why` of a workload that isn't waiting: its state, the host it is on, or why it is held; or of a waiting one that the fleet hasn't weighed yet, or that no host of the pool can take.

```text
{id} is {state}
```

Or:

```text
{id} is held: {reason}
```

Or:

```text
{id} is {state} on {host}
```

Or:

```text
{id} is pending; no pass has weighed it yet
```

Or:

```text
{id}: no host of the pool can take it
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_WHY_HOST

When: `dockingbird fleet why` of a waiting workload: for each host of the pool, the first thing that keeps the workload off it, with its figures: a gate line past its bound, what the host has against what the workload needs, a home's room, a lease of the same kind running there, or a home that links no checkout of the swarm's repository, as of the host's last sample.

```text
{host}: {hold}
```

Or:

```text
{host}: {hold}, {figure} {reading}, bound {line_bound}
```

Or:

```text
{host}: {hold}, {figure} unread, bound {line_bound}
```

Or:

```text
{host}: {hold}, has {have} millicores, needs {need}
```

Or:

```text
{host}: {hold}, has {have} MiB, needs {need}
```

Or:

```text
{host}: {hold} in {home}, room for {have}, needs {need}
```

Or:

```text
{host}: {hold}, a {kind} lease runs there
```

Or:

```text
{host}: the home {home} links no checkout of the repository, as of the host's last sample
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_LEDGER_ROW

When: `dockingbird fleet ledger` shows a swarm's ledger, one line per commit, newest first: who wrote it, which reviewer approved it and when, and its test result, which tester sent it and when, each time in UTC. `none` stands for an approval or a test line not seen yet.

```text
{sha} by {author}: approved by {reviewer} at {approved_at}; tested {result} by {tester} at {tested_at}
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_LEDGER_EMPTY

When: `dockingbird fleet ledger` of a workload for which no reviewer's approval and no tester's result has been seen yet.

```text
{id}: no approved or tested row yet
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_QUEUE_HOST

When: `dockingbird fleet queue` shows each host of the pool: whether it is live and drained, whether it takes swarms, how old its last sample is, its cores and memory reserved against what it may reserve, the load of everything the fleet didn't start, and each gate line with its value, its colour and its bounds.

```text
{host}: {liveness}, {policy}, sample {age} old
  cores: {reserved_millicores} of {millicores} millicores reserved, {foreign_millicores} foreign
  memory: {reserved_mib} of {mib} MiB reserved, {foreign_mib} foreign
  lines: {lines}
```

Or:

```text
{host}: {liveness}, {policy}, no sample yet
  cores: {reserved_millicores} of {millicores} millicores reserved, {foreign_millicores} foreign
  memory: {reserved_mib} of {mib} MiB reserved, {foreign_mib} foreign
  lines: {lines}
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_QUEUE_WORKLOAD

When: `dockingbird fleet queue` shows each workload not yet ended, in the order the fleet admits them: its project, kind, priority, state and age, the cores, memory and agents it needs, and the host it is on, why it is held, or what keeps it waiting first.

```text
{id} {project} {kind} {priority} {state}, {age} old, needs {need_millicores} millicores, {need_mib} MiB, {agents} agents
```

Or:

```text
{id} {project} {kind} {priority} held, {age} old, needs {need_millicores} millicores, {need_mib} MiB, {agents} agents: {reason}
```

Or:

```text
{id} {project} {kind} {priority} {state}, {age} old, needs {need_millicores} millicores, {need_mib} MiB, {agents} agents: {hold} on {host}
```

Or:

```text
{id} {project} {kind} {priority} {state} on {host}, {age} old, needs {need_millicores} millicores, {need_mib} MiB, {agents} agents
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_QUEUE_WORKING

When: Under a workload of `dockingbird fleet queue`: its agents still working.

```text
  still working: {names}
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_QUEUE_AGENT_EVENT

When: Under a swarm of `dockingbird fleet queue`: its agents' latest deaths, recoveries and lost processes, the newest first: an agent killed at its memory limit, one started again after its last turn failed, or one that lost a process at its memory limit and keeps working.

```text
  {name} died, {age} ago
```

Or:

```text
  {name} died, killed at its {mib} MiB memory limit, {age} ago
```

Or:

```text
  {name} recovered, {age} ago
```

Or:

```text
  {name} lost a process at its memory limit and keeps working, {age} ago
```

Or:

```text
  older agent events not shown
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_NO_CHECKOUT

When: `dockingbird fleet why` or `fleet queue` of a swarm whose start was held: its home has no checkout of the swarm's repository on its branch, or more than one, or the checkout its agents started in is no longer linked there or left the branch; or, where the home's `clones` folder in `hosts.toml` lets the fleet fetch the branch into a clone of its own, the home links no checkout of the repository with an `origin` to fetch from, or making that clone or fetching into it failed, with git's last line or the folder's error. The fleet never moves or guesses a checkout. Put it right, then release the swarm.

```text
No checkout of {repo} on branch {branch} is linked in the home {home} on {host}.
Link one there, then: dockingbird fleet release {id}
```

Or:

```text
{count} checkouts of {repo} on branch {branch} are linked in the home {home} on {host}.
A start needs exactly one: keep one, then: dockingbird fleet release {id}
```

Or:

```text
The checkout {folder} this swarm started in is no longer linked in the home {home} on {host}.
Link it there again, then: dockingbird fleet release {id}
```

Or:

```text
The checkout {folder} of this swarm, in the home {home} on {host}, is no longer on branch {branch}.
Put it back on {branch}, then: dockingbird fleet release {id}
```

Or:

```text
The home {home} on {host} links no checkout of {repo} to fetch branch {branch} from.
Link one checkout of {repo} there, on any branch, then: dockingbird fleet release {id}
```

Or:

```text
Fetching {repo} on branch {branch} into {folder}, for the home {home} on {host}, failed: {git}
Fix it (is the branch pushed? can the host's git reach the remote?), then: dockingbird fleet release {id}
```

Next step: dockingbird fleet release {id}

Exit status: 0 (done).

### FLEET_QUEUE_COMMAND

When: Under a lease of `dockingbird fleet queue`: the command its caller runs under it, as it was recorded, stripped of control characters; the fleet never runs it.

```text
  runs: {command_line}
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_QUEUE_EMPTY

When: `dockingbird fleet queue` found no host in the pool and no workload your role can see.

```text
The pool has no host and the queue no workload.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_HOST_NOW

When: A `dockingbird fleet hosts` verb took effect: the state the host entered, with `draining` when it takes nothing new, or `removed`.

```text
{host} {liveness}
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_RUN_NO_LEASE

When: `dockingbird fleet run` could not reach the fleet database, so it runs your command without a lease, as checks ran before the fleet scheduler: no reservation, no ceiling, and its own exit status. The line names the database, the role tried and why the connection failed.

```text
fleet: no answer from the database at {host} for {role} within {seconds} s: {error}; running without a lease
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_RUN_NOT_ADMITTED

When: `dockingbird fleet run` waited its whole `--wait` for a host to take the lease, and none did. The line names what kept it off each host. The lease is cancelled and the command never ran.

```text
lease not admitted within {wait}: {blocked_by}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_LEASE_NO_PROJECT

When: `dockingbird fleet run` as the owner's role, whose `fleet.toml` names no project: a lease counts against a project, and the owner's role has none of its own. Add `project = "NAME"` to `fleet.toml` and run it again; nothing was recorded.

```text
refused: fleet.toml names no project for {role}'s leases
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_RUN_BOUND

When: The command `dockingbird fleet run` ran was still running at the lease's `--bound`: it was interrupted, then stopped if it did not end, and `fleet run` ends 124.

```text
lease bound reached; CMD interrupted
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_RUN_CANCELLED

When: The lease `dockingbird fleet run` held was cancelled while its command ran, so the command was interrupted; `fleet run` ends with the command's own exit status.

```text
lease {id} cancelled; CMD interrupted
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_RUN_ENDED

When: The lease `dockingbird fleet run` asked for ended before a host took it (cancelled, or past its wait), so the command never ran.

```text
lease {id} is {state}; CMD did not run
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_RUN_NO_SCOPE

When: On Linux, `dockingbird fleet run` keeps its command to the lease's cores and memory with `systemd-run`, which isn't on this computer: the command runs under its lease with no such ceiling.

```text
{program} isn't here: CMD runs with no cores or memory ceiling
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_HOST_POLICY

When: `dockingbird fleet hosts policy` changed a host's policy: whether it takes swarms, its agent cap per home and its gate lines with their bounds.

```text
{host}: {policy}, agent cap {cap}, lines {lines}
```

Next step: none; it only informs.

Exit status: 0 (done).

## Toolchains

### TOOLCHAIN_SUMMARY

When: You started an agent in a repo. The first line names the tool versions the repo's own files ask for, as mise resolves them, each with the file that names it, or `locked` when `mise.lock` names it; while mise reads the repo, it says it is checking, with the time so far. A repo that names no version gets the image's versions, and so does a start with `--no-toolchain`.

```text
Toolchain for {repo}: {tools:and}.
```

Or:

```text
Toolchain for {repo}: checking ...
```

Or:

```text
Toolchain for {repo}: checking ... {elapsed}
```

Or:

```text
  still checking {repo}'s toolchain, {elapsed} so far
```

Or:

```text
Toolchain for {repo}: nothing named; agents get the image's versions.
```

Or:

```text
Toolchain for {repo}: the image's versions (--no-toolchain).
```

Or:

```text
Toolchain for {repo}:
```

Or:

```text
  {tools}
```

Next step: none; it only informs.

Exit status: 0 (done).

### TOOLCHAIN_INSTALLING

When: A start, or `dockingbird env install`, found a version the repo names that isn't installed yet, so mise installs it before the agent starts: mise's latest line and the time so far, and how long mise has printed nothing when it is quiet for a while. Then it names each version installed and how long it took. A second agent on the same repo installs nothing and shows no such line.

```text
Installed {tools:and} ({elapsed}).
```

Or:

```text
Installing {tools:and} ...
```

Or:

```text
Installing {tools:and} ... {elapsed}
```

Or:

```text
Installing {tools:and} ... {elapsed}: {last_line}
```

Or:

```text
Installing {tools:and} ... {elapsed}, no output for {quiet}
```

Or:

```text
  still installing {tools:and}: {last_line}, {elapsed} so far
```

Next step: none; it only informs.

Exit status: 0 (done).

### TOOLCHAIN_INSTALL_FAILED

When: mise couldn't install a version the repo names (a version that doesn't exist, a download that failed, a checksum that didn't match), or the install ended before it finished. The message shows mise's last lines, and no agent was started: fix the file that names the version, or start with the image's versions using `--no-toolchain`. After `dockingbird env install` or `dockingbird env lock`, run it again.

```text
Couldn't install {tools:and}. Its last lines:
{tail}
Fix the file that names the version, or start with the image's
versions: dockingbird {tool} --no-toolchain
```

Or:

```text
Couldn't install {tools:and}. Its last lines:
{tail}
mise.lock doesn't name what the repo asks for now, and a start can't
change it. Lock it, then start again: dockingbird env lock
```

Or:

```text
The install of {tools:and} ended before it finished.
Run this again, or: dockingbird {tool} --no-toolchain
```

Or:

```text
Couldn't install {tools:and}. Its last lines:
{tail}
Run this again.
```

Or:

```text
Couldn't install {tools:and}. Its last lines:
{tail}
mise.lock doesn't name what the repo asks for now, and env install can't
change it. Lock it instead, which installs too: dockingbird env lock
```

Or:

```text
The install of {tools:and} ended before it finished. Run this again.
```

Next step, as the message gives it:

- dockingbird {tool} --no-toolchain
- dockingbird env lock
- Run this again.

Exit status: 1 (a problem Dockingbird printed).

### TOOLCHAIN_LOOK_FAILED

When: mise couldn't read the repo's tool versions, such as from a `mise.toml` that isn't valid, and the message shows what mise said. When the checkout is marked untrusted (`dockingbird trust --off`) and its mise config needs trust, it says so and offers `dockingbird trust`. A start can still go ahead with the image's versions using `--no-toolchain`.

```text
Couldn't read {repo}'s toolchain. Its last lines:
{tail}
Fix what it says, or start with the image's
versions: dockingbird {tool} --no-toolchain
```

Or:

```text
Couldn't read {repo}'s toolchain. Its last lines:
{tail}
Fix what it says and run this again.
```

Or:

```text
Couldn't read {repo}'s toolchain: its mise config needs trust and
this checkout is untrusted. mise said:
{tail}
Trust the checkout: dockingbird trust, or start with the image's versions:
dockingbird {tool} --no-toolchain
```

Or:

```text
Couldn't read {repo}'s toolchain: its mise config needs trust and
this checkout is untrusted. mise said:
{tail}
Trust the checkout: dockingbird trust, then run this again.
```

Next step, as the message gives it:

- dockingbird {tool} --no-toolchain
- Fix what it says and run this again.
- dockingbird trust

Exit status: 1 (a problem Dockingbird printed).

### TOOLCHAIN_LOOK_UNAVAILABLE

When: You ran `dockingbird env` while Docker isn't running, so Dockingbird can't read the versions agents get. The heading, the dependencies and the downloaded tool versions still show.

```text
The versions agents get need Dockingbird
running. Start it, then: dockingbird env
```

Next step: dockingbird env

Exit status: 0 (done).

### TOOLCHAIN_LOCK_INVALID

When: The repo's `mise.lock` can't be read: it isn't valid TOML, a version in it isn't text, or it is too large. The versions it names are ignored here, and mise says why when it installs; `dockingbird env lock` writes it again.

```text
mise.lock can't be read ({rule}); the versions it names are ignored here and
mise will say why when it installs. Re-lock: dockingbird env lock
```

Next step: dockingbird env lock

Exit status: 0 (done).

### TOOLCHAIN_STORE_BUSY

When: Another start is installing tool versions, for this repo or another one, or `dockingbird clean` is removing unused ones: one of them runs at a time, so this command waits for it, with the time so far, then goes on and uses what it installed.

```text
Another start installed {repo}'s toolchain ({elapsed} waited).
```

Or:

```text
Another start is installing {repo}'s toolchain; waiting ({elapsed})
```

Or:

```text
Another start installed a toolchain ({elapsed} waited).
```

Or:

```text
Another start is installing a toolchain; waiting ({elapsed})
```

Or:

```text
dockingbird clean removed unused toolchain versions ({elapsed} waited).
```

Or:

```text
dockingbird clean is removing unused toolchain versions; waiting ({elapsed})
```

Next step: none; it only informs.

Exit status: 0 (done).

### TOOLCHAIN_INTERRUPTED

When: You pressed Ctrl-C while mise installed the repo's tool versions, or while a start waited for another start's install. The install goes on and the next start uses it; no agent was started. The command exits 130, as a Ctrl-C does.

```text
Stopped before {name} started. {repo}'s toolchain keeps installing; the
next start uses it.
```

Or:

```text
Stopped. {repo}'s toolchain keeps installing; the next start uses it.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### TOOLCHAIN_FETCHING

When: Only for an agent that starts another through Dockingbird's tools (the host MCP server): the repo's tool versions are still installing, so the start is refused at once, nothing waits, and the agent tries the start again. The install goes on.

```text
{repo}'s toolchain is still installing; try the start again.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### TOOLCHAIN_RUNNING_DIFFERS

When: `dockingbird status` found a running agent whose version of a tool is not the one the repo now asks for: the repo's files changed since it started. It keeps its version until you restart it: stop it, then start it again under its name.

```text
{name} runs {tool_name} {running}; the repo now asks for {version}. To restart it: dockingbird stop {name}, then dockingbird {subcommand} --as {name}
```

Next step: dockingbird stop {name}, then dockingbird {subcommand} --as {name}

Exit status: 0 (done).

### TOOLCHAIN_ENV_FAILED

When: An agent's container couldn't set up its tool versions before the agent started, and the agent ended. The message shows mise's last lines: fix what it says (in `mise.toml`, or an encrypted file and the key a config you added carries), then pick the agent up. When the checkout is untrusted and its mise config needs trust, it says so and offers `dockingbird trust`.

```text
{name}'s environment couldn't be set up. Its last lines:
{tail}
Fix what it says (mise.toml, or the encrypted file and the key your
added config carries), then pick it up: dockingbird {subcommand} --as {name}
```

Or:

```text
{name}'s environment couldn't be set up: its mise config needs trust and
this checkout is untrusted. mise said:
{tail}
Trust the checkout (dockingbird trust), then pick it up: dockingbird {subcommand} --as {name}
```

Next step: dockingbird {subcommand} --as {name}

Exit status: 1 (a problem Dockingbird printed).

### TOOLCHAIN_LINE_UNREADABLE

When: Under a failure's message: one of the lines Dockingbird reads from mise's run was too long or not in its form, so its first part is shown as it was printed.

```text
  Couldn't read a line the toolchain run printed (over {size}, or malformed): {printed}
```

Next step: none; it only informs.

Exit status: 0 (done).

### TOOLCHAIN_ITEM

When: One tool version in a list, such as `Python 3.12.7 (mise.toml)` or `Node 20.18.1 (locked)`: the file that names it, or `locked` when `mise.lock` does.

```text
{tool_name} {version} ({file})
```

Or:

```text
{tool_name} {version} (locked)
```

Or:

```text
{tool_name} {version}
```

Next step: none; it only informs.

Exit status: 0 (done).

### DEPS_INSTALLING

When: An agent's container installs the repo's dependencies with the repo's own command (such as `uv sync --locked` or `npm ci`) before the agent starts; the command's own output follows. A start with `--no-deps` says the install was skipped.

```text
Installing {repo}'s dependencies: {deps_command}
```

Or:

```text
Dependencies: skipped (--no-deps).
```

Next step: none; it only informs.

Exit status: 0 (done).

### DEPS_INSTALLED

When: The repo's dependencies were installed before the agent started, and how long it took.

```text
Dependencies installed ({elapsed}).
```

Next step: none; it only informs.

Exit status: 0 (done).

### DEPS_SKIPPED_UNTRUSTED

When: The checkout is marked untrusted (`dockingbird trust --off`), so the agent starts without the repo's dependencies installed. `dockingbird trust` allows the install.

```text
Dependencies: skipped (untrusted checkout; dockingbird trust allows them).
```

Next step: dockingbird trust

Exit status: 0 (done).

### DEPS_FAILED

When: The command that installs the repo's dependencies failed in the agent's container, and the agent ended. The message shows its last lines: fix what it says, or pick the agent up with `--no-deps` to start without them.

```text
{deps_command} failed ({elapsed}). Its last lines:
{tail}
Fix what it says, or start without dependencies: dockingbird {subcommand} --as {name} --no-deps
```

Next step: dockingbird {subcommand} --as {name} --no-deps

Exit status: 1 (a problem Dockingbird printed).

### DEPS_OFFLINE_REFUSED

When: The agent's network access (its egress, `none` or `models`) doesn't reach the package registries and the packages aren't cached, so its dependencies couldn't be installed and the agent ended. Pick it up with `--egress full` for the install, or with `--no-deps` to start without them.

```text
{name}'s dependencies aren't cached and this agent's egress is {egress}, so they
can't be installed. Start with network access for the install:
dockingbird {subcommand} --as {name} --egress full, or without them:
dockingbird {subcommand} --as {name} --no-deps
```

Next step: dockingbird {subcommand} --as {name} --no-deps

Exit status: 1 (a problem Dockingbird printed).

### STATUS_PREPARING

When: `dockingbird status` shows an agent whose container runs but whose tool hasn't started yet: it is setting up its environment or installing dependencies, with the time so far, and how long it has printed nothing when it is quiet for a while.

One row of a table; its cells line up with the rows around it.

```text
  {label}   preparing: {step}, {elapsed}
```

Or:

```text
  {label}   preparing: {step}, {elapsed}, no output for {quiet}
```

Next step: none; it only informs.

Exit status: 0 (done).

### DETAIL_TOOLCHAIN

When: `dockingbird status NAME` shows the tool versions the agent runs, with `(locked)` when `mise.lock` names them, or the image's versions when the repo names none.

One row of a table; its cells line up with the rows around it.

```text
  toolchain   {tools:and}
```

Or:

```text
  toolchain   {tools:and} (locked)
```

Or:

```text
  toolchain   the image's versions
```

Next step: none; it only informs.

Exit status: 0 (done).

### ENV_HEADING

When: The first line of `dockingbird env`'s table: the repo and its branch over its two columns, what the repo wants and what agents get. On a narrow screen, the repo and branch alone.

One row of a table; its cells line up with the rows around it.

```text
{repo} ({branch})   repo wants   agents get
```

Next step: none; it only informs.

Exit status: 0 (done).

### ENV_ROW

When: One tool of `dockingbird env`'s table: the version the repo's files ask for and the file that asks, then the version agents get, with `(locked)` when `mise.lock` names it, `(not installed yet)` when it isn't installed, or the image's own when nothing names the tool. On a narrow screen the two stack under the tool's name: what the repo wants, then what agents get.

One row of a table; its cells line up with the rows around it.

```text
  {tool_name}   {request} ({file})   {version}
```

Or:

```text
  {tool_name}   {request} ({file})   {version} (locked)
```

Or:

```text
  {tool_name}   nothing named   {version} (the image's)
```

Or:

```text
  {tool_name}   {request} ({file})   {version} (not installed yet)
```

Or:

```text
  {tool_name}  wants {request} ({file})
```

Or:

```text
  {tool_name}  wants nothing named
```

Or:

```text
      agents get {version}
```

Or:

```text
      agents get {version} (locked)
```

Or:

```text
      agents get {version} (the image's)
```

Or:

```text
      agents get {version} (not installed yet)
```

Next step: none; it only informs.

Exit status: 0 (done).

### ENV_NOTE

When: Only under `dockingbird --json env`: one line for each note under the table, naming the note, with the note's own facts. The note itself is described under its own name.

```text
{note}
```

Next step: none; it only informs.

Exit status: 0 (done).

### ENV_DEPENDENCIES

When: `dockingbird env` names the commands that install the repo's dependencies before an agent starts, each with its lock file, or says none are installed when the repo has no lock file, or when it names no toolchain (its agents then use Dockingbird's own tool versions and install nothing), or that they are unknown when its `package.json` beside a `yarn.lock` isn't readable JSON.

```text
Dependencies: {deps:and}
```

Or:

```text
Dependencies: none preinstalled (no lock file).
```

Or:

```text
Dependencies: none preinstalled (the repo names no toolchain).
```

Or:

```text
Dependencies: unknown (package.json isn't readable JSON).
```

Next step: none; it only informs.

Exit status: 0 (done).

### ENV_STORE

When: `dockingbird env` says how many tool versions Dockingbird has downloaded for agents; `dockingbird clean` removes the unused ones.

```text
Downloaded: {count:toolchain|toolchains}. Unused ones go with: dockingbird clean
```

Or:

```text
Downloaded: nothing yet.
```

Next step, as the message gives it:

- dockingbird clean
- none, where the message only informs

Exit status: 0 (done).

### ENV_CHANGE_HINT

When: The last line of `dockingbird env`: the command that changes a tool's version in the repo's `mise.toml`.

```text
Change one: dockingbird env use TOOL VERSION
```

Next step: dockingbird env use TOOL VERSION

Exit status: 0 (done).

### ENV_NOT_A_REPO

When: You ran `dockingbird env` outside a git repo; it reads the repo you are in.

```text
dockingbird env reads the repo you are in. cd into a repo, then: dockingbird env
```

Next step: cd into a repo, then: dockingbird env

Exit status: 1 (a problem Dockingbird printed).

### ENV_INSTALL_DONE

When: `dockingbird env install` installed the repo's tool versions, or found them installed already, and offers `dockingbird env lock` so every machine gets the same versions; or the repo names no tool version, so there was nothing to install. It writes nothing in your checkout.

```text
Lock them so every machine gets the same: dockingbird env lock
```

Or:

```text
{tools:and} are already installed. Lock them so every machine gets
the same: dockingbird env lock
```

Or:

```text
{repo} names no tool version, so there is nothing to install.
```

Next step, as the message gives it:

- dockingbird env lock
- none, where the message only informs

Exit status: 0 (done).

### ENV_LOCK_DONE

When: `dockingbird env lock` wrote each tool version into the repo's `mise.toml` and locked them in `mise.lock`: commit both so every machine gets the same. When the repo names no tool version, it writes nothing.

```text
Locked {tools:and} in mise.toml and mise.lock. Commit them so every machine
gets the same: git add mise.toml mise.lock
```

Or:

```text
Nothing to lock: {repo} names no tool version.
```

Next step, as the message gives it:

- git add mise.toml mise.lock
- none, where the message only informs

Exit status: 0 (done).

### ENV_USE_WROTE

When: `dockingbird env use` wrote the version into the repo's `mise.toml`, creating it when the repo had none, and says which version agents started from now get. When another file named the tool, it says that `mise.toml` wins now; when the repo's `mise.lock` changed too, it says so.

```text
Wrote mise.toml: {tool_word} = "{new}" (was {old}). Agents started from
now get {tool_name} {version}.
```

Or:

```text
Wrote mise.toml: {tool_word} = "{new}" (was {old}). Agents started from
now get {tool_name} {version}. mise.lock updated.
```

Or:

```text
Wrote mise.toml: {tool_word} = "{new}" (was {file}: {old}; mise.toml wins now). Agents started from
now get {tool_name} {version}.
```

Or:

```text
Wrote mise.toml: {tool_word} = "{new}" (was {file}: {old}; mise.toml wins now). Agents started from
now get {tool_name} {version}. mise.lock updated.
```

Or:

```text
Created mise.toml: {tool_word} = "{new}". Agents started from
now get {tool_name} {version}.
```

Or:

```text
Created mise.toml: {tool_word} = "{new}". Agents started from
now get {tool_name} {version}. mise.lock updated.
```

Next step: none; it only informs.

Exit status: 0 (done).

### ENV_USE_RUNNING

When: After `dockingbird env use`, the agents already running on the repo keep the versions they started with until you restart them.

```text
{names:and} keep theirs until restarted.
```

Or:

```text
{names:and} keeps theirs until restarted.
```

Next step: none; it only informs.

Exit status: 0 (done).

### ENV_USE_FAILED

When: `dockingbird env use` couldn't set the version: mise couldn't install it, such as offline or for a version that doesn't exist. The message shows mise's last lines; `dockingbird env` shows what the repo names.

```text
Couldn't set {tool_name} {new}. Its last lines:
{tail}
Check the version (dockingbird env shows what the repo names) and run
this again.
```

Next step: dockingbird env

Exit status: 1 (a problem Dockingbird printed).

### ENV_USE_NOT_A_NUMBER

When: You gave `dockingbird env use` a version that isn't a number, such as `lts` or `latest`: Dockingbird pins version numbers. The message names an example for the tool.

```text
`{word}` isn't a version number (Dockingbird pins numbers, never lts or
latest). Name one, such as {example}: dockingbird env use {tool_word} {example}
```

Next step: dockingbird env use {tool_word} {example}

Exit status: 1 (a problem Dockingbird printed).

### ENV_USE_UNKNOWN_TOOL

When: You gave `dockingbird env use` a tool it doesn't know; the message lists the tools it takes. Another tool mise knows can be written into `mise.toml` by hand.

```text
`{word}` isn't a tool. Tools: python, node, go, java, rust, ruby, bun,
deno, zig, pnpm, yarn, npm. See: dockingbird env -h
```

Next step: dockingbird env -h

Exit status: 1 (a problem Dockingbird printed).

### CLEAN_TOOLCHAIN_REMOVED

When: `dockingbird clean` removed a downloaded tool version that no running agent uses and no repo Dockingbird has read names.

```text
Removed {tool_name} {version} from the toolchains.
```

Next step: none; it only informs.

Exit status: 0 (done).

### RULES_TOOLCHAIN_SENTENCE

When: Never shown to you: the line an agent's rules file gets about its tool versions and where its own installs go.

```text
This container runs {tools:and} through mise; the commands on PATH are those.
The toolchain store at /dockingbird/toolchains is read-only: a
`mise install` here writes under $HOME and needs network, never the
store (ask for `dockingbird env install` to add a version for every
agent).
`pip install` into the interpreter fails: use the project's venv
(`uv sync`, `uv run`).
`npm -g`, `go install`, `cargo install`, `gem install` and
`deno install -g` write under $HOME.
```

Next step: none; it only informs.

Exit status: 0 (done).

### RULES_DEPS_SENTENCE

When: Never shown to you: the line an agent's rules file gets about whether the repo's dependencies were installed before it started.

```text
The project's dependencies were installed with `{deps_command}` before you started.
```

Or:

```text
The project's dependencies were not installed ({why}): install them first.
```

Next step: none; it only informs.

Exit status: 0 (done).

### LOCAL_MODEL_NO_NETWORK

When: You started an agent from a config you added that names a local model, in the `none` egress mode. The agent reaches Docker Model Runner on this Mac over its network, which `none` doesn't give it, so nothing was started. Start it with `--egress models`, or set `egress` in that config.

```text
{model} is a local model, which the agent reaches over its network, and its egress
is none, so nothing was started.
Start it with --egress models, or set egress in the config you added.
```

Next step: Start it with --egress models, or set egress in the config you added.

Exit status: 1 (a problem Dockingbird printed).

### LOCAL_MODEL_RUNNER_OFF

When: You started an agent whose config names a local model, and Docker Model Runner isn't running on this Mac (Docker Desktop leaves it off until you turn it on), so nothing was started. Turn it on in Docker Desktop's settings (AI, Enable Docker Model Runner) or with `docker desktop enable model-runner --tcp 12434`. When `docker model status` itself failed, the message shows Docker's own line instead; Dockingbird never turns Model Runner on for you.

```text
{model} is a local model, and Docker Model Runner isn't running here, so
nothing was started. Turn it on in Docker Desktop (Settings > AI > Enable
Docker Model Runner), or run:
docker desktop enable model-runner --tcp 12434
```

Or:

```text
Dockingbird couldn't ask Docker Model Runner about {model}; docker said:
  {said}
Nothing was started. docker model status shows what it says here.
```

Next step, as the message gives it:

- docker desktop enable model-runner --tcp 12434
- docker model status

Exit status: 1 (a problem Dockingbird printed).

### LOCAL_MODEL_RUNNER_UNREADABLE

When: You started an agent whose config names a local model, and `docker model status --json` or `docker model ls --json` answered something Dockingbird doesn't read, such as a Docker Model Runner far older or newer than this release knows, so nothing was started. Run the command the message names to see what it says.

```text
{command} answered in a form Dockingbird doesn't read, so nothing was started
for the local model {model}. Run {command} to see what it says.
```

Next step: Run {command} to see what it says.

Exit status: 1 (a problem Dockingbird printed).

### LOCAL_MODEL_RUNNER_KIND

When: You started an agent whose config names a local model, and Docker Model Runner here is Docker Engine's or Docker Cloud's, not Docker Desktop's. Local models run only on Docker Desktop's Model Runner on a Mac in this release, so nothing was started.

```text
{model} is a local model, and Docker Model Runner here runs on {runner_kind};
Dockingbird's local models need Docker Desktop's, so nothing was started.
Use Docker Desktop's Model Runner on this Mac.
```

Next step: Use Docker Desktop's Model Runner on this Mac.

Exit status: 1 (a problem Dockingbird printed).

### LOCAL_MODEL_BACKEND_MISSING

When: You started an agent whose config names a local model, and Docker Model Runner has no vLLM backend installed, which the model runs on, so nothing was started. Install it with `docker model install-runner --backend vllm` (Docker Desktop 4.62 or later, macOS 15 or later), then start again.

```text
{model} needs Docker Model Runner's vLLM backend, which isn't installed here, so
nothing was started. Install it with: docker model install-runner --backend vllm
```

Next step: docker model install-runner --backend vllm

Exit status: 1 (a problem Dockingbird printed).

### LOCAL_MODEL_BACKEND_NOT_READY

When: You started an agent whose config names a local model while Docker Model Runner's vLLM backend was still installing, or was in error (the message shows Docker's words), so nothing was started. `docker model status` shows the backend's state; start again once it is running.

```text
Docker Model Runner is still installing its vLLM backend, so
nothing was started for {model}. Start again once docker model status
says it is running.
```

Or:

```text
Docker Model Runner's vLLM backend is in error ({said}), so nothing was started for {model}.
docker model status shows it.
```

Next step: docker model status

Exit status: 1 (a problem Dockingbird printed).

### LOCAL_MODEL_NOT_PULLED

When: You started an agent whose config names a local model that Docker Model Runner hasn't pulled on this Mac, so nothing was started. Pull it with the `docker model pull` command the message names; Dockingbird never downloads a model for you.

```text
{model} isn't pulled into Docker Model Runner here, so nothing was started.
Pull it with: docker model pull {model}
```

Next step: docker model pull {model}

Exit status: 1 (a problem Dockingbird printed).

## The fleet's control plane

### RPC_PEER_HOST_MISMATCH

When: A fleet call from this computer was refused because its credential belongs to another computer: a bundle made for one computer was used on another. Leave the fleet here and join again with a bundle made for this computer.

```text
The control plane refused this computer's fleet credential:
it was made for another computer.
Leave the fleet here, then join with a bundle made for this one:
dockingbird node leave, then dockingbird node join
```

Next step: dockingbird node leave, then dockingbird node join

Exit status: 1 (a problem Dockingbird printed).

### RPC_FRAME_INVALID

When: A fleet call from this computer carried a message the control plane's relay doesn't read (a header missing or wrong). The two computers run different Dockingbird code; update the one that is behind.

```text
The control plane's relay didn't read a message from this computer:
its headers weren't Dockingbird's.
The two computers run different Dockingbird code;
update the one that is behind: dockingbird update
```

Next step: dockingbird update

Exit status: 1 (a problem Dockingbird printed).

### NODE_VERSION_MISMATCH

When: A fleet call found the control plane at another Dockingbird version than this computer's. Everything on this computer keeps working; fleet messages resume once both run the same version (update the control plane's home first, then each joined computer).

```text
This computer runs Dockingbird {version} and the control plane runs {other},
so fleet messages wait until they match.
Update the one that is behind: dockingbird update
```

Next step: dockingbird update

Exit status: 1 (a problem Dockingbird printed).

### NODE_ROUTE_REFUSED

When: A command on this computer made a fleet call the control plane doesn't allow a joined computer to make. Dockingbird's own commands never do; run the command again with `--verbose` and report it.

```text
The control plane refused that call: a joined computer may not make it.
Run the command again with --verbose and report what it says.
```

Next step: Run the command again with --verbose and report what it says.

Exit status: 1 (a problem Dockingbird printed).

### NODE_SESSION_ELSEWHERE

When: You started an agent whose fleet name is live from another computer (the one the message names), so this computer could not take it over. Stop it there first, or use another name.

```text
{name} already works in the fleet from {host}, so this computer can't open it.
Stop it on {host} first, or use another name here.
```

Next step: Stop it on {host} first, or use another name here.

Exit status: 1 (a problem Dockingbird printed).

### AGENT_NAME_RESERVED

When: You started an agent on the control plane's home with a name whose first part is a joined computer's label (its agents' fleet names start that way). Pick a name that doesn't start with that label and a dash.

```text
{name} starts with {label}-, which the control plane keeps
for the agents of the computer labelled {label}.
Use a name that doesn't start with {label}-.
```

Next step: Use a name that doesn't start with {label}-.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_LINK_COMMAND_REFUSED

When: A native command outside the fleet-link's short list (`fleet-link open`, `fleet-link end`, `fleet-link status`, `node enrol`, `daemon run`) was run in the fleet-link container. Dockingbird's own commands never do this; run the command as usual.

```text
dockingbird {command} isn't a command this computer's fleet-link runs.
Run it as a plain Dockingbird command instead.
```

Next step: Run it as a plain Dockingbird command instead.

Exit status: 1 (a problem Dockingbird printed).

### NODE_ALREADY_ENROLLED

When: You ran `dockingbird node join` with a bundle the control plane already enrolled a computer with. Each bundle joins once; on the control plane's home, remove the host and make a new bundle, then join with it.

```text
The control plane already enrolled a computer with this bundle,
so this join was refused. Each bundle joins once.
On the control plane's home, make a new one:
dockingbird cp remove {label}, then dockingbird cp token --host {label} --platform {platform}
```

Next step: dockingbird cp remove {label}, then dockingbird cp token --host {label} --platform {platform}

Exit status: 1 (a problem Dockingbird printed).

### CP_ALREADY_INITIALIZED

When: You ran `dockingbird cp init` on a home that is already the control plane. Nothing changed; `dockingbird cp status` lists the computers in the fleet.

```text
This home is already the fleet's control plane; nothing changed.
dockingbird cp status lists the computers in the fleet.
```

Next step: dockingbird cp status

Exit status: 1 (a problem Dockingbird printed).

### CP_HOSTS_ENABLED

When: You ran `dockingbird cp off` while computers are still in the fleet. Remove each with `dockingbird cp remove LABEL` (which closes its agents' fleet inboxes), then turn the control plane off.

```text
{count:computer|computers} still in the fleet, so this home stays its control plane.
Remove each with dockingbird cp remove LABEL, then run this again.
```

Next step: Remove each with dockingbird cp remove LABEL, then run this again.

Exit status: 1 (a problem Dockingbird printed).

### MODE_CHANGE_AGENTS_RUNNING

When: You ran `dockingbird cp init`, `dockingbird cp off`, `dockingbird node join` or `dockingbird node leave` while agents run in this home. Stop them first; a change of the fleet setup touches no running agent.

```text
With {count:agent|agents} running here, the fleet setup can't change.
Stop them first: dockingbird stop
```

Next step: dockingbird stop

Exit status: 1 (a problem Dockingbird printed).

### NODE_ALREADY_JOINED

When: You ran `dockingbird node join` on a home that is already in the fleet. Leave first (`dockingbird node leave`), then join with the new bundle.

```text
This home already joined the fleet as {label}.
To join with a new bundle, leave first: dockingbird node leave
```

Next step: dockingbird node leave

Exit status: 1 (a problem Dockingbird printed).

### NATS_SERVER_UNAVAILABLE

When: A command made Dockingbird ready on the control plane's home and the fleet's hub (its message server, in the cp-relay container) didn't answer in time. Agents and everything else on the home work; run the command again, and report it if it keeps failing.

```text
The fleet's hub didn't answer within {seconds:second|seconds},
so fleet messages can't reach the control plane yet. Everything else works.
Run the command again; if it keeps failing, report it.
```

Next step: Run the command again; if it keeps failing, report it.

Exit status: 1 (a problem Dockingbird printed).

### AGENT_ON_MEMBER

When: You ran `dockingbird clean NAME` or `dockingbird set NAME` on the control plane's home for an agent that runs on a joined computer (its fleet name). `dockingbird stop NAME` here closes its fleet inbox; everything else is done on its own computer.

```text
{name} runs on {host}, not on this computer, so this command can't change it.
Run it there instead.
```

Next step: Run it there instead.

Exit status: 1 (a problem Dockingbird printed).

### FLEET_NAME_TOO_LONG

When: You started an agent on a joined computer with a name that, after the computer's label and a dash, is longer than a name may be. Use a shorter name.

```text
{name} is too long for the fleet:
with {label}- in front it passes {count:character|characters}.
Use a shorter name.
```

Next step: Use a shorter name.

Exit status: 1 (a problem Dockingbird printed).

### NODE_SESSIONS_LIVE

When: You ran `dockingbird node leave` while agents on this computer still have a fleet inbox (their token folders exist). Stop those agents first, then leave.

```text
{count:agent on this computer still uses|agents on this computer still use} the fleet, so it can't leave.
Stop them first: dockingbird stop
```

Next step: dockingbird stop

Exit status: 1 (a problem Dockingbird printed).

### FLEET_SESSION_NOT_OPENED

When: You started an agent on a joined computer and the control plane didn't open its fleet inbox (it was asleep, unreachable, at another version, or refused the credential; the message says which). The agent runs as usual; Dockingbird opens the inbox later, once the control plane answers.

```text
{name} has no fleet inbox yet: {cause}.
It works here as usual and gets one once the control plane answers.
```

Next step: none; it only informs.

Exit status: 0 (done).

### FLEET_LINK_START_FAILED

When: A command made Dockingbird ready on a joined computer and Docker refused to run the fleet-link, the container that carries the fleet's messages. The command went on; the next command tries again, and until then the agents here have no fleet inbox.

```text
The fleet-link couldn't start ({cause}),
so this computer's agents have no fleet inbox for now.
The command goes on; the next one tries again.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CP_INITIALIZED

When: You ran `dockingbird cp init --hub-address ADDRESS`: this home is the fleet's control plane, its hub listens at that address and port, and `dockingbird cp token` makes a bundle for each computer that joins.

```text
This home is now the fleet's control plane, at {host}:{port}.
Make a bundle for each computer that joins:
dockingbird cp token --host LABEL --platform PLATFORM
```

Next step: dockingbird cp token --host LABEL --platform PLATFORM

Exit status: 0 (done).

### CP_TOKEN_ISSUED

When: You ran `dockingbird cp token --host LABEL --platform PLATFORM`: the control plane made the computer's fleet credential and printed its bundle on the next line, once. Paste it into `dockingbird node join` on that computer; the bundle isn't kept.

```text
{label} is enrolled as node {node_id} ({platform}).
Its bundle is the next line, shown once and not kept here:
paste it into dockingbird node join on that computer.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CP_HOST_REMOVED

When: You ran `dockingbird cp remove LABEL`: the computer's credential is revoked, its agents' fleet inboxes are closed (the count shown) and its hub user is gone. Its own agents keep running there without the fleet.

```text
{label} (node {node_id}) is out of the fleet;
{count:fleet inbox|fleet inboxes} of its agents closed.
Its own agents keep running there without the fleet.
```

Next step: none; it only informs.

Exit status: 0 (done).

### CP_OFF

When: You ran `dockingbird cp off`: the control plane's files and container are gone and this home works as any home; or, on a home that wasn't the control plane, nothing changed.

```text
This home is a plain home again; the fleet's control plane is off.
```

Or:

```text
This home isn't the fleet's control plane; nothing changed.
```

Next step: none; it only informs.

Exit status: 0 (done).

### NODE_JOINED

When: You ran `dockingbird node join` with a bundle from the control plane: this computer is in the fleet under that label, and each agent started here from now on gets a fleet inbox.

```text
This computer joined the fleet as {label} (node {node_id}).
Each agent started here from now on gets a fleet inbox.
```

Next step: none; it only informs.

Exit status: 0 (done).

### NODE_LEFT

When: You ran `dockingbird node leave`: this computer's fleet credential and token folders are removed and its fleet-link stopped; its agents keep running on their own.

```text
This computer left the fleet.
Its agents keep running; their fleet inboxes are gone.
```

Next step: none; it only informs.

Exit status: 0 (done).

### LICENSE_SHOWN

When: You ran `dockingbird license status`. It says whether this computer is licensed, with the plan, its seats and the day its term ends, then the seats in use, this computer's name, the day its lease ends and its last check-in with the license server; or what keeps the license from being used and what to run next. `--refresh` asks the license server first.

```text
Licensed: {plan}, {seats:seat|seats}, {term}.
```

Or:

```text
Licensed: {plan}, {seats:seat|seats}, {term}.
It ends soon: renew it to keep starting new agents after that.
```

Or:

```text
Licensed: {plan}, {seats:seat|seats}, {term}.
The license server hasn't answered lately; agents start while the lease lasts.
Check again: dockingbird license status --refresh
```

Or:

```text
The license ended; agents still start for a short grace time.
Renew it, then: dockingbird license status --refresh
```

Or:

```text
This computer has no license yet; agents start as usual for now.
License it: dockingbird license activate
```

Or:

```text
This computer has no license.
Activate it: dockingbird license activate
```

Or:

```text
The license's term ended.
Renew it, then: dockingbird license status --refresh
```

Or:

```text
The license server hasn't answered for too long.
Get online, then: dockingbird license status --refresh
```

Or:

```text
Zeusfyi ended this license.
Activate a current key: dockingbird license activate
```

Or:

```text
This computer's seat was freed from another computer.
Activate it again: dockingbird license activate
```

Or:

```text
The license file here is another computer's.
Activate this one: dockingbird license activate
```

Or:

```text
The license file here can't be read.
Activate it again: dockingbird license activate
```

Or:

```text
This license needs a newer Dockingbird.
Get it: dockingbird update
```

Or:

```text
  Seats in use: {seats_held} of {seats}
```

Or:

```text
  This computer: {label}
```

Or:

```text
  Lease until: {lease}
```

Or:

```text
  Last check-in: {seen}
```

Next step, as the message gives it:

- none, where the message only informs
- dockingbird license status --refresh
- dockingbird license activate
- dockingbird update

Exit status: 0 (done).

### LICENSE_ACTIVATED

When: You ran `dockingbird license activate` and pasted or piped your key: this computer now uses one seat of that license.

```text
This computer is activated: {plan}, {seats:seat|seats}, {term}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### LICENSE_TRIAL_STARTED

When: You ran `dockingbird license trial`: this computer's trial started, and the line says until when.

```text
The trial started on this computer: {plan}, {term}.
```

Next step: none; it only informs.

Exit status: 0 (done).

### LICENSE_RELEASED

When: You ran `dockingbird license deactivate`: this computer's seat is free for another computer, and its license is gone from it.

```text
This computer no longer uses a seat of the license.
```

Next step: none; it only informs.

Exit status: 0 (done).

### LICENSE_ACTIVATIONS

When: You ran `dockingbird license activations` with your key: one line for each computer that uses a seat, with the day it was activated and the day it was last seen, and how to free a seat with `--release`.

```text
{label}: activated {activated}, last seen {seen}, id {id}
```

Or:

```text
No computer uses a seat of this license.
```

Or:

```text
Free a seat: dockingbird license activations --release ID
```

Next step, as the message gives it:

- none, where the message only informs
- dockingbird license activations --release ID

Exit status: 0 (done).

### LICENSE_ACTIVATION_RELEASED

When: You ran `dockingbird license activations --release` with an activation's id: that computer no longer uses a seat, and the list that follows is without it.

```text
The seat of activation {id} is free again.
```

Next step: none; it only informs.

Exit status: 0 (done).

### LICENSE_NOTE

When: You started an agent, and the license has something to say: its term ends soon, the license server hasn't answered lately, it ended and its grace time runs, or it can't be used while licensing isn't enforced. The agent starts; `dockingbird license status` says more.

```text
Your Dockingbird license ends {until}; renew it to keep starting new agents.
```

Or:

```text
The license server hasn't answered lately; agents start while the lease lasts.
```

Or:

```text
The license ended; starts stop after a grace time: dockingbird license status
```

Or:

```text
The license can't be used, and isn't enforced yet: dockingbird license status
```

Next step, as the message gives it:

- none, where the message only informs
- dockingbird license status

Exit status: 0 (done).

### LICENSE_REFUSED

When: You started an agent, and the license doesn't allow new agents: this computer has none, its term ended, the license server hasn't answered for too long, Zeusfyi ended it, its seat was freed elsewhere, the license file belongs to another computer or can't be read, or it needs a newer Dockingbird. Nothing started; agents already running go on, and the line says what to run.

```text
A new agent needs a license, and this computer has none.
Activate it: dockingbird license activate
```

Or:

```text
Your Dockingbird license ended, so no new agent starts; running ones go on.
Renew it, then: dockingbird license status --refresh
```

Or:

```text
The license server hasn't answered for too long, so no new agent starts.
Get online, then: dockingbird license status --refresh
```

Or:

```text
Zeusfyi ended this license, so no new agent starts.
Activate a current key: dockingbird license activate
```

Or:

```text
This computer's seat was freed from another computer, so no new agent starts.
Activate it again: dockingbird license activate
```

Or:

```text
The license file here is another computer's, so no new agent starts.
Activate this one: dockingbird license activate
```

Or:

```text
The license file here can't be read, so no new agent starts.
Activate it again: dockingbird license activate
```

Or:

```text
This license needs a newer Dockingbird, so no new agent starts.
Get it: dockingbird update
```

Next step, as the message gives it:

- dockingbird license activate
- dockingbird license status --refresh
- dockingbird update

Exit status: 1 (a problem Dockingbird printed).

### LICENSE_CLIENT_DAMAGED

When: Dockingbird's license program is missing, took too long, or answered something Dockingbird can't read. `dockingbird update` gets a fresh copy.

```text
Dockingbird's license program didn't answer as expected.
Get a fresh copy: dockingbird update
```

Next step: dockingbird update

Exit status: 1 (a problem Dockingbird printed).

### LICENSE_CLIENT_UNAVAILABLE

When: You started an agent, and Dockingbird couldn't download its license program from Zeusfyi; the line says why (no network, the server's answer, a timeout). Nothing started; `dockingbird license status` downloads it when the server answers.

```text
Dockingbird couldn't download its license program ({detail}),
so no new agent starts.
Try again: dockingbird license status
```

Next step: dockingbird license status

Exit status: 1 (a problem Dockingbird printed).

### LICENSE_CLIENT_DIGEST_MISMATCH

When: Dockingbird downloaded its license program, and the file isn't the one this version of Dockingbird expects, so it wasn't kept.

```text
The license program Dockingbird downloaded isn't the one this version
expects, so it wasn't kept.
Get the latest Dockingbird: dockingbird update
```

Next step: dockingbird update

Exit status: 1 (a problem Dockingbird printed).

### LICENSE_CLIENT_PATH_INVALID

When: The variable that names a license program of your own is set in your shell, and it isn't the full path of an existing program. That variable is for development and tests: fix it, or unset it to use the program Dockingbird downloads.

```text
DOCKINGBIRD_LICENSE_CLIENT_PATH must be the full path of a program.
Fix it, or stop using it: unset DOCKINGBIRD_LICENSE_CLIENT_PATH
```

Next step: unset DOCKINGBIRD_LICENSE_CLIENT_PATH

Exit status: 1 (a problem Dockingbird printed).

### LICENSE_PLATFORM_UNSUPPORTED

When: Dockingbird's license program is made for Apple silicon Macs and arm64 Linux, and this computer is neither.

```text
Dockingbird's license program runs on Apple silicon Macs and arm64
Linux, not on {platform}.
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### LICENSE_AUTHORITY_UNAVAILABLE

When: Dockingbird couldn't reach the license server, to download its license program or for a `dockingbird license` action. Nothing changed; try again when you are online.

```text
Dockingbird couldn't reach the license server, so nothing changed.
Try again later.
```

Next step: Try again later.

Exit status: 1 (a problem Dockingbird printed).

### LICENSE_AUTHORITY_REFUSED

When: A `dockingbird license` action didn't work for a reason Dockingbird has no words of its own for, so the line shows what the license program said. Nothing changed.

```text
The license server didn't do that, so nothing changed.
The license program said: {detail}
```

Next step: none; it only informs.

Exit status: 1 (a problem Dockingbird printed).

### LICENSE_SEATS_FULL

When: You ran `dockingbird license activate`, and every seat of that license is in use. `dockingbird license activations` lists the computers that use them, and frees one.

```text
Every seat of this license is in use, so this computer can't take one.
See them, and free one: dockingbird license activations
```

Next step: dockingbird license activations

Exit status: 1 (a problem Dockingbird printed).

### LICENSE_KEY_INVALID

When: The key you pasted or piped isn't one Zeusfyi knows, or isn't a key at all: `ZF-` then five groups of five letters or digits. It is never shown.

```text
Zeusfyi doesn't know that license key; nothing changed.
Check it, then: dockingbird license activate
```

Or:

```text
A license key is ZF- then five groups of five letters or digits.
Try again: dockingbird license activate
```

Next step: dockingbird license activate

Exit status: 1 (a problem Dockingbird printed).

### LICENSE_TRIAL_USED

When: You ran `dockingbird license trial`, and this computer has had its trial. Activate it with a key instead.

```text
This computer has had its trial already.
Activate it with a key: dockingbird license activate
```

Next step: dockingbird license activate

Exit status: 1 (a problem Dockingbird printed).

### LICENSE_KEY_IN_ARGV

When: You typed a license key on the command line, where other programs and your shell history can read it. Nothing ran; run `dockingbird license activate` and paste the key when asked, or pipe it in.

```text
A license key never goes on the command line, where your shell
history and other programs can read it.
Paste it when asked: dockingbird license activate
```

Next step: dockingbird license activate

Exit status: 2 (usage).

### LICENSE_SEAT_STILL_HELD

When: You ran `dockingbird clean --all`, and the license server didn't answer, so this computer still uses a seat. Free it from another computer with `dockingbird license activations`.

```text
Dockingbird couldn't reach the license server, so this computer
still uses a seat.
Free it from another computer: dockingbird license activations
```

Next step: dockingbird license activations

Exit status: 0 (done).

### LICENSE_UPDATE_NEEDS_LICENSE

When: `dockingbird update` (or `--check`) on an install from Zeusfyi's release index found no activation on this computer: the index serves new versions only to an activated computer, with the download token its activation came with. Nothing changed; `dockingbird license activate`, then update again.

```text
Updating Dockingbird needs this computer's license: its release index
lets in only an activated computer. Nothing changed.
Activate it: dockingbird license activate
```

Next step: dockingbird license activate

Exit status: 1 (a problem Dockingbird printed).

### LICENSE_TERMS

When: You activated this computer or started a trial: the line says where the terms you use Dockingbird under are.

```text
You use Dockingbird under its terms: {link}
```

Next step: none; it only informs.

Exit status: 0 (done).

### LICENSE_OPTION_INVALID

When: You gave `dockingbird license` a `--label`, `--accept-terms` or `--release` value the license program doesn't take: a label is letters, digits, `-` and `.`, a terms version the same and `_`, an activation's id letters, digits, `-` and `_`. Nothing ran.

```text
--label takes letters, digits, - and . only, at most {count} characters.
See: dockingbird license -h
```

Or:

```text
--accept-terms takes a version of letters, digits, -, . and _ only.
See: dockingbird license -h
```

Or:

```text
--release takes an activation's id: letters, digits, - and _ only.
See: dockingbird license -h
```

Next step: dockingbird license -h

Exit status: 2 (usage).

### LICENSE_KEY_PROMPT

When: You ran `dockingbird license activate` or `activations` in a terminal: paste your license key; it isn't shown as you paste it.

```text
Paste your Dockingbird license key (hidden):
```

Next step: none; it only informs.

Exit status: 0 (done).
