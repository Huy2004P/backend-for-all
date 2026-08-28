# Contributing to Backend for All (BFA)

Thank you for your interest in contributing to Backend for All! We welcome contributions from developers across all programming language ecosystems, domains, and backgrounds.

---

## 1. Core Principles Alignment

All contributions to BFA should align with our **Ten Core Principles**:
1. Open by default
2. Language independent (All Languages)
3. System independent (All Systems)
4. Code-first
5. GUI-assisted
6. Interoperable
7. Extensible
8. Developer-first
9. Community-driven
10. Specification-first

---

## 2. Specification-First Principle

> [!IMPORTANT]
> BFA is built on a shared, language-independent and system-independent foundation. **Core specifications, protocol definitions, and runtime architectural changes must be discussed and agreed upon via an RFC / Issue before submitting major pull requests.**

If you want to propose changes to:
- Protocol message envelopes or wire formats
- Universal schema specifications
- Core service lifecycle state machines
- Cross-language interoperability standards
- Universal building block interfaces

Please open an **Issue / Discussion (RFC)** first to outline your proposal.

---

## 3. Contribution Workflow

To contribute code or documentation:

1. **Fork the Repository**  
   Create your own fork of `backend-for-all` on GitHub.

2. **Clone Locally**  
   ```bash
   git clone https://github.com/<your-username>/backend-for-all.git
   cd backend-for-all
   ```

3. **Create a Feature Branch**  
   ```bash
   git checkout -b feature/my-new-feature
   ```

4. **Make Changes**  
   - Follow the established coding standards.
   - Adhere to the "Standard library first" philosophy.
   - Avoid adding unnecessary external dependencies.
   - Keep code modular, well-documented, and readable.

5. **Run Tests**  
   Ensure all unit and integration tests pass:
   ```bash
   pytest
   ```

6. **Submit a Pull Request**  
   - Push your branch to your fork.
   - Open a Pull Request targeting the `main` branch.
   - Provide a clear, descriptive summary of the changes and link any related RFC / issue.

---

## 4. Code of Conduct & Community Guidelines

- Be respectful, constructive, and collaborative.
- Respect all programming language communities and domain paradigms equally.
- Keep discussions focused on engineering merit, interoperability, simplicity, and ergonomics.
