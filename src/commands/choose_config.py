import sublime
import sublime_plugin

from sublime import ListInputItem

from os.path import split, splitext
from os import sep

from ..envault_data import get_envault_config, set_envault_config
from ..config_loader import scan_project_configs, load_and_fetch_config
from ..logging import log


## ----------------------------------------------------------------------------


class ConfigInputHandler(sublime_plugin.ListInputHandler):
    """
    Scan the window for all potential configuration files, then prompt the user
    to select one of the files as the configuration to use.
    """
    def __init__(self, window):
        # Get the currently selected config in this window, if any
        current = get_envault_config(window)

        # Get the full list of potential configuration files available in this
        # window; these files may or may not contain valid configs; all we can
        # say is, they seem to be files that exist at the moment./
        configs = scan_project_configs(window)
        self.choices = list(configs)

        # If the currently selected item is in the list of configs, then store
        # that one as current. Otherwise, pluck the first one from the list,
        # but only if there IS a list.
        if current in configs:
            self.current = current
        else:
            self.current = self.choices[0] if self.choices else None


    def placeholder(self):
        return "Choose Envault config for this window"


    def list_items(self):
        # The selected index should be the index that holds the current item,
        # but only if there IS a current item (there will not be if there
        # are no configs present, for example).
        selected = self.choices.index(self.current) if self.current is not None else 0

        def make_item(entry):
            # Split the absolute path into a path and filename, then split the
            # extension off the filename to get just the name of the config
            # itself.
            pathname, filename = split(entry)
            config, _ = splitext(filename)

            # For the path name, split it on path separators and take the one
            # second from the end, since we know it ends in the common config
            # folder.
            config_path = pathname.split(sep)[-2]

            return ListInputItem(config, value=entry, details=config_path)

        return [make_item(choice) for choice in self.choices], selected


## ----------------------------------------------------------------------------


class EnvaultChooseConfigCommand(sublime_plugin.WindowCommand):
    """
    Given the fully qualified path to a potential Envault configuration file,
    attempt to load that configuration, then make a web request to fetch the
    actual variables that associate with that configuration file.

    If no configuration file is present, the folders in the window will be
    scanned for potential configuration files, and the user will be prompted to
    select one.

    This will re-load and re-fetch the configuration even if the config has
    been previously loaded. This allows it to also function as a potential
    cache updater.

    The configuration file provided is marked in the project data for the
    window when it is selected.
    """
    def run(self, config):
        # If we get invoked with None as a config, it's generally because the
        # command was invoked from the command palette and the window has no
        # configs, which causes the list input handler to immediately return
        # None as the arg.
        if config is None:
            return log('no envault configs found in project', status=True)

        # Store this configuration into the window.
        set_envault_config(self.window, config)

        # Load it up
        load_and_fetch_config(config, self.window)


    def input(self, args):
        if "config" not in args:
            return ConfigInputHandler(self.window)


    def input_description(self):
        return "Envault Config"


## ----------------------------------------------------------------------------

