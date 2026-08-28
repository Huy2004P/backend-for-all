# Contributing to Backend for All (BFA)

Thank you for your interest in contributing to Backend for All! We welcome contributions from developers across all programming languages, domains, and global communities.

---

## 1. Ten Core Principles Alignment

All contributions to BFA should align with our **Ten Core Principles**:
1. **Open by default**: Open-source, community-owned, and vendor-neutral.
2. **Language independent**: Equal support across programming languages (All Languages).
3. **System independent**: Universal building blocks for any domain (All Systems).
4. **Developer accessible**: Global multilingual documentation and tooling (All Developers).
5. **Code-first**: Plain source code is the single source of truth.
6. **GUI-assisted**: Visual interfaces assist without creating proprietary lock-in.
7. **Interoperable**: Frictionless cross-language communication and universal schemas.
8. **Extensible**: Modular plugin architecture for external infrastructure.
9. **Community-driven**: Transparent governance, open RFCs, and peer review.
10. **Specification-first**: Formal specifications precede implementation.

---

## 2. Types of Contributions

You can contribute to BFA in multiple ways:
- **Core Specifications & Protocols**: Proposing RFCs for service models, message formats, and schemas.
- **Language SDKs**: Implementing or improving SDK bindings (Python, Go, Rust, Java, TypeScript, etc.).
- **Runtime & Transports**: Enhancing runtime coordinators, HTTP/gRPC transports, and discovery logic.
- **Plugins & Integrations**: Building connectors for databases, messaging systems, auth providers, and telemetry.
- **Documentation & Tutorials**: Writing conceptual guides, architecture deep-dives, and domain examples.
- **Translations & Localization**: Translating documentation into your native language and keeping it synchronized.

---

## 3. Specification-First RFC Process

> [!IMPORTANT]
> BFA is built on a shared, language-independent foundation. **Core specifications, protocol definitions, runtime architecture changes, and schema models must be proposed and discussed via an RFC / Issue before writing implementation code.**

---

## 4. Translation & Documentation Contribution Workflow

For contributors translating documentation into regional languages:

1. **Reference Canonical Source**: Always base translations on the canonical English files in `docs/en/`.
2. **Preserve Technical Identifiers**: Do not translate code symbols, method names, protocol verbs, or machine error codes (`BFA_SERVICE_NOT_FOUND`).
3. **Ensure Technical Precision**: Prioritize accurate engineering terminology over literal translation.
4. **Follow Directory Structure**: Place translations under `docs/<lang_code>/` matching the file hierarchy in `docs/en/`.
5. **Update Language Metadata**: Update `docs/languages.json` with the translation progress and status.

---

## 5. General Contribution Workflow

1. **Fork the Repository**  
   Create your own fork of `backend-for-all` on GitHub.

2. **Clone Locally**  
   ```bash
   git clone https://github.com/<your-username>/backend-for-all.git
   cd backend-for-all
   ```

3. **Create a Feature Branch**  
   ```bash
   git checkout -b feature/my-contribution
   ```

4. **Make Changes**  
   - Follow standard coding guidelines and formatting.
   - Adhere to the "Standard library first" philosophy for core modules.
   - Avoid introducing unnecessary external dependencies.

5. **Run Tests**  
   ```bash
   pytest
   ```

6. **Submit a Pull Request**  
   - Push your branch to your fork.
   - Open a PR targeting `main`.
   - Describe the changes clearly and reference any associated RFC or Issue.
