import os
import heapq
from src.index.compression import vb_decode_stream, gap_decode_list

# Pfade zu Block-Indizes und Zieldateien
INDEX_DIR = 'data/index'
FINAL_DICT = os.path.join(INDEX_DIR, 'dict_final.tsv')
FINAL_POSTINGS = os.path.join(INDEX_DIR, 'postings_final.bin')

def merge_indexes():
    # Sammle alle Teil-Lexika
    dict_files = sorted(f for f in os.listdir(INDEX_DIR) if f.startswith('dict_') and f.endswith('.tsv'))
    # Mapping: Block-ID (z.B. '1') → post_<ID>.bin
    post_files = {f.split('_')[1].split('.')[0]: f for f in os.listdir(INDEX_DIR) if f.startswith('post_') and f.endswith('.bin')}

    # Öffne alle Wörterbuch-Streams
    handles = [open(os.path.join(INDEX_DIR, df), 'r') for df in dict_files]
    heap = []  # (term, block_id, offset, length)

    # Min-Heap initialisieren (Block-IDs beginnen bei 1)
    for idx, h in enumerate(handles, start=1):
        line = h.readline()
        if line:
            term, off, length = line.strip().split('\t')
            heapq.heappush(heap, (term, str(idx), int(off), int(length)))

    # Ausgabe-Dateien öffnen
    with open(FINAL_DICT, 'w') as dict_out, open(FINAL_POSTINGS, 'wb') as post_out:
        while heap:
            term, blk, off, length = heapq.heappop(heap)
            # Gesamte Postings-Daten für diesen Term sammeln
            data_accum = bytearray()
            # Erste Fragment aus Block blk
            with open(os.path.join(INDEX_DIR, post_files[blk]), 'rb') as pf:
                pf.seek(off)
                data_accum.extend(pf.read(length))

            # Weitere Fragmente aus anderen Blocks hinzufügen
            while heap and heap[0][0] == term:
                _, blk2, off2, len2 = heapq.heappop(heap)
                with open(os.path.join(INDEX_DIR, post_files[blk2]), 'rb') as pf:
                    pf.seek(off2)
                    data_accum.extend(pf.read(len2))
                # Nachrücken im Block blk2
                next_line = handles[int(blk2)-1].readline()
                if next_line:
                    t3, o3, l3 = next_line.strip().split('\t')
                    heapq.heappush(heap, (t3, blk2, int(o3), int(l3)))

            # In finalen Index schreiben
            ptr = post_out.tell()
            post_out.write(data_accum)
            dict_out.write(f"{term}\t{ptr}\t{len(data_accum)}\n")

            # Nachrücken im ursprünglichen Block blk
            next_line = handles[int(blk)-1].readline()
            if next_line:
                t2, o2, l2 = next_line.strip().split('\t')
                heapq.heappush(heap, (t2, blk, int(o2), int(l2)))

    # Alle Handles schließen
    for h in handles:
        h.close()

if __name__ == '__main__':
    merge_indexes()
