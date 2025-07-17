import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ir_entrypoint import IR_main

if __name__ == '__main__':
    index_path = 'data/index'
    query = "information "

    results = IR_main(index_path, query)
    print(f"Gefundene Dokumente für Query: '{query}'")
    for i, docid in enumerate(results[:10], 1):
        print(f"{i:>2}. DocID: {docid}")
