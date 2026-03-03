#!/usr/bin/env python3
import sys, json
from sklearn.metrics import adjusted_rand_score, cohen_kappa_score

def encode_labels(y_true, y_pred, drop_negative=True):
    # Optionally drop entries where y_pred == -1 (unmapped)
    pairs = [(t,p) for t,p in zip(y_true, y_pred) if not (drop_negative and p == -1)]
    if not pairs:
        raise SystemExit("No data left after dropping unmapped entries.")
    t_vals = [t for t,_ in pairs]
    p_vals = [p for _,p in pairs]
    # Build a shared label-to-int mapping from union of values
    unique = []
    for v in t_vals + p_vals:
        if v not in unique:
            unique.append(v)
    mapping = {v:i for i,v in enumerate(unique)}
    y_true_enc = [mapping[v] for v in t_vals]
    y_pred_enc = [mapping[v] for v in p_vals]
    return y_true_enc, y_pred_enc

if len(sys.argv) < 2:
    print("Usage: python compute_metrics.py labels.json")
    raise SystemExit(2)

j = json.load(open(sys.argv[1], 'r', encoding='utf8'))
y_true = j['labels']['canonical']
y_pred = j['labels']['parse']
if len(y_true) != len(y_pred):
    raise SystemExit("Error: label arrays have different lengths")

# encode to consistent integer labels; set drop_negative=False if you want to keep -1 as a label
y_true_enc, y_pred_enc = encode_labels(y_true, y_pred, drop_negative=True)

ari = adjusted_rand_score(y_true_enc, y_pred_enc)
k = cohen_kappa_score(y_true_enc, y_pred_enc)
print("ARI,{:.3f}".format(ari))
print("CohensK,{:.3f}".format(k))