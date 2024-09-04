---
title: Configuring Envault
description: Available configuration settings for Envault
---

## Opening Settings

You can open the `Envault` settings by selecting `Preferences > Package
Settings > Envault > Settings` from the menu or by choosing the
`Preferences: Envault Settings` item from the command palette.

!!! info

    On MacOS, the `Preferences` menu is directly under the `Sublime Text` top
    level menu item

Package settings open in a new window, with the default settings displayed (and
un-editable) in the left hand pane and your user configuration in the right
hand pane.

To configure the package, simply copy the configuration item you would like to
edit from the left and paste it into the right, and customize. Your changes
will take effect as soon as you save the file.


!!! warning

    `sublime-settings` files are [JSON](https://www.json.org/json-en.html)
    formatted files (with the ability to have `// comments` and trailing commas
    to make your editing experience better). In order to avoid problems, your
    custom settings should be structured the same as the one on the left.


## Available Settings

Currently, `Envault` supports the following settings:


### "added_watch_commands"

- _Default_: `["exec", "terminus_exec", "terminus_open"],`

In normal use, `Envault` will seamlessly ensure that the desired custom
environment  variables are made available to any builds that are  executed from
within a window that has an active `Envault` configuration.

This setting allows for the configuration of additional commands that should
have environment variables set for them.

The default values here ensure that if you use a command palette entries or key
bindings that directly use the `exec` command to run a tool, that the
environment will be set. Additionally, they ensure that when using
[Terminus](https://packagecontrol.io/packages/Terminus), any terminals you open
within the window to run commands manually will also have the environment set.

!!! warning

    When customizing this setting, if you would like to keep any of the default
    values, ensure that you copy them to your user settings; otherwise your
    change will override the defaults

    Note also that `Envault` only supports augmenting the environment for a
    `WindowCommand`; that is, commands that can be used as a
    [custom build target](https://www.sublimetext.com/docs/build_systems.html#target).


### "debug"

- _Default_: `false`

When enabled, this setting causes `Envault` to send extra information on  what
it is doing to the Sublime Text console (visible via `View > Show Console` in
the menu or via the key binding you see mentioned there).

Generally speaking, you do not need to turn this on unless you're curious about
what the package is doing, or requested to do so by support.
