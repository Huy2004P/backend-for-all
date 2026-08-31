"""
Unit tests for BFA Core Service abstraction.
"""
from bfa.core.method import Method
from bfa.core.request import Request
from bfa.core.service import Service


def test_service_initialization():
    service = Service("users")

    assert service.name == "users"
    assert service.methods == {}


def test_service_invoke_success():
    service = Service("users")

    def create_user_handler(req: Request):
        return {"id": 1, "username": req.payload.get("username")}

    method = Method("create_user", handler=create_user_handler)
    service.add_method(method)

    req = Request("users", "create_user", {"username": "huy"})
    res = service.invoke(req)

    assert res.status == "SUCCESS"
    assert res.data == {"id": 1, "username": "huy"}
    assert res.error is None


def test_service_invoke_method_not_found():
    service = Service("users")
    req = Request("users", "non_existent_method")
    res = service.invoke(req)

    assert res.status == "ERROR"
    assert res.error == "BFA_METHOD_NOT_FOUND"
