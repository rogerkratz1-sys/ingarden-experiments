#!/usr/bin/env python3
# bootstrap_tokenoverlap_ci.py
# Usage: python bootstrap_tokenoverlap_ci.py [--iters N]
# Default iterations: 2000

import os, json, argparse, math, csv
import numpy as np
from sklearn.metrics import adjusted_rand_score, cohen_kappa_score
from collections import OrderedDict

PARS = ["tokengran","punctsplit","discourseboundary","srlsim"]
THRESHOLDS = [5,15,25]  # corresponds to 0.05, 0.15, 0.25
ROOT = "supplement_s7"
RESULTS_DIR = os.path.join(ROOT, "results")
OUT_DIR = os.path.join(ROOT, "diagnostics_bootstrap")
os.makedirs(OUT_DIR, exist_ok=True)

def load_pairs(parse, th_pct):
    fname = os.path.join(RESULTS_DIR, f"labels_{parse}_tokenoverlap_{th_pct}_remapped.json")
    if not os.path.exists(fname):
        return None
    j = json.load(open(fname, encoding="utf8"))
    y_true = j.get("labels", {}).get("canonical", [])
    y_pred = j.get("labels", {}).get("parse", [])
    # ensure same length
    if len(y_true) != len(y_pred):
        # truncate to min length
        n = min(len(y_true), len(y_pred))
        y_true = y_true[:n]
        y_pred = y_pred[:n]
    if not y_true:
        return None
    return np.array(y_true), np.array(y_pred)

def bootstrap_metrics(y_true, y_pred, iters=2000, seed=0):
    rng = np.random.default_rng(seed)
    n = len(y_true)
    if n == 0:
        return None
    ari_vals = []
    k_vals = []
    # compute point estimates on full sample
    try:
        ari_point = adjusted_rand_score(y_true, y_pred)
    except Exception:
        ari_point = float("nan")
    try:
        k_point = cohen_kappa_score(y_true, y_pred)
    except Exception:
        k_point = float("nan")
    # bootstrap
    for _ in range(iters):
        idx = rng.integers(0, n, n)
        yt = y_true[idx]
        yp = y_pred[idx]
        try:
            ari_vals.append(adjusted_rand_score(yt, yp))
        except Exception:
            ari_vals.append(float("nan"))
        try:
            k_vals.append(cohen_kappa_score(yt, yp))
        except Exception:
            k_vals.append(float("nan"))
    ari_arr = np.array(ari_vals, dtype=float)
    k_arr = np.array(k_vals, dtype=float)
    # remove NaNs if any
    ari_arr = ari_arr[~np.isnan(ari_arr)]
    k_arr = k_arr[~np.isnan(k_arr)]
    def ci(arr):
        if len(arr) == 0:
            return (float("nan"), float("nan"))
        lo = float(np.percentile(arr, 2.5))
        hi = float(np.percentile(arr, 97.5))
        return (lo, hi)
    return {
        "ari_point": float(ari_point),
        "ari_ci": ci(ari_arr),
        "k_point": float(k_point),
        "k_ci": ci(k_arr),
        "n_pairs": int(n)
    }

def main(iters):
    summary_rows = []
    for parse in PARS:
        for th in THRESHOLDS:
            pairs = load_pairs(parse, th)
            if pairs is None:
                print(f"Missing remapped file for {parse} threshold {th}; skipping.")
                continue
            y_true, y_pred = pairs
            # sanity: lengths
            n = len(y_true)
            if n == 0:
                print(f"No pairs for {parse} threshold {th}; skipping.")
                continue
            res = bootstrap_metrics(y_true, y_pred, iters=iters)
            if res is None:
                print(f"Bootstrap failed for {parse} {th}")
                continue
            # write per-parse-threshold CSV of bootstrap samples? (optional)
            # Save summary JSON
            out_json = os.path.join(OUT_DIR, f"bootstrap_{parse}_th{th}.json")
            with open(out_json, "w", encoding="utf8") as oj:
                json.dump(res, oj, indent=2, ensure_ascii=False)
            # append to summary table
            summary_rows.append(OrderedDict([
                ("parse", parse),
                ("threshold_pct", th),
                ("n_pairs", res["n_pairs"]),
                ("ari_point", res["ari_point"]),
                ("ari_ci_lo", res["ari_ci"][0]),
                ("ari_ci_hi", res["ari_ci"][1]),
                ("k_point", res["k_point"]),
                ("k_ci_lo", res["k_ci"][0]),
                ("k_ci_hi", res["k_ci"][1])
            ]))
            print(f"{parse} th={th/100:.2f} n={res['n_pairs']} ARI={res['ari_point']:.3f} CI=({res['ari_ci'][0]:.3f},{res['ari_ci'][1]:.3f}) K={res['k_point']:.3f} CI=({res['k_ci'][0]:.3f},{res['k_ci'][1]:.3f})")
    # write summary CSV
    csv_out = os.path.join(OUT_DIR, "bootstrap_summary.csv")
    if summary_rows:
        with open(csv_out, "w", newline="", encoding="utf8") as cf:
            w = csv.DictWriter(cf, fieldnames=list(summary_rows[0].keys()))
            w.writeheader()
            for r in summary_rows:
                w.writerow(r)
        print(f"Wrote summary CSV to {csv_out}")
    else:
        print("No results to write.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--iters", type=int, default=2000, help="Bootstrap iterations (default 2000)")
    args = parser.parse_args()
    main(args.iters)