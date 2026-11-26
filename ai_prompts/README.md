# Team Nova — AI & Prompt Engineering (`feature/ai-prompts`)

AI-powered Pre-Visit Government Service Guide & Step-by-Step Form Filling Assistant for Sri Lankan citizens (**Sinhala, Tamil, English, Singlish, Tanglish**), built for **AI Kasthiram Buildathon 2026 (Track 1: Government Digitalisation)**.

## Stack & Privacy Rule

- **Model:** Gemini 2.5 Flash (`google-genai` SDK with Structured Outputs)
- **Backend Integration:** FastAPI (Stateless endpoints)
- **Zero-Storage Privacy Rule:** No NIC numbers, phone numbers, addresses, or document photos are stored in any database or logs. All inputs are processed in-memory and discarded immediately. Raw PII is omitted/redacted (`pii_redacted: true`) in JSON responses.

## Covered Departments

1. **DMT (Department of Motor Traffic):** Driving Licence Renewal / Duplicate Licence
2. **Department of Immigration & Emigration:** Passport Application / Renewal & Lost Passport Request Letter
3. **Divisional Secretariat & Grama Niladhari (DS_GN):** Residency/Character Certifications, Jargon Simplification, Document Validity Check

## Folder Structure

Each AI module folder contains 3 standard files:

- `system_instruction.txt` — Prompt rules & persona for Gemini 2.5 Flash (for **Backend**)
- `schema.json` — Strict JSON Schema for Structured Outputs (for **Backend**)
- `sample_output.json` — Verified example response (for **Frontend** UI mapping)

```text
ai_prompts/
├── README.md
├── common/
│   └── common_schema.py          # Shared Pydantic envelope across all AI endpoints
├── member_a/                     # AI Member A (Team Lead)
│   ├── 01_pre_visit_advisor/
│   ├── 02_nic_scan_to_guide/
│   └── 03_form_error_checker/
└── member_b/                     # AI Member B (Co-AI Member)
    ├── 01_document_validity_checker/
    ├── 02_snap_to_explain/
    ├── 03_jargon_simplifier/
    └── 04_official_letter_drafter/
```
