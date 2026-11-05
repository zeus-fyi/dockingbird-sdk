---
title: Agent set-up prompt
summary: A block of plain text to paste into Claude Code or Codex so that it sets up Dockingbird on this computer with you.
audience: first-day
commands:
  - dockingbird --version
  - dockingbird license activate
  - dockingbird license status
  - dockingbird init
  - dockingbird start
  - dockingbird status
  - dockingbird wait
  - dockingbird send
  - dockingbird read
  - dockingbird login claude
  - dockingbird login codex
  - dockingbird fleet hosts set
  - dockingbird org login
  - dockingbird org status
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../llms.txt).

# Agent set-up prompt

The block below is a prompt for Claude Code or Codex on the computer that will run Dockingbird. Clone this
repository on that computer, open your coding agent in the clone, and paste the whole block as your first message.
The agent reads the quickstart and the prerequisites, checks Docker, uv, git, the disk and the platform, and then
waits while you install and activate. After that it runs `dockingbird init` in your repository, starts one agent
with `dockingbird start`, proves a message round trip and ends with a table of every step and its done line.

```text
1. Who you are
You are setting up Dockingbird on this computer with its owner. The owner types the license key and does any
sign-in; you run every other step, and only after the checks below pass.
Each step ends with its done line: the exact line Dockingbird prints when the step worked. A step that prints a
message id instead stops the setup. Open the id's entry in docs/troubleshooting.md (its anchor is the id in lower
case), show the owner its "Next step:", and report it.

2. Read first
Read these files of this repository: llms.txt, docs/quickstart.md, docs/getting-started/prerequisites.md and
templates/AGENTS.md. Once the owner names the topology in step 4, read its page too:
  one Mac              examples/one-mac/README.md
  two Macs over ssh    examples/two-macs-ssh/README.md
  a cloud VM           examples/cloud-vm-gcloud/README.md
  a team fleet         examples/team-fleet/README.md
Read, do not skim: the done line of each step is on those pages.

3. Check before you act
Run each check and report it as pass or fail, with the command you used.
  Platform: uname -m prints arm64 (an Apple silicon Mac) or aarch64 (arm64 Linux). Intel Macs, x86 Linux and
    Windows are not supported.
  Docker: docker buildx version prints the plugin's version, and docker version answers without an error. On a Mac
    a stopped Docker Desktop passes, because Dockingbird starts it.
  uv: uv --version prints its version.
  git: /usr/bin/git --version prints its version.
  Disk: df -h ~ shows room for the first build, which downloads about 1 GB and fills a 441 MB package folder.
  Home: ls -A "${DOCKINGBIRD_HOME:-$HOME/.local/share/dockingbird}" prints nothing, or the folder does not exist.
    Files there that Dockingbird did not make stop the first start with HOME_NOT_EMPTY.
Stop on any fail. Show the owner the entry the prerequisites page names for it, and report.

4. Hand the key steps to the owner
Ask the owner which repository to set up, and which topology this is: one Mac, two Macs over ssh, a cloud VM or
a team fleet. Then ask the owner to run these two steps at their own terminal:
  the install line for this platform from docs/getting-started/install.md, with the key from the purchase email;
  dockingbird license activate, which asks for the key at a hidden prompt.
Never ask for the key: a key pasted into this chat lands in your transcript. Go on once the owner says both ran.

5. Check the owner's steps
  dockingbird --version
Done when it prints a line that starts with dockingbird and a version. When the shell finds no dockingbird, the
owner runs uv tool update-shell and opens a new terminal.
  dockingbird license status
Done when the first line reads "Licensed: {plan}, {seats}, {term}." (LICENSE_SHOWN). Any other first line means
the activation did not take: show it to the owner and go back to step 4.

6. Make the repository ready
cd into the repository the owner named, then run:
  dockingbird init
Done when it prints "Set up {project} for Dockingbird {release}: the project file, its rules," and exits 0
(INIT_DONE). Without an org login a line follows saying the project is not in your organisation's store
(INIT_NOT_REGISTERED); both mean success. A repository set up before prints "{project} is set up for Dockingbird
{release}: nothing to change." instead, which is also success. Outside a git repository init stops with
INIT_NOT_A_CHECKOUT.
Agents start from the last commit. Show the owner the files init wrote and, on their word, commit them:
  git add .dockingbird .agents .claude && git commit -m "Add the Dockingbird project files"

7. First start
  dockingbird start "say hello and stop"
Add --harness codex when the owner uses Codex. Run it in the background, or with a 10-minute timeout: the first
start builds the image (about 5 minutes and about 1 GB, once) and takes the Claude Code or Codex sign-in that this
computer already has. Done when it prints these two lines (AGENT_STARTED_BUS):
  {name} started on {repo} ({branch}).
  Thread {thread}. Watch: dockingbird wait {name}
Use the name it printed, claude-1 on a new computer, in every step below. Then run:
  dockingbird status
  dockingbird wait {name}
Done when status lists the agent and wait prints "{kind} from {name}: {subject}" (WAIT_DELIVERY). A wait that
prints "Nothing arrived" or "Nothing new" has used its 25 seconds; run it again.
On SIGNIN_NEEDED or START_NO_SIGNIN_BUS, stop. The owner signs in at their terminal with dockingbird login claude
(or dockingbird login codex), and then you run this step again.

8. Prove it
  dockingbird status --json
Done when it exits 0 and one line of JSON has "name" set to the agent and "state" set to working or idle.
  dockingbird license status
Done when the first line starts with "Licensed:".
  dockingbird send {name} "Reply with the word ready."
Done when it prints "Sent {kind} to {name} (message {value})." (SENT).
  dockingbird wait {name}
  dockingbird read {index}
Done when wait prints "Read it: dockingbird read {index}" and read prints "{kind} from {name}, {priority}:
{subject}" (READ_HEADER), with the agent's reply under it.

9. Optional topology
For a second computer the owner reaches with ssh, or a Compute Engine VM:
  dockingbird fleet hosts set NAME --ssh DEST
  dockingbird fleet hosts set NAME --gcloud VM --zone ZONE --project PROJECT
Done when it prints "{host}: {route} {target}, saved in {path}." (FLEET_HOSTS_SET).
For a team fleet the owner logs this computer in to the organisation's store, at their terminal, because it asks
for a password at a hidden prompt:
  dockingbird org login HOST:PORT --as user --role ROLE
Done when dockingbird org status, which you run, ends 0.

10. Report
End with a table of every step: the command, the done line you saw and the exit status. Under it, list each
message id you met with its troubleshooting entry, then your own next step.

11. Never
  ask for the key, or read it from the clipboard, a file or this chat;
  put the key in a command line, the shell history, a file or the report;
  run uv tool install dockingbird without the --index part of the install line;
  edit files outside the repository being set up;
  run dockingbird clean --all without the owner's word.
```

You run four commands at your own terminal: the install line with your key and `dockingbird license activate` in step 4, `dockingbird login claude` or `dockingbird login codex` when step 7 stops for a sign-in, and `dockingbird org login` in step 9 for a team fleet.
