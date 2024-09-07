---
title: Configuring Envault
description: Available configuration settings for Envault
---

## Opening Package Settings

You can open the `Envault` settings by selecting
`Preferences > Package Settings > Envault > Settings` from the menu or by
choosing the `Preferences: Envault Settings` item from the command palette.

!!! info

    On MacOS, the `Preferences` menu is directly under the `Sublime Text` top
    level menu item, as is standard for applications on this platform.

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
    custom settings should be structured the same as the default settings file
    on the left of the preferences window.


## Available Settings

Currently, `Envault` supports the following settings, shown here with
explanations of what they do and their default values.


### ^^default_api_key^^

- _**Type**_: String
- _**Default**_: `"envault_dev_key"`

When using the command to [create a config file](../command/create_config.md)
for your project, this value is used to fill out the `apiKeyName` portion of
the `Envault Config File`.

If you have a default API key that you use, you can set it here so that when
you create configuration files, they're already set up. The default is used as
a placeholder in generated configuration files to ensure the structure of the
configuration is correct.


### ^^default_api_url^^

- _**Type**_: String
- _**Default**_: `"http://localhost:8787/"`

Similar to `default_api_key`, the value of this configuration value is used
when you [create a config file](../command/create_config.md) for your project
to fill out the `url` portion of the
[envault config file](../usage/config_format.md).


### ^^reload_config_on_save^^

- _**Type**_: Boolean
- _**Default**_: `true`

When this file is enabled, saving an
[envault config file](../usage/config_format.md) that is currently loaded in a
window will cause the file to be immediately reloaded as if you used the
[reload config](../command/reload_config.md) command.

In combination with the command to
[open the current config](../command/open_config.md) or
[create a config file](../command/create_config.md), this setting makes it easy
for you to make changes to your configuration and have it be immediately
available.


### ^^status_bar_format^^

- _**Type**_: String
- _**Default**_: `"[Envault: ${file_base_name}]"`

When an `Envault` configuration is active within a current window, the status
bar will contain a text segment that indicates tells you what configuration
file is currently active.

This configuration variable controls what that text looks like, allowing you to
customize it as you would like. The following variables are allowed:

`$file`

:  The absolute path of the currently active config file; this will
   include the full path and extension on the file:
   `/home/username/project/envault/config.yml`.

`$file_path`

:  The absolute path of the currently active config file, without
   the filename portion: `/home/username/project/envault`.

`$file_name`

:  The name of the configuration file, including the extension,
   but without any path: `config.yml`

`file_base_name`

:  The name of the configuration file, but without the
   extension: `config`

`$file_extension`

:  The extension of the configuration file: `.yml`

`$folder`

:  the name of the folder (without any parent folders) that contains the
   `envault` configuration files; useful if you have multiple folders open in
   the project and you want to disambiguate which one is currently being used:
   `project`



!!! note

    If you do not want to have an indication of the active configuration in the
    window, set this to an empty string.


### ^^added_watch_commands^^

- _**Type**_: List of Strings
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
    change will override the defaults, which might not be what you want.

    Note also that `Envault` only supports augmenting the environment for a
    `WindowCommand`; that is, commands that can be used as a
    [custom build target](https://www.sublimetext.com/docs/build_systems.html#target).


### ^^debug^^

- _**Type**_: Boolean
- _Default_: `false`

When enabled, this setting causes `Envault` to send extra information on  what
it is doing to the Sublime Text console (visible via `View > Show Console` in
the menu or via the key binding you see mentioned there).

Generally speaking, you do not need to turn this on unless you're curious about
what the package is doing, or requested to do so by support.
