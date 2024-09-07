---
title: Choose Active Envault Config
description: Command to select the Envault configuration to use
---

This command will scan for all of the `Envault` configuration files that are
present within all of the top level folders open in the current folder, and
show them to you in a list so that you can choose the one you would like to be
active.

When you select a configuration file, it will be parsed and used to make an
`Envault` request.

This command is always visible in the command palette, even if the current
window contains no configuration files. In such a case, trying to run the
command will display a message to that effect in the status bar.
