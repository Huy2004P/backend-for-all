"""
Core runtime orchestrator for Backend for All.

This module manages the execution environment, dispatching incoming requests
to registered services, and coordinating runtime state.
"""

from bfa.core.response import Response


class Runtime:
    def __init__(self):
        self.services = {}

    def register_service(self, service) -> None:
        self.services[service.name] = service

    def handle_request(self, request) -> Response:
        if request.service_name not in self.services:
            return Response(status="ERROR", error="BFA_SERVICE_NOT_FOUND")

        service = self.services[request.service_name]
        return service.invoke(request)

    def __repr__(self) -> str:
        return f"Runtime(services={list(self.services.keys())})"
