import sublime

from ..lib.bootstrap import bootstrap_legacy_package


## ----------------------------------------------------------------------------


def loaded():
    """
    Invoked when the root plugin loads; this does any setup that is required
    when the package starts, which in our case here is to bootstrap out the
    command that is responsible for adjusting the environment into the Python
    3.3 plugin host so that we can support build targets from both versions of
    Sublime the same.
    """
    bootstrap_legacy_package()


def unloaded():
    """
    Invoked when the root plugin is unloaded.
    """
    pass


## ----------------------------------------------------------------------------
