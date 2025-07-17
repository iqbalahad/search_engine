import os
from src.index.compression import vb_decode_stream, gap_decode_list

class InvertedIndex:
    def __init__(self, dict_path, postings_path):
        self.dict_path = dict_path
        self.postings_path = postings_path
        self._load_dict()

    def _load_dict(self):
        self.lexicon = {}
        with open(self.dict_path, 'r') as f:
            for line in f:
                term, offset, length = line.strip().split('\t')
                self.lexicon[term] = (int(offset), int(length))

    def retrieve_postings(self, term):
        if term not in self.lexicon:
            return []
        offset, length = self.lexicon[term]
        with open(self.postings_path, 'rb') as f:
            f.seek(offset)
            data = f.read(length)
        gaps = vb_decode_stream(data)
        postings = gap_decode_list(gaps)
        return postings