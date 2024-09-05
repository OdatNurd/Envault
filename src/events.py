import sublime
import sublime_plugin

from .settings import ev_setting
from .env_cache import fetch_env


## ----------------------------------------------------------------------------


class EnvaultEventListener(sublime_plugin.EventListener):
    """
    Listen for build commands that are either just about or or have just
    finished executing in the current window and, if required, update or
    restore the environment in the host.
    """
    def is_build(self, command, args):
        """
        Return a determination of whether the provided command is a valid build
        command for which we want to rewrite the environment or not.

        This is a build command that is not being used to set the build system
        that will be used to run the actual build later.
        """
        selecting = (args or {}).get('select', False)
        return command == "build" and not selecting


    def is_watched_command(self, command):
        """
        Check to see if the command provided is within the list of commands
        that the user has configured as one that should be watched, to extend
        how the environment gets extended.
        """
        return command in ev_setting("added_watch_commands")


    def execute_env_op(self, window, cmd, operation, env):
        """
        Execute the given environment update operation in both of the plugin
        hosts, using the environment dictionary provided.
        """
        env = fetch_env(window)
        for env_cmd in ('envault_internal_env_38', 'envault_internal_env_33'):
            window.run_command(env_cmd, {
                "command": cmd,
                "operation": operation,
                "env": env
            })


    def on_window_command(self, window, cmd, args):
        """
        If the command about to be executed in the window is a valid build
        command, then trigger the command that will update the plugin host
        environment before the command executes.
        """
        # We only care about build commands and watched commands
        if self.is_build(cmd, args) or self.is_watched_command(cmd):
            env = fetch_env(window)
            self.execute_env_op(window, cmd, "set", env)


    def on_post_window_command(self, window, cmd, args):
        """
        If the command that just `executed `in the window was a valid build
        command, then trigger the command that will restore the plugin host
        environment to what it was before the command originally executed.
        """
        # We only care about build commands and watched commands
        if self.is_build(cmd, args) or self.is_watched_command(cmd):
            self.execute_env_op(window, cmd, "restore", { })


## ----------------------------------------------------------------------------
