import sublime
import sublime_plugin

from ..logging import log

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

        if not env:
            return log(f"current configuration contains no variables", status=True)

        items = list(env.keys())

        primary = 'cmd' if sublime.platform == 'osx' else 'ctrl'
        self.window.show_quick_panel(items,
            placeholder=f'{primary}+enter to copy variable value to the clipboard',
            on_select=lambda idx,evt: self.pick(idx, evt, env, items),
            flags=sublime.QuickPanelFlags.WANT_EVENT)


    def pick(self, idx, evt, env, items):
        """
        On a pick that was not a cancel and where the key used to select the
        item included the primary key for the platform (ctrl on Linux/Windows
        or cmd on MacOS), copy the value of that variable to the clipboard.
        """
        if idx == -1:
            return

        if evt["modifier_keys"].get("primary") is None:
            return log(f"key value not copied", status=True)

        key = items[idx]
        value = env[key]
        sublime.set_clipboard(value)
        log(f"Copied value of '{key}' to the clipboard", status=True)


    def is_enabled(self):
        return get_envault_config(self.window) != ''


## ----------------------------------------------------------------------------

