---
title: Using Envault
description: Using Envault to do the thing that it does
---

## Overview

This package is a [Sublime Text](https://www.sublimetext.com) package for the
overall [Envault](https://github.com/axel669/envault) service being written by
[@axel669](https://github.com/axel669).

The goal of the service itself is to make it easier and more secure version of
`.env` files, allowing you to easily set up a set of environment variables that
are needed for development tasks, automated deployments, and so on and **_keep
those files safely in source control without leaking anything_**.

Standard `.env` files are typically not stored in source control because to do
so would be to leak potentially sensitive information. This leaves you open to
accidental checkins that leak data, and also loses you a key piece of project
setup documentation, making onboarding of new developers more difficult.

In use, you create one or more [configuration files](config_format.md) that
describe the sets of environment variables that you need, and the `Envault`
service safely and securely stores the variables and their values. Since the
configuration file contains only the names of sets of variables to download and
not the variables themselves (and, crucially, not their actual **_values_**),
you can safely add the files to source control.


## The Envault Package

This package is a [Sublime Text](https://sublimetext.com) package for
interfacing with the `Envault` service, and aims to make it as painless as
possible to use Envault in projects without a minimum of fuss.

Commands are provided to easily
[create a configuration file](../command/create_config.md) and
[activate it](../command/choose_config.md). From there, all
[build systems](https://www.sublimetext.com/docs/build_systems.html) that you
run will automatically have the appropriate environment variables applied to
them; they will even be applied if you use the
[Terminus](https://packagecontrol.io/packages/Terminus) package to open a
Terminal directly within Sublime.

The configuration file that you select is remembered on a per-project basis and
will be automatically activated when you restart Sublime or reload the project
itself.
