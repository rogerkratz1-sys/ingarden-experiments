A root‑level README should give anyone landing on the repository a clear, high‑level orientation: what the project is, how the repository is structured, and where to find the manuscript, supplements, appendices, and reproducibility materials. It should complement (not duplicate) `manifest.txt`, and it should match the clean architecture you’ve now established.

Here is a polished, publication‑ready `README.md` you can paste directly into the repo root.

---

# Ingarden Project Repository

This repository contains the manuscript, supplements, appendices, and reproducibility materials for the Ingarden Project. The structure is designed to provide clarity for reviewers, maintain provenance, and support full reproducibility of all analyses.

The repository is organized into three primary layers:

- **supplement/** — canonical Supplement S‑1 through S‑8, plus artifact bundles for S‑7 and S‑8  
- **appendices/** — canonical Appendix A through Appendix I  
- **docs/** — lightweight pointer files for Supplements S‑1 through S‑8  

A complete index of all long‑form materials is provided in `manifest.txt` at the repository root.

---

## Repository Structure

### supplement/
This directory contains the authoritative versions of all eight supplements.  
Supplements S‑7 and S‑8 include full artifact bundles with diagnostics, mappings, stability analyses, and configuration files.  
A dedicated `README.md` inside this directory describes the contents and structure in detail.

### appendices/
This directory contains the canonical versions of Appendix A through Appendix I.  
Each appendix is stored as a standalone text file.  
A dedicated `README.md` inside this directory provides an overview of the appendix materials.

### docs/
This directory contains only pointer files for Supplements S‑1 through S‑8.  
These files preserve legacy paths and ensure manuscript links remain stable.  
All canonical supplement content resides in the `supplement/` directory.

### manifest.txt
A complete index of all supplements, appendices, artifact bundles, and pointer files.  
This file serves as the authoritative map of the repository.

---

## Reproducibility Materials

Artifact bundles for S‑7 and S‑8 contain:

- diagnostics and stability analyses  
- eventizations and mappings  
- intermediate and final results  
- configuration files  
- provenance and checksum files  

These bundles provide full transparency into the computational workflow and support independent verification of all results.

---

## Notes on Usage

- All long‑form materials (supplements and appendices) reside exclusively in their respective directories.  
- Pointer files in `docs/` exist only for navigation and backward compatibility.  
- No supplement or appendix content should be stored in the repository root or in `docs/`.  
- The repository is designed to be self‑narrating: each directory includes a README where appropriate, and `manifest.txt` provides a complete index.

---


