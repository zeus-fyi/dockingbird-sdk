---
title: Data and privacy
summary: What leaves your computer when you use Dockingbird, where its data is kept, and the commands that show it.
audience: daily
commands:
  - license status
  - egress
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Data and privacy

This page lists what leaves your computer when you use Dockingbird, where each kind of data is kept and how to see it. It lists every kind of traffic the documentation names. For what an agent can reach and what it cannot, see [the security model](../concepts/security-model.md).

## Before you start

- Dockingbird is set up. `dockingbird --version` prints a version.
- You know which egress mode your agents use. `dockingbird egress` prints it.

## What leaves the computer

| Traffic | To whom | When |
|---|---|---|
| The agent's own tool, Claude Code or Codex, sending its requests | Anthropic or OpenAI, or the gateway you set with `--base-url` | Whenever an agent works, under your sign-in or your API key |
| The tool's sign-in | The tool's own sign-in hosts | When you sign in |
| Downloads of Claude Code and Codex | Their vendors | The first start of each tool, and `dockingbird update` |
| Dockingbird's own releases | Zeusfyi's release index, with this computer's activation as the password | `dockingbird update` and `update --check` |
| License actions | Zeusfyi's license server | `license activate`, `license trial`, `license status --refresh`, `license activations`, `license deactivate`, and `clean --all`, which gives the seat back first |
| The license client download | Zeusfyi, checked against a SHA-256 Dockingbird pins | The first `license` command |
| The image build | Pinned public base images and Ubuntu packages, pulled without your login | The first start and a rebuild after an update |
| A fetch or a push of a connection's branch | The hosts of the connections you registered | Only when an agent asks for it and a config names that connection |

Dockingbird pushes no image to a registry, and its own pulls need no login. Licensing sends nothing from a repo or an agent to Zeusfyi, and Zeusfyi's privacy note lists what it does send. The note is not yet published in this repository.

### Licensing in this release

This release does not enforce licensing. A start reaches no network for licensing and downloads no license client. It runs the license client only when one is already on the computer. The daily check-in that an enforced start would make, and the refusals that follow it, are not yet available. Until then the only license traffic is what you start yourself with a `license` command.

### What an agent can send

An agent reaches the network by its egress mode, which you set with [egress and network](egress-and-network.md).

| Mode | What an agent reaches |
|---|---|
| `allowlist` | Its tool's own hosts, the presets and hosts you allow, through a proxy that sees only host names and ports |
| `models` | Its tool's own hosts alone |
| `none` | Nothing, the model API included |
| `full` | The whole network, with no list. This is Dockingbird's default |

Under `full`, a hijacked agent can send out the repo it works on and its own Docker sign-in or key to any host. `dockingbird egress allowlist` closes that for the agents you start afterwards. An agent can read its own tool's sign-in or saved key and cannot change it. It cannot read the other tool's, and nothing it does touches your computer's own sign-in. Your claude.ai connectors, such as Gmail and Drive, never load in an agent in any mode.

## Where data is kept

| Data | Where | Notes |
|---|---|---|
| Your repo's history in each agent's copy | The Docker volume `dockingbird-state` | Never on your computer's disk as a folder you open |
| Sign-ins and saved API keys | The Docker volumes `dockingbird-home-claude` and `dockingbird-home-codex` | A key is mode 0600, never in an argument list, a container environment, a log or a file on your computer |
| Files an agent attached | `DOCKINGBIRD_HOME/results/<agent>/` | Mode 0700, files 0600 |
| Each agent's log | `logs/agents/<name>-<stamp>.log` | Dockingbird's own events, never the tool's output |
| Unexpected errors | `logs/dockingbird.log` | Redacted, rotated |
| The license | `license.json` in `DOCKINGBIRD_HOME` | The license document, this computer's id and label, the last check-in, the terms accepted and the download token; mode 0600 |
| Your connections' keys | A Docker volume, never the folder | An agent asks for a fetch or a push, never for the key |
| Links and refs in your checkout | `branch.<branch>.dockingbird` in `.git/config` and `refs/remotes/dockingbird/<branch>` | `clean --all` removes them |

Docker runs every Dockingbird command with its own configuration folder, so your saved registry logins and credential helper are never used. A `proxies` setting of yours reaches every container Dockingbird creates, with any user name and password in the proxy URL.

## How to see it

```bash
dockingbird license status
dockingbird license status --refresh
dockingbird egress
```

`license status` reads the license file with no network. Done when the line prints.

```text
Licensed: {plan}, {seats:seat|seats}, {term}.
```

Message id `LICENSE_SHOWN`. `--refresh` checks in with Zeusfyi first, so it is the one status command that sends something. `dockingbird egress` prints what new agents may reach and whether `egress.toml` sets it.

```text
Egress for new agents: full.
Nothing is set: this is Dockingbird's own default.
```

Message id `EGRESS_SHOWN`. `dockingbird status` repeats it as `Egress for new agents: full`. To remove what Dockingbird made, `dockingbird clean --all` removes the containers, volumes, images and files, and your code stays untouched. See [clean and uninstall](clean-and-uninstall.md).

## When it fails

- [`LICENSE_AUTHORITY_UNAVAILABLE`](../troubleshooting.md#license_authority_unavailable): the license server did not answer.
- [`LICENSE_CLIENT_DIGEST_MISMATCH`](../troubleshooting.md#license_client_digest_mismatch): the downloaded client did not match its pinned checksum; nothing was kept.
- [`EGRESS_FILE_INVALID`](../troubleshooting.md#egress_file_invalid): `egress.toml` cannot be read, so no new agent starts until you fix or reset it.
