import os
from src.search import boolean_retrieval
from src.index.inverted_index import InvertedIndex

INV = None

def IR_main(index_path, query):
    """
    Parameters:
        index_path (str): path to 'dict_final.tsv' and 'postings_final.bin'
        query (str): textbased query

    Returns:
        list[int]: Document IDs
    """
    global INV
    if INV is None:
        dict_file = os.path.join(index_path, 'dict_final.tsv')
        post_file = os.path.join(index_path, 'postings_final.bin')
        INV = InvertedIndex(dict_file, post_file)
        boolean_retrieval.INV = INV 

    return boolean_retrieval.main(query) 

