"""
BFA Catalog System — 100 Master Backend Architecture Blueprints.
"""

from bfa.catalog.loader import load_blueprint_by_key, mount_blueprint_to_runtime
from bfa.catalog.registry import BLUEPRINT_CATALOG, CATEGORIES, get_blueprint, list_all_blueprints

__all__ = [
    "BLUEPRINT_CATALOG",
    "CATEGORIES",
    "get_blueprint",
    "list_all_blueprints",
    "load_blueprint_by_key",
    "mount_blueprint_to_runtime",
]
