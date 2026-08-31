"""
Unit tests for BFA Core Method abstraction.
"""

from bfa.core.method import Method
from bfa.core.service import Service


def test_method_initialization():
    method = Method("get_user")

    assert method.name == "get_user"
    assert method.handler is None


def dummy_handler(request=None):
    return "ok"


def test_service_add_method():
    service = Service("users")
    method = Method("create_user", handler=dummy_handler)

    service.add_method(method)
    assert len(service.methods) == 1
    assert "create_user" in service.methods
    assert service.methods["create_user"] == method
    assert service.methods["create_user"].handler() == "ok"
