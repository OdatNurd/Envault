import sublime

from ..lib.bootstrap import bootstrap_legacy_package

from .config_loader import load_and_fetch_config
from .envault_data import get_envault_config
from .logging import log


## ----------------------------------------------------------------------------


def load_window_configs():
    """
    Scan over all windows, and for each one check to see if there is a current
    envault configuration file specified. If there is, then dispatch a request
    to fetch that configuration.
    """
    for window in sublime.windows():
        config = get_envault_config(window)
        if config:
            log(f"doing startup fetch for {config}")
            load_and_fetch_config(config, window)


## ----------------------------------------------------------------------------


def loaded():
    """
    Invoked when the root plugin loads; this does any setup that is required
    when the package starts, which in our case here is to bootstrap out the
    command that is responsible for adjusting the environment into the Python
    3.3 plugin host so that we can support build targets from both versions of
    Sublime the same, and ensure that any restored windows that had envault
    configs have that config loaded.
    """
    log("initializing")
    bootstrap_legacy_package()
    load_window_configs()


def unloaded():
    """
    Invoked when the root plugin is unloaded.
    """
    pass


## ----------------------------------------------------------------------------
