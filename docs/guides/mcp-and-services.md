---
title: MCP servers, services and browsers for agents
summary: Give agents an MCP server by URL, a program of yours with typed arguments, or a browser, and serve them as yourself.
audience: daily
commands:
  - connect --mcp
  - connect --service
  - connect --browser
  - serve
  - serve --all
  - serve --unit
  - watch
---

# MCP servers, services and browsers for agents

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

Agents can call an MCP server by its URL, run a program of yours with arguments you allow, and drive a browser. This page connects each one, then shows how `serve` runs the program or lends the browser as you, by hand or from a unit that starts at login. The model behind all of them is on [connections.md](connections.md).

## Before you start

- Dockingbird is set up. `dockingbird status` must not print "Dockingbird isn't set up yet."
- For a service, you hold the program, the checkout it lives in, and the commit that checkout is at. `git rev-parse HEAD` in the checkout prints the commit.
- For a browser of this Mac, you use a Mac with Google Chrome installed. Lending Chrome, Firefox or Safari works on a Mac only.
- For a browser in Docker, you need nothing on the Mac. The first start builds the browser's image once.

## An MCP server by URL

An MCP connection registers a streamable-HTTP server for the roles of a swarm that list its name in `connections`. Each of their agents gets the server's tools beside Dockingbird's own at every start.

```bash
dockingbird connect search --mcp https://mcp.example/mcp
```

The URL is `https`, with a lowercase host, an optional port, a path and a query, no user name and no fragment, at most 2048 characters. Dockingbird keeps nothing else, and a server that needs a key is not yet available. The catalogue lists no done line for this form. The step is done when the command exits 0 and `dockingbird connections` lists `search`.

## A program as a service

A service file says what runs and what an agent may choose. It must be a file of yours that only you can read, not a link, and not inside Dockingbird's folder. The file below is `convert.toml`.

```toml
# What dockingbird serve convert runs when an agent asks.
# The program, and the checkout it lives in at this commit (both or neither).
# serve will not run it once the checkout moved.
program = "/path/to/convert/bin/convert"
checkout = "/path/to/convert"
commit = "0123456789abcdef0123456789abcdef01234567"
# The most seconds one run may take; then it is stopped.
timeout_s = 600
# Its words: {output} is the folder it writes its result to (once),
# each {NAME} is an argument declared below.
argv = ["--pages", "{pages}", "--mode", "{mode}", "{output}"]

# A whole number from 1 to 500.
[arguments.pages]
type = "int"
minimum = 1
maximum = 500

# One of these words.
[arguments.mode]
type = "choice"
choices = ["fast", "best"]
```

| Key | Meaning |
|---|---|
| `program` | the program to run, with `checkout` and `commit` to pin the code it runs |
| `timeout_s` | most seconds one run may take, then `SIGTERM`, and `SIGKILL` 10 seconds later |
| `argv` | the program's words, each `{NAME}` replaced by a declared argument and `{output}` by the output folder |
| `uses` | the database connection whose credential each run gets, such as `uses = ["scores"]` |
| `[call]` | in place of `argv`, a Python function in the checkout, named by `python`, `module` and `function` |
| `[arguments.NAME]` | one argument an agent may fill in |

The same keys are listed in [the roles and connections reference](../reference/files/roles-and-connections.md).

| Argument `type` | Keys it takes | What the agent may send |
|---|---|---|
| `int` | `minimum`, `maximum` | a whole number between the two bounds |
| `choice` | `choices` | one word from the list |
| `text` | `max_chars` | text up to that many characters, passed on as typed |

A `text` argument reaches the program as the agent typed it. If the program reads one as a path or a command's name, the agent gains that reach. Declare `choice` or `int` where the program takes a path, a name or a mode.

1. Connect the file. Dockingbird checks every key, checks that `argv` uses each declared argument, and checks that the checkout is at the commit. It runs nothing.

   ```bash
   dockingbird connect convert --service ./convert.toml
   ```

   The step is done when the command prints these lines.

   ```text
   Connected convert: agents of a config that names it run /path/to/convert/bin/convert here, as you,
   with the arguments it declares, when you run dockingbird serve convert.
   A config that names it: connections = ["convert"]
   ```

2. Serve it. An agent of a config that names `convert` asks for a run with `bus_request`. Its request waits in `dockingbird status` until this runs.

   ```bash
   dockingbird serve convert
   ```

   The step is done when the command prints this line. Each request then prints how its run ended.

   ```text
   Serving convert: agents' requests to it run here, as you, one at a time.
   Ran convert for runner-1: done in 3 s.
   ```

A run starts the program alone, never through a shell. It gets the file's words with the checked arguments in place and runs in its checkout. It sees five variables and nothing else of your shell: `PATH`, your `HOME`, `LANG=C.UTF-8`, a `TMPDIR` of its own and `DOCKINGBIRD_SERVICE_OUTPUT`, the output folder's path. The output folder is the result. It holds what the program wrote plus `stdout.txt` and `stderr.txt`, at most 64 MiB and 10,000 entries, with links left out. It lands in the agent's log folder under `log/connections/<job>/`.

Before each run, `serve` checks the request again. It refuses a request that came too late or names a program or arguments the file does not allow. It also refuses when the checkout moved, or the program is gone, a link, or writable by anyone else. Ctrl-C, closing the terminal or ending `serve` stops the run, and the agent learns its request did not run.

A service that needs a database gets its credential through `uses`. The broker puts `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER` and `PGPASSWORD` into that run's environment alone, never into a file, a log or an agent. A `uses` that names more than one connection, or one that is not an enabled database, is declined before the run starts. The agent needs no grant on that database, because its grant is the service's. The worked case is [the database cookbook](../../examples/database-without-the-password/README.md).

## A browser of this Mac

```bash
dockingbird connect chrome --browser chrome
dockingbird serve chrome
```

An agent of a config that names `chrome` asks for the browser and waits until `serve` runs in a terminal on this Mac. `serve` lends it to one agent at a time, either your own browser with its logins, cookies and open tabs, or a fresh one that exists for that session alone. Each request picks, and your own is the default. `firefox` and `safari` work the same way after `connect NAME --browser firefox` or `--browser safari`.

| Browser | One-time set-up for your own profile |
|---|---|
| Chrome | open `chrome://inspect/#remote-debugging`, turn remote debugging on, keep Chrome running, and click Allow when it asks, which it does for each use |
| Firefox | quit Firefox before the first request; `serve` starts it with remote control on and closes it when `serve` stops, and a Firefox you opened by hand is refused |
| Safari | in Settings > Advanced turn on "Show features for web developers", then in Settings > Developer turn on "Allow Remote Automation" and "Allow JavaScript from Apple Events", and click OK when macOS asks |

In your own browser the agent can act as you on every site you are signed in to, and Dockingbird restricts nothing it does on any website. The browser loads pages with your Mac's network, so the agent's egress setting does not limit what it reaches there. A fresh browser has none of your logins and is removed afterwards. The agent keeps the browser until it lets go, its container ends, the browser closes, the session's time limit passes, or you press Ctrl-C.

Clicks, typing, scrolling and dragging are real mouse and keyboard input on this Mac when the browser has a window. That needs Accessibility for the app you run `serve` from, under System Settings > Privacy & Security > Accessibility. Start `serve` from Terminal. A `serve` started by an agent app counts as its own program, which no app's switch covers. A screenshot of your own Safari needs Screen Recording the same way. Moving the pointer into a corner of the screen stops an input.

The step is done when the command prints this line.

```text
Google Chrome is open for review-1 (own profile) until review-1 lets it go,
its container ends, or Ctrl-C.
```

## A browser of its own, in Docker

An added config with `browser = "chrome"` gives each of its agents a Google Chrome of Dockingbird's own. It runs headed on a virtual screen, in a container beside the agent's, behind the agent's egress proxy. No `connect` or `serve` is needed, nothing runs on your Mac, and none of your logins is in it. A repo's own config that asks for one is refused at its start.

```toml
command = "surf"
workspace = "scratch"
browser = "chrome"
egress = "allowlist"
allow = ["registries", "github"]
```

A start prints a line for each wait, then the agent runs.

```text
Building the agent's browser ... done ({elapsed})
Starting the agent's browser ... done ({elapsed})
```

`dockingbird watch surf-1` shows that screen in your VNC viewer, Screen Sharing on a Mac, and lets you take over. The address it prints, `vnc://127.0.0.1:<port>`, takes connections from this Mac alone. Anything you type or paste there, the agent can read. The command is done when it prints these lines, and `--no-open` prints the address and opens no viewer.

```text
Opening surf-1's browser, vnc://127.0.0.1:<port>, in your VNC viewer.
Anything you type or paste into this browser is visible to the agent surf-1,
which reads the page. Sign in to nothing you would not hand it.
VNC password: <the browser's own password>
```

## Serve every connection of a home

`dockingbird serve --all` serves every service and browser connection of the home in one process. `dockingbird serve --unit` prints the unit that keeps it running, a launchd property list on a Mac and a systemd user unit on Linux, and installs nothing. Save the text as the unit's file and install it the way your system does. A home started with a folder rather than a name needs `dockingbird --home NAME serve --unit`.

```bash
dockingbird serve --all
dockingbird serve --unit
```

`serve --all` never starts Docker or Dockingbird. While Docker does not answer, or no coordinator runs, it exits 1, and the unit starts it again every 10 seconds until they answer. `dockingbird stop` ends it with exit 0, and the unit leaves it stopped. Browsers are lent from a Mac only, so a Linux unit serves services.

## When it fails

- [`CONNECT_MCP_INVALID`](../troubleshooting.md#connect_mcp_invalid): the URL is not an `https` address with a lowercase host, no user and no fragment, or it is too long.
- [`CONNECT_SERVICE_INVALID`](../troubleshooting.md#connect_service_invalid): the service file is missing, readable by others, a link, too large, or holds a key to fix. The line names the key and never its value.
- [`CONNECT_SERVICE_CHECKOUT_MOVED`](../troubleshooting.md#connect_service_checkout_moved): the checkout is not at the file's commit. Check that commit out, or write the commit it is at.
- [`SERVE_NOT_A_SERVICE`](../troubleshooting.md#serve_not_a_service): the name is a GitHub repo, a folder or a database, which `serve` does not run.
- [`SERVE_CHECKOUT_MOVED`](../troubleshooting.md#serve_checkout_moved): the checkout moved since `connect`, and nothing ran. Connect the service again.
- [`SERVE_COORDINATOR_GONE`](../troubleshooting.md#serve_coordinator_gone): Dockingbird stopped while `serve` waited. Start `serve` again.
- [`SERVE_ALL_NONE`](../troubleshooting.md#serve_all_none): the home has no service or browser connection to serve.
- [`SERVE_UNIT_UNNAMED`](../troubleshooting.md#serve_unit_unnamed): the home has no name, so the unit cannot start it. Pass `--home NAME`.
- [`CONNECT_BROWSER_UNSUPPORTED`](../troubleshooting.md#connect_browser_unsupported): `--browser` takes `chrome`, `firefox` or `safari`.
- [`SERVE_BROWSER_MAC_ONLY`](../troubleshooting.md#serve_browser_mac_only) and [`SERVE_BROWSER_MISSING`](../troubleshooting.md#serve_browser_missing): the computer is not a Mac, or Chrome is not installed where the line says.
- [`SERVE_BROWSER_NOT_ENABLED`](../troubleshooting.md#serve_browser_not_enabled): Chrome's remote debugging is off. Turn it on once and the next request works.
- [`SERVE_BROWSER_ACCESSIBILITY`](../troubleshooting.md#serve_browser_accessibility): Accessibility is off for the app running `serve`, so the agent's clicks are refused while serving goes on.
- [`SERVE_FIREFOX_RUNNING`](../troubleshooting.md#serve_firefox_running): a Firefox you opened by hand holds the profile. Quit it.
- [`BROWSER_SIDECAR_FAILED`](../troubleshooting.md#browser_sidecar_failed) and [`BROWSER_NO_WINDOW`](../troubleshooting.md#browser_no_window): the agent's own browser did not start or showed no window. The start was undone, so run it again.
- [`BROWSER_STORE_NO_EGRESS`](../troubleshooting.md#browser_store_no_egress): the config installs Web Store extensions and the start's egress is `none`.
- [`WATCH_NO_BROWSER`](../troubleshooting.md#watch_no_browser): the agent has no browser in a container to watch. Its config asks for none, or the container stopped.
