#!/usr/bin/env python3
"""
Usage:
  python build_labels.py canonical.txt parse.txt mapping.csv out_labels.json

mapping.csv should contain two columns: parse_unit_id and canonical_index.
If the header names differ, the script will use the first two columns.
If mapping.csv == "NONE", the script will align by line index.
"""
import sys, csv, json
from collections import defaultdict

def load_lines(path):
    with open(path, 'r', encoding='utf8') as f:
        return [line.rstrip('\n') for line in f if line.strip()]

def load_mapping(path):
    if path.upper() == "NONE":
        return None
    m = {}
    with open(path, 'r', encoding='utf8', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)
        if not rows:
            return {}
        header = rows[0]
        # If header looks like two columns with expected names, use DictReader semantics
        if len(header) >= 2 and ('parse_unit_id' in [h.strip() for h in header] and 'canonical_index' in [h.strip() for h in header]):
            # use csv.DictReader to preserve quoting behavior
            f.seek(0)
            dreader = csv.DictReader(f)
            for row in dreader:
                # tolerate whitespace in header names
                keys = {k.strip(): v for k, v in row.items()}
                if 'parse_unit_id' in keys and 'canonical_index' in keys:
                    try:
                        m[keys['parse_unit_id']] = int(keys['canonical_index'])
                    except:
                        pass
        else:
            # treat first column as parse_unit_id and second as canonical_index
            for r in rows[1:]:
                if len(r) < 2:
                    continue
                pu = r[0]
                try:
                    ci = int(r[1])
                except:
                    # try stripping quotes/spaces
                    try:
                        ci = int(r[1].strip().strip('"').strip("'"))
                    except:
                        continue
                m[pu] = ci
    return m

def aggregate(parse_units, mapping):
    agg = defaultdict(list)
    if mapping is None:
        for i, pu in enumerate(parse_units):
            agg[i].append(pu)
    else:
        for pu in parse_units:
            # exact match on parse_unit_id string
            if pu in mapping:
                agg[mapping[pu]].append(pu)
            else:
                # try trimmed variant
                key = pu.strip()
                if key in mapping:
                    agg[mapping[key]].append(pu)
    return agg

def main():
    if len(sys.argv) < 5:
        print("Usage: python build_labels.py canonical.txt parse.txt mapping.csv out_labels.json")
        sys.exit(2)
    can_path, parse_path, map_path, out_path = sys.argv[1:5]
    canonical = load_lines(can_path)
    parse_units = load_lines(parse_path)
    mapping = load_mapping(map_path)
    agg = aggregate(parse_units, mapping)
    n = len(canonical)
    labels_canonical = list(range(n))
    labels_parse = [-1]*n
    for idx in range(n):
        if idx in agg and agg[idx]:
            labels_parse[idx] = agg[idx][0]
        else:
            labels_parse[idx] = -1
    out = {
        "metadata": {
            "canonical_path": can_path,
            "parse_path": parse_path,
            "mapping_path": map_path,
            "aggregation_rule": "first_parse_unit_or_index",
        },
        "labels": {
            "canonical": labels_canonical,
            "parse": labels_parse
        }
    }
    with open(out_path, 'w', encoding='utf8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("Wrote", out_path)

if __name__ == "__main__":
    main()