import sublime
import sublime_plugin


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


    def on_window_command(self, window, command, args):
        """
        If the command about to be executed in the window is a valid build
        command, then trigger the command that will update the plugin host
        environment before the command executes.
        """
        # We only care about build commands
        if not self.is_build(command, args):
            return

        # Set in the environment prior to the command executing
        for env_cmd in ('envault_internal_env', 'envault_internal_env_33'):
            window.run_command(env_cmd, {
                "operation": "set",
                "env": {
                    "ENVAULT": "ENABLED"
                }
            })


    def on_post_window_command(self, window, command, args):
        """
        If the command that just executed in the window was a valid build
        command, then trigger the command that will restore the plugin host
        environment to what it was before the command originally executed.
        """
        # We only care about build commands
        if not self.is_build(command, args):
            return

        for env_cmd in ('i_am_the_command', 'i_am_the_command_33'):
            window.run_command(env_cmd, {
                "operation": "restore",
                "env": {}
            })


## ----------------------------------------------------------------------------
