# check_identity.py
import json
paths = {
    "tokengran": "supplement_s7/results/labels_tokengran_remapped.json",
    "punctsplit": "supplement_s7/results/labels_punctsplit_remapped.json",
    "discourseboundary": "supplement_s7/results/labels_discourseboundary_remapped.json",
    "srlsim": "supplement_s7/results/labels_srlsim_remapped.json"
}

def identical(path):
    j = json.load(open(path, 'r', encoding='utf8'))
    can = j['labels']['canonical']
    par = j['labels']['parse']
    return all(c == p for c, p in zip(can, par))

for name, path in paths.items():
    try:
        print(f"{name}: identical to canonical -> {identical(path)}")
    except FileNotFoundError:
        print(f"{name}: file not found -> {path}")