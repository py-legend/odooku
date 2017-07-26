import os.path
import importlib

from odooku.helpers.env import get_envvar
from odooku.helpers.split import split
from odooku.params import params


def init_packages():
    for module_name in split(get_envvar('PACKAGES', ''), ','):
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            # For now be explicit..
            raise

        # Look for addons folder in module package
        addons_path = os.path.join(os.path.dirname(module.__file__), 'addons')
        if os.path.isdir(addons_path):
            params.addon_paths.append(addons_path)

        # Look for cli commands
        params.cli_commands.extend(getattr(module, 'cli_commands', []))
