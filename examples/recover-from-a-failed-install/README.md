---
title: Recover from a failed install
summary: Check the platform, remove a bare install, install with the key, and fix the three failures: no index, a wrong key and a wrong platform.
audience: first-day
commands:
  - uv tool install
  - dockingbird --version
  - license activate
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Recover from a failed install

This cookbook gets a computer from a failed install to a working `dockingbird` with an activated seat. It covers the three failures a first install meets: no index, a wrong key and a wrong platform. Each step ends with the line that shows it worked.

## Before you start

- Your license key is in the purchase email. The clipboard holds it on a Mac. Check with `pbpaste | wc -c`, which prints a number above zero.
- uv is installed. Check with `uv --version`. On a Mac, `brew install uv` adds it.
- git exists at `/usr/bin/git`. Check with `/usr/bin/git --version`.
- Docker Desktop, or Docker Engine with buildx on Linux, is installed. Check with `docker buildx version`.

## 1. Check the platform

Dockingbird runs on Apple silicon Macs and arm64 Linux.

```bash
uname -m
```

The step is done when it prints `arm64` on a Mac or `aarch64` on Linux. On `x86_64`, stop here. An Intel Mac, an x86 Linux machine and Windows are not supported, and the first `dockingbird license` command on one prints this.

```text
Dockingbird's license program runs on Apple silicon Macs and arm64
Linux, not on {platform}.
```

That is [LICENSE_PLATFORM_UNSUPPORTED](../../docs/troubleshooting.md#license_platform_unsupported), exit 1. The fix is another computer: an Apple silicon Mac, or an arm64 Linux machine or cloud VM.

## 2. Remove a bare install

A command without the index, `uv tool install dockingbird`, installs a package of that name that is not Dockingbird. Remove it.

```bash
uv tool uninstall dockingbird
```

The step is done when uv exits 0. If you never ran the bare command, skip it.

## 3. Install with the key

On a Mac, with the key on the clipboard, run this.

```bash
UV_INDEX_ZEUSFYI_USERNAME=license UV_INDEX_ZEUSFYI_PASSWORD="$(pbpaste)" uv tool install dockingbird --index zeusfyi=https://license.zeus.fyi/simple/
```

On Linux, read the key without echo, run the command with it, then unset it.

```bash
read -rs UV_INDEX_ZEUSFYI_PASSWORD
UV_INDEX_ZEUSFYI_USERNAME=license UV_INDEX_ZEUSFYI_PASSWORD="$UV_INDEX_ZEUSFYI_PASSWORD" uv tool install dockingbird --index zeusfyi=https://license.zeus.fyi/simple/
unset UV_INDEX_ZEUSFYI_PASSWORD
```

The step is done when uv exits 0. A wrong, truncated or revoked key makes the index answer with an HTTP 401, and uv installs nothing. Dockingbird is not on the computer yet, so uv prints that failure and no message id exists for it. Copy the key from the email again and repeat the step. A trial cannot install from the index.

## 4. Check the version

```bash
dockingbird --version
```

The step is done when it prints the Dockingbird version. If the shell says the command is not found, run this, then open a new terminal and repeat the check.

```bash
uv tool update-shell
```

## 5. Activate the computer

```bash
dockingbird license activate
```

Paste the key when it asks. The input is hidden. The step is done when the product prints this line, then the terms line and the count of linked computers.

```text
This computer is activated: {plan}, {seats:seat|seats}, {term}.
```

Typing the key after the command is refused with exit 2. The refusal is [LICENSE_KEY_IN_ARGV](../../docs/troubleshooting.md#license_key_in_argv). Run the command with no argument.

## When it fails

| Message id | What it means and the fix |
|---|---|
| [LICENSE_PLATFORM_UNSUPPORTED](../../docs/troubleshooting.md#license_platform_unsupported) | This computer is not Apple silicon or arm64 Linux. Use another one. |
| [LICENSE_KEY_IN_ARGV](../../docs/troubleshooting.md#license_key_in_argv) | Paste the key when asked. |
| [LICENSE_KEY_INVALID](../../docs/troubleshooting.md#license_key_invalid) | The server does not know the key. Copy it again. |
| [LICENSE_SEATS_FULL](../../docs/troubleshooting.md#license_seats_full) | Every computer the license admits is linked. See [move your seat](../move-your-seat/README.md). |
| [LICENSE_AUTHORITY_UNAVAILABLE](../../docs/troubleshooting.md#license_authority_unavailable) | The license server was out of reach. Get online and run the command again. |
| [DOCKER_NOT_INSTALLED](../../docs/troubleshooting.md#docker_not_installed) | Install Docker, then run `dockingbird claude` again. |

The longer story, with Docker and git, is on [install fails](../../docs/troubleshooting/install-fails.md).
