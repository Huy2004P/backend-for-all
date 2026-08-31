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


def create_crud_service_for_table(table_name: str, storage: BaseStorage) -> Service:
    """
    Tự động sinh ra một BFA Service hoàn chỉnh với đầy đủ các API CRUD cho một bảng dữ liệu.
    """
    service = Service(table_name)

    # 1. Method: find_all
    def handle_find_all(req: Request) -> dict:
        limit = req.payload.get("limit", 100) if req.payload else 100
        records = storage.find_all(table_name)
        return {
            "table": table_name,
            "total": len(records),
            "records": records[:limit],
        }

    service.add_method(
        Method(
            "find_all",
            handler=handle_find_all,
            input_schema=Schema({"limit": int}) if False else None,  # Optional payload
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
        # Remove empty or wrapper keys if needed
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
        results = storage.find(table_name, filters)
        return {
            "table": table_name,
            "filter": filters,
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
