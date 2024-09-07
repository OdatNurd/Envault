---
title: Show currently active Envault variables
description: Command to show the list of fetched Envault variables
---

This command will open a simple quick panel, showing the full name of the
currently active configuration file, and the list of variables that are being
applied as  a result of that configuration.

!!! note

    The panel shows only the list of variables, but not their values for security
    reasons.

If the configuration has no fetched variables (which includes if there was an
error making the `Envault` web request), no panel will be displayed and a
message will be displayed in the status bar instead.
