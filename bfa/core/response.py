"""
Response abstraction for Backend for All.

Encapsulates execution results, status, payload data, and error information.
"""


class Response:
    def __init__(self, status: str, data: dict | list | str | None = None, error: str | None = None):
        self.status = status  # e.g., "SUCCESS", "ERROR"
        self.data = data
        self.error = error

    def to_dict(self) -> dict:
        """Serialize Response into a standard dictionary envelope."""
        return {
            "status": self.status,
            "data": self.data,
            "error": self.error,
        }

    def __repr__(self) -> str:
        return f"Response(status='{self.status}', data={self.data}, error={self.error})"
