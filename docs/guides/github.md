---
title: Connect agents to GitHub
summary: Connect one GitHub branch so agents fetch and push it while the ssh key stays with Dockingbird.
audience: daily
commands:
  - connect
  - connections
  - connect --branch
  - connections --release
  - revoke
  - disconnect
  - config add
---

# Connect agents to GitHub

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

This page connects one branch of a GitHub repo to your agents. They fetch and push that branch through Dockingbird, and none of them ever holds the key. The model behind it is on [connections.md](connections.md).

## Before you start

- Dockingbird is set up. `dockingbird status` must not print "Dockingbird isn't set up yet."
- You stand in a checkout of the repo, on the branch the agents work on. `git branch --show-current` prints it.
- GitHub accepts a key of yours. `ssh -G github.com` lists the key files your ssh would try, in order, and Dockingbird tries the same ones.
- To limit the connection to one repository, you hold a deploy key with write access to it. Step 2 makes one.
- To use the ssh-agent, you run Docker Desktop. The plain Docker Engine forwards no agent.

## Steps

1. Connect with the key your own ssh uses for GitHub. Here `github` is only the connection's name. Dockingbird copies your branch first when no agent has copied it yet, as a start does, and then connects that branch.

   ```bash
   dockingbird connect github --github example-org/example-app
   ```

   To connect another branch, switch to it and run the same command there, or add `--branch NAME` for a branch Dockingbird has already copied. A key with a passphrase makes ssh-keygen ask for it once, on your terminal, so it can write Dockingbird's copy without one. Dockingbird never sees the passphrase. The step is done when the command prints these lines.

   ```text
   Connected github: example-org/example-app (main) over SSH as somebody, with a copy of
   ~/.ssh/id_ed25519 (no passphrase) kept in Dockingbird until you disconnect.
   A config that names it: connections = ["github"]
   ```

2. Limit the connection to one repository with a deploy key. Add the public half to the repo as a deploy key with write access, then name the private file. Only you may read that file, it cannot be a link, and it cannot sit inside Dockingbird's folder.

   ```bash
   ssh-keygen -t ed25519 -N '' -f ~/.ssh/dockingbird_github
   dockingbird connect github --github example-org/example-app --key ~/.ssh/dockingbird_github
   ```

   The step is done when the same "Connected github" lines print. A key of your account reaches every repository your account does, while a deploy key reaches the one repo.

3. Use your Mac's ssh-agent instead of a copy of a key. Docker Desktop forwards the agent into Dockingbird's coordinator, so no key is copied anywhere. Docker Desktop opened from the Dock has no agent in its session. Open it from a terminal, and load your key first.

   ```bash
   open -a Docker
   ssh-add --apple-use-keychain ~/.ssh/id_ed25519
   dockingbird connect github --github example-org/example-app --agent
   ```

   When no agent is forwarded yet, Dockingbird restarts itself to take it and prints a line for that. The step is done when the command prints these lines.

   ```text
   Restarting Dockingbird to use your Mac's ssh-agent ... done
   ```

   ```text
   Connected github: example-org/example-app (main) over SSH as somebody, with your Mac's
   ssh-agent; no key is copied.
   A config that names it: connections = ["github"]
   ```

   Every key in the agent reaches every repository your account does. Running `ssh-add -D`, or quitting Docker Desktop, ends that at once. If your Mac's agent restarts, requests fail with "your Mac's ssh-agent isn't reachable". Then `dockingbird stop`, followed by any command, binds the socket again.

4. Name the connection in a config you add. Agents ask for a fetch or a push with a `bus_request`, and Dockingbird's coordinator runs it. A push sends the head the agents published. A command that pushes therefore needs a `tools` setting of `default` or `full`, since `bus` shares no commits.

   ```toml
   command = "fixer"
   connections = ["github"]
   tools = "default"
   ```

   The four tools that use a connection, `bus_connections`, `bus_request`, `bus_request_status` and `bus_request_cancel`, sit in the `default` and `full` sets and not in `bus`, which is what `tools` holds when you leave it out. A config that names `github` with no `tools` line gives its agents no tool to fetch or push. In a swarm role, `tools` takes `bus`, `full` or a list, so use `full`, or a list that holds those four tools and every `bus` tool. [The agent tools page](../reference/agent-tools.md) lists each set, and [How a secret is brokered](connections.md#how-a-secret-is-brokered) follows a request through the broker.

   ```bash
   dockingbird config add fixer.toml
   ```

   The step is done when the command prints this line.

   ```text
   Registered fixer: dockingbird fixer "task" (connections: github)
   ```

5. See what the connection lets agents do. The `status` screen lists each connection after the sign-in line. `dockingbird status fixer-1` adds that agent's last request and, when it failed, the reason in plain words.

   ```bash
   dockingbird connections github
   ```

   The step is done when the output holds this line, followed by one `Agent:` line for each grant.

   ```text
   Fetch and push example-org/example-app (main)
   ```

## How a fetch and a push work

A fetch leaves the branch as a bundle file in the agent's log folder, with its SHA-256. A push needs a fetch of the same connection first. It fails when GitHub's branch holds commits the published head lacks. The agent then merges its newest fetch into its work, shares it, and pushes again. It fetches again first when GitHub's branch moved since the last fetch.

Dockingbird checks the copy of your key against GitHub's own host keys from this computer before it says done. `--known-hosts PATH` names a file of host keys to trust instead. Fetch and push over SSH are all that connections run today. HTTPS tokens are not yet available.

## Grants, revoke and a stuck push

Each start of an added config's command grants its connections to that agent for at most its `session_hours`. Take the connection from one agent with `dockingbird revoke github --to fixer-1`, from a swarm role with `dockingbird connect github --revoke --role grader`, or from everyone with `dockingbird disconnect github`. The disconnect also deletes Dockingbird's copy of the key. `dockingbird clean --all` removes it too. Your own key file stays where it is. The commands and their done lines are on [connections.md](connections.md).

A push that stopped midway, after which GitHub's branch moved, has a result Dockingbird cannot tell. It holds every other push back and lists the case under "Needs your attention" in `dockingbird status`. Open the branch on GitHub, check whether the push landed, then release it.

```bash
dockingbird connections --release
```

The command is done when it prints these lines. The next push starts with a fresh fetch.

```text
Released the push to example-org/example-app whose result was unknown.
The next push starts with a fresh fetch.
```

## When it fails

- [`CONNECT_NOT_IN_REPO`](../troubleshooting.md#connect_not_in_repo): you ran `connect` outside a checkout, or `--branch` names a branch Dockingbird has not copied. Switch to the branch and run it again.
- [`CONNECT_GITHUB_INVALID`](../troubleshooting.md#connect_github_invalid): the value after `--github` is not an owner and a name joined by one slash.
- [`CONNECT_NO_KEY`](../troubleshooting.md#connect_no_key): none of the key files `ssh -G github.com` lists exists. Pass `--key PATH`, or make the deploy key of step 2.
- [`CONNECT_KEY_UNREADABLE`](../troubleshooting.md#connect_key_unreadable): the key file is missing, a link, readable by others, or inside Dockingbird's folder.
- [`CONNECT_KEY_INVALID`](../troubleshooting.md#connect_key_invalid): the file is not a private key, for example the `.pub` file. Name the one without `.pub`.
- [`CONNECT_KEY_HARDWARE`](../troubleshooting.md#connect_key_hardware): the key lives on a security key and cannot be copied. A deploy key works.
- [`CONNECT_PASSPHRASE_WRONG`](../troubleshooting.md#connect_passphrase_wrong): `ssh-keygen` could not unlock the key. Run the command again, or make a deploy key.
- [`CONNECT_PASSPHRASE_NEEDS_TERMINAL`](../troubleshooting.md#connect_passphrase_needs_terminal): the key has a passphrase and the command has no terminal to ask on.
- [`CONNECT_KEY_REFUSED`](../troubleshooting.md#connect_key_refused): GitHub refused every key tried. Add the key's `.pub` to your account, or to the repo as a deploy key with write access.
- [`CONNECT_GITHUB_UNREACHABLE`](../troubleshooting.md#connect_github_unreachable): this computer could not reach GitHub. Nothing was saved.
- [`CONNECT_HOST_KEY_MISMATCH`](../troubleshooting.md#connect_host_key_mismatch): GitHub answered with a host key Dockingbird does not hold. Run `dockingbird update`.
- [`CONNECT_KEY_CHANGED`](../troubleshooting.md#connect_key_changed): the connection keeps a different key than the file holds now. Disconnect it, then connect again.
- [`CONNECT_NO_AGENT`](../troubleshooting.md#connect_no_agent), [`CONNECT_AGENT_REFUSED`](../troubleshooting.md#connect_agent_refused), [`CONNECT_AGENT_NO_DESKTOP`](../troubleshooting.md#connect_agent_no_desktop): `--agent` found no ssh-agent, an agent without a key GitHub knows, or a Docker that is not Docker Desktop.
- [`CONNECT_AGENT_UNREACHABLE`](../troubleshooting.md#connect_agent_unreachable) and [`CONNECT_AGENT_EMPTY`](../troubleshooting.md#connect_agent_empty): the connection is saved, but Docker Desktop reaches no agent, or an agent with no key. Both exit 0.
- [`STATUS_PUSH_UNRESOLVED`](../troubleshooting.md#status_push_unresolved): a push ended with an unknown result. Check the branch on GitHub, then run `dockingbird connections --release`.
