---
title: Reload the current Envault Config
description: Command to reload the current Envault configuration file
---

This command will reload and reparse the currently active configuration file in
the window, and cause a new `Envault` request to be made to fetch the list of
environment variables and their values.

As a time saver, while editing the currently active configuration file, a normal
`save` operation will cause this command to be automatically invoked to reload
the config.

!!! note

    The automatic reload of a configuration when the file is saved only applies
    when the file is saved from within Sublime Text; editing the file with an
    external editor (or file updates that happen as a result of source control)
    will not cause an automatic reload.

!!! warning

    Remember that environment variables are set at the time that a program is
    first launched! If you alter the current configuration file in a way that
    alters the names or values of environment variables, you will need to stop
    any running task and restart it for them to become available.
