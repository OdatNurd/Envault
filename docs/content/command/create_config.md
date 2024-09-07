---
title: Create Envault Config File
description: Command to create an Envault configuration file
---

This command will provide a series of interactive prompts to create a brand new
configuration file. You can select any top level folder that is currently open
in the window as the place to save the file, provide the filename (with or
without an extension), and the file will be created.

If the `envault` configuration storage folder in the root of the project does
not exist yet, it will be created as a part of the file creation operation. In
addition, the newly created file is opened to allow you to make further edits.

The command will also prompt you as to whether you want to activate the new
configuration file after it is created; doing so allows every save of the file
to reload via [Envault: Reload Config](reload_config.md) unless the
[reload_config_on_save](../config/settings.md#reload_config_on_save) setting
has been turned off.


The generated configuration will include an `api` key populated by the
[default_api_key](../config/settings.md#default_api_key) setting and a `url`
key populated by the
[default_api_url](../config/settings.md#default_api_url) setting.
