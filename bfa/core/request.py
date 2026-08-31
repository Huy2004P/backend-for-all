"""
Request abstraction for Backend for All.

Encapsulates incoming invocation data including target service name,
method name, and payload.
"""


class Request:
    def __init__(self, service_name: str, method_name: str, payload: dict | None = None):
        self.service_name = service_name
        self.method_name = method_name
        self.payload = payload if payload is not None else {}

    def __repr__(self) -> str:
        return f"Request(service='{self.service_name}', method='{self.method_name}', payload={self.payload})"
