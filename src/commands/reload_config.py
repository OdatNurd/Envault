import sublime
import sublime_plugin

from ..envault_data import get_envault_config
from ..config_file import load_and_fetch_config
from ..logging import log


## ----------------------------------------------------------------------------


class EnvaultReloadConfigCommand(sublime_plugin.WindowCommand):
    """
    If the current window has an Envault configuration file already selected
    within it, reload the config from disk and re-fetch the appropriate
    environment to go with it.

    The command will disable itself when the current window does not have a
    selected configuration.
    """
    def run(self):
        # Get the current configuration file that's in use in the window, and
        # reload it
        config = get_envault_config(self.window)
        log(f"reloading envault config {config}")
        load_and_fetch_config(config)


    def is_enabled(self):
        return get_envault_config(self.window) != ''


## ----------------------------------------------------------------------------

