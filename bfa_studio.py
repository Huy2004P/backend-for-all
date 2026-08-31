"""
BFA Studio - GUI Client for testing BFA Services and Runtime.

This script simulates a Client GUI using Python's built-in tkinter library.
It allows developers to interactively send requests to registered BFA services,
test Schema Validation, and view formatted response outputs.
"""

import json
import tkinter as tk
from tkinter import ttk

from bfa.core.method import Method
from bfa.core.request import Request
from bfa.core.schema import Schema
from bfa.core.service import Service
from bfa.runtime.runtime import Runtime


def setup_demo_runtime() -> Runtime:
    """Initialize BFA Runtime with demo services, schemas, and handlers."""
    runtime = Runtime()

    # 1. Setup 'users' Service
    users_service = Service("users")

    # 2. Define Input Schema for 'create_user'
    create_user_schema = Schema(
        fields={
            "username": str,
            "age": int,
        }
    )

    # 3. Define Handlers
    def create_user_handler(req: Request) -> dict:
        username = req.payload.get("username")
        age = req.payload.get("age")
        return {
            "id": 101,
            "username": username,
            "age": age,
            "status": "active",
            "message": f"User '{username}' (age: {age}) created successfully via BFA Runtime!",
        }

    def get_user_handler(req: Request) -> dict:
        username = req.payload.get("username", "vanbaphathuy")
        return {
            "id": 101,
            "username": username,
            "role": "developer",
            "platform": "Backend for All (BFA)",
        }

    # 4. Attach Methods with Schema to Service
    users_service.add_method(
        Method("create_user", handler=create_user_handler, input_schema=create_user_schema)
    )
    users_service.add_method(Method("get_user", handler=get_user_handler))

    # 5. Register into runtime
    runtime.register_service(users_service)
    return runtime


class BFAStudioApp:
    def __init__(self, root: tk.Tk, runtime: Runtime):
        self.root = root
        self.runtime = runtime
        self.root.title("BFA Studio - API Tester")
        self.root.geometry("720x680")
        self.root.minsize(600, 550)

        self._configure_styles()
        self._build_ui()

    def _configure_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#1e293b")
        style.configure("SubHeader.TLabel", font=("Segoe UI", 9), foreground="#64748b")
        style.configure("FieldLabel.TLabel", font=("Segoe UI", 10, "bold"), foreground="#334155")
        style.configure("Send.TButton", font=("Segoe UI", 11, "bold"), background="#2563eb", foreground="#ffffff")
        style.map("Send.TButton", background=[("active", "#1d4ed8")])

    def _build_ui(self) -> None:
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        ttk.Label(main_frame, text="BFA Studio - API Tester", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            main_frame,
            text="Interactive GUI Client for Backend for All (BFA) Runtime with Schema Validation",
            style="SubHeader.TLabel",
        ).pack(anchor="w", pady=(0, 15))

        # Inputs Grid
        grid_frame = ttk.Frame(main_frame)
        grid_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(grid_frame, text="Service Name:", style="FieldLabel.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=5)
        self.service_entry = ttk.Entry(grid_frame, font=("Segoe UI", 10))
        self.service_entry.insert(0, "users")
        self.service_entry.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(grid_frame, text="Method Name:", style="FieldLabel.TLabel").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)
        self.method_entry = ttk.Entry(grid_frame, font=("Segoe UI", 10))
        self.method_entry.insert(0, "create_user")
        self.method_entry.grid(row=1, column=1, sticky="ew", pady=5)

        grid_frame.columnconfigure(1, weight=1)

        # Payload Section
        ttk.Label(main_frame, text="Request Payload (JSON):", style="FieldLabel.TLabel").pack(anchor="w", pady=(5, 2))
        self.payload_text = tk.Text(
            main_frame, height=6, font=("Consolas", 10), bg="#f8fafc", fg="#0f172a", relief="solid", borderwidth=1
        )
        default_payload = json.dumps({"username": "vanbaphathuy", "age": 20}, indent=2)
        self.payload_text.insert(tk.END, default_payload)
        self.payload_text.pack(fill=tk.X, pady=(0, 15))

        # Send Button
        self.send_button = ttk.Button(
            main_frame, text="Send Request 🚀", style="Send.TButton", command=self.on_send_request, cursor="hand2"
        )
        self.send_button.pack(fill=tk.X, pady=(0, 15), ipady=5)

        # Response Section
        ttk.Label(main_frame, text="Response Output:", style="FieldLabel.TLabel").pack(anchor="w", pady=(5, 2))
        self.response_text = tk.Text(
            main_frame, height=12, font=("Consolas", 10), bg="#0f172a", fg="#38bdf8", insertbackground="white", relief="solid", borderwidth=1
        )
        self.response_text.insert(tk.END, "// Response from BFA Runtime will appear here...\n")
        self.response_text.pack(fill=tk.BOTH, expand=True)

    def on_send_request(self) -> None:
        service_name = self.service_entry.get().strip()
        method_name = self.method_entry.get().strip()
        raw_payload = self.payload_text.get("1.0", tk.END).strip()

        # Parse Payload JSON
        payload = {}
        if raw_payload:
            try:
                payload = json.loads(raw_payload)
            except json.JSONDecodeError as err:
                self._display_response({"status": "ERROR", "error": f"Invalid JSON Payload: {err}"})
                return

        # Create BFA Request and dispatch to Runtime
        request = Request(service_name=service_name, method_name=method_name, payload=payload)
        response = self.runtime.handle_request(request)

        # Display Response
        self._display_response(response.to_dict())

    def _display_response(self, response_dict: dict) -> None:
        self.response_text.delete("1.0", tk.END)
        formatted_json = json.dumps(response_dict, indent=2, ensure_ascii=False)
        self.response_text.insert(tk.END, formatted_json)


def main() -> None:
    runtime = setup_demo_runtime()
    root = tk.Tk()
    app = BFAStudioApp(root, runtime)
    root.mainloop()


if __name__ == "__main__":
    main()
