import sublime
import sublime_plugin

from sublime import ListInputItem

from os.path import split, join, splitext, exists
from os import sep

from ..envault_data import set_envault_config
from ..config_file import CONFIG_FOLDER, CONFIG_EXTENSION
from ..config_file import load_and_fetch_config, create_config
from ..config_status import set_status_config
from ..settings import ev_setting
from ..logging import log


## ----------------------------------------------------------------------------


class FolderInputHandler(sublime_plugin.ListInputHandler):
    """
    Present a list of the top level folders available within the window for the
    user to choose within which the configuration should be created.
    """
    def __init__(self, window):
        self.window = window


    def placeholder(self):
        """
        Text displayed when the user is selecting an option to remind them of
        what the selection will be used for.
        """
        return "Parent Folder"


    def description(self, _, text):
        """
        When the user has selected a folder and the next input handler is
        active, display as the breadcrumb the selected root pathand the envault
        folder that the config lives within as the chosen value, to make the
        next input clearer.
        """
        return f"{text}{sep}{CONFIG_FOLDER}{sep}"


    def list_items(self):
        """
        The user can select from a list of all of the top level folders that
        are currently open in the window; the display shows just the last path
        segment as the main value, with the full path as details for clarity
        as needed.

        The submitted value is always the full path.
        """
        return [ListInputItem(split(f)[1], value=f, details=f) for f in self.window.folders()]


    def next_input(self, args):
        """
        After selecting a folder, move on to asking for the name or activation
        state, if either of those arguments has not been provided yet.
        """
        if "name" not in args:
            return NameInputHandler()

        if "activate" not in args:
            return ActivateInputHandler()


## ----------------------------------------------------------------------------


class NameInputHandler(sublime_plugin.TextInputHandler):
    """
    Arbitrary text input handler to allow for the user to specify the name of
    the configuration file that should be created.

    The filename is presumed to always end in a specific extension (which is
    not enforced here and must be enforced at the call point), but the
    input handler ensures that the visible name in the command palette has the
    desired extension.

    A confirmation is made prior to allowing the input through to ensure that
    the filename will not have any invalid characters in it, although this is
    not foolproof.
    """
    def placeholder(self):
        """
        Text displayed in the input before the user starts typing the filename,
        to remind them what they are being asked to enter.
        """
        return "Configuration Name"


    def description(self, value):
        """
        When the user has chosen a filename, and that filename is valid, and
        the next input handler is active, display as the breadcrumb the name of
        the file that will be created, which is the entered text with an
        explicit extension applied to it.
        """
        return f"{splitext(value)[0].strip()}{CONFIG_EXTENSION}"


    def validate(self, value):
        """
        Called to validate that what the user is trying to enter should be
        accepted. If this returns False, the user will not be able to submit
        the result.

        Here we do some simple checks to ensure that the filename is not empty
        and that it does not contain any characters that would make it an
        invalid filename.
        """
        value = value.strip()

        # Filename has to be non-empty and not contain any instances of
        # charcters that are known to be invalid on at least one platform.
        if value and not any(e in value for e in ['/', '<', '>', ':', '"', '\\', '|', '?', '*']):
            return True

        # Filename must not be valid.
        return False


    def next_input(self, args):
        """
        After selecting a filename, move on to asking for the activation state,
        if that argument has not been provided yet.
        """
        if "activate" not in args:
            return ActivateInputHandler()


## ----------------------------------------------------------------------------


class ActivateInputHandler(sublime_plugin.ListInputHandler):
    """
    Input handler that provides a True/False result to the question of whether
    or not the configuration file that is about to be created should be
    immediately activated or not.
    """
    def placeholder(self):
        """
        Text displayed when the user is selecting an option to remind them of
        what the selection will be used for.
        """
        return "Activate?"


    def list_items(self):
        """
        Display exactly two items to the user to allow them to select whether
        they want to immediately activate the config once created or not.
        """
        return [
            ListInputItem("Activate after creation", value=True),
            ListInputItem("Create config only", value=False),
        ]


## ----------------------------------------------------------------------------


class EnvaultCreateConfigCommand(sublime_plugin.WindowCommand):
    """
    Given the top level project folder to create a config within and a config
    file name with or without extension, generate and create an envault config
    file in the appropriate location, creating the folder structure if it does
    not exist.

    If the activate argument is True, the newly created configuration will be
    set as the active config in the window and automatically loaded as well.
    """
    def run(self, folder, name, activate):
        # Create the full configuration file name that we are going to be
        # making.
        config_name = join(folder, CONFIG_FOLDER,
                           f"{splitext(name)[0].strip()}{CONFIG_EXTENSION}")

        # If the file exists and the user does not want to clobber over it,
        # then leave.
        if (exists(config_name) and
            sublime.yes_no_cancel_dialog("Config file exists. Overwrite it?") != sublime.DIALOG_YES):
            return log(f"skipping file creation; asked not to overwrite", status=True)

        log(f"creating {config_name}")

        # Get the values that we need to fill out the template, then create
        # the config.
        apiKey = ev_setting("default_api_key")
        url = ev_setting("default_api_url")
        create_config(config_name, apiKey, url, self.window)

        # If we are supposed to activate the config file, set it into the
        # window and fetch it now.
        if activate:
            set_envault_config(self.window, config_name)
            set_status_config(config_name, self.window)
            load_and_fetch_config(config_name)


    def is_enabled(self, **_):
        """
        Regardless of the arguments that are provided to the command, it can
        only be enabled if the current window has at least one folder open in
        it, or there will not be a place to create the configuration.
        """
        return len(self.window.folders()) != 0


    def input(self, args):
        """
        If any arguments to the command are missing, prompt for them. This is
        done in a specific order, and each of the input handlers will also
        use the same sequence if any additional arguments are missing.
        """
        if "folder" not in args:
            return FolderInputHandler(self.window)

        if "name" not in args:
            return NameInputHandler()

        if "activate" not in args:
            return ActivateInputHandler()


    def input_description(self):
        """
        Override the command name that is displayed in the command palette
        while the command is actively collecting arguments; this makes the
        command arguments easier to understand, and makes more room for the
        input.
        """
        return "Create Config"


## ----------------------------------------------------------------------------

