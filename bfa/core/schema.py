"""
Universal Schema abstraction for Backend for All.

Provides lightweight, language-agnostic data validation contracts
using pure Python primitives.
"""


class Schema:
    def __init__(self, fields: dict):
        """
        Initialize Schema with expected field types.
        Example: fields = {"username": str, "age": int}
        """
        self.fields = fields

    def validate(self, payload: dict) -> tuple[bool, str]:
        """
        Validate incoming payload against defined fields and types.
        Returns:
            (True, "OK") if valid.
            (False, "Error message") if invalid.
        """
        if not isinstance(payload, dict):
            return False, f"Payload must be a dictionary/JSON object, got {type(payload).__name__}"

        for key, expected_type in self.fields.items():
            # 1. Check missing field
            if key not in payload:
                return False, f"Missing required field: '{key}'"

            # 2. Check field type
            value = payload[key]
            if not isinstance(value, expected_type):
                return (
                    False,
                    f"Field '{key}' must be of type {expected_type.__name__}, got {type(value).__name__}",
                )

        return True, "OK"

    def __repr__(self) -> str:
        field_types = {k: v.__name__ for k, v in self.fields.items()}
        return f"Schema(fields={field_types})"