"""
Unit tests for BFA Universal Schema module.
"""

from bfa.core.schema import Schema


def test_schema_validation_success():
    schema = Schema(fields={"username": str, "age": int})
    payload = {"username": "vanbaphathuy", "age": 20}

    is_valid, msg = schema.validate(payload)
    assert is_valid is True
    assert msg == "OK"


def test_schema_missing_field():
    schema = Schema(fields={"username": str, "age": int})
    payload = {"username": "vanbaphathuy"}

    is_valid, msg = schema.validate(payload)
    assert is_valid is False
    assert "Missing required field: 'age'" in msg


def test_schema_invalid_type():
    schema = Schema(fields={"username": str, "age": int})
    payload = {"username": "vanbaphathuy", "age": "twenty"}

    is_valid, msg = schema.validate(payload)
    assert is_valid is False
    assert "Field 'age' must be of type int, got str" in msg


def test_schema_invalid_payload_type():
    schema = Schema(fields={"username": str})
    is_valid, msg = schema.validate("invalid-payload")
    assert is_valid is False
    assert "Payload must be a dictionary" in msg
