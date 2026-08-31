"""
Protocol decoder for Backend for All.

Deserializes wire-format byte payloads into structured Python dictionaries.
"""

import json


class JSONDecoder:
    def decode(self, raw_bytes: bytes) -> dict:
        """
        Decode raw bytes into a Python dictionary.

        Args:
            raw_bytes: Raw bytes received from the transport layer.

        Returns:
            dict: Parsed payload dictionary.

        Raises:
            ValueError: If payload is invalid JSON or not a dictionary.
        """
        if not raw_bytes or not raw_bytes.strip():
            return {}

        try:
            data = json.loads(raw_bytes.decode("utf-8"))
            if not isinstance(data, dict):
                raise ValueError(f"Decoded payload must be a JSON object/dict, got {type(data).__name__}")
            return data
        except json.JSONDecodeError as err:
            raise ValueError(f"Invalid JSON format: {err}") from err

    def __repr__(self) -> str:
        return "JSONDecoder()"
