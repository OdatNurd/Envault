import sublime
import sublime_plugin

from sys import version_info
from os import environ


## ----------------------------------------------------------------------------


class EnvaultEnvironmentCommand(sublime_plugin.WindowCommand):
    """
    Based on the arguments provided, either set or restore the environment in
    the plugin host in which the command executes.

    The original environment will be saved the first time a set operation is
    executed, to ensure that on systems running MacOS that the environment has
    a chance to be updated by the startup mechanism that launches a terminal.
    """
    original_env = None

    def name(self):
        """
        Override the native handling that names this command so that it
        presents its name differently depending on the plugin host that it
        runs within.
        """
        if version_info >= (3, 8):
            return "envault_internal_env"
        else:
            return "envault_internal_env_33"


    def run(self, operation, env):
        if operation == "set":
            self.set_env(env)

        elif operation == "restore":
            self.restore_env()

        else:
            print("Envault: unknown env operation '%s'" % operation)


    def set_env(self, env):
        """
        Set the environment for the plugin host by extending the currently
        available environment with the keys from the provided dictionary.

        This will also lazily save the current environment if it has not
        previously been saved.
        """
        if self.original_env is None:
            self.original_env = environ.copy()

        print("Envault: setting environment variables")
        environ.update(env)


    def restore_env(self):
        """
        Restore the environment that was previously in effect prior to the
        last call to set_env().

        This will restore the environment to the environment that was set as
        a part of that call.

        If the environment was not previously saved, then this will do nothing.
        """
        print("Envault: removing environment variables")

        def restore():
            environ.clear()
            environ.update(self.original_env)

        if self.original_env is not None:
            sublime.set_timeout_async(lambda: restore())
        else:
            print("Envault: attempt to restore environment before it was saved")


## ----------------------------------------------------------------------------

