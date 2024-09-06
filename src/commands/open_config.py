import sublime
import sublime_plugin

from ..envault_data import get_envault_config


## ----------------------------------------------------------------------------


class EnvaultOpenConfigCommand(sublime_plugin.WindowCommand):
    """
    If the current window has an Envault configuration file selected within it,
    open the file for editing.
    The command will disable itself when the current window does not have a
    selected configuration.
    """
    def run(self):
        # Get the current configuration file that's in use in the window, and
        # open it
        config = get_envault_config(self.window)
        self.window.open_file(config)


    def is_enabled(self):
        return get_envault_config(self.window) != ''


## ----------------------------------------------------------------------------

