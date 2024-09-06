import sublime


## ----------------------------------------------------------------------------


def ev_setting(key):
    """
    Get an Envault setting from a cached settings object.
    """
    if getattr(ev_setting, "obj", None) is None:
        # Note: the core also loads this settings file so that it can add
        #       a setting listener without causing a circular reference in
        #       other code; if you change the config file name, change it there
        #       too.
        ev_setting.obj = sublime.load_settings("Envault.sublime-settings")
        ev_setting.default = {
            "status_bar_format": "[Envault: ${file_base_name}]",

            # Template file actually lists some packages here.
            "added_watch_commands": [],

            "default_api_key": "envault_dev_key",
            "default_api_url": "http://localhost:8787/",

            "reload_config_on_save": True,

            "debug": False
        }

    default = ev_setting.default.get(key, None)
    return ev_setting.obj.get(key, default)


## ----------------------------------------------------------------------------
