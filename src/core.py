import sublime

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


def get_envault_data(window):
    """
    Given a window, return back the value of the envault configuration stored
    in the project data, if any. This includes not only windows that have an
    associated project, but also windows with anonymous project data that have
    at least one folder open.

    If there is no project data associated with the window, a default empty
    object is returned instead.
    """
    project_data = window.project_data() or {}
    return project_data.get("envault", {})


def set_envault_data(window, data):
    """
    Given a window and a new value to persist into the window for the envault
    configuration data, store that data into the project data in the window.

    This works both in windows with explicit projects or workspaces and also in
    windows with anonymous projects, so long as they have at least one folder
    open (Sublime does not persist the anonymous project data if there is no
    reason to do so).
    """
    project_data = window.project_data() or {}
    project_data["envault"] = data
    window.set_project_data(project_data)


## ----------------------------------------------------------------------------
