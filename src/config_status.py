import sublime

from os.path import split, splitext
from os import sep

from .settings import ev_setting


## ----------------------------------------------------------------------------


# The status key that is used to provide information in the status bar of the
# window for the currently selected Envault configuration (if any).
CONFIG_STATUS_KEY="_envault_config"


## ----------------------------------------------------------------------------


def _clear_view_status_keys(view):
    """
    Clear all of the Envault status keys from the provided view.
    """
    view.erase_status(CONFIG_STATUS_KEY)


def _clear_window_status_keys(window):
    """
    Clear all of the Envault status keys from all views in the provided window.
    """
    for view in window.views():
        _clear_view_status_keys(view)


def _clear_keys(view_or_window):
    """
    Clear all of the Envault status keys from either all views in the window
    or just the specific view, depending on the type of view_or_window.
    """
    if isinstance(view_or_window, sublime.View):
        _clear_view_status_keys(view_or_window)
    else:
        _clear_window_status_keys(view_or_window)


## ----------------------------------------------------------------------------


def _set_view_config(view, config_str):
    """
    Set the configuration status key in the provided view to the given config
    string.
    """
    view.set_status(CONFIG_STATUS_KEY, config_str)


def _set_window_config(window, config_str):
    """
    Set the configuration status key for all views in the provided window to
    the given config string.
    """
    for view in window.views():
        _set_view_config(view, config_str)


def _set_config(view_or_window, config_str):
    """
    Set the configuration status key for either all views in the window or just
    the specific view to the string provided, depending on the type of
    view_or_window.
    """
    if isinstance(view_or_window, sublime.View):
        _set_view_config(view_or_window, config_str)
    else:
        _set_window_config(view_or_window, config_str)


## ----------------------------------------------------------------------------


def set_status_config(file, view_or_window):
    """
    Given the full name of an Envault configuration file, update the status bar
    to include an entry that says what configuration is currently set as active
    in the window.

    The status bar will update either for the passed in view, or for every
    view in the window, depending on whether view_or_window is an instance of
    a window or a view.

    If the config file provided is the empty string, the status key is removed
    instead of being added.
    """
    template_string = ev_setting("status_bar_format")

    # Erase keys if the incoming configuration file name is not provided, or if
    # the template string indicates that the user does not want to see any
    # status. The latter ensures that if the user adjusts the setting while a
    # config is active to remove the keys, they will be clobbered.
    if not file or not template_string:
        return _clear_keys(view_or_window)

    file_path, file_name = split(file)
    folder_root = file_path.split(sep)[-2]
    file_base_name, file_extension = splitext(file_name)

    variables = {
        "file": file,
        "folder": folder_root,
        "file_path": file_path,
        "file_name": file_name,
        "file_base_name": file_base_name,
        "file_extension": file_extension,
    }
    config_str = sublime.expand_variables(template_string, variables)

    _set_config(view_or_window, config_str)


## ----------------------------------------------------------------------------
