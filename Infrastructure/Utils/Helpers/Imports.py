import importlib
import pkgutil

import Core.Models.Events
import Infrastructure.Utils.Parser.Matchers


def run():
    __load_all_events()
    __load_all_matchers()


def __load_all_events():
    for _, module_name, _ in pkgutil.iter_modules(Core.Models.Events.__path__):
        importlib.import_module(f"Core.Models.Events.{module_name}")


def __load_all_matchers():
    for _, module_name, _ in pkgutil.iter_modules(Infrastructure.Utils.Parser.Matchers.__path__):
        importlib.import_module(f"Infrastructure.Utils.Parser.Matchers.{module_name}")
