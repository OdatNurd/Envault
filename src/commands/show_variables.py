import sublime
import sublime_plugin

from ..envault_data import get_envault_config
from ..env_cache import fetch_env

## ----------------------------------------------------------------------------


class EnvaultShowVariablesCommand(sublime_plugin.WindowCommand):
    """
    If the current window has an Envault configuration file already selected
    within it, show a quick panel that displays all of the variables that are
    currently in effect as a result of that configuration.

    The command will disable itself when the current window does not have a
    selected configuration.
    """
    def run(self):
        config = get_envault_config(self.window)
        env = fetch_env(config)

        def ignore(idx): pass

        self.window.show_quick_panel(list(env.keys()),
            placeholder=config,
            on_select=ignore)


    def is_enabled(self):
        return get_envault_config(self.window) != ''


## ----------------------------------------------------------------------------

