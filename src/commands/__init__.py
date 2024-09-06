from ...envault import reload

reload("src.commands", ["env_command","choose_config", "reload_config",
                        "create_config", "open_config", "show_variables"])

from .env_command import EnvaultEnvironmentCommand
from .choose_config import EnvaultChooseConfigCommand
from .reload_config import EnvaultReloadConfigCommand
from .create_config import EnvaultCreateConfigCommand
from .open_config import EnvaultOpenConfigCommand
from .show_variables import EnvaultShowVariablesCommand

__all__ = [
    # Command that adjusts the environment for us
    "EnvaultEnvironmentCommand",

    # Commands that scan form, load, and select the current configuration
    # file
    "EnvaultChooseConfigCommand",
    "EnvaultReloadConfigCommand",
    "EnvaultCreateConfigCommand",
    "EnvaultOpenConfigCommand",
    "EnvaultShowVariablesCommand",
]
