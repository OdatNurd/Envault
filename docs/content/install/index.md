---
title: Installing Envault
description: Installing the Envault package for Sublime Text
---

# Installing Envault

## Requirements

`Envault` supports all builds of Sublime Text across Windows, MacOS and Linux,
but requires `Sublime Text Build >=4095+` in order to work properly.


## Package Control

!!! warning

    Currently, this package is under development as the `Envault` service grows
    and evolves, and as such has not yet been officially released to
    `Package Control`.

    If, when you follow the instructions below, you do not see the `Envault`
    package, select the `Package Control: Add Repository` command from the
    command palette and enter the following URL, and then retry the
    installation:

        https://raw.githubusercontent.com/STealthy-and-haSTy/SublimePackages/master/unreleased-packages.json


The fastest and easiest way to install `Envault` is via
[Package Control](https://packagecontrol.io/), the de-facto package manager for
Sublime Text. Package Control not only installs your packages for you, it also
ensures that they are kept up to date to make sure that you always have the
benefit of the latest bug fixes and features for all of your installed
packages.

To install Envault using this method, open the command palette in Sublime
(++shift+ctrl+p++ on Windows/Linux or ++shift+cmd+p++ on MacOS) and
select the `Package Control: Install Package` command, then select `Envault`
from the list of packages.

If you are new to Sublime Text and don't have Package Control installed yet,
you'll have to do that first. Sublime Text has an option in the `Tools` menu
named `Install Package Control...` that will install Package Control for you,
while older versions require you to follow the installation instructions here.

!!! info

    If you do not see the menu option to install `Package Control`, you may
    have already installed it; the menu item hides itself when Package Control
    is installed.




## Manual Installation

If you're unable to use Package Control to install `Envault`, it's also
possible to perform a manual installation by cloning the package source from
its [GitHub repository](https://github.com/OdatNurd/Envault) into your local
`Packages` directory, which you can locate by selecting the `Browse Packages`
command from the command palette or from the `Preferences` menu.

This method of installation is more complicated and requires that you have a
knowledge of `git` and how to use it in order to install the package.

!!! warning

    If you install Envault manually, it will be up to you to ensure that
    you check for and install any upgrades that may exist to ensure that your
    version of the package is up to date.

    For this reason, it is highly recommended that you **NOT** install manually
    unless you have a compelling reason or need to do so.
