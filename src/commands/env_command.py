import sublime
import sublime_plugin

from sys import version_info
from os import environ


## ----------------------------------------------------------------------------


# Capture the version of the current plugin host that the command is running
# in; this is used for logging and to help determine the command name
host = "%d.%d" % (version_info.major, version_info.minor)


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
        return "envault_internal_env_%s" % (host.replace('.', ''))


    def debugging(self):
        """
        Return True or False to indicate whether debugging is currently enabled
        for the package.

        This cannot use the function from the core because this file runs in
        both hosts and the bootstrapped 3.3 package only gains the command
        and no other support files.
        """
        s = sublime.load_settings("Envault.sublime-settings")
        return s.get("debug", False)


    def run(self, command, operation, config_file, env):
        """
        Execute the specified environment operation using the provided args.
        """
        if operation == "set":
            self.set_env(command, config_file, env)

        elif operation == "restore":
            self.restore_env(command)

        else:
            print("Envault: unknown env operation '%s' in %s" % (operation, host))


    def set_env(self, command, config_file, env):
        """
        Set the environment for the plugin host by extending the currently
        available environment with the keys from the provided dictionary.

        This will also lazily save the current environment if it has not
        previously been saved.
        """
        if self.original_env is None:
            self.original_env = environ.copy()

        if self.debugging():
            print("Envault: setting environment variables in %s for %s" % (host, command))

        # It is possible that we might get triggered to set the environment
        # while the environment is currently set, such as when a build triggers
        # a target that itself triggers a command that is in the user's watch
        # list.
        #
        # In order to ensure that we don't leak any environment, create a fresh
        # copy of the original environment of the host, update it with the
        # passed in environment, and then apply that environment.
        new_env = self.original_env.copy()
        new_env.update(env)

        # Set up some environment values to be included in the new environment
        # if the applied environment keys does not already include them; they
        # can be used to allow launched tasks to know how they're running.
        extra_vars = {
            "ENVAULT": "1",
            "ENVAULT_CONFIG": config_file
        }

        # Explicitly set the variables in the new environment if they do not
        # exist in the environment being applied; this ensures that if the
        # original environment has these values set, we can still override
        # them.
        for var, value in extra_vars.items():
            if var not in env:
                new_env[var] = value

        # Apply the new environment now
        environ.clear()
        environ.update(new_env)


    def restore_env(self, command):
        """
        Restore the environment that was previously in effect prior to the
        last call to set_env().

        This will restore the environment to the environment that was set as
        a part of that call.

        If the environment was not previously saved, then this will do nothing.
        """
        if self.debugging():
            print("Envault: removing environment variables in %s after %s" % (host, command))

        def restore():
            environ.clear()
            environ.update(self.original_env)

        if self.original_env is not None:
            sublime.set_timeout_async(lambda: restore())
        else:
            print("Envault: attempt to restore environment before it was saved")


## ----------------------------------------------------------------------------

