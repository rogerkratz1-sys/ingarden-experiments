# compute_local_ari_k.py
import json, sys
from sklearn.metrics import adjusted_rand_score, cohen_kappa_score

def find_label_lists(obj, lists):
    if isinstance(obj, list) and all(isinstance(x, (int,str)) for x in obj):
        lists.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            find_label_lists(v, lists)
    elif isinstance(obj, list):
        for v in obj:
            find_label_lists(v, lists)

def load_labels(path):
    j = json.load(open(path, 'r', encoding='utf8'))
    if isinstance(j, dict):
        if 'aggregated_labels' in j:
            return j['aggregated_labels']
        if 'targeted' in j and isinstance(j['targeted'], dict):
            a = j['targeted'].get('aggregated_canonical_permutation')
            b = j['targeted'].get('aggregated_parse_permutation')
            if a and b:
                return a, b
    lists = []
    find_label_lists(j, lists)
    if len(lists) >= 2:
        return lists[0], lists[1]
    raise ValueError(f"Could not find label arrays in {path}")

def compute(canonical_json, parse_json):
    c = load_labels(canonical_json)
    p = load_labels(parse_json)
    if isinstance(c, tuple):
        labels_c, labels_p = c
    else:
        labels_c = c
        if isinstance(p, tuple):
            _, labels_p = p
        else:
            labels_p = p
    if len(labels_c) != len(labels_p):
        raise ValueError("Label arrays differ in length")
    ari = adjusted_rand_score(labels_c, labels_p)
    k = cohen_kappa_score(labels_c, labels_p)
    print(f"ARI,{ari:.3f}")
    print(f"CohensK,{k:.3f}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compute_local_ari_k.py canonical.json parse.json")
        sys.exit(2)
    compute(sys.argv[1], sys.argv[2])