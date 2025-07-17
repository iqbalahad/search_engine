import yaml
from src.search.boolean_retrieval import boolean_and

CONFIG = yaml.safe_load(open('configs/config.yaml'))


def precision_at_k(res, rel, k=10):
    return len(set(res[:k]) & set(rel)) / k


def average_precision(res, rel, k=10):
    ap=0; rc=0
    for i, d in enumerate(res[:k],1):
        if d in rel:
            rc+=1
            ap+=rc/i
    return ap/min(len(rel),k)


def evaluate(qrels, queries):
    for qid, q in queries.items():
        res = boolean_and(q.split())
        prec = precision_at_k(res, qrels[qid])
        ap = average_precision(res, qrels[qid])
        print(f"Q{qid}: P@10={prec:.3f}, AP={ap:.3f}")

if __name__=='__main__':
    # Einlesen Qrels und Query-File
    pass