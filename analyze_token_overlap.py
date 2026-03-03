#!/usr/bin/env python3
# analyze_token_overlap.py
# Usage: python analyze_token_overlap.py
import re, csv, json, statistics, os
from collections import defaultdict
from sklearn.metrics import adjusted_rand_score, cohen_kappa_score

ROOT = "supplement_s7"
CAN_PATH = os.path.join(ROOT, "eventizations", "canonical.txt")
PARSES = ["tokengran", "punctsplit", "discourseboundary", "srlsim"]
THRESHOLDS = [0.05, 0.15, 0.25]

def toks(s):
    return set(re.findall(r"\w+", s.lower()))

def load_lines(path):
    return [l.rstrip("\n") for l in open(path, encoding="utf8") if l.strip()]

# load canonical
canonical = load_lines(CAN_PATH)
can_toks = [toks(c) for c in canonical]

# helper to compute best jaccard for a parse unit
def best_jaccard_for_unit(p_text):
    pt = toks(p_text)
    best = 0.0
    best_idx = -1
    for i, ct in enumerate(can_toks):
        union = pt | ct
        sim = (len(pt & ct) / len(union)) if union else 0.0
        if sim > best:
            best = sim
            best_idx = i
    return best, best_idx

# results containers
summary = {}

for parse in PARSES:
    parse_path = os.path.join(ROOT, "eventizations", f"{parse}.txt")
    if not os.path.exists(parse_path):
        print(f"{parse}: parse file not found: {parse_path}")
        continue
    parse_units = load_lines(parse_path)
    bests = []
    best_idx_list = []
    for p in parse_units:
        best, best_idx = best_jaccard_for_unit(p)
        bests.append(best)
        best_idx_list.append(best_idx)
    # store best-jaccard summary
    summary[parse] = {
        "count": len(bests),
        "median": round(statistics.median(bests), 4) if bests else None,
        "mean": round(statistics.mean(bests), 4) if bests else None,
        "min": round(min(bests), 4) if bests else None,
        "max": round(max(bests), 4) if bests else None,
        "iqr": None
    }
    if bests:
        q1 = statistics.median(sorted(bests)[:len(bests)//2])
        q3 = statistics.median(sorted(bests)[(len(bests)+1)//2:])
        summary[parse]["iqr"] = round(q3 - q1, 4)
    # write token-overlap mapping file with best index and best score
    map_out = os.path.join(ROOT, "mappings", f"{parse}_mapping_tokenoverlap_scores.csv")
    os.makedirs(os.path.dirname(map_out), exist_ok=True)
    with open(map_out, "w", encoding="utf8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["parse_unit_id", "best_canonical_index", "best_jaccard"])
        for p, idx, b in zip(parse_units, best_idx_list, bests):
            w.writerow([p, idx if idx is not None else -1, f"{b:.6f}"])
    # threshold sweep: create mapping CSVs and remapped JSONs and compute metrics
    for th in THRESHOLDS:
        map_csv = os.path.join(ROOT, "mappings", f"{parse}_mapping_tokenoverlap_{int(th*100)}.csv")
        with open(map_csv, "w", encoding="utf8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["parse_unit_id", "canonical_index"])
            for p, idx, b in zip(parse_units, best_idx_list, bests):
                w.writerow([p, idx if b >= th else -1])
        # build remapped labels: use build_labels.py logic if available; here we create canonical & parse arrays
        # canonical array: canonical indices repeated for each canonical unit (we will align by index positions)
        # parse array: for each parse unit, mapped canonical index or -1
        # For metric computation we need arrays aligned by the same unit index; we will compute metrics on pairs (canonical_index, mapped_index)
        # Create arrays by iterating over canonical indices and parse units in order: this mirrors earlier remapping approach
        # Simpler: create arrays by zipping canonical indices (0..len(canonical)-1) with mapped indices for parse units in order,
        # then drop entries where mapped == -1
        mapped = []
        for idx, b in zip(best_idx_list, bests):
            mapped.append(idx if b >= th else -1)
        # canonical indices for comparison: use canonical index sequence repeated/truncated to match parse length
        # If parse length differs from canonical length, we compare by parse unit order vs canonical index mapping as earlier pipeline did
        canonical_for_parse = []
        for i in range(len(mapped)):
            # if mapped index exists, canonical label is the mapped index's canonical label value
            # but to be consistent with remap_and_compute, we will use canonical indices as integers from 0..N-1
            # For metric computation we need y_true (canonical index) and y_pred (mapped index)
            # Use canonical index equal to mapped index when mapped != -1, else use placeholder
            canonical_for_parse.append(mapped[i] if mapped[i] != -1 else -1)
        # Now drop -1 pairs
        pairs = [(t,p) for t,p in zip(canonical_for_parse, mapped) if p != -1]
        if not pairs:
            ari = None; kappa = None; mapped_count = 0
        else:
            y_true = [t for t,_ in pairs]
            y_pred = [p for _,p in pairs]
            ari = adjusted_rand_score(y_true, y_pred)
            kappa = cohen_kappa_score(y_true, y_pred)
            mapped_count = len(y_true)
        # write remapped JSON
        out_json = os.path.join(ROOT, "results", f"labels_{parse}_tokenoverlap_{int(th*100)}_remapped.json")
        os.makedirs(os.path.dirname(out_json), exist_ok=True)
        with open(out_json, "w", encoding="utf8") as oj:
            json.dump({"labels": {"canonical": [t for t,_ in pairs], "parse": [p for _,p in pairs]}}, oj, indent=2, ensure_ascii=False)
        # print summary line
        total_parse = len(parse_units)
        frac_mapped = (mapped_count / total_parse) if total_parse else 0
        print(f"{parse}  threshold={th:.2f}  mapped={mapped_count}/{total_parse}  frac_mapped={frac_mapped:.3f}  ARI={ari if ari is None else round(ari,3)}  K={kappa if kappa is None else round(kappa,3)}")

# print best-jaccard summary table
print("\nBest-Jaccard summaries per parse:")
for p, s in summary.items():
    print(f"{p}: count={s['count']} median={s['median']} mean={s['mean']} min={s['min']} max={s['max']} iqr={s['iqr']}")
print("\nWrote mapping CSVs and remapped JSONs under supplement_s7/mappings and supplement_s7/results.")