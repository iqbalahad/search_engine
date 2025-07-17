import random
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from src.data_import import stream_collection


def sample_docs(stream, k=500):
    reservoir = []
    for i, doc in enumerate(stream, 1):
        if i <= k:
            reservoir.append(doc)
        else:
            j = random.randint(1, i)
            if j <= k:
                reservoir[j-1] = doc
    return reservoir


def tokenize(text):
    return text.lower().split()


def run_eda(tar_path):
    docs = sample_docs(stream_collection(tar_path))
    lengths = [len(tokenize(d)) for d in docs]
    all_tokens = [t for d in docs for t in tokenize(d)]
    vocab = set(all_tokens)

    print(f"Vokabular-Größe: {len(vocab)}")
    print(f"Dokumentlängen: min={min(lengths)}, avg={np.mean(lengths):.1f}, max={max(lengths)}")

    freq = Counter(all_tokens)
    ranks = np.arange(1, len(freq)+1)
    freqs = np.array([f for _, f in freq.most_common()])
    plt.loglog(ranks, freqs)
    plt.xlabel("Rang")
    plt.ylabel("Frequenz")
    plt.title("Zipf-Verteilung (Sample)")
    plt.show()