import importlib
import pkgutil

import spacy
import spacy.cli
from spacy.util import is_package

import Core.Models.Events
import Infrastructure.Utils.Parser.Matchers
from Infrastructure.Utils.Logs.Logger import Logger


def run():
    __load_all_events()
    __load_all_matchers()


def __load_all_events():
    for _, module_name, _ in pkgutil.iter_modules(Core.Models.Events.__path__):
        importlib.import_module(f"Core.Models.Events.{module_name}")


def __load_all_matchers():
    for _, module_name, _ in pkgutil.iter_modules(Infrastructure.Utils.Parser.Matchers.__path__):
        importlib.import_module(f"Infrastructure.Utils.Parser.Matchers.{module_name}")


def ensure_spacy_model(model: str):
    if not is_package(model):
        Logger.warning(f"spaCy model '{model}' not found. Downloading...")
        spacy.cli.download(model)
    return spacy.load(model)
