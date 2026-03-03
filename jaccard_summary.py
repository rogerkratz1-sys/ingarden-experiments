#!/usr/bin/env python3
# jaccard_summary.py
import re, statistics, sys
def toks(s): return set(re.findall(r"\w+", s.lower()))

canonical_path = 'supplement_s7/eventizations/canonical.txt'
parses = ['tokengran','punctsplit','discourseboundary','srlsim']

can = [l.rstrip("\n") for l in open(canonical_path, encoding='utf8') if l.strip()]
can_toks = [toks(c) for c in can]

for parse in parses:
    parse_path = f'supplement_s7/eventizations/{parse}.txt'
    try:
        par = [l.rstrip("\n") for l in open(parse_path, encoding='utf8') if l.strip()]
    except FileNotFoundError:
        print(parse, 'file not found:', parse_path)
        continue
    bests = []
    for p in par:
        pt = toks(p)
        best = 0.0
        for ct in can_toks:
            union = pt | ct
            sim = (len(pt & ct) / len(union)) if union else 0.0
            if sim > best:
                best = sim
        bests.append(best)
    if bests:
        print(parse, 'count', len(bests),
              'median', round(statistics.median(bests),3),
              'mean', round(statistics.mean(bests),3),
              'min', round(min(bests),3),
              'max', round(max(bests),3))
    else:
        print(parse, 'no parse units found')