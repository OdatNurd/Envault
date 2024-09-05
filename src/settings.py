import sublime


## ----------------------------------------------------------------------------


def ev_setting(key):
    """
    Get an Envault setting from a cached settings object.
    """
    if getattr(ev_setting, "obj", None) is None:
        ev_setting.obj = sublime.load_settings("Envault.sublime-settings")
        ev_setting.default = {
            # Template file actually lists some packages here.
            "added_watch_commands": [],

            "default_api_key": "envault_dev_key",
            "default_api_url": "http://localhost:8787/",

            "debug": False
        }

    default = ev_setting.default.get(key, None)
    return ev_setting.obj.get(key, default)


## ----------------------------------------------------------------------------
