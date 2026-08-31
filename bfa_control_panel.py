"""
BFA Control Panel — 100 Master System Blueprints Catalog & Live API Console.

Features:
1. Master Catalog Browser: Search & filter across 100 complete backend blueprints.
2. 1-Click System Mounting: Instantly provision tables, seed demo data, and generate live APIs.
3. Interactive API Runner: Test any endpoint directly from the GUI.
4. Database Connector: Point BFA to SQLite, PostgreSQL, MySQL, or Memory.
"""

import importlib
import json
import customtkinter as ctk

from bfa.catalog.registry import BLUEPRINT_CATALOG, CATEGORIES, list_all_blueprints
from bfa.config.settings import settings
from bfa.core.request import Request
from bfa.storage.factory import get_storage_engine, test_database_connection


# ==============================================================================
# 1. LIVE BACKEND INTROSPECTION & EXECUTION
# ==============================================================================
def get_live_runtime_and_services():
    """Tải Runtime thực tế từ main.py."""
    try:
        import main as app_main
        importlib.reload(app_main)

        if not hasattr(app_main, "setup_application"):
            return None, {}, "File main.py không có hàm setup_application()"

        runtime = app_main.setup_application()

        services_dict = {}
        for service_name, service in runtime.services.items():
            methods_list = []
            for method_name, method in service.methods.items():
                schema_fields = {}
                sample_payload = {}
                if method.input_schema and hasattr(method.input_schema, "fields"):
                    for k, v in method.input_schema.fields.items():
                        schema_fields[k] = v.__name__
                        if v is int:
                            sample_payload[k] = 1 if "id" in k or "user" in k else 100000
                        elif v is str:
                            sample_payload[k] = "sample_value" if "name" not in k else "huy_nguyen"
                        elif v is list:
                            sample_payload[k] = []
                        else:
                            sample_payload[k] = None
                else:
                    if method_name == "find_all":
                        sample_payload = {"limit": 10}
                    elif method_name in ("find_by_id", "delete"):
                        sample_payload = {"id": 1}
                    elif method_name == "insert":
                        sample_payload = {"name": "Sample Record", "status": "ACTIVE"}
                    elif method_name == "update":
                        sample_payload = {"id": 1, "data": {"status": "UPDATED"}}
                    elif method_name == "query":
                        sample_payload = {"filter": {"status": "ACTIVE"}}

                if method_name == "place_order":
                    sample_payload = {"user_id": 1, "product_id": 1, "quantity": 1}
                elif method_name == "deposit":
                    sample_payload = {"user_id": 1, "amount": 200000}
                elif method_name == "follow":
                    sample_payload = {"user_id": 1, "target_id": 2}
                elif method_name == "like_post":
                    sample_payload = {"post_id": 1, "user_id": 1}

                methods_list.append({
                    "name": method_name,
                    "schema": schema_fields,
                    "sample_payload": sample_payload,
                })

            services_dict[service_name] = {
                "name": service_name,
                "methods": methods_list,
            }

        return runtime, services_dict, None
    except Exception as e:
        return None, {}, f"Lỗi đọc Live Runtime: {e}"


# ==============================================================================
# 2. GUI APPLICATION (CustomTkinter)
# ==============================================================================
class BFAControlPanelApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BFA Control Panel — 100 Master Backend Blueprints")
        self.geometry("1200x820")
        self.minsize(1040, 680)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.runtime = None
        self.services_data = {}
        self.current_view = "SERVICES"
        self.selected_filter = "ALL"
        self.selected_method = None
        self.selected_service_name = None
        self.selected_category_filter = "ALL"
        self.search_keyword = ""

        self._build_sidebar()
        self._build_main_view()
        self.refresh_runtime()

    def _build_sidebar(self):
        """Thanh điều hướng bên trái (25% width)."""
        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar_frame.pack_propagate(False)

        # Logo
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="🧱 BFA Control Panel",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        self.logo_label.pack(anchor="w", padx=20, pady=(25, 4))

        self.subtitle_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="100 Master Backend Blueprints",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8",
        )
        self.subtitle_label.pack(anchor="w", padx=20, pady=(0, 15))

        # SECTION 1: 100 BLUEPRINTS CATALOG NAV BUTTON
        self.cat_section_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="MASTER BLUEPRINTS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#f59e0b",
        )
        self.cat_section_label.pack(anchor="w", padx=20, pady=(0, 6))

        self.catalog_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="📚 100 Blueprints Catalog",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            corner_radius=8,
            anchor="w",
            fg_color="#d97706",
            hover_color="#b45309",
            command=self.switch_to_catalog,
        )
        self.catalog_btn.pack(fill="x", padx=15, pady=(0, 10))

        # SECTION 2: DATABASE CONNECTOR
        self.db_section_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="DATABASE CONNECTOR",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#38bdf8",
        )
        self.db_section_label.pack(anchor="w", padx=20, pady=(0, 6))

        self.db_config_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="⚙️ Database Settings",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=36,
            corner_radius=8,
            anchor="w",
            fg_color="transparent",
            text_color="#38bdf8",
            hover_color="#1e293b",
            command=self.switch_to_database_config,
        )
        self.db_config_btn.pack(fill="x", padx=15, pady=(0, 10))

        # SECTION 3: CURRENT SYSTEM'S SERVICES
        self.section_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="ACTIVE SYSTEM APIS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#10b981",
        )
        self.section_label.pack(anchor="w", padx=20, pady=(0, 6))

        self.services_nav_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.services_nav_frame.pack(fill="x", padx=15)
        self.nav_buttons = {}

        # Footer Box
        self.status_box = ctk.CTkFrame(self.sidebar_frame, fg_color="#0f172a", corner_radius=8)
        self.status_box.pack(side="bottom", fill="x", padx=15, pady=20)

        self.bp_badge = ctk.CTkLabel(
            self.status_box,
            text=f"📦 Blueprint: #{settings.blueprint}",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#f59e0b",
        )
        self.bp_badge.pack(padx=10, pady=(10, 2))

        self.status_badge = ctk.CTkLabel(
            self.status_box,
            text=f"🗄️ DB: {settings.database_driver.upper()} • :8080 Active",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#38bdf8",
        )
        self.status_badge.pack(padx=10, pady=(0, 10))

    def _render_sidebar_service_filters(self):
        for widget in self.services_nav_frame.winfo_children():
            widget.destroy()

        all_btn = ctk.CTkButton(
            self.services_nav_frame,
            text="🌟 All Active APIs",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=32,
            corner_radius=6,
            anchor="w",
            fg_color="#2563eb" if self.selected_filter == "ALL" and self.current_view == "SERVICES" else "transparent",
            text_color="#ffffff" if self.selected_filter == "ALL" and self.current_view == "SERVICES" else "#cbd5e1",
            hover_color="#1e293b",
            command=lambda: self.switch_to_service_filter("ALL"),
        )
        all_btn.pack(fill="x", pady=1)
        self.nav_buttons["ALL"] = all_btn

        for s_name in self.services_data.keys():
            btn = ctk.CTkButton(
                self.services_nav_frame,
                text=f"📦 {s_name}",
                font=ctk.CTkFont(size=12, weight="bold"),
                height=30,
                corner_radius=6,
                anchor="w",
                fg_color="#2563eb" if self.selected_filter == s_name and self.current_view == "SERVICES" else "transparent",
                text_color="#ffffff" if self.selected_filter == s_name and self.current_view == "SERVICES" else "#cbd5e1",
                hover_color="#1e293b",
                command=lambda k=s_name: self.switch_to_service_filter(k),
            )
            btn.pack(fill="x", pady=1)
            self.nav_buttons[s_name] = btn

    def _build_main_view(self):
        """Khu vực hiển thị chính (75% width)."""
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Header Bar
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 12))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="📚 100 Master Backend Blueprints Catalog",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w",
        )
        self.title_label.pack(side="left")

        self.sync_btn = ctk.CTkButton(
            self.header_frame,
            text="🔄 Reload Runtime",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=130,
            height=34,
            fg_color="#334155",
            hover_color="#475569",
            command=self.refresh_runtime,
        )
        self.sync_btn.pack(side="right")

        self.content_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True)

        self._build_catalog_view()
        self._build_services_view()
        self._build_database_config_view()

        self.switch_to_catalog()

    def _build_catalog_view(self):
        """Khung duyệt 100 Master Blueprints."""
        self.catalog_container = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.catalog_container.pack(fill="both", expand=True)

        # Search and Category Filter Toolbar
        self.cat_toolbar = ctk.CTkFrame(self.catalog_container, fg_color="#1e293b", corner_radius=10)
        self.cat_toolbar.pack(fill="x", pady=(0, 12), padx=5)

        # Search Box
        self.search_entry = ctk.CTkEntry(
            self.cat_toolbar,
            placeholder_text="🔍 Tìm kiếm trong 100 hệ thống (VD: ride, crypto, hotel, pos, clinic, streaming...)",
            font=ctk.CTkFont(size=13),
            height=38,
        )
        self.search_entry.pack(fill="x", padx=15, pady=(12, 8))
        self.search_entry.bind("<KeyRelease>", self._on_search_key)

        # Category Filter Pills Frame
        self.cat_pills_scroll = ctk.CTkScrollableFrame(
            self.cat_toolbar,
            height=44,
            orientation="horizontal",
            fg_color="transparent",
        )
        self.cat_pills_scroll.pack(fill="x", padx=10, pady=(0, 10))

        # "All (100)" Button
        all_cat_btn = ctk.CTkButton(
            self.cat_pills_scroll,
            text="🌟 Tất Cả (100)",
            font=ctk.CTkFont(size=11, weight="bold"),
            height=28,
            corner_radius=14,
            fg_color="#f59e0b",
            text_color="#ffffff",
            command=lambda: self.set_category_filter("ALL"),
        )
        all_cat_btn.pack(side="left", padx=3)
        self.cat_pill_buttons = {"ALL": all_cat_btn}

        for cat in CATEGORIES:
            btn = ctk.CTkButton(
                self.cat_pills_scroll,
                text=f"{cat['name']} ({cat['count']})",
                font=ctk.CTkFont(size=11, weight="bold"),
                height=28,
                corner_radius=14,
                fg_color="transparent",
                text_color="#cbd5e1",
                hover_color="#334155",
                command=lambda k=cat["key"]: self.set_category_filter(k),
            )
            btn.pack(side="left", padx=3)
            self.cat_pill_buttons[cat["key"]] = btn

        # Scrollable Cards Grid
        self.catalog_scroll = ctk.CTkScrollableFrame(
            self.catalog_container,
            label_text="100 Production-Ready Architecture Blueprints (Click 'Launch' to load)",
            label_font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#0f172a",
            corner_radius=10,
        )
        self.catalog_scroll.pack(fill="both", expand=True, padx=5)

        self._render_catalog_cards()

    def _render_catalog_cards(self):
        for widget in self.catalog_scroll.winfo_children():
            widget.destroy()

        keyword = self.search_keyword.lower()
        blueprints = list_all_blueprints()

        matched = []
        for bp in blueprints:
            if self.selected_category_filter != "ALL" and bp["category"] != self.selected_category_filter:
                continue
            if keyword:
                search_text = f"{bp['id']} {bp['name']} {bp['description']} {' '.join(bp['tables'])}".lower()
                if keyword not in search_text:
                    continue
            matched.append(bp)

        if not matched:
            empty_lbl = ctk.CTkLabel(
                self.catalog_scroll,
                text="Không tìm thấy Blueprint nào phù hợp với từ khóa.",
                font=ctk.CTkFont(size=13),
                text_color="#64748b",
            )
            empty_lbl.pack(pady=40)
            return

        for bp in matched:
            card = ctk.CTkFrame(
                self.catalog_scroll,
                fg_color="#1e293b",
                corner_radius=8,
                border_width=1,
                border_color="#f59e0b" if bp["key"] == settings.blueprint else "#334155",
            )
            card.pack(fill="x", padx=8, pady=6)

            header_box = ctk.CTkFrame(card, fg_color="transparent")
            header_box.pack(fill="x", padx=12, pady=(10, 4))

            title_text = f"#{bp['id']} {bp['icon']} {bp['name']}"
            if bp["key"] == settings.blueprint:
                title_text += " [ACTIVE LIVE 🟢]"

            ctk.CTkLabel(
                header_box,
                text=title_text,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#f8fafc",
            ).pack(side="left")

            ctk.CTkLabel(
                header_box,
                text=f" {bp['category'].upper()} ",
                font=ctk.CTkFont(size=10, weight="bold"),
                fg_color="#334155",
                text_color="#38bdf8",
                corner_radius=4,
            ).pack(side="right")

            # Description
            ctk.CTkLabel(
                card,
                text=bp["description"],
                font=ctk.CTkFont(size=12),
                text_color="#94a3b8",
                anchor="w",
                justify="left",
            ).pack(fill="x", padx=12, pady=(0, 6))

            # Tables and Launch button row
            bottom_row = ctk.CTkFrame(card, fg_color="transparent")
            bottom_row.pack(fill="x", padx=12, pady=(0, 10))

            # Table chips
            tables_box = ctk.CTkFrame(bottom_row, fg_color="transparent")
            tables_box.pack(side="left", fill="x", expand=True)

            ctk.CTkLabel(tables_box, text="Tables:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#cbd5e1").pack(side="left", padx=(0, 6))

            for t in bp["tables"]:
                ctk.CTkLabel(
                    tables_box,
                    text=f"📦 {t}",
                    font=ctk.CTkFont(size=10),
                    fg_color="#0f172a",
                    text_color="#38bdf8",
                    corner_radius=4,
                    padx=6,
                    pady=2,
                ).pack(side="left", padx=2)

            # Launch button
            launch_btn = ctk.CTkButton(
                bottom_row,
                text="⚡ Launch System 🚀",
                font=ctk.CTkFont(size=12, weight="bold"),
                height=30,
                fg_color="#f59e0b" if bp["key"] != settings.blueprint else "#059669",
                hover_color="#d97706",
                corner_radius=6,
                command=lambda k=bp["key"]: self.launch_blueprint(k),
            )
            launch_btn.pack(side="right")

    def _on_search_key(self, event=None):
        self.search_keyword = self.search_entry.get().strip()
        self._render_catalog_cards()

    def set_category_filter(self, cat_key: str):
        self.selected_category_filter = cat_key
        for k, btn in self.cat_pill_buttons.items():
            if k == cat_key:
                btn.configure(fg_color="#f59e0b", text_color="#ffffff")
            else:
                btn.configure(fg_color="transparent", text_color="#cbd5e1")
        self._render_catalog_cards()

    def launch_blueprint(self, blueprint_key: str):
        bp = BLUEPRINT_CATALOG.get(blueprint_key)
        if not bp:
            return

        full_cfg = settings.config.copy()
        full_cfg["blueprint"] = blueprint_key
        full_cfg["domain"] = bp["category"]
        full_cfg["tables"] = bp["tables"]
        settings.save_config(full_cfg)

        self.bp_badge.configure(text=f"📦 Blueprint: #{blueprint_key}")
        self.refresh_runtime()
        self.switch_to_service_filter("ALL")

    def _build_services_view(self):
        self.services_container = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.services_container.pack_forget()

        self.services_scroll = ctk.CTkScrollableFrame(
            self.services_container,
            label_text="Active BFA Services & Workflows",
            label_font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#0f172a",
            corner_radius=10,
        )
        self.services_scroll.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.test_panel = ctk.CTkFrame(
            self.services_container,
            width=400,
            fg_color="#1e293b",
            corner_radius=10,
            border_width=1,
            border_color="#334155",
        )
        self.test_panel.pack(side="right", fill="both", padx=(0, 0))
        self.test_panel.pack_propagate(False)

        self._build_test_panel()

    def _build_test_panel(self):
        pad = 12
        self.tp_header = ctk.CTkLabel(
            self.test_panel,
            text="⚡ Interactive API Tester",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#38bdf8",
        )
        self.tp_header.pack(anchor="w", padx=pad, pady=(pad, 2))

        self.tp_sub = ctk.CTkLabel(
            self.test_panel,
            text="Gửi request thật đến Endpoint của hệ thống đang chạy.",
            font=ctk.CTkFont(size=11),
            text_color="#94a3b8",
        )
        self.tp_sub.pack(anchor="w", padx=pad, pady=(0, 8))

        self.endpoint_label = ctk.CTkLabel(
            self.test_panel,
            text="POST /api/users/find_all",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#0f172a",
            text_color="#10b981",
            corner_radius=6,
            padx=8,
            pady=4,
        )
        self.endpoint_label.pack(fill="x", padx=pad, pady=(0, 8))

        ctk.CTkLabel(
            self.test_panel,
            text="Request Payload (JSON):",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#cbd5e1",
        ).pack(anchor="w", padx=pad, pady=(0, 2))

        self.payload_box = ctk.CTkTextbox(
            self.test_panel,
            height=130,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#0f172a",
            text_color="#f8fafc",
            corner_radius=6,
        )
        self.payload_box.pack(fill="x", padx=pad, pady=(0, 10))

        self.run_btn = ctk.CTkButton(
            self.test_panel,
            text="🚀 Execute API Request",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            corner_radius=6,
            command=self.execute_current_method,
        )
        self.run_btn.pack(fill="x", padx=pad, pady=(0, 10))

        ctk.CTkLabel(
            self.test_panel,
            text="Live Response Result:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#cbd5e1",
        ).pack(anchor="w", padx=pad, pady=(0, 2))

        self.response_box = ctk.CTkTextbox(
            self.test_panel,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#0f172a",
            text_color="#38bdf8",
            corner_radius=6,
        )
        self.response_box.pack(fill="both", expand=True, padx=pad, pady=(0, pad))

    def _build_database_config_view(self):
        """Khung cấu hình Database Connector."""
        self.db_container = ctk.CTkScrollableFrame(
            self.content_container,
            label_text="Database Configuration",
            label_font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#0f172a",
            corner_radius=10,
        )
        self.db_container.pack_forget()

        pad = 20
        db_card = ctk.CTkFrame(self.db_container, fg_color="#1e293b", corner_radius=10, border_width=1, border_color="#334155")
        db_card.pack(fill="x", padx=pad, pady=(10, pad))

        ctk.CTkLabel(
            db_card,
            text="Kết Nối Cơ Sở Dữ Liệu",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#f8fafc",
        ).pack(anchor="w", padx=pad, pady=(pad, 4))

        curr_driver = settings.database_driver
        self.driver_var = ctk.StringVar(value=curr_driver)
        self.driver_selector = ctk.CTkSegmentedButton(
            db_card,
            values=["sqlite", "postgres", "mysql", "memory"],
            variable=self.driver_var,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=40,
            command=self._on_driver_changed,
        )
        self.driver_selector.pack(fill="x", padx=pad, pady=(0, 15))

        self.form_frame = ctk.CTkFrame(db_card, fg_color="transparent")
        self.form_frame.pack(fill="x", padx=pad, pady=(0, 10))

        self.sqlite_box = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        ctk.CTkLabel(self.sqlite_box, text="SQLite Database File Path:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(0, 4))
        self.sqlite_path_entry = ctk.CTkEntry(self.sqlite_box, font=ctk.CTkFont(size=12), height=36)
        self.sqlite_path_entry.insert(0, settings.database_config.get("sqlite_path", "bfa_database.db"))
        self.sqlite_path_entry.pack(fill="x")

        self.network_box = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        hp_frame = ctk.CTkFrame(self.network_box, fg_color="transparent")
        hp_frame.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(hp_frame, text="Host:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, sticky="w", padx=(0, 10))
        ctk.CTkLabel(hp_frame, text="Port:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=1, sticky="w")

        self.host_entry = ctk.CTkEntry(hp_frame, font=ctk.CTkFont(size=12), height=36)
        self.host_entry.insert(0, str(settings.database_config.get("host", "localhost")))
        self.host_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(4, 0))

        self.port_entry = ctk.CTkEntry(hp_frame, font=ctk.CTkFont(size=12), height=36, width=100)
        self.port_entry.insert(0, str(settings.database_config.get("port", 5432)))
        self.port_entry.grid(row=1, column=1, sticky="ew", pady=(4, 0))

        hp_frame.columnconfigure(0, weight=3)
        hp_frame.columnconfigure(1, weight=1)

        ctk.CTkLabel(self.network_box, text="Database Name:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(8, 4))
        self.dbname_entry = ctk.CTkEntry(self.network_box, font=ctk.CTkFont(size=12), height=36)
        self.dbname_entry.insert(0, str(settings.database_config.get("database_name", "bfa_ecommerce")))
        self.dbname_entry.pack(fill="x")

        up_frame = ctk.CTkFrame(self.network_box, fg_color="transparent")
        up_frame.pack(fill="x", pady=(8, 0))

        ctk.CTkLabel(up_frame, text="Username:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, sticky="w", padx=(0, 10))
        ctk.CTkLabel(up_frame, text="Password:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=1, sticky="w")

        self.user_entry = ctk.CTkEntry(up_frame, font=ctk.CTkFont(size=12), height=36)
        self.user_entry.insert(0, str(settings.database_config.get("username", "postgres")))
        self.user_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(4, 0))

        self.pass_entry = ctk.CTkEntry(up_frame, font=ctk.CTkFont(size=12), height=36, show="•")
        self.pass_entry.insert(0, str(settings.database_config.get("password", "")))
        self.pass_entry.grid(row=1, column=1, sticky="ew", pady=(4, 0))

        up_frame.columnconfigure(0, weight=1)
        up_frame.columnconfigure(1, weight=1)

        self._on_driver_changed(curr_driver)

        btn_box = ctk.CTkFrame(db_card, fg_color="transparent")
        btn_box.pack(fill="x", padx=pad, pady=(15, pad))

        self.test_conn_btn = ctk.CTkButton(
            btn_box,
            text="🔍 Test DB Connection",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            fg_color="#334155",
            hover_color="#475569",
            command=self.on_test_db_connection,
        )
        self.test_conn_btn.pack(side="left", padx=(0, 10))

        self.save_db_btn = ctk.CTkButton(
            btn_box,
            text="💾 Save Database Settings",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            fg_color="#059669",
            hover_color="#047857",
            command=self.on_save_db_config,
        )
        self.save_db_btn.pack(side="left")

        self.db_result_lbl = ctk.CTkLabel(
            db_card,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            wraplength=600,
            justify="left",
        )
        self.db_result_lbl.pack(fill="x", padx=pad, pady=(0, pad))

    def _on_driver_changed(self, driver: str):
        if driver == "sqlite":
            self.network_box.pack_forget()
            self.sqlite_box.pack(fill="x")
        elif driver in ("postgres", "mysql"):
            self.sqlite_box.pack_forget()
            self.network_box.pack(fill="x")
            if driver == "mysql" and self.port_entry.get() == "5432":
                self.port_entry.delete(0, "end")
                self.port_entry.insert(0, "3306")
                self.user_entry.delete(0, "end")
                self.user_entry.insert(0, "root")
            elif driver == "postgres" and self.port_entry.get() == "3306":
                self.port_entry.delete(0, "end")
                self.port_entry.insert(0, "5432")
                self.user_entry.delete(0, "end")
                self.user_entry.insert(0, "postgres")
        elif driver == "memory":
            self.sqlite_box.pack_forget()
            self.network_box.pack_forget()

    def _gather_db_config(self) -> dict:
        driver = self.driver_var.get()
        return {
            "driver": driver,
            "sqlite_path": self.sqlite_path_entry.get().strip() or "bfa_database.db",
            "host": self.host_entry.get().strip() or "localhost",
            "port": int(self.port_entry.get().strip() or 5432),
            "database_name": self.dbname_entry.get().strip() or "bfa_ecommerce",
            "username": self.user_entry.get().strip() or "postgres",
            "password": self.pass_entry.get().strip(),
        }

    def on_test_db_connection(self):
        db_cfg = self._gather_db_config()
        is_ok, msg = test_database_connection(db_cfg)
        if is_ok:
            self.db_result_lbl.configure(text=f"✅ {msg}", text_color="#10b981")
        else:
            self.db_result_lbl.configure(text=f"❌ {msg}", text_color="#ef4444")

    def on_save_db_config(self):
        db_cfg = self._gather_db_config()
        full_cfg = settings.config.copy()
        full_cfg["database"] = db_cfg
        settings.save_config(full_cfg)

        get_storage_engine(db_cfg, force_reload=True)

        self.status_badge.configure(text=f"🗄️ DB: {db_cfg['driver'].upper()} • :8080 Active")
        self.db_result_lbl.configure(
            text=f"🎉 Đã lưu và chuyển đổi Storage sang '{db_cfg['driver'].upper()}' thành công!",
            text_color="#10b981",
        )
        self.refresh_runtime()

    def switch_to_catalog(self):
        self.current_view = "CATALOG"

        self.services_container.pack_forget()
        self.db_container.pack_forget()
        self.catalog_container.pack(fill="both", expand=True)

        self.catalog_btn.configure(fg_color="#d97706", text_color="#ffffff")
        self.db_config_btn.configure(fg_color="transparent", text_color="#38bdf8")

        for btn in self.nav_buttons.values():
            btn.configure(fg_color="transparent", text_color="#cbd5e1")

        self.title_label.configure(text="📚 100 Master Backend Blueprints Catalog")
        self._render_catalog_cards()

    def switch_to_service_filter(self, filter_key: str):
        self.current_view = "SERVICES"
        self.selected_filter = filter_key

        self.catalog_container.pack_forget()
        self.db_container.pack_forget()
        self.services_container.pack(fill="both", expand=True)

        self.catalog_btn.configure(fg_color="transparent", text_color="#f59e0b")
        self.db_config_btn.configure(fg_color="transparent", text_color="#38bdf8")

        for key, btn in self.nav_buttons.items():
            if key == filter_key:
                btn.configure(fg_color="#2563eb", text_color="#ffffff")
            else:
                btn.configure(fg_color="transparent", text_color="#cbd5e1")

        self.title_label.configure(text=f"🟢 Live System APIs (Blueprint: #{settings.blueprint})")
        self.render_services()

    def switch_to_database_config(self):
        self.current_view = "DATABASE_CONFIG"

        self.catalog_container.pack_forget()
        self.services_container.pack_forget()
        self.db_container.pack(fill="both", expand=True)

        self.db_config_btn.configure(fg_color="#0284c7", text_color="#ffffff")
        self.catalog_btn.configure(fg_color="transparent", text_color="#f59e0b")

        for btn in self.nav_buttons.values():
            btn.configure(fg_color="transparent", text_color="#cbd5e1")

        self.title_label.configure(text="⚙️ Database Connector Configuration")

    def refresh_runtime(self):
        self.runtime, self.services_data, err = get_live_runtime_and_services()
        if err:
            self._render_error(err)
            return

        self._render_sidebar_service_filters()

        if self.current_view == "SERVICES":
            self.render_services()

        first_service = list(self.services_data.keys())[0] if self.services_data else None
        if first_service:
            self.select_method_for_test(first_service, "find_all", {"limit": 10})

    def render_services(self):
        for widget in self.services_scroll.winfo_children():
            widget.destroy()

        if not self.services_data:
            empty_lbl = ctk.CTkLabel(
                self.services_scroll,
                text="Chưa có Service nào trong hệ thống hiện tại.",
                font=ctk.CTkFont(size=13),
                text_color="#64748b",
            )
            empty_lbl.pack(pady=40)
            return

        for service_name, s_info in self.services_data.items():
            if self.selected_filter != "ALL" and self.selected_filter != service_name:
                continue

            card = ctk.CTkFrame(
                self.services_scroll,
                fg_color="#1e293b",
                corner_radius=8,
                border_width=1,
                border_color="#334155",
            )
            card.pack(fill="x", padx=8, pady=6)

            header_box = ctk.CTkFrame(card, fg_color="transparent")
            header_box.pack(fill="x", padx=12, pady=(10, 4))

            ctk.CTkLabel(
                header_box,
                text=f"🟢 📦 Service: {service_name}",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#f8fafc",
            ).pack(side="left")

            ctk.CTkLabel(
                header_box,
                text=f" {len(s_info['methods'])} Methods ",
                font=ctk.CTkFont(size=10, weight="bold"),
                fg_color="#059669",
                text_color="#ffffff",
                corner_radius=4,
            ).pack(side="right")

            methods_container = ctk.CTkFrame(card, fg_color="transparent")
            methods_container.pack(fill="x", padx=12, pady=(4, 10))

            for m in s_info["methods"]:
                method_name = m["name"]
                schema_dict = m["schema"]
                sample_payload = m["sample_payload"]

                m_row = ctk.CTkFrame(methods_container, fg_color="#0f172a", corner_radius=6)
                m_row.pack(fill="x", pady=2)

                if schema_dict:
                    params_str = ", ".join([f"{k}: {v}" for k, v in schema_dict.items()])
                    sig_text = f"⚡ {method_name}({params_str})"
                else:
                    sig_text = f"⚡ {method_name}()"

                ctk.CTkLabel(
                    m_row,
                    text=sig_text,
                    font=ctk.CTkFont(family="Consolas", size=11),
                    text_color="#38bdf8",
                    anchor="w",
                ).pack(side="left", padx=10, pady=6)

                test_btn = ctk.CTkButton(
                    m_row,
                    text="Test 🚀",
                    font=ctk.CTkFont(size=11, weight="bold"),
                    width=65,
                    height=24,
                    fg_color="#2563eb",
                    hover_color="#1d4ed8",
                    corner_radius=4,
                    command=lambda s=service_name, mn=method_name, sp=sample_payload: self.select_method_for_test(s, mn, sp),
                )
                test_btn.pack(side="right", padx=6, pady=4)

    def select_method_for_test(self, service_name: str, method_name: str, sample_payload: dict):
        self.selected_service_name = service_name
        self.selected_method = method_name

        self.endpoint_label.configure(text=f"POST /api/{service_name}/{method_name}")
        self.payload_box.delete("1.0", "end")
        self.payload_box.insert("1.0", json.dumps(sample_payload, indent=2, ensure_ascii=False))

        self.response_box.delete("1.0", "end")
        self.response_box.insert("1.0", f"// Sẵn sàng gọi API: {service_name}.{method_name}()\n// Nhấn 'Execute API Request' để thực thi.")

    def execute_current_method(self):
        if not self.selected_service_name or not self.selected_method:
            return

        raw_payload = self.payload_box.get("1.0", "end").strip()
        payload = {}
        if raw_payload:
            try:
                payload = json.loads(raw_payload)
            except json.JSONDecodeError as err:
                self.response_box.delete("1.0", "end")
                self.response_box.insert("1.0", json.dumps({"status": "ERROR", "error": f"Invalid JSON Payload: {err}"}, indent=2))
                return

        request = Request(service_name=self.selected_service_name, method_name=self.selected_method, payload=payload)
        response = self.runtime.handle_request(request)

        self.response_box.delete("1.0", "end")
        formatted = json.dumps(response.to_dict(), indent=2, ensure_ascii=False)
        self.response_box.insert("1.0", formatted)

    def _render_error(self, err_message: str):
        for widget in self.services_scroll.winfo_children():
            widget.destroy()
        ctk.CTkLabel(
            self.services_scroll,
            text=f"❌ {err_message}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#ef4444",
        ).pack(pady=40)


def main():
    app = BFAControlPanelApp()
    app.mainloop()


if __name__ == "__main__":
    main()
