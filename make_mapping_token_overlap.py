#!/usr/bin/env python3
"""
make_mapping_token_overlap.py
Usage:
  python make_mapping_token_overlap.py canonical.txt parse.txt out_mapping.csv [threshold]

For each parse unit, find the canonical unit with the highest token Jaccard
(sim = |tokens_parse ∩ tokens_can| / |tokens_parse ∪ tokens_can|).
If best_sim >= threshold, write (parse_unit_id, canonical_index), else write (parse_unit_id, -1).
"""
import sys, csv, re

def toks(s):
    # simple whitespace + punctuation tokenization, lowercased
    return set(re.findall(r"\w+", s.lower()))

if len(sys.argv) < 4:
    print("Usage: python make_mapping_token_overlap.py canonical.txt parse.txt out_mapping.csv [threshold]")
    raise SystemExit(2)

can_path, parse_path, out_path = sys.argv[1:4]
th = float(sys.argv[4]) if len(sys.argv) > 4 else 0.05

canonical = [l.rstrip("\n") for l in open(can_path, encoding="utf8") if l.strip()]
parse_units = [l.rstrip("\n") for l in open(parse_path, encoding="utf8") if l.strip()]

can_toks = [toks(c) for c in canonical]

with open(out_path, "w", encoding="utf8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["parse_unit_id", "canonical_index"])
    for p in parse_units:
        pt = toks(p)
        best_sim = 0.0
        best_idx = -1
        for i, ct in enumerate(can_toks):
            union = pt | ct
            sim = (len(pt & ct) / len(union)) if union else 0.0
            if sim > best_sim:
                best_sim = sim
                best_idx = i
        if best_sim >= th:
            w.writerow([p, best_idx])
        else:
            w.writerow([p, -1])
print("Wrote", out_path)