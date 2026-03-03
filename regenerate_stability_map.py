# 1) Go to repo root
Set-Location -Path "C:\Users\ctint\Desktop\Scripts\repo_candidate"

# 2) Create and activate virtual environment (only if not already active)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3) Install dependencies (adjust if you use a different requirements file)
pip install --upgrade pip
if (Test-Path .\requirements.txt) { pip install -r requirements.txt } else { Write-Host "requirements.txt not found; install dependencies manually" }

# 4) Ensure permutations file exists (compute_stability expects 5000 permutations)
if (-Not (Test-Path .\data\permutations_5000.csv)) { Write-Host "WARNING: data\permutations_5000.csv not found; create or copy it before running the script" }

# 5) Run your regeneration script (this should produce supplement/S-8/diagnostics/stability_map.csv)
python .\regenerate_stability_map.py --permutations-file data\permutations_5000.csv --outdir supplement\S-8\diagnostics

# 6) Quick verification: list and preview the produced file
Get-ChildItem -Path .\supplement\S-8\diagnostics -File | Select-Object Name,Length,LastWriteTime
Get-Content -Path .\supplement\S-8\diagnostics\stability_map.csv -TotalCount 10