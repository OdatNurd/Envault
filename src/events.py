import sublime
import sublime_plugin

from .config_file import scan_project_configs, load_and_fetch_config
from .config_status import set_status_config
from .env_cache import has_env, fetch_env
from .envault_data import get_envault_config, set_envault_config
from .logging import log
from .settings import ev_setting


## ----------------------------------------------------------------------------


def load_project_config(config_file):
    """
    Given a window's envault configuration file, schedule a fetch to get the
    environment to use for it.
    """
    if has_env(config_file):
        return log(f"no fetch needed; already loaded {config_file}")

    log(f"doing project load fetch for {config_file}")
    load_and_fetch_config(config_file)


def check_project_for_envault_config(window):
    """
    Given a newly opened project window that does not yet have a selected
    envault config, scan to see if there are any configuration files present
    in the project.

    If there are not, do nothing; if there is exactly one, then pre-select it
    as the appropriate one. Otherwise, trigger the user to select the config
    that they want to use in the project.
    """
    configs = scan_project_configs(window)
    if not configs:
        return

    # If there is more than one configuration file, we need to prompt the
    # user for which one to use.
    if len(configs) != 1:
        return window.run_command("show_overlay", {
            "overlay": "command_palette",
            "command": "envault_choose_config"
            })

    # There is exactly one file; set it as the currently selected envault
    # config, then fire the load
    set_envault_config(window, configs[0])
    load_project_config(configs[0])


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
            # Check for a known envault config; if so, fetch the environment
            # for it. Otherwise, we can just use an empty environment. This is
            # what happens for windows that don't have a config.
            config = get_envault_config(window)
            env = fetch_env(config) if config else { }
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


    def on_load_project(self, window):
        """
        When a project loads, check to see if it has a currently defined
        Envault configuration or not.

        If it does, trigger a load to ensure that the Envault config gets set
        for that window as appropriate.

        If it does not, do a scan to see if there are any configurations
        available, and if so choose one as needed.
        """
        config = get_envault_config(window)
        if config:
            load_project_config(config)
        else:
            check_project_for_envault_config(window)


    def on_post_save(self, view):
        """
        When a file is saved, if it appears in the list of currently loaded
        configuration values, reload and re-query the environment associated
        with it.
        """
        config_file = view.file_name()
        if ev_setting("reload_config_on_save") and has_env(config_file):
            log(f"reloading envault config {config_file}")
            load_and_fetch_config(config_file)


    def update_view_status_keys(self, view):
        """
        Update the status keys in the provided view so that they properly track
        the envault configuration that is currently active, if any.
        """
        if view.window():
            config = get_envault_config(view.window())
            set_status_config(config, view)


    # When a file is loaded or cloned, or when a new tab is created, ensure
    # that it has the appropriate view status keys.
    on_load = on_clone = on_new = update_view_status_keys


    def on_pre_move(self, view):
        """
        Since the event to tell us when an event to move a view from one
        window to another does not trigger when you move a view out into its
        own new window, handle the intent to move a file by deferring the
        status update operation until after the move has occured so that the
        correct configuration is picked up.
        """
        sublime.set_timeout(lambda: self.update_view_status_keys(view))


## ----------------------------------------------------------------------------
