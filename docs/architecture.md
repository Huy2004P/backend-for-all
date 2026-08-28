# Conceptual Architecture — Backend for All (BFA)

## 1. Overview & Dual-Axis Architecture

Backend for All is architected around two core axes: **All Languages** (Polyglot) and **All Systems** (Universal Domain Capabilities).

```text
                    BACKEND FOR ALL
                           │
             ┌─────────────┴─────────────┐
             │                           │
        ALL LANGUAGES               ALL SYSTEMS
             │                           │
      ┌──────┼──────┐          ┌────────┼────────┐
      │      │      │          │        │        │
   Python   Go    Java       Shop     SaaS     AI
      │      │      │          │        │        │
    Rust    C++   TypeScript  Social  Game     IoT
      │      │      │          │        │        │
      └──────┼──────┘          └────────┼────────┘
             │                           │
             └─────────────┬─────────────┘
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

## 2. The Architectural Stack

The BFA architecture is composed of distinct, decoupled layers:

### Layer 1: BFA Foundation
- **BFA Specification**: Formal, language-agnostic standards for defining services, methods, schemas, error taxonomies, and event semantics.
- **BFA Protocol**: Universal binary and text wire protocol defining request/response envelopes, streaming frames, metadata headers, and distributed tracing contexts.
- **BFA Runtime**: The coordination engine managing service registration, discovery, health checking, state transitions, and transport dispatching.

### Layer 2: BFA Building Blocks (The Backend LEGO)
The universal primitives provided to all language SDKs:
- **Service**: Logical boundary and deployable unit.
- **Method / Function**: Strongly typed RPC procedure or streaming endpoint.
- **Schema**: Universal data contracts and validation rules.
- **Request / Response**: Uniform envelopes with tracing, tenancy, and payload semantics.
- **Event / Messaging**: Pub/sub topic definitions and message dispatching.
- **Storage Abstraction**: Universal interfaces for key-value, document, and relational persistence.
- **Auth & Security**: Uniform context carrying identity, roles, and permissions.
- **Configuration**: Layered settings, environment overrides, and secrets management.
- **Observability**: Distributed tracing, metrics emission, and structured logging.

### Layer 3: Language SDK Layer
Language-native reference bindings implementing the BFA Specification:
- `bfa-python` *(Initial reference & validator)*
- `bfa-go`
- `bfa-typescript`
- `bfa-rust`
- `bfa-java`
- `bfa-csharp`
- `bfa-cpp`
- `bfa-kotlin`

### Layer 4: Pluggable Transport & Plugin Layer
- **Transport Adapters**: HTTP/REST, gRPC, WebSockets, IPC/UDS, Message Queues.
- **Plugin Ecosystem**: Connectors for PostgreSQL, Kafka, Redis, S3, OIDC, OpenTelemetry, etc.

### Layer 5: Developer Tooling Layer
- **BFA CLI (`bfa`)**: Developer workflow automation (`init`, `dev`, `run`, `test`, `build`, `generate`).
- **BFA Studio**: Code-first visual developer interface for topology visualization, RPC testing, and live inspection.

---

## 3. Polyglot & Multi-Domain Interaction Model

Services in different languages collaborate effortlessly across diverse application domains:

```text
[ Go Service: Payment ] ──(BFA Request Envelope)──► [ BFA Protocol ]
                                                           │
                                                   (Transport Layer)
                                                           │
[ Java Service: Orders ] ◄──(BFA Request Envelope)─────────┼──────────► [ Python Service: AI ]
```

Each service only needs to implement its local BFA SDK bindings. The underlying BFA Protocol and Runtime manage serialization, transport delivery, tracing propagation, and error translation transparently.
