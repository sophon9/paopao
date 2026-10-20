"""Question bank package. Importing it registers every topic, skill and template."""

import importlib
import pkgutil

from backend.bank import core, topics  # noqa: F401  (topics registers topic list)

CONTENT_PREFIXES = ("math_", "english_")


def _load_content():
    pkg_path = __path__  # noqa: F821
    for info in sorted(pkgutil.iter_modules(pkg_path), key=lambda m: m.name):
        if info.name.startswith(CONTENT_PREFIXES):
            importlib.import_module(f"{__name__}.{info.name}")


_load_content()

TOPICS = core.TOPICS
SKILLS = core.SKILLS
TEMPLATES = core.TEMPLATES
