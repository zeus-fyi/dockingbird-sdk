---
title: Sign agents in with a password vault
summary: Connect a gopass store so Dockingbird types a login's password and one-time code into an agent's browser, in its own Docker browser or on your Mac's Chrome, and the agent sees neither.
audience: daily
commands:
  - connect --vault
  - connect --browser
  - config add
  - serve
  - watch
  - connections
  - disconnect
---

# Sign agents in with a password vault

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

An agent that browses may need to sign in to a site. With a vault connection, the agent names a login, and Dockingbird types the stored password and the current one-time code into the page itself. This page makes the gopass store, connects it, and gives an agent a browser to sign in with. The model behind it is on [connections.md](connections.md).

There are two routes, and both use the same store and the same `browser_login` tool.

| Route | The browser | What you run |
|---|---|---|
| the agent's own browser | the Chrome in a container beside the agent, from `browser = "chrome"` in an added config | `connect --vault`, then `config add`; no `serve` and no Chrome on your Mac |
| your Mac's Chrome | a temporary Chrome that `dockingbird serve` lends the agent | `connect --vault`, `connect --browser chrome`, `config add`, then `serve` |

## Before you start

- Dockingbird is set up. `dockingbird status` must not print "Dockingbird isn't set up yet."
- Sign-ins work in Chrome only in this release, and Firefox and Safari requests are refused in words.
- For the Mac route, you use a Mac with Google Chrome, and the browser connection exists or you make it in Route 2. [mcp-and-services.md](mcp-and-services.md) covers lending Chrome. The agent's own browser route needs no Chrome on your Mac.
- A passphrase for the store is ready. Dockingbird asks for it on your terminal, hidden, and keeps it inside Dockingbird the way it keeps a database password.

## Steps

1. Install gopass 1.17.4, the version Dockingbird's image carries. The release is `gopass-1.17.4-darwin-arm64.tar.gz` at `https://github.com/gopasspw/gopass/releases/tag/v1.17.4`. Check its checksum before you open the archive, then put the `gopass` program it holds on your `PATH`.

   ```bash
   shasum -a 256 gopass-1.17.4-darwin-arm64.tar.gz
   ```

   The step is done when the command prints this checksum.

   ```text
   b052f36631e619fa9391edeee581d1f3937c4c41d432aa4ba673b53401800c0f  gopass-1.17.4-darwin-arm64.tar.gz
   ```

2. Make the store once, in the `vaults/logins` folder of your Dockingbird home. That is `~/.local/share/dockingbird/vaults/logins` unless you set `DOCKINGBIRD_HOME`, and then it is the `vaults/logins` folder there. The command makes the store with an age identity under your passphrase. A bare `gopass init` fails, because it needs an identity first.

   ```bash
   export GOPASS_HOMEDIR=~/.local/share/dockingbird/vaults/logins
   export GOPASS_AGE_PASSWORD="<the passphrase>"
   gopass setup --crypto age --storage fs
   ```

   Keep the whole folder that `setup` made, including its `.config` and `.cache`, because the reads need them. The step is done when the folder exists and holds those two.

3. Insert each login, with the same two environment variables set. Type the password on the first line. For a site with two-factor sign-in, paste the `otpauth://totp/...` line from the enrolment page below it. An entry that holds a counter-based `otpauth://hotp/...` line is refused when it is used.

   ```bash
   gopass insert alice
   ```

   The step is done when `gopass ls` lists `alice`.

4. Connect the store. Each `--login` takes three words. The first is a slug such as `alice`, which is both the agent's word for the login and the store entry's name. The second is the site's origin, `https://host` or `https://host:port`. The third is the username. `--totp NAME` marks a login whose entry holds a code. `--store NAME` picks another folder under `vaults`.

   ```bash
   dockingbird connect logins --vault gopass --login alice https://site.example alice@site.example --totp alice
   ```

   Dockingbird checks each word and that the store is a real folder of yours there. It then asks for the passphrase and prints these lines.

   ```text
   Passphrase for the gopass store logins (hidden):
   Connected logins: a gopass vault with 1 login.
   Configs that name logins may sign in to those sites.
   Add it to a config: connections = ["logins"].
   ```

5. Give the agent a browser, by one of the two routes below.

## Route 1: sign in in the agent's own browser

An added config that says `browser = "chrome"` and names the vault in `connections` gives each of its agents a Chrome of Dockingbird's own, in a container beside the agent's, and lets the agent sign in there. You lend no Chrome, run no `connect --browser` and no `serve`. Both keys count only in a config you added with `dockingbird config add`, and a repo's own config that asks for them is refused at its start.

```toml
command = "surf"
workspace = "scratch"
browser = "chrome"
connections = ["logins"]
```

```bash
dockingbird config add surf.toml
```

Start an agent of that config as usual. Dockingbird starts a small process on your computer, a courier, beside the agent's browser. The courier carries each sign-in into the browser through Docker, so no network port opens for it. The step is done when the agent's first sign-in adds these two lines to `logs/browser-login-<agent>.log` in your Dockingbird home, which is `~/.local/share/dockingbird/logs/` unless you set `DOCKINGBIRD_HOME`.

```text
Signing in with a vault login in the agent's browser tab <target> ...
The sign-in in the agent's browser tab <target> ended: <detail>
```

The log names no password and no code. The vault must be in the config before the agent starts. A vault granted later to a running agent cannot start a courier into a browser that is already running, so the agent's sign-in request is refused in words that name the config's `connections`. Start the agent again with the vault in its config.

While the courier types, the browser refuses the agent's other commands in words, for at most 300 seconds (`BROWSER_LOGIN_HOLD_S`). Past that the sign-in is stopped and its fields are cleared. The agent's browser takes one sign-in at a time, and a sign-in never overlaps a CAPTCHA solve. If you use the browser through `dockingbird watch` while it types, the typing pauses, the sign-in ends refused, and the fields are cleared. Wait until no one is watching, then ask the agent to sign in again.

## Route 2: sign in on your Mac's Chrome

1. Connect the browser.

   ```bash
   dockingbird connect chrome --browser chrome
   ```

2. Name both connections in a config you add, then serve the browser. Until `serve` runs, an agent's sign-in request waits.

   ```toml
   command = "surf"
   workspace = "scratch"
   connections = ["logins", "chrome"]
   ```

   ```bash
   dockingbird config add surf.toml
   dockingbird serve chrome
   ```

   Each sign-in prints a line in the `serve` terminal. It names the agent, the site and the login, never the username, the password or the code. The step is done when one appears.

   ```text
   surf-1 signed in to https://site.example as alice for chrome: <how the typing went>
   ```

## List what the vault holds

The listing names the logins and shows no site, username, password or code.

```bash
dockingbird connections logins
```

The step is done when the output holds this line.

```text
logins: gopass vault, 1 login: alice
```

## How a gopass secret reaches an agent

It does not. The password and the code take these steps, and the agent takes none of them.

1. The store is a folder of yours under `vaults`. Dockingbird reads it from its own side, read-only, with the gopass that its image carries, and runs no gopass on your Mac.
2. The store's passphrase stays inside Dockingbird, the way a database password does. No command asks for, reads or shows a password or a code.
3. When an agent asks for a sign-in, Dockingbird reads the entry, checks the page's site against the login's, and types the value into the browser itself.
4. The agent gets one answer in words, success or a refusal, and never the value or its length.

The value passes through you (when you insert it), Dockingbird's coordinator (gopass), the courier or `serve`, the typing process and Chrome. It is not in the agent's container, its transcripts, receipts, logs, command lines or environment. On Route 1, one limit remains: under `full` egress, an agent that reads the browser's VNC password through a `file://` page and reaches `dockingbird watch` can see the typing tab while it types. See [egress-and-network.md](egress-and-network.md) for the other modes.

[connections.md](connections.md) covers how `connect` registers and grants every kind of connection, and [mcp-and-services.md](mcp-and-services.md) covers lending a browser.

## What an agent can and cannot do

The agent asks for one sign-in at a time, with `browser_login`, by the login's name and the address of the sign-in page on that site. That is all it must give. Dockingbird finds the username, password, code and submit fields the request leaves out, in a separate script context that the page's own scripts cannot reach, and checks each one it finds as it checks one the agent names. The agent may still name a field by CSS selector when Dockingbird misses it. `browser_read` lists a page's visible fields, without their values, on Chrome. A sign-in waits up to 30 seconds for a login form that the page draws after it loads.

The agent is told success or a refusal in words. A refusal says the page is not on the login's site, the field is not a password field, the vault is unreadable, or the site did not accept the sign-in. When no field was found, it adds the page's title and the number of input elements on it, so the agent can tell a wrong page from a wrong field. It is never told the password, the code, or how long either is. The tab stays signed in until the browser session ends with the agent.

The agent cannot read, list, add or change a login or the store. It cannot sign in on your own Chrome profile. Sign-ins run only in a temporary profile with Chrome's password manager off, so Chrome's save-password offer and your Google account never see the password. While a sign-in is typed, the agent's other browser commands are refused in words until it ends.

## Sites with several steps

A sign-in that moves the page to a new address is settled by what the new page shows after it loads. The form gone is a success. The form shown again is a failed sign-in, and a new page that does not load within the sign-in's bound is a failed sign-in that says "the next page didn't load". This holds for single sign-on pages that put each step in the address.

When the sign-in reached a new page, the answer's tab is that page, with its history cleared, so the agent sees the step it reached: the second factor, the site, or the form again with the site's error. A page that holds a password field is never handed over, so the agent's own tab is moved to it instead. When the sign-in changed no address, the agent's own tab stays signed in and the agent reloads it. The answer ends with words such as "the agent was handed the tab the sign-in reached" or "the agent's tab was moved to the page the sign-in reached", and never names the page's address, which may carry a token.

## A code entered on its page

For a login marked `--totp`, the agent makes one `browser_login` call with the login and the address alone. Dockingbird types the password, follows the page to the code page in the same tab, reads the current code from the store at that moment, and types it. The agent never clicks through the code page itself. After the code, it clicks yes to a device question. If the site asks for no code, because the browser is remembered, the sign-in ends as a success that says "no code page came".

Without more setup the code page must be on the login's own site. Nothing is typed or clicked outside the sites the sign-in allows.

### A code page on another site

A code page that another site hosts needs two options of `connect --vault`, which `connect --help` does not list. Both name a login that `--totp` marks.

| Option | What it holds | Rule |
|---|---|---|
| `--code-origin ALIAS ORIGIN` | the origin of the page that asks that login's code | `https://host` or `https://host:port` with nothing after it; once per login |
| `--reveal ALIAS TEXT` | the visible text of one control to click before the code field shows | up to 4 per login, in the order you give them; each 1 to 64 characters, with no control character and no space at either end |

```bash
dockingbird connect logins --vault gopass \
  --login alice https://site.example alice@site.example --totp alice \
  --code-origin alice https://sso.provider.example \
  --reveal alice "TEXT OF THE FIRST CONTROL" \
  --reveal alice "TEXT OF THE SECOND CONTROL"
```

The typist widens the allowed sites to the code origin only once the password was submitted. It clicks the reveal controls only while the page is at the code origin, then types the code and hands the agent that tab. A login with a code origin refuses a separate code step, with words that send the agent to the one-call sign-in. When the code field never shows, the sign-in ends `field-not-code` with `reveal step N of M was not on the page`, or `clicked M of M reveal steps`. A sign-in that ends on the code origin, such as the provider's question about the browser, says "the sign-in ended at the code origin: read the tab".

A name that is already connected with other words is refused as `CONNECTION_CONFIG_CHANGED`. Run `dockingbird disconnect logins`, then the `connect` again, to replace it. A `--code-origin` or `--reveal` that names a login `--totp` does not mark is refused as `CONNECT_VAULT_INVALID`, as are a second `--code-origin` for one login, a code origin that is no origin, and a list of reveal steps outside the rule above. Nothing is saved then.

## Addresses with a `#` part

An address copied from a page with its `#` part is a valid sign-in address, for example `https://site.example/#/login`. Dockingbird reads the site from the text before the first `#` and opens the address whole in the typing tab. Every check that blocks a wrong site still runs. `browser_open` answers `loaded: true` at once for a move inside the same document, where it used to wait 30 seconds. The origin you store with `--login` is a site, never a page, so it takes no `#`.

## After an update

The typing runs in the agent's browser container and in `serve`. A new release's sign-in changes reach a running agent only when that agent starts again, and a `serve` process only when it starts again. The agent's MCP tools arrive at its next switch.

## Remove it

`dockingbird disconnect logins` removes the connection and the passphrase Dockingbird kept. The store stays yours to delete. `dockingbird clean --all` keeps your `vaults` folder whenever anything is in it, and prints this.

```text
Kept the stores of your vault connections: <path>
Delete that folder yourself if you no longer want them.
```

## When it fails

- [`CONNECT_VAULT_INVALID`](../troubleshooting.md#connect_vault_invalid) names the word refused before the passphrase was asked. Nothing was saved. The causes are a manager other than `gopass`, a store folder that is missing or a link, and a login name outside lowercase letters, digits and hyphens. An origin with a path after it, an empty username, a `--totp` that matches no login and a repeated name are refused too, and so are the faults of `--code-origin` and `--reveal` listed above.
- [`CONNECT_VAULT_PASSPHRASE_SHORT`](../troubleshooting.md#connect_vault_passphrase_short) means the passphrase was empty or not text Dockingbird can keep. Type it at the question, or pipe it in.
- [`SERVE_BROWSER_LOGIN_REFUSED`](../troubleshooting.md#serve_browser_login_refused) reports, in the `serve` terminal of Route 2, a sign-in that was refused or not accepted, with the reason the agent was told.
- [`BROWSER_LOGIN_WATCH`](../troubleshooting.md#browser_login_watch) is the line of Route 1's courier log for a sign-in's start and end, and for the courier's own end when the browser container stops answering. Nothing to do unless a sign-in ended otherwise than you expected: the line says why.
- [`BROWSER_LOGIN_CHANNEL_FAILED`](../troubleshooting.md#browser_login_channel_failed) means the channel between the agent's browser and your computer failed. The browser was started without a vault in its config, its service is gone, or Docker could not be started. Start the agent again to get a new browser and courier.
- [`SERVE_VAULT_FOLDER_FAILED`](../troubleshooting.md#serve_vault_folder_failed) says Dockingbird could not make its `vaults` folder, or found a link or another user's folder there. Check the path and its disk.
- [`SERVE_BROWSER_MAC_ONLY`](../troubleshooting.md#serve_browser_mac_only) means the computer is not a Mac, so Route 2 cannot lend a browser.
