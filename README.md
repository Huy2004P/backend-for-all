# Backend for All

**Backend for All (BFA)** is an open-source, language-independent, system-independent, and developer-accessible backend platform designed to provide a universal foundation, specification, and building blocks where backend services written in any programming language can seamlessly coexist, communicate, and power any type of system—accessible to developers worldwide.

> **Backend for All = Backend for All Languages, All Systems, and All Developers.**

---

## 🌐 Documentation Languages / Chọn Ngôn Ngữ

[English (Canonical)](docs/en/vision.md) | [Tiếng Việt (Bản dịch chính thức)](docs/vi/vision.md) | [Documentation Hub](docs/README.md)

---

## Vision

The name **Backend for All** carries three fundamental pillars:

1. **ALL LANGUAGES**: A language-independent architecture where services written in Python, Go, Java, Rust, TypeScript, C++, C#, Kotlin, and future languages operate as a unified system without friction.
2. **ALL SYSTEMS**: A general-purpose, extensible platform providing universal backend building blocks capable of powering any domain—from E-Commerce and SaaS to AI platforms, Games, Social Networks, IoT, Education, and Enterprise systems.
3. **ALL DEVELOPERS**: A global, multilingual developer ecosystem eliminating language barriers with canonical specifications and synchronized native-language documentation.

```text
                         BACKEND FOR ALL
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
     ALL LANGUAGES         ALL SYSTEMS         ALL DEVELOPERS
          │                     │                     │
    Python / Go / Java      E-Commerce / SaaS     Global Community
    Rust / C++ / TS         AI / Social / Game    Multilingual Docs
    C# / Kotlin / ...       IoT / Enterprise      Accessibility
          │                     │                     │
          └─────────────────────┼─────────────────────┘
                                │
                       BFA FOUNDATION
                                │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
   Specification        Protocol            Runtime
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    BFA Building Blocks
```

---

## The Problem

1. **Language Silos**: Modern stacks leverage different languages for distinct strengths (Python for AI, Go for microservices, Rust for speed, TypeScript for BFF/APIs). Yet uniting them requires fragile glue code, duplicated data transfer objects (DTOs), and custom communication bridges.
2. **System-Specific Reinvention**: Developers building different application domains (E-Commerce, SaaS, Social, IoT, Games) constantly reinvent identical foundational backend concerns: discovery, RPC contracts, schema validation, event routing, lifecycle state machines, and authentication envelopes.
3. **Language Barriers for Global Developers**: High-quality backend architecture knowledge, documentation, and error diagnostics are predominantly English-only, hindering talented developers worldwide from adopting and contributing to modern distributed patterns.
4. **Lack of Universal Contracts**: REST/JSON endpoints lack unified cross-language type contracts, causing runtime serialization errors and breaking cross-team collaboration.

---

## The Idea

BFA establishes a **Universal Common Foundation**:
- **Specification-First**: Language-agnostic definitions for services, methods, schemas, and events.
- **Universal Protocol**: High-efficiency wire messaging for RPC, streaming, and pub/sub events.
- **Universal Building Blocks**: Standardized abstractions (Services, Schemas, Requests, Events, Storage, Auth, Observability) that assemble like LEGO pieces into any backend system.
- **Runtime Coordinator**: A lightweight runtime managing discovery, lifecycle, health, and transport across all services.
- **Global Documentation Ecosystem**: Single source of truth with synchronized multilingual documentation, preserving immutable machine identifiers.

---

## What BFA Is

* **An Open-Source Backend Platform**: A unified foundation for modern backend engineering.
* **Language-Independent (Polyglot)**: Built from the ground up to support any programming language.
* **System-Independent (General-Purpose)**: Designed to power any domain or architectural style (monoliths, microservices, event-driven, serverless).
* **Developer-Accessible (Multilingual)**: Global documentation and developer experience without language barriers.
* **A Common Layer & Specification**: Standardizing contracts, types, and wire protocols across language boundaries.
* **A Universal Wire Protocol**: Structured RPC, streaming, and event delivery across heterogeneous nodes.
* **A Backend LEGO Set**: Providing universal building blocks to assemble custom backend solutions rapidly.
* **Developer-First & Code-First**: Clean code is the single source of truth, enhanced by optional CLI and GUI tooling.

---

## What BFA Is Not

* **NOT a Python-only framework**: Python is simply the initial reference SDK used to bootstrap and validate the BFA specification. Python is not the center of BFA.
* **NOT a framework mechanically ported across languages**: BFA defines shared specifications, protocols, and standard behaviors that feel idiomatic in every host language.
* **NOT a microservices-only system**: BFA works equally well for modular monoliths, distributed microservices, hybrid setups, or edge nodes.
* **NOT an e-commerce-only or AI-only platform**: BFA provides foundational primitives, not rigid vertical product templates.
* **NOT a closed no-code platform**: BFA is strictly code-first; source code remains in your full control.
* **NOT a GUI replacing source code**: Visual tools (like BFA Studio) exist solely to visualize, test, and inspect services.

---

## Core Principles

1. **Open by Default**: Fully open-source, vendor-neutral, and community-owned.
2. **Language Independent**: No single programming language is privileged. Services in Python, Go, Rust, Java, and TypeScript coexist as equals.
3. **System Independent**: One backend platform capable of powering any vertical or architecture.
4. **Developer Accessible (Global Multilingual)**: Documentation, guides, and developer workflows accessible across natural languages.
5. **Code-First**: Hand-written, idiomatic code is the single source of truth.
6. **GUI-Assisted**: Visual tooling assists development and observability without locking code into proprietary formats.
7. **Interoperable**: Frictionless cross-language communication and universal schema compatibility.
8. **Extensible**: Open plugin architecture for databases, message brokers, authentication, and storage.
9. **Developer-First**: Ergonomic APIs, comprehensive documentation, and standard-library-first implementations.
10. **Community-Driven**: Specifications, protocols, and translations evolve transparently through open RFCs and discussions.
11. **Specification-First**: Formal specifications precede implementation, ensuring consistency across all language SDKs.

> [!NOTE]
> **Language Independent $\neq$ System Independent $\neq$ Developer Accessible**  
> - **Language Independent**: A single backend system can be constructed using multiple programming languages seamlessly.  
> - **System Independent**: The exact same BFA platform, protocol, and runtime can be used to construct entirely different types of applications (E-Commerce, SaaS, Social, AI, Game, IoT, Enterprise).  
> - **Developer Accessible**: Developers worldwide can learn, adopt, and contribute to BFA in their native languages.

---

## The Mental Model: Backend LEGO

Think of BFA as a comprehensive **Backend LEGO Set**. BFA delivers universal, precision-engineered building blocks. Developers combine and assemble these blocks to build their specific system:

```text
                      BFA BUILDING BLOCKS
                               │
   ┌───────────┬───────────┬───┴───────┬───────────┬───────────┐
   │           │           │           │           │           │
Service      Method      Schema     Request     Response     Event
   │           │           │           │           │           │
Messaging   Storage       Auth        Config     Telemetry    Runtime
   │           │           │           │           │           │
   └───────────┴───────────┬───────────┴───────────┴───────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
    [ Domain System A ]         [ Domain System B ]
       (e.g., E-Commerce)            (e.g., AI Application)
       ├── User Service (Go)         ├── Model Gateway (Go)
       ├── Catalog Service (Java)    ├── Inference Worker (Python)
       ├── Payment Service (Rust)    ├── Job Scheduler (Rust)
       └── AI Assistant (Python)     └── Pipeline API (TypeScript)
```

---

## All Languages — Polyglot Backend

BFA is language-independent at the specification and architectural level:

```text
Python
└── AI & Inference Service

Go
└── Payment & Concurrency Service

Java
└── Core Order & Transaction Service

Rust
└── High-Performance Processing Service

TypeScript
└── API Gateway & BFF Service

               ↓

          BFA Protocol

               ↓

          BFA Runtime
```

---

## All Systems — General-Purpose Foundation

BFA does not hardcode domain-specific entities (like "Cart" or "Student"); instead, it provides the general-purpose primitives to build any system:

| Domain | Example Services & Components Built with BFA |
| :--- | :--- |
| **E-Commerce** | User, Product Catalog, Cart, Order Processing, Payment Gateway, Inventory |
| **SaaS** | User Management, Organization / Multi-tenancy, Subscription, Billing, Permissions, Workflow Engine |
| **Social Network** | User Profile, Posts, Comments, Likes, Graph / Follows, Direct Messaging, Notifications |
| **Education System** | Student Records, Teachers, Courses, Classes, Grading, Enrollment Pipelines |
| **Game Backend** | Player Identity, Matchmaking, Inventory / Assets, Leaderboards, Real-time Game State |
| **AI Applications** | Model Serving, Dataset Pipelines, Batch Inference, Agent Workflows, Vector Memory |
| **IoT Systems** | Device Registry, Sensor Telemetry Ingestion, Command Dispatch, Edge Event Stream |
| **Enterprise Systems** | Identity Federation, Organization Hierarchy, Business Workflows, Audit Logs, Legacy Integrations |

---

## Documentation Languages & Status

BFA documentation follows a **Single Source of Truth** model rooted in canonical English specifications with community-maintained translations:

| Language | Native Name | Status | Documentation Path |
| :--- | :--- | :--- | :--- |
| **English** | English | 🟢 Canonical (100%) | [docs/en/vision.md](docs/en/vision.md) |
| **Vietnamese** | Tiếng Việt | 🟢 Available (100%) | [docs/vi/vision.md](docs/vi/vision.md) |
| **Japanese** | 日本語 | 🟡 Planned | *Community requested* |
| **Korean** | 한국어 | 🟡 Planned | *Community requested* |
| **Chinese** | 简体中文 | 🟡 Planned | *Community requested* |
| **Spanish** | Español | 🟡 Planned | *Community requested* |
| **French** | Français | 🟡 Planned | *Community requested* |
| **German** | Deutsch | 🟡 Planned | *Community requested* |
| **Portuguese** | Português | 🟡 Planned | *Community requested* |
| **Hindi** | हिन्दी | 🟡 Planned | *Community requested* |
| **Arabic** | العربية | 🟡 Planned | *Community requested* |

For full language registry metadata and contributing instructions, see [docs/README.md](docs/README.md) and [docs/languages.json](docs/languages.json).

---

## Universal Schema & Protocol

* **Universal Schema**: Formally specifies data contracts, field validations, and type mappings across languages.
* **BFA Protocol**: Defines structured envelopes carrying message IDs, target service/method names, typed payloads, error taxonomies, tracing spans, and security contexts across transports (HTTP, gRPC, IPC, WebSocket).
* **Immutable Machine Error Codes**: Error codes (`BFA_SERVICE_NOT_FOUND`) remain constant across all languages, while human-readable diagnostic messages are localized.

---

## BFA Runtime

The BFA Runtime orchestrates service execution:
* **Lifecycle Management**: Standard state transitions (`init`, `start`, `ready`, `stop`, `terminated`).
* **Registry & Discovery**: Local and distributed service catalog and method routing.
* **Health & Probes**: Liveness, readiness, and graceful shutdown coordination.
* **Observability**: Distributed tracing, metrics, and structured logging.

---

## Language SDKs

* **bfa-python** *(Active Reference Implementation)*
* **bfa-go** *(Planned)*
* **bfa-typescript** *(Planned)*
* **bfa-rust** *(Planned)*
* **bfa-java** *(Planned)*
* **bfa-csharp** *(Planned)*
* **bfa-cpp** *(Planned)*
* **bfa-kotlin** *(Planned)*

---

## Plugin Ecosystem

An open extension system for infrastructure integrations:
* **Database**: PostgreSQL, MySQL, SQLite, MongoDB.
* **Messaging**: RabbitMQ, Apache Kafka, NATS, Redis Streams.
* **Authentication**: JWT, OAuth2, OpenID Connect, API Keys.
* **Storage**: S3-compatible, Local Filesystem, Azure Blob, GCS.
* **AI & LLM**: Model runtimes, vector store adapters.
* **Observability**: OpenTelemetry, Prometheus, Jaeger.

---

## BFA Studio & Tooling

* **Code-first, GUI-assisted**: Source code remains the single source of truth.
* **BFA CLI (`bfa`)**: Developer workflow commands (`init`, `dev`, `run`, `test`, `build`, `generate`).
* **BFA Studio**: Visual companion for inspecting service topologies, interactive RPC debugging, live telemetry, and event inspection.

---

## MVP

The initial Minimum Viable Product validates the core specification and cross-language interoperability:

```text
Languages:
├── Python
├── Go
└── TypeScript

Transport:
└── HTTP / gRPC

Database:
└── PostgreSQL

Core:
├── BFA Specification
├── BFA Protocol
├── BFA Runtime
├── BFA CLI
└── BFA SDK
```

---

## Project Structure

```text
backend-for-all/
│
├── README.md
├── LICENSE
├── pyproject.toml
├── .gitignore
│
├── docs/
│   ├── README.md
│   ├── languages.json
│   ├── en/
│   │   ├── vision.md
│   │   ├── architecture.md
│   │   ├── protocol.md
│   │   ├── contributing.md
│   │   └── internationalization.md
│   │
│   └── vi/
│       ├── vision.md
│       ├── architecture.md
│       ├── protocol.md
│       ├── contributing.md
│       └── internationalization.md
│
├── bfa/
│   │
│   ├── __init__.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── service.py
│   │   ├── method.py
│   │   ├── schema.py
│   │   ├── request.py
│   │   ├── response.py
│   │   └── error.py
│   │
│   ├── runtime/
│   │   ├── __init__.py
│   │   ├── runtime.py
│   │   ├── lifecycle.py
│   │   └── registry.py
│   │
│   ├── protocol/
│   │   ├── __init__.py
│   │   ├── encoder.py
│   │   ├── decoder.py
│   │   └── message.py
│   │
│   ├── transport/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── http.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   │
│   └── cli/
│       ├── __init__.py
│       └── main.py
│
├── plugins/
│   └── README.md
│
├── examples/
│   │
│   ├── hello_world/
│   │   └── main.py
│   │
│   ├── user_service/
│   │   └── main.py
│   │
│   └── multi_service/
│       ├── user_service.py
│       └── order_service.py
│
└── tests/
    │
    ├── unit/
    │   ├── test_service.py
    │   ├── test_schema.py
    │   ├── test_registry.py
    │   └── test_protocol.py
    │
    └── integration/
        └── test_services.py
```

---

## ⚡ Quick Start (Khởi Động Nhanh)

### 1. Run BFA Runtime & Studio Console
```bash
python main.py
```

### 2. Access Web Studio & Documentation
- **BFA Studio Management Console:** `http://127.0.0.1:8080`
- **Interactive Documentation & Tutorials:** `http://127.0.0.1:8080/tutorial`

### 3. Universal Technical Contracts & API Exports
- **Universal Invocation Endpoint:** `POST http://127.0.0.1:8080/api/bfa/call`
- **Universal Contract Spec (JSON):** `GET http://127.0.0.1:8080/api/bfa/contract`
- **OpenAPI 3.0 Specification:** `GET http://127.0.0.1:8080/api/bfa/openapi.json`
- **Android Retrofit Contract:** `GET http://127.0.0.1:8080/api/bfa/android-contract`
- **Postman Collection v2.1:** `GET http://127.0.0.1:8080/api/bfa/postman.json`

---

## 🌌 Universal Single Contract (Hợp Đồng Nhất Thể Duy Nhất)

Backend for All provides a **single, universal invocation gateway** for all client platforms (Android, iOS, Flutter, React, Vue, Next.js, Python, Java, C#, PHP):

```text
               ┌────────────────────────────────────────────────────────┐
               │         POST http://127.0.0.1:8080/api/bfa/call        │
               └──────────────────────────┬─────────────────────────────┘
                                          │
                  ┌───────────────────────┼───────────────────────┐
                  ▼                       ▼                       ▼
           [ Single CRUD ]        [ One-Shot Snapshot ]     [ Batch Aggregate ]
        service: "users"           action: "snapshot"        action: "batch"
        action: "find_all"         payload: {                payload: {
        payload: { limit: 10 }       tables: ["users",         queries: {
                                       "products", "orders"]     me: { ... },
                                   }                             catalog: { ... }
                                                             }
```

---

## 📜 Development Logs (DEV_LOGS)

### 🚀 Milestone 7: Universal Single Contract & One-Shot Composite Data (BFF)
- **Universal Invocation Gateway:** Implemented `POST /api/bfa/call` and `GET /api/bfa/contract` as a single, universal entry point for all frontend and mobile languages.
- **One-Shot Composite Snapshot:** Added `POST /api/bfa/snapshot` allowing client applications to fetch all required tables across an entire screen in 1 single HTTP request.
- **Multi-Query Batch Aggregate:** Added `POST /api/bfa/batch` executing multiple distinct service methods within memory in a single round-trip.
- **Unified SDK Generators:** Updated Studio code generators to produce single-contract implementations for Android (Kotlin/Retrofit), Flutter (Dart), React/JS, and Python.

### 📱 Milestone 6: Android Native Contracts & OpenAPI 3.0 Integration
- **OpenAPI 3.0 Document Generation:** Created dynamic `GET /api/bfa/openapi.json` generator reflecting runtime active services and custom endpoints.
- **Android Technical Contract:** Implemented `GET /api/bfa/android-contract` with `AndroidManifest.xml` permissions, `10.0.2.2` emulator base URL, and Retrofit 2 method signatures.
- **Postman Collection v2.1 Export:** Added `GET /api/bfa/postman.json` for one-click API testing across mobile devices.
- **Android Kotlin SDK:** Added complete Retrofit 2 + Coroutines + Gson Singleton client templates to Studio Tab 3.

### 🔍 Milestone 5: System Feature Details Inspector & Modular Table Selection
- **Feature Inspector Modal:** Built `#system-details-modal` providing search, live counts, schema breakdown, and quick action to add custom APIs per table.
- **Modular Table Cherry-Picking:** Enabled developers to activate individual standalone tables without running a full pre-configured blueprint (`POST /api/bfa/cherry-pick`).
- **Dynamic Custom API Creator:** Enabled instant addition of custom endpoints (`POST /api/bfa/add-custom-api`) and deletion (`POST /api/bfa/remove-api`).

### 🎨 Milestone 4: Studio Web Dashboard & Live Flow Topology Visualization
- **Interactive Dashboard:** Built `bfa/web/index.html` with dark theme, responsive layout, SVG icons, and zero-emoji design.
- **Live Architecture Topology:** Created dynamic SVG canvas rendering real-time interconnected nodes between Client, HTTP Transport, BFA Runtime, Active Services, and Storage Engine.
- **Flow Statistics API:** Added `GET /api/bfa/flow-stats` returning live active services count, storage mode, and uptime.
- **Integrated API Tester:** Added instant RPC testing panel with JSON payload editor, response visualizer, and millisecond latency tracking.

### 💾 Milestone 3: Storage Factory & SQLite Persistence
- **Storage Abstraction Layer:** Created `bfa/storage/base.py`, `memory.py`, and `sqlite.py` supporting ACID transactions and query filtering.
- **Automated Database Table Discovery:** Added SQLite inspection and auto-generation of BFA services from pre-existing database tables.
- **Dynamic CRUD Bridge:** Created `generate_services_for_tables` producing 6 standardized CRUD actions (`find_all`, `find_by_id`, `insert`, `update`, `delete`, `query`) per table.

### 🏛️ Milestone 2: 100+ Enterprise Domain Blueprint Catalog
- **Catalog Registry:** Built `bfa/catalog/registry.py` containing 100+ enterprise architecture presets across 10 industry categories:
  - *E-Commerce & Retail (10 blueprints)*
  - *Logistics, Delivery & Transport (10 blueprints)*
  - *Social, Community & Media (10 blueprints)*
  - *Fintech, Banking & Payment (10 blueprints)*
  - *Healthcare & Medical (10 blueprints)*
  - *Education, EdTech & LMS (10 blueprints)*
  - *Hospitality, Travel & F&B (10 blueprints)*
  - *Real Estate & Smart City (10 blueprints)*
  - *Enterprise, ERP & HR (10 blueprints)*
  - *AI, Web3 & High-Tech (10 blueprints)*
- **Catalog Loader:** Implemented `mount_blueprint_to_runtime` for one-click runtime switching and database schema initialization.

### 🏗️ Milestone 1: Core Foundation & Polyglot Runtime Orchestrator
- **Core Abstractions:** Created `Service`, `Method`, `Schema`, `Request`, `Response`, `Error`.
- **In-Memory Runtime:** Built `Runtime` orchestrator managing request dispatching and lifecycle states.
- **Protocol Encoders/Decoders:** Implemented standard JSON wire protocol codec.
- **HTTP Transport Adapter:** Built `HTTPTransport` on top of Python's standard library `http.server` with zero external runtime dependencies.
- **Automated Test Suite:** Created 26 integration and unit tests passing in <1s.

---

## Roadmap

* **Phase 1: Project Foundation** *(Completed)* — Repository skeleton, specification docs, package setup, multilingual docs hub.
* **Phase 2: Core Concepts** *(Completed)* — Service, Method, Request, Response, Error abstractions.
* **Phase 3: Universal Schema** *(Completed)* — Universal schema definition and validation rules.
* **Phase 4: Service Registry** *(Completed)* — In-memory and distributed service registration.
* **Phase 5: Runtime** *(Completed)* — Lifecycle management, coordination, and dispatching.
* **Phase 6: Protocol** *(Completed)* — Wire format, encoders, decoders, and envelope design.
* **Phase 7: Transport** *(Completed)* — HTTP transport adapter and universal invocation gateway.
* **Phase 8: 100+ Domain Blueprints** *(Completed)* — Catalog across 10 industry domains.
* **Phase 9: Storage Engine & CRUD** *(Completed)* — SQLite persistence and schema auto-discovery.
* **Phase 10: BFA Studio Web Console** *(Completed)* — Topology visualization, tester, and code generators.
* **Phase 11: Polyglot SDKs & Contracts** *(Completed)* — Android Kotlin, Flutter, React, OpenAPI 3.0.
* **Phase 12: Python ↔ Go Interoperability** *(In Progress)* — Cross-language binary communication bridge.
* **Phase 13: Python ↔ TypeScript Interoperability** *(Planned)* — Web/Node.js service integration.
* **Phase 14: Distributed Plugin System** *(Planned)* — Message brokers (Kafka, NATS) and OAuth2/JWT auth.

---

## Contributing

We welcome contributions across all language ecosystems, domain specialties, and translation efforts. Please read [English Contributing Guide](docs/en/contributing.md) or [Hướng Dẫn Đóng Góp Tiếng Việt](docs/vi/contributing.md) for details on our specification-first RFC process and pull request workflow.

---

## License

License terms are currently to be determined. See [LICENSE](LICENSE) for details.

