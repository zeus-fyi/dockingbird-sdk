---
title: Install fails
summary: Each way the install can stop, in the order you meet it, with what the screen shows and the fix.
audience: first-day
commands:
  - uv tool install
  - dockingbird --version
  - license activate
  - completion --install
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Install fails

This page follows the install from the first command to the first `dockingbird claude` and names every place it can stop. Each step gives what the screen shows, the message id when Dockingbird printed it, and the fix. Ids link to the [catalogue](../troubleshooting.md). Steps 1 to 3 happen before Dockingbird exists on the computer, so uv prints them and they carry no id.

## Before you start

| You need | The check | If it is missing |
|---|---|---|
| An Apple silicon Mac or arm64 Linux | `uname -m` prints `arm64` on a Mac and `aarch64` on Linux | Use another computer |
| uv | `uv --version` prints a version | `brew install uv` on a Mac |
| git at `/usr/bin/git` | `/usr/bin/git --version` prints a version | Install git |
| Docker Desktop, or Docker Engine with buildx on Linux | `docker version` and `docker buildx version` print versions | Install Docker |
| Your license key | The purchase email holds it | See the support page |

The install is done when uv exits 0 and this command prints a version.

```bash
dockingbird --version
```

## Step 1. A bare install

The command `uv tool install dockingbird` with no index installs a package of that name from the public index. That package is not Dockingbird. Nothing from Dockingbird prints, because the installed program is not ours.

Remove it, then run the full command from step 2.

```bash
uv tool uninstall dockingbird
```

## Step 2. A key that is wrong or revoked

The install command hands the key to uv as the index's password, through the environment.

```bash
UV_INDEX_ZEUSFYI_USERNAME=license UV_INDEX_ZEUSFYI_PASSWORD="$(pbpaste)" uv tool install dockingbird --index zeusfyi=https://license.zeus.fyi/simple/
```

A wrong, truncated or revoked key makes the release index answer with an HTTP 401. uv reports the refusal and installs nothing. Dockingbird is not on the computer yet, so no message id exists for this failure.

The fix has three checks.

1. Copy the key from the purchase email again. The `pbpaste` in the command reads whatever is on the clipboard, so a link or a copied sentence in its place fails.
2. On Linux, run `read -rs UV_INDEX_ZEUSFYI_PASSWORD`, paste the key, press Enter, and use `"$UV_INDEX_ZEUSFYI_PASSWORD"` in place of `"$(pbpaste)"`. Run `unset UV_INDEX_ZEUSFYI_PASSWORD` when uv is done.
3. If the key is right and the 401 stays, the license may have ended. See [SUPPORT.md](../../SUPPORT.md) for where to ask.

## Step 3. A trial

The index serves an active license only, so a trial cannot install from it. Install with a license key as in step 2, then run `dockingbird license activate`.

## Step 4. The command is not found

uv installed Dockingbird, but the shell does not know where uv puts programs. The shell prints its own "command not found".

```bash
uv tool update-shell
```

Open a new terminal, then run `dockingbird --version` again. The step is done when it prints a version.

## Step 5. Tab completion run twice

`dockingbird completion --install` adds tab completion. A second run is not a failure. It prints [COMPLETION_ALREADY](../troubleshooting.md#completion_already) and exits 0.

```text
Tab completion for {shell} was installed already; its script is current:
  {path}
  {rc} sources it
```

## Step 6. Activation stops

`dockingbird license activate` is the first command that reaches the license server. Three messages can stop it here.

- [LICENSE_KEY_IN_ARGV](../troubleshooting.md#license_key_in_argv) exits 2. You typed the key after the command. Nothing ran. Run `dockingbird license activate` alone and paste the key when asked.
- [LICENSE_KEY_INVALID](../troubleshooting.md#license_key_invalid) exits 1. The server does not know that key, or the text is not a key. Nothing changed. Copy the key again and rerun the command.
- [LICENSE_PLATFORM_UNSUPPORTED](../troubleshooting.md#license_platform_unsupported) exits 1. This computer is an Intel Mac, an x86 Linux machine or Windows.

The platform message reads like this.

```text
Dockingbird's license program runs on Apple silicon Macs and arm64
Linux, not on {platform}.
```

No fix exists on that computer. Dockingbird runs on Apple silicon Macs and arm64 Linux only. Use one of those, or an arm64 cloud VM.

When the server cannot be reached, the command prints [LICENSE_AUTHORITY_UNAVAILABLE](../troubleshooting.md#license_authority_unavailable) and changes nothing. Get online and run it again. The [licensing guide](../guides/licensing.md) lists the other license messages.

## Step 7. Docker is missing

The first `dockingbird claude` checks Docker before it builds anything.

[DOCKER_NOT_INSTALLED](../troubleshooting.md#docker_not_installed) exits 1 when no `docker` command exists. On a Mac it prints this.

```text
Dockingbird needs Docker Desktop. Install it, then run this again:
  https://www.docker.com/products/docker-desktop/
```

On Linux it names `https://docs.docker.com/engine/install/` instead. Install Docker, then run the command again.

[DOCKER_NOT_RUNNING](../troubleshooting.md#docker_not_running) exits 1 when Docker is installed but did not start in time. Start Docker Desktop and run the command again.

[DOCKER_BUILDX_MISSING](../troubleshooting.md#docker_buildx_missing) exits 1 when Docker has no buildx plugin. Docker Desktop includes it, so update Docker Desktop. On Linux, install Docker's `docker-buildx-plugin` package.

## Step 8. git is missing

The prerequisite is git at `/usr/bin/git`. The catalogue holds no message for a missing git, so the check is yours: `/usr/bin/git --version` must print a version. Install git so that `/usr/bin/git` exists, then run `dockingbird claude` again.

## When it fails

| Message id | What it means and the fix |
|---|---|
| [COMPLETION_ALREADY](../troubleshooting.md#completion_already) | Informs only, exit 0. |
| [LICENSE_KEY_IN_ARGV](../troubleshooting.md#license_key_in_argv) | Paste the key when asked. |
| [LICENSE_KEY_INVALID](../troubleshooting.md#license_key_invalid) | Copy the key again. |
| [LICENSE_PLATFORM_UNSUPPORTED](../troubleshooting.md#license_platform_unsupported) | Use Apple silicon or arm64 Linux. |
| [LICENSE_AUTHORITY_UNAVAILABLE](../troubleshooting.md#license_authority_unavailable) | Get online, then run it again. |
| [DOCKER_NOT_INSTALLED](../troubleshooting.md#docker_not_installed) | Install Docker. |
| [DOCKER_NOT_RUNNING](../troubleshooting.md#docker_not_running) | Start Docker. |
| [DOCKER_BUILDX_MISSING](../troubleshooting.md#docker_buildx_missing) | Install the buildx plugin. |

The cookbook [recover from a failed install](../../examples/recover-from-a-failed-install/README.md) runs the three main failures with their fixes. The next failure a reader meets is [the first start stops](first-start-stops.md), and the one after is [a license refused](licence-refused.md).
