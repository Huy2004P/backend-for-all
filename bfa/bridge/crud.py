"""
Dynamic Database-to-API Bridge Engine for Backend for All.

Automatically transforms any database table into a fully functional BFA Service
with standardized CRUD methods (find_all, find_by_id, insert, update, delete, query).
"""

from bfa.core.method import Method
from bfa.core.request import Request
from bfa.core.schema import Schema
from bfa.core.service import Service
from bfa.storage.base import BaseStorage


def resolve_relations(record: dict, table_name: str, storage: BaseStorage, expand_list: list[str]) -> dict:
    """
    Tự động giải quyết và nhúng dữ liệu liên kết khóa ngoại (Foreign Keys / Joins / Nested Relations).
    - Hỗ trợ Many-to-One: user_id -> nhúng object "user", product_id -> nhúng "product"
    - Hỗ trợ One-to-Many: user.id -> nhúng danh sách "orders"
    """
    if not record or not expand_list:
        return record

    expanded_record = record.copy()
    expand_set = set(e.lower().strip() for e in expand_list if isinstance(e, str))

    # 1. Quét quan hệ Nhiều - 1 (Many-to-One qua cột _id)
    for key, val in list(record.items()):
        if key.endswith("_id") and val is not None:
            singular_name = key[:-3]  # e.g., user_id -> user
            parent_table = singular_name + "s"  # e.g., users
            if singular_name in expand_set or parent_table in expand_set or "*" in expand_set:
                parent_record = storage.get(parent_table, val)
                if not parent_record:
                    parent_record = storage.get(singular_name, val)
                if parent_record:
                    expanded_record[singular_name] = parent_record

    # 2. Quét quan hệ 1 - Nhiều (One-to-Many)
    rec_id = record.get("id")
    if rec_id is not None:
        for expand_target in expand_set:
            if expand_target == "*":
                continue
            child_fk_candidates = [
                f"{table_name.rstrip('s')}_id",
                f"{table_name}_id",
            ]
            for child_fk in child_fk_candidates:
                child_records = storage.find(expand_target, {child_fk: rec_id})
                if child_records:
                    expanded_record[expand_target] = child_records
                    break

    return expanded_record


def create_crud_service_for_table(table_name: str, storage: BaseStorage) -> Service:
    """
    Tự động sinh ra một BFA Service hoàn chỉnh với đầy đủ các API CRUD cho một bảng dữ liệu.
    """
    service = Service(table_name)

    # 1. Method: find_all
    def handle_find_all(req: Request) -> dict:
        limit = req.payload.get("limit", 100) if req.payload else 100
        expand = req.payload.get("expand") or req.payload.get("include") if req.payload else None
        if isinstance(expand, str):
            expand = [x.strip() for x in expand.split(",") if x.strip()]

        records = storage.find_all(table_name)
        sliced = records[:limit]

        if expand:
            sliced = [resolve_relations(r, table_name, storage, expand) for r in sliced]

        return {
            "table": table_name,
            "total": len(records),
            "records": sliced,
        }

    service.add_method(
        Method(
            "find_all",
            handler=handle_find_all,
            input_schema=Schema({"limit": int}) if False else None,
        )
    )

    # 2. Method: find_by_id
    def handle_find_by_id(req: Request) -> dict:
        record_id = req.payload.get("id")
        if record_id is None:
            raise ValueError(f"Missing required parameter 'id' to query table '{table_name}'.")
        record = storage.get(table_name, record_id)
        if not record:
            raise ValueError(f"Record with ID '{record_id}' not found in table '{table_name}'.")

        expand = req.payload.get("expand") or req.payload.get("include")
        if isinstance(expand, str):
            expand = [x.strip() for x in expand.split(",") if x.strip()]

        if expand:
            record = resolve_relations(record, table_name, storage, expand)

        return {"table": table_name, "record": record}

    service.add_method(
        Method(
            "find_by_id",
            handler=handle_find_by_id,
            input_schema=Schema({"id": int}) if False else None,
        )
    )

    # 3. Method: insert
    def handle_insert(req: Request) -> dict:
        data = req.payload.get("data", req.payload)
        if not data or not isinstance(data, dict):
            raise ValueError(f"Payload must be a dictionary of record data to insert into '{table_name}'.")
        insert_data = {k: v for k, v in data.items() if k != "data"} if "data" in req.payload else data
        created_record = storage.insert(table_name, insert_data)
        return {
            "table": table_name,
            "created": created_record,
            "message": f"Record inserted successfully into table '{table_name}'.",
        }

    service.add_method(
        Method(
            "insert",
            handler=handle_insert,
        )
    )

    # 4. Method: update
    def handle_update(req: Request) -> dict:
        record_id = req.payload.get("id")
        if record_id is None:
            raise ValueError(f"Missing required parameter 'id' to update table '{table_name}'.")
        updates = req.payload.get("data", {k: v for k, v in req.payload.items() if k != "id"})
        updated_record = storage.update(table_name, record_id, updates)
        if not updated_record:
            raise ValueError(f"Record with ID '{record_id}' not found in table '{table_name}'.")
        return {
            "table": table_name,
            "updated": updated_record,
            "message": f"Record #{record_id} in table '{table_name}' updated successfully.",
        }

    service.add_method(
        Method(
            "update",
            handler=handle_update,
        )
    )

    # 5. Method: delete
    def handle_delete(req: Request) -> dict:
        record_id = req.payload.get("id")
        if record_id is None:
            raise ValueError(f"Missing required parameter 'id' to delete from table '{table_name}'.")
        success = storage.delete(table_name, record_id)
        if not success:
            raise ValueError(f"Record with ID '{record_id}' not found in table '{table_name}'.")
        return {
            "table": table_name,
            "deleted_id": record_id,
            "message": f"Record #{record_id} deleted successfully from table '{table_name}'.",
        }

    service.add_method(
        Method(
            "delete",
            handler=handle_delete,
        )
    )

    # 6. Method: query (Filter)
    def handle_query(req: Request) -> dict:
        filters = req.payload.get("filter", req.payload)
        if isinstance(filters, dict):
            # Tách expand ra khỏi filters nếu có
            expand = filters.pop("expand", None) or filters.pop("include", None)
            clean_filters = {k: v for k, v in filters.items() if k not in ("expand", "include", "limit")}
        else:
            expand = None
            clean_filters = filters

        results = storage.find(table_name, clean_filters)

        if expand:
            if isinstance(expand, str):
                expand = [x.strip() for x in expand.split(",") if x.strip()]
            results = [resolve_relations(r, table_name, storage, expand) for r in results]

        return {
            "table": table_name,
            "filter": clean_filters,
            "total": len(results),
            "records": results,
        }

    service.add_method(
        Method(
            "query",
            handler=handle_query,
        )
    )

    return service


def generate_services_for_tables(table_names: list[str], storage: BaseStorage) -> list[Service]:
    """
    Tạo danh sách BFA Service tương ứng cho tất cả các bảng được cấu hình.
    """
    services = []
    for table_name in table_names:
        clean_name = table_name.strip()
        if clean_name:
            services.append(create_crud_service_for_table(clean_name, storage))
    return services
