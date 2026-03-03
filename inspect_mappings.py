# inspect_mappings.py
import csv, sys
names = ['punctsplit','discourseboundary','srlsim','tokengran_mapping_tokenoverlap']
for name in names:
    path = f'supplement_s7/mappings/{name}.csv'
    try:
        rows = list(csv.reader(open(path, encoding='utf8')))
    except FileNotFoundError:
        print(path, 'not found')
        continue
    total = max(0, len(rows)-1)
    unmapped = sum(1 for r in rows[1:] if len(r) >= 2 and r[1].strip() == '-1')
    print(name, 'total', total, 'unmapped', unmapped, 'fraction_unmapped:{:.2f}'.format(unmapped/total if total else 0))
    print('sample rows:')
    for r in rows[1:11]:
        print(r)
    print('---')