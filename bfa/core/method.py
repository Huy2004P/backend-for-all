"""
Method and function abstraction for Backend for All.

This module defines callable procedures, RPC endpoints,
and invocation signatures exposed by a BFA service.
"""


class Method:
    def __init__(self, name: str, handler=None, input_schema=None):
        self.name = name
        self.handler = handler
        self.input_schema = input_schema

    def __repr__(self) -> str:
        return f"Method(name='{self.name}', handler={self.handler}, input_schema={self.input_schema})"