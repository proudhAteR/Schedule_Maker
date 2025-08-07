import importlib
import pkgutil

import spacy
import spacy.cli

import Core.Models.Events
import Infrastructure.Utils.Parser.Matchers
from Infrastructure.Utils.Logs.Logger import Logger


def run():
    _load_all_modules(Core.Models.Events.__path__, "Core.Models.Events")
    _load_all_modules(Infrastructure.Utils.Parser.Matchers.__path__, "Infrastructure.Utils.Parser.Matchers")


def _load_all_modules(package_path, package_prefix : str):
    for _, module_name, _ in pkgutil.iter_modules(package_path):
        full_name = f"{package_prefix}.{module_name}"
        try:
            importlib.import_module(full_name)
        except Exception as e:
            Logger.warning(f"Failed to import {full_name}: {e}")


def load_spacy_model(model_name: str):
    try:
        return spacy.load(model_name)
    except OSError:
        Logger.warning(f"spaCy model '{model_name}' not found. Downloading...")
        spacy.cli.download(model_name)
        return spacy.load(model_name)
