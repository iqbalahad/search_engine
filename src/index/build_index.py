
import os
import yaml
from src.data_import import stream_collection
from src.preprocess import Preprocessor
from src.index.compression import gap_encode_list, vb_encode_list

CONFIG = yaml.safe_load(open('configs/config.yaml'))
BATCH = CONFIG['index']['batch_size']
INDEX_DIR = CONFIG['paths']['index_dir']
PRE = Preprocessor(**CONFIG['preprocessing'])


def write_block(block_id, lexicon, postings_out):
    os.makedirs(INDEX_DIR, exist_ok=True)
    dict_path = os.path.join(INDEX_DIR, f'dict_{block_id}.tsv')
    post_path = os.path.join(INDEX_DIR, f'post_{block_id}.bin')
    with open(dict_path, 'w') as d_f, open(post_path, 'wb') as p_f:
        for term, postings in sorted(lexicon.items()):
            gaps = gap_encode_list(postings)
            data = vb_encode_list(gaps)
            offset = p_f.tell()
            p_f.write(data)
            length = len(data)
            d_f.write(f"{term}\t{offset}\t{length}\n")


def build_index():
    lexicon = {}
    docs = []
    for doc_id, text in enumerate(stream_collection(CONFIG['paths']['data_tar']), 1):
        tokens = PRE.process(text)
        for pos, t in enumerate(tokens):
            lexicon.setdefault(t, []).append(doc_id)
        if doc_id % BATCH == 0:
            write_block(doc_id//BATCH, lexicon, None)
            lexicon.clear()
    if lexicon:
        write_block((doc_id//BATCH)+1, lexicon, None)

if __name__ == '__main__':
    build_index()

