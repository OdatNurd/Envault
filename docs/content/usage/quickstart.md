---
title: Envault QuickStart
description: Getting up and running with  Envault
---

## Getting Started

This page describes getting up and running with the `Envault` service in a new
project. As seen in the steps below, if you already have a project that is
using Envault, you can skip the initial steps and
[get up and running faster](#switch-projects)!

The instructions here presume that you already have an `Envault` server URL and
associated API key to use to make requests; if you do not have that, set that
up first.

!!! note "The Envault service is not yet available"

    At the time of this writing, the `Envault` service itself is still under
    development and, as such, is not yet available. The code for the server is
    publicly available [on GitHub](https://github.com/axel669/envault) and can
    be deployed easily as a
    [Cloudflare Worker](https://developers.cloudflare.com/workers/) if you would
    like to experiment, however.


## Create a config file

To begin with, your project will need at least one
[envault config file](config_format.md) to use the `Envault` service. All
configuration files are [YAML](https://yaml.org/) files with a `.yml` extension
that live within a folder named `envault` at the root of your project.

The name of the file can be anything you like, and you can have as many files
as you might like; for example, for different deployment scenarios, or to be
able to easily swap between different variables or values.

Create a new configuration file using the
[Envault: Create New Config](../command/create_config.md) command from the
`Command Palette`. This will create a new stub configuration file and open it
for editing.

!!! tip

    When creating a config file, you can choose to automatically activate the
    file as soon as it is created. If you do this, you only need to save
    changes to the file to have them immediately take effect (unless you have
    turned off the
    [reload_config_on_save](../config/settings.md#reload_config_on_save)
    setting).


### Set initial configuration

The configuration that is created will look like the below (but note that there
are [settings](../config/settings.md) that can be used to alter the default
values of `apiKeyName` and `url` that are created):

```yaml
# Envault to request keys from, and the API key to use to authenticate the
# request. The API key provided here specifies the name of an environment
# variable whose value is the actual API key to use.
apiKeyName: envault_dev_key
url: http://localhost:8787/

# The list of variable specifications to request from the server; each spec
# will produce some number of environment variables and values. See the
# Envault server documentation for more information.
vars: []
#  - spec1
#  - spec2
```

Edit the configuration to use the appropriate `apiKeyname` and `url` if they
are not already correct; then, specify the variable sets that you would like to
use for this configuration.

The template generates an empty list with `[]`, but also includes an example of
specifying a list of keys.

!!! tip

    If you chose to activate the configuration as a part of the creation, then
    saving the file will cause it to automatically be re-loaded so that your
    changes take effect instantly! This can be controlled by the
    [reload_config_on_save](../config/settings.md#reload_config_on_save)
    setting if you prefer to manually refresh your configuration instead.


## Activate a config

If you did not choose to automatically activate the configuration when you
created it, choose the
[Envault: Choose Active Config](../command/choose_config.md) from the command
palette and select the configuration file to activate it.

"Activating" the configuration file will cause it to be parsed and loaded, and
will send off a request to the `Envault` server specified to collect the
variables.

Once activated, saving edits to the file will cause it to be automatically
reloaded, so that your changes take effect instantly. If you would rather have
the refresh operation be manual, turn off the
[reload_config_on_save](../config/settings.md#reload_config_on_save) setting;
you will need to use the [Envault: Reload Config](../command/reload_config.md)
command to reload.

The chosen configuration for a project will be stored directly within the
project information itself, and will be automatically selected and loaded for
you the next time you open the project.


## Edit a config

At any point, if you would like to see the contents of the configuration file or
make edits, you can easily open the file using the
[Envault: Open Current Config](../command/open_config.md) command, which will
open the configuration that is currently activated within the window.

From here, you can make edits as needed, which are automatically applied unless
you turned off the
[reload_config_on_save](../config/settings.md#reload_config_on_save) setting, in
which case you will need to use the
[Envault: Reload Config](../command/reload_config.md) command to manually
reload your changes when you're ready.


## Select a different config

If you have created other configuration files, you can easily select between the
various configuration files that are available by using the
[Envault: Choose Active Config](../command/choose_config.md) command to switch
between configurations.

Selecting a configuration will cause it to be reloaded and activated in the
window, replacing any previously activated configuration (if any).


## See defined env vars

The keys in the [configuration file](config_format.md) each specify a set of
environment variables and values that should be fetched down and applied to any
external tasks launched from within the window.

The [Envault: Show Variables](../command/show_variables.md) command will pop up
a list that shows you the full list of environment variables that are being
set as a result of the configuration that is active in the window.

!!! tip

    The displayed list shows only the name of the environment variables; the
    values are not displayed. This ensures that you do not accidentally leak or
    expose a secret.


## Launch tasks

Once a configuration is activated in the window, the environment variables that
it defines will be applied to any external task that is launched from within the
window via a standard
[build system](https://www.sublimetext.com/docs/build_systems.html).

If you use the  [Terminus](https://packagecontrol.io/packages/Terminus) package,
all terminals that you open in the window will also have the environment
variables set as well.

!!! tip

    In addition to the environment variables that are defined by the current
    configuration file, `Envault` also applies the following environment
    variables as well (unless the configuration defines them instead):

    `ENVAULT`

    :  Set to the value "1" to allow tooling and other external tasks that are
       launched to be able to tell that they are being run in an environment
       that has been adjusted by `Envault`

    `ENVAULT_CONFIG`

    :  The absolute path of the currently active configuration file, from which
       the remainder of the environment that is applied came from. This is
       useful as a debugging aid, to be able to determine what configuration was
       used to set the environment.

!!! tip

    By default, `Envault` handles builds that use the `exec` command as the
    build target (which is the default), as well as `terminus_exec` and
    `terminus_open`, which use the Terminus package to execute builds that you
    can interact with.

    If you are using a build with some other custom `target` key, you can adjust
    the value of the
    [added_watch_commands](../config/settings.md#added_watch_commands) setting
    to include your `target`.


!!! warning

    Remember that environment variables are set at the time that a program is
    first launched! If you alter the current configuration file in a way that
    alters the names or values of environment variables, you will need to stop
    any running task and restart it for them to become available.


## Switch Projects

When you open a project that already has one or more `Envault` configuration
files in it, one of three things will happen:

1. If you had previously already opened this project, the `Envault` config file
   that was last active will immediately be loaded and applied, so that you can
   pick up right where you left off.

2. If you open a project for the first time that has a single `Envault` config
   file in it, the config file will be automatically loaded and applied, so that
   you can get working without taking any further steps.

3. If you open a project for the first time that has more than one `Envault`
   config file in it, you will be prompted to select the configuration to apply
   as if you had manually selected the
   [Envault: Choose Active Config](../command/choose_config.md) command.


!!! note

    If, upon opening a project for the first time, you are prompted to select a
    config file, and you close the panel without choosing, you will need to
    manually select a configuration.

    This also applies to starting a new project which does not have a config
    file already within it; after creating the config file, you will need to
    manually activate it.
