"""
Protocol encoder for Backend for All.

Serializes Python dictionaries and response structures into wire-format bytes.
"""

import json


class JSONEncoder:
    def encode(self, response_dict: dict) -> bytes:
        """
        Encode a response dictionary into UTF-8 JSON bytes.

        Args:
            response_dict: Dictionary representation of response or error payload.

        Returns:
            bytes: Encoded JSON byte array ready for network transport.
        """
        json_str = json.dumps(response_dict, indent=2, ensure_ascii=False)
        return json_str.encode("utf-8")

    def __repr__(self) -> str:
        return "JSONEncoder()"
