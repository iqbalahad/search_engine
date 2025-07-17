import sys, os
# Projektwurzel zum PYTHONPATH hinzufügen
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import argparse
import yaml

# Konfiguration laden
CONFIG = yaml.safe_load(open(os.path.join(os.path.dirname(__file__), '..', 'configs', 'config.yaml')))

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['build-index','merge-index','eda','search','bm25','evaluate','build-forward'],)
    parser.add_argument('--query', type=str)
    parser.add_argument('--topk', type=int, default=10, help="Anzahl der zurückgegebenen Dokumente (BM25)")

    args = parser.parse_args()

    if args.command == 'build-index':
        from src.index.build_index import build_index
        build_index()

    elif args.command == 'merge-index':
        from src.index.merge_indexes import merge_indexes
        merge_indexes()

    elif args.command == 'eda':
        from src.eda import run_eda
        run_eda(CONFIG['paths']['data_tar'])

    elif args.command == 'search':
        from src.search.boolean_retrieval import main as bool_search
        print(bool_search(args.query))


    elif args.command == 'evaluate':
        from src.evaluate import evaluate
        # ggf. Qrels/Queries einlesen und übergeben
        evaluate(None, None)
