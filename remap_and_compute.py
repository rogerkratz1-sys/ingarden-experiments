#!/usr/bin/env python3
# remap_and_compute.py
import csv, json, sys
from sklearn.metrics import adjusted_rand_score, cohen_kappa_score

if len(sys.argv) < 4:
    print("Usage: python remap_and_compute.py labels.json mapping.csv out_prefix")
    raise SystemExit(2)

labels_json, mapping_csv, out_prefix = sys.argv[1:4]

# load labels JSON
j = json.load(open(labels_json, 'r', encoding='utf8'))
can = j['labels']['canonical']
parse = j['labels']['parse']

# load mapping: normalize parse_unit_id keys to stripped strings
m = {}
with open(mapping_csv, newline='', encoding='utf8') as f:
    reader = csv.reader(f)
    rows = list(reader)
    if not rows:
        pass
    else:
        # if header present, skip it
        start = 1 if any('parse_unit_id' in c.lower() for c in rows[0]) else 0
        for r in rows[start:]:
            if len(r) < 2:
                continue
            pu = r[0]
            ci_raw = r[1]
            try:
                ci = int(ci_raw)
            except:
                try:
                    ci = int(ci_raw.strip().strip('"').strip("'"))
                except:
                    continue
            key = str(pu).strip()
            m[key] = ci

# helper to normalize parse value for lookup
def norm_key(v):
    if v is None:
        return ''
    return str(v).strip()

# remap parse labels to canonical indices; unmapped -> -1
remapped = []
for p in parse:
    k = norm_key(p)
    mapped = None
    if k in m:
        mapped = m[k]
    else:
        # try additional fallbacks: numeric string -> int key, or original p as-is
        if k.isdigit():
            if int(k) in m:
                mapped = m[int(k)]
    remapped.append(mapped if mapped is not None else -1)

# drop unmapped entries (-1) before computing metrics
pairs = [(t,r) for t,r in zip(can, remapped) if r != -1]
if not pairs:
    raise SystemExit("No mapped items found after remapping.")
y_true = [t for t,_ in pairs]
y_pred = [r for _,r in pairs]

# compute metrics
ari = adjusted_rand_score(y_true, y_pred)
k = cohen_kappa_score(y_true, y_pred)

# write remapped JSON
out_json = f"{out_prefix}_remapped.json"
json.dump({'labels':{'canonical': y_true, 'parse': y_pred}}, open(out_json,'w', encoding='utf8'), indent=2, ensure_ascii=False)

print("Wrote", out_json)
print("ARI,{:.3f}".format(ari))
print("CohensK,{:.3f}".format(k))