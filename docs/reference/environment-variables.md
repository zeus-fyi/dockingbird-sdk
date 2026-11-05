---
title: Environment variables
summary: The DOCKINGBIRD_ variables you may set, how Dockingbird treats a setting, and the variables of other tools it reads.
audience: daily
commands:
  - dockingbird homes
  - dockingbird stop
  - dockingbird status
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../llms.txt).

# Environment variables

Settings reach Dockingbird through the shell that runs it, and each one is spelled `DOCKINGBIRD_` followed by its name.
Dockingbird hands every exported setting to the containers that read it, which is why a setting never sits at its default without you knowing.
Only one variable names a folder, `DOCKINGBIRD_HOME`, and one runtime setting, the database statement timeout, is documented by name.

## Variables you may set

| Variable | Values | Default | What it does |
|---|---|---|---|
| `DOCKINGBIRD_HOME` | an absolute path | `~/.local/share/dockingbird` | the folder of one Dockingbird installation, its home; another path gives a second, fully separate installation with its own containers, volumes and image tag |
| `DOCKINGBIRD_DB_QUERY_TIMEOUT_S` | a whole number within its bounds | its built-in value | how long one database statement may run, for the check of `connect --database` and for the agents' queries; `export DOCKINGBIRD_DB_QUERY_TIMEOUT_S=60` raises it |
| `DOCKINGBIRD_<NAME>` | a whole number within its bounds | its built-in value | any other runtime setting of Dockingbird: a poll interval, a timeout or a page size; the name is upper case and spelled exactly |

## What `DOCKINGBIRD_HOME` refuses

| Value or folder | Result |
|---|---|
| `/`, your home folder, or a folder above it | refused |
| a folder that holds native state (`operator.token`, `mode.json` or `pg`) | refused |
| an existing folder with files in it but no marker | refused; the empty `logs/` that `clean --all` keeps, your `instructions/` and `vaults/` folders, `versions.toml`, `config.toml`, `browser-solver.json`, `hosts.toml`, `fleet.toml` and Finder's `.DS_Store` do not count |
| a path with a space or `%$"'\` in it | not refused, but avoid it: `connect` passes a folder below it to ssh, which cannot take those characters |
| set together with `--home NAME` | exit 2: "--home and DOCKINGBIRD_HOME both name a home; use one of them." |

## How a setting behaves

| Case | Result |
|---|---|
| a value outside its bounds, or values that break a rule between settings | the command stops before it runs and names the variable, never its value |
| a name spelled in another case | the command stops before it runs, naming the variable |
| another variable that starts with `DOCKINGBIRD_` and that no command reads | the command stops before it does anything, exit 2, naming the variable |
| a setting of Dockingbird outside Docker (the database's address and roles, the developer's role switch, the host git's path) | the command stops the same way, since Docker mode never uses it |
| a setting changed while Dockingbird runs | the next command says "Dockingbird is running with other settings than this terminal's." and names `dockingbird stop`; the command after that starts Dockingbird with the new settings |
| `dockingbird status` after a change | shows the same lines under "Needs your attention" and restarts nothing |
| who sees a setting | the agents' harnesses read it too, none is a secret, and `docker inspect` shows them |

## Variables of other tools that Dockingbird reads

| Variable | Read by | What it does |
|---|---|---|
| `XDG_CONFIG_HOME` | the org login | when it is a path from `/`, `org.toml` lives in `$XDG_CONFIG_HOME/dockingbird/`; otherwise in `~/.config/dockingbird/` |
| `PGPASSFILE` | the org login and the fleet commands | names the PostgreSQL password file in place of `~/.pgpass`; it must be yours and readable by you alone |
| `DOCKER_HOST`, `DOCKER_CONTEXT` | every command that uses Docker | name the Docker daemon Dockingbird reaches, as for any docker command; Dockingbird otherwise uses the current context |
| `UV_INDEX_ZEUSFYI_USERNAME`, `UV_INDEX_ZEUSFYI_PASSWORD` | uv, at install | the index's user name (`license`) and your license key as its password; the key reaches uv in its environment only |
| `SHELL` | `dockingbird completion --install` | picks the shell whose completion script is written, unless you name one |

## Related

| Page | What it holds |
|---|---|
| [home-layout.md](files/home-layout.md) | what lives under `DOCKINGBIRD_HOME` and the `--home NAME` form |
| [org-file.md](files/org-file.md) | `org.toml`, `~/.pgpass` and the variables that move them |
| [commands.md](commands.md) | the global options, `--home` among them |
