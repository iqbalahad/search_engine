from src.index.inverted_index import InvertedIndex
import yaml, os

CONFIG = yaml.safe_load(open('configs/config.yaml'))
INV = InvertedIndex(os.path.join(CONFIG['paths']['index_dir'], 'dict_final.tsv'),
                    os.path.join(CONFIG['paths']['index_dir'], 'postings_final.bin'))


def intersect(a, b):
    i=j=0; res=[]
    while i<len(a) and j<len(b):
        if a[i]==b[j]: res.append(a[i]); i+=1; j+=1
        elif a[i]<b[j]: i+=1
        else: j+=1
    return res


def union(a, b): return sorted(set(a)|set(b))

def difference(a, b): return [x for x in a if x not in set(b)]


def boolean_and(terms):
    lists = [INV.retrieve_postings(t) for t in terms]
    res = lists[0]
    for l in lists[1:]: res = intersect(res, l)
    return res


def main(query):
    terms = query.lower().split()
    return boolean_and(terms)