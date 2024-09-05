import sublime

from os import makedirs
from os.path import join, split

from textwrap import dedent


## ----------------------------------------------------------------------------


# Get the name of the package that contains us
PKG_NAME=__name__.split(".")[0]

# The resource path to the plugin that contains thje command that is
# responsible for setting and restoring the environment.
#
# The command outlined here should be smart enough to rename itself depending
# on the plugin host it is running in, and should use only Python from the
# Python 3.3 plugin host.
COMMAND_PLUGIN_RESOURCE = f"Packages/{PKG_NAME}/src/commands/env_command.py"

# A small common header to be included in the boostrapped plugin to warn people
# about modifying it.
BOOTSTRAP_PLUGIN_HEADER = dedent("""
    ############
    # WARNING! #
    ############

    # This package and plugin file are part of the {package} Package, and are
    # used to support build commands defined in the older Python 3.3 plugin
    # host.
    #
    # You should not delete or modify this file, as it will be replaced when
    # Sublime Text loads the {package} Package at startup.

""".format(package=PKG_NAME)).lstrip()


## ----------------------------------------------------------------------------


def bootstrap_legacy_package():
    """
    Create or update a version of our package for the Python 3.3 legacy
    plugin host that contains the command that is used to adjust the
    environment for builds.
    """
    print(f"{PKG_NAME}: bootstrapping the Python 3.3 environment handler")
    plugin_name = split(COMMAND_PLUGIN_RESOURCE)[1]
    plugin_code = sublime.load_resource(COMMAND_PLUGIN_RESOURCE)

    new_pkg_path = join(sublime.packages_path(), f"{PKG_NAME}33")
    new_plugin_name = join(new_pkg_path, plugin_name)
    makedirs(new_pkg_path, exist_ok=True)

    with open(new_plugin_name, "w") as handle:
        handle.write(BOOTSTRAP_PLUGIN_HEADER)
        handle.write(plugin_code)


## ----------------------------------------------------------------------------
