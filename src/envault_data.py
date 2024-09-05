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


def get_envault_config(window):
    """
    Given a window, query it's envault configuration and return back the value
    for what the currently set envault configuration file is.

    If there is no file set, the empty string is returned.
    """
    envault = get_envault_data(window)
    return envault.get("current", "")


def set_envault_config(window, config):
    """
    Given a window, update it's envault data store to set the currently set
    configuration file to the one that is present here.

    If the window does not already have envault data, this will add it.
    """
    envault = get_envault_data(window)
    envault["current"] = config
    set_envault_data(window, envault)


## ----------------------------------------------------------------------------
