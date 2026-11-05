---
title: Sign-in and API keys
summary: Reuse the Claude and Codex logins already on your computer, sign in again or as someone else, use an API key, and sign out.
audience: first-day
commands:
  - login claude
  - login claude --here
  - login codex
  - login claude --api-key
  - login codex --api-key
  - logout claude
  - logout codex
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Sign-in and API keys

Agents need a Claude or a Codex sign-in, and Dockingbird has three ways to give one. It can follow the login that your own Claude Code or Codex already holds on this computer. It can run a separate sign-in inside Docker. Or it can store an API key. Whichever you set up last is the one in use, and each step below ends with the line that proves it.

## Before you start

- Dockingbird is set up. `dockingbird --version` prints a version.
- For a sign-in, a terminal. `login` without one stops with `LOGIN_NEEDS_TERMINAL`, and an API key does not need a terminal.
- None of that tool's agents is running. `login` and `logout` refuse while they run. `dockingbird status` lists them.

## 1. Let the first start reuse your computer's login

The first start that needs a sign-in reads the login Claude Code or Codex already uses on this computer, keeps a copy in Dockingbird's store and follows it from then on. When it finds one, it says so.

```text
Claude uses this computer's login from now on (dockingbird logout claude stops that).
```

Message id `LOGIN_HERE_ADOPTED`. Claude's login is looked for in three places, in the order Claude Code uses them: a token in the `env` block of Claude Code's `settings.json`, the macOS Keychain item, then the login file `.credentials.json`. From `settings.json` only the token and its gateway address are read. For Codex it reads `auth.json`. When the computer has no login, the start runs the tool's own sign-in inside the agent's container: open the link it shows on this computer, sign in, and paste the code. Only the first time.

## 2. Use your computer's login on demand

```bash
dockingbird login claude --here
```

Run it again whenever you like; when nothing changed it says so. Done when the line prints.

```text
Claude uses this computer's login now, and Dockingbird follows it.
```

Message id `LOGIN_HERE_DONE`. The copy leaves out the refresh token, which never leaves your computer, so no agent can renew or sign out your login. Your own Claude Code or Codex keeps it fresh by being used. When Dockingbird is on, it copies a renewed login at once. A gateway in `settings.json` must be an `https://` address, or an address of this computer itself. Dockingbird refuses to send a token to any other plain `http://` gateway (`LOGIN_HERE_GATEWAY_NOT_HTTPS`). If macOS asks whether security may read the login, choose Always Allow.

## 3. Sign in again, or as someone else

```bash
dockingbird login claude
dockingbird login codex
```

This runs the tool's sign-in in a login container, for an expired or revoked sign-in or another account. The first line says what it will ask.

```text
Signing in to Claude. Open the link it shows, sign in, then paste the code here.
```

Message id `SIGNIN_START`. Codex shows a device code instead: open the link on this computer and enter the code. If Codex's device code login does not finish, turn on device code login in ChatGPT's security settings. Done when the line prints.

```text
Claude is signed in.
```

Message id `SIGNIN_DONE`. A sign-in that does not finish changes nothing, and names the API key route (`SIGNIN_FAILED`). Press Ctrl-C to quit one; only those two lines follow.

## 4. Reuse a sign-in you made elsewhere

For Claude, run `claude setup-token` in a terminal and copy the token it shows. For Codex, keep the file `auth.json` of a Codex sign-in.

```bash
pbpaste | dockingbird login claude --oauth-token -
cat auth.json | dockingbird login codex --auth-json -
```

Both forms read the value from the pipe only. It never appears in a command line, a log or a file on your computer. Clear the clipboard afterwards with `pbcopy < /dev/null`. Done when the line prints.

```text
Saved. Claude will use this token.
```

Message id `LOGIN_IMPORTED`. A Claude token is the subscription's credential, not an API key: `status` says "signed in". Both forms refuse while that tool's agents run.

## 5. Use an API key

```bash
dockingbird login claude --api-key
```

The command asks for an Anthropic API key and hides what you type. `dockingbird login codex --api-key` does the same for an OpenAI key. Without a terminal it reads the key from standard input.

```text
Paste your Anthropic API key (hidden):
```

Message id `API_KEY_PROMPT`. Done when the line prints.

```text
Saved. Claude will use this key; your Claude sign-in is not used.
```

Message id `API_KEY_SAVED`. While a key is saved, `dockingbird status` says "Claude uses an API key". The key goes from the prompt through a container's standard input into the tool's volume, mode 0600. It is never in an argument list, a container environment, a log or a file on your computer. An agent asks Dockingbird for its own tool's key at its start and cannot change it or read the other tool's. `--base-url URL`, with an `https://` address, sends that tool's requests to a gateway of yours. Give Codex's URL in the form of `OPENAI_BASE_URL`, ending in `/v1`.

A key the provider refuses is refused in seconds ("its provider refused the saved Claude key"), never after the tool's own timeout.

## 6. The last login wins

A plain `login` after `--api-key` removes the key once the sign-in succeeds.

```text
Claude is signed in. Your saved Claude API key is removed.
```

Message id `SIGNIN_DONE_KEY_REMOVED`. `--api-key` in turn replaces the sign-in, and either token form removes the saved key. The tool uses whatever you did last.

## 7. Sign out

```bash
dockingbird logout claude
dockingbird logout codex
```

This removes that tool's sign-in and saved API key from Dockingbird's store. When Dockingbird followed your computer's login, it stops following it and leaves your own login unchanged. Done when the line prints.

```text
Signed out of Claude. Dockingbird has no Claude sign-in or key now.
```

Message id `SIGNED_OUT`. With neither there, the line is `Claude wasn't signed in. Nothing to do.` (`LOGOUT_NOT_SIGNED_IN`, exit 0). A sign-out revokes nothing at Anthropic or OpenAI. If an agent may have copied the sign-in, also sign out in your account. To follow your computer's login again, run `dockingbird login claude --here`.

## Where the sign-in lives

Each tool has a Docker volume, `dockingbird-home-claude` and `dockingbird-home-codex`, that holds its credentials store and the saved key. Dockingbird itself mounts them. No agent does: an agent asks for its sign-in at its start and runs with a private home folder. An agent that works without a terminal takes a changed sign-in within about 20 seconds. Claude restarts between two tasks to use it and resumes its conversation. An agent at a terminal gets the new copy within the same time. Dockingbird writes nothing into your own Claude or Codex folders. See [data and privacy](data-and-privacy.md).

## When it fails

- A tool with no sign-in at a start gives [`SIGNIN_NEEDED`](../troubleshooting.md#signin_needed). The line names the command to run.
- Quitting the sign-in before it finishes ends with [`SIGNIN_FAILED`](../troubleshooting.md#signin_failed), which says nothing changed. Run the sign-in again or use an API key.
- A sign-in that finished but could not be stored prints [`SIGNIN_NOT_SAVED`](../troubleshooting.md#signin_not_saved). Run `login` again.
- `login` in a script, with no terminal, prints [`LOGIN_NEEDS_TERMINAL`](../troubleshooting.md#login_needs_terminal). Save an API key instead.
- Both `login` and `logout` refuse while an agent of that tool runs: [`LOGIN_AGENTS_RUNNING`](../troubleshooting.md#login_agents_running) and [`LOGOUT_AGENTS_RUNNING`](../troubleshooting.md#logout_agents_running) name the agent. Stop it, then run the command again.
- A computer with no Claude Code or Codex login gives [`LOGIN_HERE_NOT_FOUND`](../troubleshooting.md#login_here_not_found) for `--here`. Sign in with the tool itself first.
- A login that has expired gives [`LOGIN_HERE_EXPIRED`](../troubleshooting.md#login_here_expired). Use Claude Code once so it renews, then run `--here` again.
- A gateway in Claude Code's `settings.json` that starts with `http://` gives [`LOGIN_HERE_GATEWAY_NOT_HTTPS`](../troubleshooting.md#login_here_gateway_not_https).
- A piped token with spaces or an unreadable `auth.json` gives [`LOGIN_IMPORT_INVALID`](../troubleshooting.md#login_import_invalid).
- An empty key, or a Ctrl-C at the prompt, gives [`API_KEY_INVALID`](../troubleshooting.md#api_key_invalid). A key that could not be stored gives [`API_KEY_NOT_SAVED`](../troubleshooting.md#api_key_not_saved).
- When signing out stops half way, [`LOGOUT_FAILED`](../troubleshooting.md#logout_failed) says whether the saved key is still in use. Run `logout` again.
