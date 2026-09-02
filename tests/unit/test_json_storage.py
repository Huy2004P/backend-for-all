"""
Unit tests for Pure JSONStorage without SQLite.
"""

from pathlib import Path
from bfa.storage.json_store import JSONStorage


def test_json_storage_crud(tmp_path):
    test_file = tmp_path / "test_store.json"
    storage = JSONStorage(data_file=str(test_file))

    # 1. Insert
    user = storage.insert("users", {"name": "Huy", "role": "ADMIN"})
    assert user["id"] == 1
    assert user["name"] == "Huy"

    # 2. Get
    fetched = storage.get("users", 1)
    assert fetched is not None
    assert fetched["name"] == "Huy"

    # 3. Update
    updated = storage.update("users", 1, {"name": "Huy Pro", "role": "SUPERADMIN"})
    assert updated["name"] == "Huy Pro"
    assert updated["role"] == "SUPERADMIN"

    # 4. Find All & Stats
    all_users = storage.find_all("users")
    assert len(all_users) == 1
    stats = storage.get_stats()
    assert stats["users"] == 1

    # 5. Persistence across re-init
    storage_reloaded = JSONStorage(data_file=str(test_file))
    reloaded_user = storage_reloaded.get("users", 1)
    assert reloaded_user is not None
    assert reloaded_user["name"] == "Huy Pro"

    # 6. Delete
    deleted = storage_reloaded.delete("users", 1)
    assert deleted is True
    assert storage_reloaded.get("users", 1) is None
