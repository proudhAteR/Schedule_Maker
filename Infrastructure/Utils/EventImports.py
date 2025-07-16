import importlib
import pkgutil

import Core.Models.Events


def run():
    for _, module_name, _ in pkgutil.iter_modules(Core.Models.Events.__path__):
        if module_name != "Event":  # skip the base Event itself
            importlib.import_module(f"Core.Models.Events.{module_name}")
