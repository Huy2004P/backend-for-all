# Multilingual Documentation & Internationalization (i18n)

Backend for All (BFA) is committed to global developer accessibility. Our mission is to eliminate natural language barriers so developers worldwide can understand, adopt, and contribute to BFA in their native languages.

---

## 1. Core Architecture & Single Source of Truth

To prevent divergence and maintain strict architectural integrity, BFA enforces a **Single Source of Truth** model:

```text
                  BFA Canonical Specification
                               │
                               ▼
               Canonical Documentation (English)
                               │
         ┌─────────────┬───────┴───────┬─────────────┐
         ▼             ▼               ▼             ▼
    Tiếng Việt      日本語           한국어          Español
     (vi)           (ja)            (ko)           (es)
```

1. **Canonical Documentation (`docs/en/`)**: The authoritative source of truth. All specification changes, API modifications, and architecture updates originate here in English.
2. **Synchronized Representations (`docs/<lang_code>/`)**: Translated documentation sets that represent the canonical specification in regional languages.
3. **Outdated Detection**: When canonical documents change, translations are marked as *Needs Update* until synchronized by community contributors.

---

## 2. Rule of Technical Terminology

> [!CRITICAL]
> **Technical identifiers, code symbols, API constructs, and machine-readable error codes must NEVER be translated in source code or APIs.**

Translations localize **explanations, prose, conceptual descriptions, and guides**—not code identifiers.

| Type | Rule | Correct Example | Incorrect Example |
| :--- | :--- | :--- | :--- |
| **Code Identifiers** | Keep Original English | `class Service:`, `def handle_request():` | `class DịchVụ:`, `def xử_lý_yêu_cầu():` |
| **BFA Primitives** | Explain in native language; preserve term | *Tiếng Việt*: "BFA Service là một đơn vị logic..." | *Tiếng Việt*: "BFA BộPhụcVụ là..." |
| **Machine Error Codes** | Keep Immutable | `BFA_SERVICE_NOT_FOUND` | `BFA_KHONG_TIM_THAY_SERVICE` |
| **Human Error Messages** | Localize freely | *EN*: "Service 'users' not found."<br>*VI*: "Không tìm thấy service 'users'." | Changing error code alongside message |

---

## 3. Translation Quality & Human Review

- **Accuracy over Literal Translation**: Prioritize technical clarity and conceptual accuracy over word-for-word translation.
- **Role of AI / Machine Translation**: AI and automated translation tools may be used to draft initial translations. However, **human review by native-speaking engineers is required** before merging into official documentation.
- **Untranslatable Concepts**: If a technical term lacks a natural equivalent in a target language (e.g., *middleware*, *broker*, *payload*), keep the English term and provide context in the surrounding prose.

---

## 4. Documentation Directory Structure

```text
docs/
├── README.md               # Documentation portal & translation status
├── languages.json          # Machine-readable language registry metadata
├── en/                     # Canonical Documentation (Source of Truth)
│   ├── vision.md
│   ├── architecture.md
│   ├── protocol.md
│   ├── contributing.md
│   └── internationalization.md
│
├── vi/                     # Vietnamese Translation
│   ├── vision.md
│   ├── architecture.md
│   ├── protocol.md
│   ├── contributing.md
│   └── internationalization.md
│
└── <lang>/                 # Future Community Translations (ja, ko, zh, es, etc.)
```

---

## 5. Translation Contribution Lifecycle

1. **Check Status**: Inspect `docs/languages.json` and `docs/README.md` for existing progress and maintainers.
2. **Sync with Canonical**: Read the corresponding file under `docs/en/`.
3. **Draft Translation**: Translate prose while preserving all code blocks, technical terms, and link structures.
4. **Review & PR**: Submit a Pull Request targeting the main repository with descriptive metadata.
5. **Ongoing Sync**: Watch for RFCs and updates to `docs/en/` to keep translations updated.
