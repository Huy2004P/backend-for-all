"""
Core service abstraction for Backend for All.

This module defines the language-independent concept of a BFA service,
representing a logical unit of functionality and domain boundary.
"""

from bfa.core.response import Response


class Service:
    def __init__(self, name: str):
        self.name = name
        self.methods = {}

    def add_method(self, method) -> None:
        self.methods[method.name] = method

    def invoke(self, request) -> Response:
        # 1. Kiểm tra method có tồn tại không
        if request.method_name not in self.methods:
            return Response(status="ERROR", error="BFA_METHOD_NOT_FOUND")

        method = self.methods[request.method_name]

        # 2. Kiểm tra handler đã được gán chưa
        if method.handler is None:
            return Response(status="ERROR", error="BFA_METHOD_HANDLER_NOT_IMPLEMENTED")

        # 3. Xác thực dữ liệu đầu vào qua Schema (nếu method có khai báo input_schema)
        if method.input_schema is not None:
            is_valid, error_msg = method.input_schema.validate(request.payload)
            if not is_valid:
                return Response(status="ERROR", error=f"BFA_VALIDATION_ERROR: {error_msg}")

        # 4. Thực thi handler an toàn
        try:
            result = method.handler(request)
            if isinstance(result, Response):
                return result
            return Response(status="SUCCESS", data=result)
        except Exception as e:
            return Response(status="ERROR", error=str(e))

    def __repr__(self) -> str:
        return f"Service(name='{self.name}', methods={list(self.methods.keys())})"