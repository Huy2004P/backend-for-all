"""
Unit tests for BFA Runtime and Service Registry.
"""

from bfa.core.method import Method
from bfa.core.request import Request
from bfa.core.service import Service
from bfa.runtime.runtime import Runtime


def test_runtime_initialization():
    runtime = Runtime()
    assert runtime.services == {}


def test_runtime_register_and_handle_request():
    runtime = Runtime()
    users_service = Service("users")

    def create_user_handler(req: Request):
        return {"id": 1, "username": req.payload.get("username", "anonymous")}

    users_service.add_method(Method("create_user", handler=create_user_handler))
    runtime.register_service(users_service)

    # Valid request
    req = Request("users", "create_user", {"username": "vanbaphathuy"})
    res = runtime.handle_request(req)

    assert res.status == "SUCCESS"
    assert res.data == {"id": 1, "username": "vanbaphathuy"}
    assert res.error is None


def test_runtime_service_not_found():
    runtime = Runtime()
    req = Request("non_existent_service", "any_method")
    res = runtime.handle_request(req)

    assert res.status == "ERROR"
    assert res.error == "BFA_SERVICE_NOT_FOUND"
