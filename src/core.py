import sublime

import textwrap

from ..lib.bootstrap import bootstrap_legacy_package


## ----------------------------------------------------------------------------


def loaded():
    """
    Invoked when the root plugin loads; this does any setup that is required
    when the package starts, which in our case here is to bootstrap out the
    command that is responsible for adjusting the environment into the Python
    3.3 plugin host so that we can support build targets from both versions of
    Sublime the same.
    """
    log("Initializing")
    bootstrap_legacy_package()

    ev_setting.obj = sublime.load_settings("Envault.sublime-settings")
    ev_setting.default = {
        # Template file actually lists some packages here.
        "added_watch_commands": [],

        "debug": False
    }


def unloaded():
    """
    Invoked when the root plugin is unloaded.
    """
    pass


## ----------------------------------------------------------------------------


def log(msg, *args, dialog=False, error=False, status=False, **kwargs):
    """
    Generate a message to the console and optionally as either a message or
    error dialog. The message will be formatted and dedented before being
    displayed, and will be prefixed with its origin.
    """
    msg = textwrap.dedent(msg.format(*args, **kwargs)).strip()

    if error:
        print("Envault error:")
        return sublime.error_message(msg)

    for line in msg.splitlines():
        print("Envault: {msg}".format(msg=line))

    if status:
        sublime.status_message(message)

    if dialog:
        sublime.message_dialog(msg)


def ev_syntax(file):
    """
    Return the full name of an Envault syntax based on the short name.
    """
    return "Packages/Envault/resources/syntax/%s.sublime-syntax" % file


def ev_setting(key):
    """
    Get an Envault setting from a cached settings object.
    """
    default = ev_setting.default.get(key, None)
    return ev_setting.obj.get(key, default)



## ----------------------------------------------------------------------------
