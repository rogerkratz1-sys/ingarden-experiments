# pairwise_metrics.py
import json, itertools
from sklearn.metrics import adjusted_rand_score, cohen_kappa_score

def load_remapped(path):
    j=json.load(open(path,'r',encoding='utf8'))
    return j['labels']['canonical'], j['labels']['parse']

files = {
  'canonical':'supplement_s7/results/labels_tokengran_remapped.json', # canonical arrays are stored in each remapped file
  'tokengran':'supplement_s7/results/labels_tokengran_remapped.json',
  'punctsplit':'supplement_s7/results/labels_punctsplit_remapped.json',
  'discourseboundary':'supplement_s7/results/labels_discourseboundary_remapped.json',
  'srlsim':'supplement_s7/results/labels_srlsim_remapped.json'
}

# load parse label arrays (use canonical array from any remapped file as the canonical reference)
arrays = {}
for name,path in files.items():
    try:
        can,par = load_remapped(path)
        arrays[name] = par
    except FileNotFoundError:
        arrays[name] = None

names = [n for n in arrays if arrays[n] is not None]
print('Names:', names)
print('Pairwise ARI and Cohen kappa:')
for a,b in itertools.combinations(names,2):
    y1=arrays[a]; y2=arrays[b]
    ari=adjusted_rand_score(y1,y2)
    k=cohen_kappa_score(y1,y2)
    print(f'{a} vs {b}: ARI={ari:.3f}, K={k:.3f}')