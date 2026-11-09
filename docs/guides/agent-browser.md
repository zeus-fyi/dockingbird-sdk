---
title: An agent's own browser
summary: Give an agent a full Google Chrome of its own in a container, turn it on in an added config, watch and take over its screen, and see how it ends with the agent.
audience: daily
commands:
  - config add
  - watch
  - status
  - stop
---

# An agent's own browser

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

An added config with `browser = "chrome"` gives each of its agents a headed Google Chrome of Dockingbird's own. Chrome runs on a virtual screen in a container beside the agent's, called the sidecar. Nothing runs on your Mac, and none of your logins is in it. This page turns it on, lists what a page sees and what the agent can do, and shows `watch`, extensions, the local network list and how the sidecar ends with its agent.

A browser of your Mac, lent through `connect --browser`, is another route, covered in [the MCP servers, services and browsers guide](mcp-and-services.md). [The connections guide](connections.md) compares the two.

## Before you start

- Docker runs, and Dockingbird is set up. `dockingbird status` must not print "Dockingbird isn't set up yet."
- The config is a file you add with `dockingbird config add PATH`. A config that lives in a repo's own `.dockingbird/` and says `browser` is refused when the agent starts, so a repo cannot give itself a browser.
- A swarm role cannot have a sidecar: `browser` is not a role key. Start the agent from a config command instead.

## Turn it on

Write the config. The example runs a command called `surf` in an empty scratch folder, behind an allowlist.

```toml
command = "surf"
workspace = "scratch"
browser = "chrome"
egress = "allowlist"
allow = ["registries", "github"]
```

Add it, then start the command with a task.

```bash
dockingbird config add agents/surf.toml
dockingbird surf "Open the status page of our service and tell me what it says"
```

The first start of a new Dockingbird version builds the browser stage of the image once. Every start then waits while the sidecar starts. The lines show while each step runs and end with how long it took.

```text
Building the agent's browser ... done ({elapsed})
Starting the agent's browser ... done ({elapsed})
```

The agent starts after the second line, and the start is done when `dockingbird status` lists surf-1. A config you change takes effect for agents you start after you add it again. Agents already running keep the config they started with.

| Key | Values | What it does |
|---|---|---|
| `browser` | `chrome` | the sidecar. Only a config you added may name it, and a command may set its own |
| `browser_extensions` | a list | Chrome extensions to install. See [Extensions and policies](#extensions-and-policies) |
| `[browser_policy]` | a table | Chrome policies by Google's names. See the same section |
| `egress`, `allow` | as in any config | how far the agent and its browser reach, which [the egress guide](egress-and-network.md) explains |
| `tools` | `bus`, `default` or `full` | not needed: a config with a browser has the browser tools whatever it says |

[The config keys page](../reference/files/app-config.md) lists every key. The 14 tools the agent gets are on [the agent tools page](../reference/agent-tools.md).

## What runs

The sidecar is its own container, `dockingbird-browser-NAME`, made from the browser stage of Dockingbird's image. It runs an X screen, a window manager, Chrome, and a small service that listens on a Unix socket.

- The agent's container and the sidecar share one Docker volume, `dockingbird-browser-sock-NAME`, and the socket lives in it. The agent never sees Chrome's screen or its debugging port, and Dockingbird publishes no port.
- The sidecar joins the agent's network and, under `allowlist` or `models`, goes through the agent's proxy. The agent's egress setting bounds the browser too. Under `none` the browser has no network.
- Under `full` there is no proxy, so the browser reaches your Mac's loopback services through `host.docker.internal`, as any `full` agent can.
- The sidecar starts and says it is ready before the agent's container is created. Dockingbird waits up to 180 seconds for that line.
- Chrome opens `file://` addresses of its own container, which hold the VNC password that `watch` uses, and the agent can read what Chrome shows of them. Nothing of your Mac is in that container.

## What a page sees

| Item | Value |
|---|---|
| Browser | Google Chrome on Linux: `navigator.platform` is `Linux x86_64` and the client hint `Sec-CH-UA-Platform` is `Linux` |
| `navigator.webdriver` | `false` |
| Screen | 1440 by 900 pixels |
| WebGL | none, as on a Linux computer with no supported GPU; a page that needs it shows its fallback |
| Fonts | Latin, Greek and Cyrillic, Chinese, Japanese and Korean, Arabic, Hebrew, Thai, Devanagari, Bengali, Tamil, Armenian and Georgian, and emoji |
| Time zone and language | your computer's: the zone follows `TZ` and the language follows `LANG`, so a German Mac gives pages `de-DE` |
| Input | real mouse and keyboard events on the virtual screen, so a page sees `isTrusted: true` |

Dockingbird spoofs no other identity. A site can tell this browser from the Chrome on a Mac.

## What the agent can do

The agent opens pages, reads a page's url, title, visible text and visible form fields (never a field's value), clicks, types, presses keys, hovers, scrolls, drags and takes a screenshot. Each click and key moves along a human path at a person's pace. With a vault connection, it signs in with a stored login without seeing the password, which [the secrets vault guide](secrets-vault.md) sets up. `browser_cdp` sends any Chrome DevTools Protocol method for what the other tools do not cover. `browser_release` lets the browser go. The screenshot is a PNG in the agent's log folder, and the tool answers its path.

[The agent tools page](../reference/agent-tools.md) lists every tool with its arguments and its answer.

## Watch and take over

`dockingbird watch NAME` shows the sidecar's screen in your VNC viewer, Screen Sharing on a Mac, and lets you take over. NAME is an agent whose config asks for a browser and that is running.

```bash
dockingbird watch surf-1
```

The command is done when it prints these lines and opens the viewer.

```text
Opening surf-1's browser, vnc://127.0.0.1:<port>, in your VNC viewer.
Anything you type or paste into this browser is visible to the agent surf-1,
which reads the page. Sign in to nothing you would not hand it.
VNC password: <the browser's own password>
```

- The address takes connections from this Mac and nothing else, one at a time. Screen Sharing connects once to ask for the password and again to sign in.
- The password Dockingbird prints belongs to the browser alone. It is not a password of yours.
- The agent reads the page, so a password you type there is a password you hand over.
- While you move the mouse or type, the agent's input waits a moment, and its tool says so.
- Close the viewer or press Ctrl-C to stop.
- `dockingbird watch surf-1 --no-open` prints the address and the password and opens nothing.

## Extensions and policies

An added config with `browser = "chrome"` can add extensions and Chrome policies. A repo's own config that names either key is refused, as one that names `browser` is, and either key with no `browser` is refused too.

```toml
browser = "chrome"
browser_extensions = [
  "https://chromewebstore.google.com/detail/ublock-origin-lite/ddkjiahejlhfcafbddmgiahcphecmpfh",
  "/path/to/my-extension",
]

[browser_policy]
URLBlocklist = ["file://*"]
```

- An entry is a Chrome Web Store link, a bare 32-letter extension id, or an absolute folder (starting with `/` or `~/`) that holds a `manifest.json`.
- `config add` packs each folder as an extension signed with a key it keeps under `configs/.extension-keys`. The same folder keeps its id whichever config names it, and a folder you move gets a new key and a new id. Names that start with a dot are left out, and the command says how many. After a change to a folder or to the lists, run `config add` again: the packed copy is what runs.
- Chrome downloads Web Store extensions at each start, so a start with egress `none` is refused with [`BROWSER_STORE_NO_EGRESS`](../troubleshooting.md#browser_store_no_egress). Under `allowlist` or `models`, the proxy admits `clients2.google.com` and `clients2.googleusercontent.com`, and the agent can reach them too, which the start says.
- These policies are refused because they would cut Dockingbird's control of the browser: `RemoteDebuggingAllowed`, `DeveloperToolsDisabled`, `DeveloperToolsAvailabilityAllowlist`, `DeveloperToolsAvailabilityBlocklist`, `ProxyMode`, `ProxyServer`, `ProxyPacUrl`, `ProxyBypassList`, `ProxySettings`, `ProxyServerMode`, `UserDataDir`, `ExtensionInstallForcelist` and `ExtensionSettings`. `DeveloperToolsAvailability` may be 0 or 1 only.
- A command may set its own list or table, which replaces the config's.
- Chrome's menu shows "Managed by your organization".
- An extension that never starts stops the browser, and the start fails with [`BROWSER_EXTENSIONS_NOT_RUNNING`](../troubleshooting.md#browser_extensions_not_running), which names it.

`dockingbird status surf-1` shows the agent's extension ids in an `extensions` row, and one `policy` row for each policy with its state as Chrome's own policy page showed it: applied, not applied with Chrome's words, or not on the page. The start also names the policies Chrome did not apply, with [`BROWSER_POLICY_NOT_APPLIED`](../troubleshooting.md#browser_policy_not_applied).

## The local network list of the computer

Chrome 142 and later asks before a page on the internet sends a request to your local network or to the loopback address of this computer. A sign-in provider's page may call a local app that way. Nobody can answer Chrome's question inside a sidecar.

Write the patterns of the pages that may do it in a file called `browser.toml` in Dockingbird's data root, `~/.local/share/dockingbird/browser.toml`. It has one key.

```toml
local_network_access = ["[*.]example.com"]
```

- Patterns use Chrome's URL pattern format. The file holds at most 32 patterns, each at most 512 printable ASCII characters with no space.
- Every agent with a browser that you start on this computer after that, in any home, gets the list as Chrome's managed policy `LocalNetworkAccessAllowedForUrls`, followed by any policies its config names in `[browser_policy]`. `dockingbird status NAME` shows whether Chrome applied it.
- Dockingbird never writes the file. You do.
- A file that cannot be read, is not TOML, holds a key other than `local_network_access`, or lists something that is not a Chrome URL pattern refuses every start of an agent with a browser with [`BROWSER_SETTINGS_INVALID`](../troubleshooting.md#browser_settings_invalid). Fix the file or remove it to give Chrome no list.
- The temporary Chrome that `serve` starts on your Mac does not get the list, since macOS has no policy for one Chrome process.

## How it ends with its agent

The sidecar runs only while its agent runs.

1. The start makes the socket volume, then the sidecar, and waits for its ready line.
2. The agent's container is created and started.
3. When the agent ends or you run `dockingbird stop surf-1`, the agent's container goes first. Then Dockingbird stops the sidecar, removes it, and removes the socket volume. If a removal fails, the sweep that later commands run removes what is left.
4. If Chrome stops while the agent uses it, the agent's next browser call is refused and the sidecar's container stops. [`BROWSER_EXITED`](../troubleshooting.md#browser_exited) says how it ended and quotes the last line it wrote.

### A sidecar that runs an older version

`dockingbird update` switches a running agent to the new Dockingbird version in place, at its next stopping point, as [the updates guide](updates.md) describes. The sidecar is not part of that switch: it keeps the version it started with until its agent starts again. `dockingbird status` then prints a line under the agents.

```text
surf-1's browser and proxy run Dockingbird 0.15.27 since surf-1 started; they take 0.15.28 at surf-1's next start.
To take 0.15.28 now:
dockingbird stop surf-1, then start the agent again
```

The line is [`STATUS_SIDECAR_BEHIND`](../troubleshooting.md#status_sidecar_behind). Nothing is wrong with the agent, and the browser keeps working. To take the new version, run `dockingbird stop surf-1`, then start the agent again. The line goes once its agents end or take the new version.

## When it fails

| Message | What happened | What to do |
|---|---|---|
| [`BROWSER_SIDECAR_FAILED`](../troubleshooting.md#browser_sidecar_failed) | the sidecar's container did not start or did not say it was ready in time; the message shows its last log lines, or what Docker said | everything the start made was removed, so run the same command again |
| [`BROWSER_NO_WINDOW`](../troubleshooting.md#browser_no_window) | Chrome showed no window on its screen within the time the message names, or showed one and did not answer the agent's connection; Chrome and its screen were stopped | the message quotes Chrome's last line, and the agent's browser tools then say the browser is unavailable |
| [`BROWSER_SETTINGS_INVALID`](../troubleshooting.md#browser_settings_invalid) | the computer's `browser.toml` is unreadable or holds something other than `local_network_access` | fix or remove the file |
| [`BROWSER_STORE_NO_EGRESS`](../troubleshooting.md#browser_store_no_egress) | the config installs Web Store extensions and the start's egress is `none` | start with `allowlist`, `models` or `full`, or remove the store entries and add the config again |
| [`BROWSER_EXTENSIONS_NOT_RUNNING`](../troubleshooting.md#browser_extensions_not_running) | an extension the message names did not start in time, so the browser was stopped | check the folder or link of that extension, then add the config again |
| [`BROWSER_VNC_UNAVAILABLE`](../troubleshooting.md#browser_vnc_unavailable) | `watch` could not open the view: the screen's password file is missing, or the viewer's server refused | the message names which of the two failed, and nothing is shown |

The full catalogue of browser messages is in [the troubleshooting catalogue](../troubleshooting.md), and [the connection messages](../troubleshooting/connections.md) list them by domain.

## Not built

Firefox and Safari do not run in the sidecar. The sidecar runs Chrome only, and `browser_bidi` and `browser_webdriver` work on a browser your Mac lends through `connect --browser`.
