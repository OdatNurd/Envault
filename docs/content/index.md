---
title: Envault for Sublime Text
description: Sublime Text package for working with the Envault service in your projects
---

# About Envault

[Envault](https://github.com/axel669/envault) is a service envisioned by fellow
developer and Twitch Streamer [@axel669](https://github.com/axel669) to make it
easier to set up and use `environment variables` to configure applications and
tooling, both during development and also during deployment.

Traditionally, one would create one or more `.env` files to set such
environment variables. However, this runs the risk of accidentally checking
such files into source control, which can disastrously leak secret information.
Additionally, sets of related projects may have a common configuration
required, which can be not only painful to set up, but also to keep up to date
as shared values change.


## Purpose

The `Envault` service resolves these problems by having a per-project
configuration file that is intended to be checked into source control, which
contains the information required for the `Envault` service to provide the
required information to set up the environment.

This package attempts to make this functionality seamless while working in
Sublime Text by allowing you to easily select the configuration file that is to
be used, and ensuring that the environment variables specified by that config
are always applied, whether running a
[Sublime Text Build](https://www.sublimetext.com/docs/build_systems.html) or
using [Terminus](https://packagecontrol.io/packages/Terminus) to open a terminal
to run interactive commands.

The package currently requires Sublime Text build 4095 or higher.