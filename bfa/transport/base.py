"""
Base transport abstraction for Backend for All.

This module defines the abstract interface and contracts that all BFA
transport adapters (HTTP, gRPC, WebSocket, IPC, etc.) must implement.
"""

from abc import ABC, abstractmethod
from bfa.protocol.decoder import JSONDecoder
from bfa.protocol.encoder import JSONEncoder
from bfa.runtime.runtime import Runtime


class BaseTransport(ABC):
    def __init__(self, runtime: Runtime, encoder: JSONEncoder | None = None, decoder: JSONDecoder | None = None):
        self.runtime = runtime
        self.encoder = encoder if encoder is not None else JSONEncoder()
        self.decoder = decoder if decoder is not None else JSONDecoder()

    @abstractmethod
    def serve_forever(self) -> None:
        """Start listening for incoming network/IPC connections and dispatch to runtime."""
        pass
