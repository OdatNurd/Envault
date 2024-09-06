import sublime

from ..lib.bootstrap import bootstrap_legacy_package

from .config_file import load_and_fetch_config
from .config_status import set_status_config
from .envault_data import get_envault_config
from .logging import log


## ----------------------------------------------------------------------------


# On plugin load we add a settings listener so we can adjust the status bar in
# windows if the format string changes; this is the key used for that.
ENVAULT_SETTINGS_KEY="envault"


## ----------------------------------------------------------------------------


def scan_window_configs(fetch=False):
    """
    Scan over all windows and fetch the current envault config in use in that
    window and use it to update the status keys in the window to display the
    appropriate config in the desired format.

    If fetch is True and a config is found, the configuration will be fetched.
    Care is taken to only fetch each config once, in case the same config is
    in use in multiple windows at the same time.
    """
    fetched = set()
    for window in sublime.windows():
        config = get_envault_config(window)
        set_status_config(config, window)

        # If we found a config, we're supposed to fetch, and we have not tried
        # to fetch this one yet, then schedule that now.
        if config and fetch and config not in fetched:
            fetched.add(config)
            log(f"doing startup fetch for {config}")
            load_and_fetch_config(config)


## ----------------------------------------------------------------------------


def add_settings_listener():
    """
    Set up a settings listener that listens for changes being made to the
    settings of the package.

    When settings change, we re-scan the window configurations to ensure that
    if the user modified the format string for the status message, that all of
    the windows update with it.
    """
    log("adding settings listener")
    settings = sublime.load_settings("Envault.sublime-settings")
    settings.add_on_change(ENVAULT_SETTINGS_KEY, scan_window_configs)


def remove_settings_listener():
    """
    Remove the settings listener added by add_settings_listener(); this ensures
    that when the plugin unloads we don't keep that listener active, since that
    will cause each change to be handled multiple times.
    """
    log("removing settings listener")
    settings = sublime.load_settings("Envault.sublime-settings")
    settings.clear_on_change(ENVAULT_SETTINGS_KEY)


## ----------------------------------------------------------------------------


def loaded():
    """
    Invoked when the root plugin loads; this does any setup that is required
    when the package starts, which in our case here is to bootstrap out the
    command that is responsible for adjusting the environment into the Python
    3.3 plugin host so that we can support build targets from both versions of
    Sublime the same, and ensure that any restored windows that had envault
    configs have that config loaded.
    """
    log("initializing")
    add_settings_listener()
    bootstrap_legacy_package()
    scan_window_configs(fetch=True)


def unloaded():
    """
    Invoked when the root plugin is unloaded.
    """
    remove_settings_listener()


## ----------------------------------------------------------------------------
