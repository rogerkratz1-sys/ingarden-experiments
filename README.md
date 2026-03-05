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
This directory contains the authoritative versions of all eight supplements. Supplements S‑7 and S‑8 include full artifact bundles with diagnostics, mappings, stability analyses, and configuration files. A dedicated `README.md` inside this directory describes the contents and structure in detail.

### appendices/
This directory contains the canonical versions of Appendix A through Appendix I. Each appendix is stored as a standalone text file. A dedicated `README.md` inside this directory provides an overview of the appendix materials.

### docs/
This directory contains only pointer files for Supplements S‑1 through S‑8. These files preserve legacy paths and ensure manuscript links remain stable. All canonical supplement content resides in the `supplement/` directory.

### manifest.txt
A complete index of all supplements, appendices, artifact bundles, and pointer files. This file serves as the authoritative map of the repository.

---

## Reproducibility Quick Start

This section provides a concise, end‑to‑end guide for reproducing the computational results underlying the manuscript. All canonical supplement texts, appendices, and artifact bundles are stored in the repository under the `supplement/` and `appendices/` directories. The full index of long‑form materials is available in `manifest.txt`.

### Environment Setup

Use either a conda or pip environment with pinned versions:

```bash
conda env create -f environment.yml
conda activate ingarden-project
```

or

```bash
pip install -r requirements.txt
```

The environment files include pinned versions of the packages required to run the full pipeline, including pandas, numpy, scipy, scikit‑learn, scikit‑posthocs, seaborn, and matplotlib.

### Pipeline Overview

The workflow consists of the following stages:

- enumerating linear extensions  
- computing features and score_dir  
- fitting κ/α displacement parameters  
- computing the Kendall distance matrix  
- embedding via hybrid dissimilarity (classical or nonmetric)  
- clustering and selecting representative exemplars  
- assigning motifs  
- computing Dunn/Cliff posthoc statistics  
- generating publication tables and figures  

All scripts referenced below are included in the repository and documented in the S‑7 and S‑8 supplement artifact bundles.

### Reproduction Commands

```bash
# 1. Enumerate linear extensions
python compute_linear_extensions.py \
  --out all_perms.csv --seed 42

# 2. Compute features and score_dir
python score_extensions.py \
  --in all_perms.csv --out all_scored.csv --seed 42

# 3. Fit kappa displacement (grid search)
python compute_kappa_disp.py \
  --in all_scored.csv --out kappa_fit.json --seed 42

# 4. Compute Kendall distance matrix
python compute_kendall_matrix.py \
  --in all_perms.csv --out kendall_distance_matrix.npy

# 5. Embed in 3D (classical or nonmetric)
python mds_embed.py \
  --kendall kendall_distance_matrix.npy \
  --kappa kappa_fit.json \
  --method nonmetric \
  --dims 3 \
  --out combined_coords_nystrom_rotated_v5.csv

# 6. Cluster and select representative exemplars
python cluster_and_representative_exemplars.py \
  --in combined_coords_nystrom_rotated_v5.csv \
  --out representative_exemplars.csv

# 7. Assign motifs
python assign_motif.py \
  --in all_scored.csv \
  --coords combined_coords_nystrom_rotated_v5.csv \
  --out assigned_motifs.csv

# 8. Compute Dunn posthoc and Cliff's delta
python compute_dunn_and_cliff.py \
  --in all_scored.csv \
  --clusters assigned_motifs.csv \
  --out dunn/

# 9. Build publication tables and figures
python build_report.py \
  --in all_scored.csv --out publication_table.csv

python make_publication_figure.py \
  --in combined_coords_nystrom_rotated_v5.csv \
  --out figures/
```

### Essential Files for Reproduction

The following files are required to reproduce the manuscript’s figures and tables:

- `all_perms.csv`  
- `all_scored.csv`  
- `combined_coords_nystrom_rotated_v5.csv`  
- `assigned_motifs.csv`  
- `representative_exemplars.csv`  
- `kappa_fit.json`  
- `kendall_distance_matrix.npy` (optional; can be recomputed)  
- `publication_table.csv`  
- all scripts listed above  
- `environment.yml` or `requirements.txt`  

All additional diagnostics, stability analyses, and intermediate outputs are stored in the S‑7 and S‑8 artifact bundles under `supplement/`.

### Notes on Repository Layout

This repository does not use top‑level `/data/` or `/artifacts/` directories. Instead:

- canonical supplement texts are stored in `supplement/`  
- canonical appendices are stored in `appendices/`  
- pointer files are stored in `docs/`  
- reproducibility materials are stored in the S‑7 and S‑8 artifact bundles  
- `manifest.txt` provides a complete index of all long‑form materials  

This structure ensures clarity, provenance, and long‑term maintainability.

---

