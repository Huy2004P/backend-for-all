"""
Unit tests for BFA 100 Master Blueprints Catalog and Loader.
"""

from bfa.catalog.loader import mount_blueprint_to_runtime
from bfa.catalog.registry import (
    BLUEPRINT_CATALOG,
    CATEGORIES,
    clear_custom_blueprints,
    get_blueprint,
    list_all_blueprints,
    register_custom_blueprint,
)
from bfa.storage.memory import MemoryStorage


def test_100_blueprints_total_count():
    """Verify that exactly 100 blueprints are defined in the master registry."""
    clear_custom_blueprints()
    assert len(BLUEPRINT_CATALOG) == 100
    assert len(list_all_blueprints()) == 100


def test_10_categories_distribution():
    """Verify that all 10 categories exist and each has 10 blueprints."""
    assert len(CATEGORIES) == 10

    category_counts = {}
    for bp in BLUEPRINT_CATALOG.values():
        cat = bp["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1

    for cat_def in CATEGORIES:
        cat_key = cat_def["key"]
        assert category_counts.get(cat_key) == 10, f"Category '{cat_key}' does not have 10 blueprints."


def test_blueprint_schema_integrity():
    """Verify that every blueprint has valid id, name, category, tables and description."""
    ids_seen = set()
    for key, bp in BLUEPRINT_CATALOG.items():
        assert "id" in bp
        assert 1 <= bp["id"] <= 100
        assert bp["id"] not in ids_seen, f"Duplicate blueprint id {bp['id']}"
        ids_seen.add(bp["id"])

        assert bp["name"]
        assert bp["description"]
        assert isinstance(bp["tables"], list) and len(bp["tables"]) >= 2


def test_mount_sample_blueprints():
    """Verify that blueprints from different categories mount into Runtime successfully."""
    storage = MemoryStorage()

    test_keys = ["b2c_store", "digital_wallet", "ride_hailing", "clinic_appointment", "smart_home_telemetry"]
    for key in test_keys:
        runtime, bp = mount_blueprint_to_runtime(key, storage)
        assert bp["key"] == key
        for table in bp["tables"]:
            assert table in runtime.services, f"Table '{table}' service was not mounted in Runtime for '{key}'."
