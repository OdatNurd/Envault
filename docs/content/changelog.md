---
title: Release History
description: The release history for Envault
---

# Changelog

## ^^0.0.2^^ - Small buxfixes (09/11/2024)

Fix an issue in logging related to error messages from the envault service if
keys are not valid. This would cause an error to be logged which is a string
that has `{` `}` in it, causing the logger to try to do a format operation,
when it should not. This is now fixed.

Additionally, augment the The [Envault: Show Variables](command/show_variables.md)
command so that choosing a variable will copy the value of that variable to the
clipboard.


## ^^0.0.1^^ - Initial Version (09/07/2024)

Initial version of the package, fleshed out during streams on my
[Twitch Channel](https://twitch.tv/odatnurd) as an initial version of the
package for [@axel669](https://github.com/axel669).

This version works, but currently requires that you run your own version of the
server since an official one is not yet available.
