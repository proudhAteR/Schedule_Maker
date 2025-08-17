import asyncio
import importlib
import pkgutil
from collections.abc import Sequence, MutableSequence

import spacy
import spacy.cli

import Core.Models.Events
import Infrastructure.Utils.Matchers
from Infrastructure.Utils.CLI.Logger import Logger


def run():
    _load_all_modules(
        [Core.Models.Events.__path__, Infrastructure.Utils.Matchers.__path__],
        ["Core.Models.Events", "Infrastructure.Utils.Matchers"]
    )


def _load_all_modules(package_paths: Sequence[MutableSequence[str]], package_prefixes: Sequence[str]):
    for package_path, package_prefix in zip(package_paths, package_prefixes):
        _recursive_load(package_path, package_prefix)


def _recursive_load(package_path: Sequence[str], package_prefix: str):
    for _, module_name, is_pkg in pkgutil.iter_modules(package_path):
        full_name = f"{package_prefix}.{module_name}"
        try:
            module = importlib.import_module(full_name)
        except Exception as e:
            Logger.warning(f"Failed to import {full_name}: {e}")
            continue
        if is_pkg:
            _recursive_load(module.__path__, full_name)


async def load_spacy_model_async(model_name: str):
    def _load_model():
        try:
            return spacy.load(model_name)
        except OSError:
            return None

    def _download_and_load():
        Logger.warning(f"spaCy model '{model_name}' not found. Downloading...")
        spacy.cli.download(model_name)
        return spacy.load(model_name)

    model = await asyncio.to_thread(_load_model)

    if model is None:
        model = await asyncio.to_thread(_download_and_load)

    return model
