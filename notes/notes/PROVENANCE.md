# Provenance Notes

This file records decisions, workflow changes, and rationale for the Ingarden Experiments repository.  
Entries should be brief, dated, and focused on reproducibility and auditability.

---

## 2026‑03‑07 — Repository Initialization

- Created new repository `ingarden-experiments` to serve as the authoritative home of the Ingarden Project.
- Established clean directory structure:
  - `scripts/`
  - `data/`
  - `outputs/`
  - `notes/`
  - `supplement/`
- Added `.gitignore` to prevent accidental commits of caches, temporary files, and large generated artifacts.
- Added initial README describing purpose, structure, and reproducibility philosophy.
- Decision: abandon previous repository (`ingarden-project`) due to persistent Zenodo/GitHub integration failures and UI inconsistencies.  
  This repository replaces it entirely.

---

## How to Add Future Entries

Each time a script, dataset, supplement, or workflow changes in a way that affects reproducibility, add a short entry:

**Example template:**

### YYYY‑MM‑DD — Short description of change
- What changed  
- Why it changed  
- Any implications for reproducibility  
- Any files, commits, or parameters involved  

This ensures long‑term clarity for reviewers and for future you.
