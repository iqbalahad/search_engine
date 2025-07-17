import os
from src.search import boolean_retrieval
from src.index.inverted_index import InvertedIndex

# Globaler Index – wird nur einmal geladen
INV = None

def IR_main(index_path, query):
    """
    Parameters:
        index_path (str): Pfad zu 'dict_final.tsv' und 'postings_final.bin'
        query (str): Textbasierte Suchanfrage

    Returns:
        list[int]: Dokument-IDs (sortiert aufsteigend, aber nicht nach Relevanz)
    """
    global INV
    if INV is None:
        dict_file = os.path.join(index_path, 'dict_final.tsv')
        post_file = os.path.join(index_path, 'postings_final.bin')
        INV = InvertedIndex(dict_file, post_file)
        boolean_retrieval.INV = INV  # Übergib geladenen Index an boolean_retrieval

    return boolean_retrieval.main(query)  # verwendet deine bestehende Suchlogik

