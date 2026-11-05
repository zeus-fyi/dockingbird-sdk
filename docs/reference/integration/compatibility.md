---
title: Compatibility, what you can build on
summary: The surfaces a script may rely on and the promise about how they change between releases.
audience: integrator
commands: []
---

> Part of the Dockingbird customer docs. The index for agents is [llms.txt](../../../llms.txt).

# Compatibility: what you can build on

The surfaces a customer may build on are:

1. `--json`: the envelope's keys and each message's `id`, `fields` and `exit_code` as the troubleshooting page
   ([the catalogue](../../troubleshooting.md)) lists the messages ([the envelope](json.md));
2. `dockingbird mcp`'s host tools, `agent_start`, `agent_list`, `agent_status`, `agent_send`, `agent_inbox`,
   `agent_read`, `agent_wait`, `agent_results`, `agent_stop`, `agent_set` and `agent_artifact_put`, by name and
   argument ([the tools](mcp.md));
3. the exit statuses 0, 1, 2, 69, 77 and 78 and the tools' own ([exit codes](exit-codes.md));
4. the files a customer writes: `.dockingbird/*.toml` configs ([the app config](../files/app-config.md)), `hosts.toml`
   ([its format](../files/hosts-file.md)), `org.toml` ([the org file](../files/org-file.md)), `fleet.toml` and a swarm
   definition at `schema = 1` ([its keys](../files/swarm-definition.md)).

The promise: a surface listed here changes only with a line in the release notes; an `id`, a field, a tool, an argument
or a file key is never removed or renamed in the release that announces it, only in a later one, so a script has one
release to follow; additions need no notice; a message's `lines` text and the GUI's drawing are never a surface.
