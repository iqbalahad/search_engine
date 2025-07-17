# Search Engine

A lightweight search-engine prototype that performs **Boolean AND retrieval** over a text collection.

---

## 1 · Installation

```bash
# clone the repo
git clone https://github.com/iqbalahad/search_engine.git
cd search_engine

# create & activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scriptsctivate

# install requirements
pip install -r requirements.txt
```

## 2 · Prepare the index

### **Option A – use a pre-built index**

Copy the two index files:

- `dict_final.tsv`
- `postings_final.bin`

into `data/index/`

---

### **Option B – build the index yourself**

```bash
# create block indexes
python src/cli.py build-index

# merge them into the final files above
python src/cli.py merge-index
```

## 3 · Search / run tests

Run the sample queries defined in `src/main.py`:

```bash
python src/main.py
```

Or an ad-hoc query:

```bash
python src/cli.py search --query "information retrieval"
```

## Project structure

```text
search_engine/
├── configs/
│   └── config.yaml                 # preprocessing & path settings
├── data/
│   ├── collectionand_queries.tar.gz
│   └── index/                      # final index files live here
│       ├── dict_final.tsv
│       ├── postings_final.bin
├── src/
│   ├── cli.py                      # command-line interface (build / search)
│   ├── main.py                     # tiny demo script with sample queries
│   ├── ir_entrypoint.py            # ← IR_main(index_path, query)
│   ├── search/
│   │   └── boolean_retrieval.py    # Boolean AND retrieval logic
│   └── index/
│       ├── build_index.py          # builds block indexes
│       ├── merge_indexes.py        # merges blocks → final index
│       └── inverted_index.py       # index reader
├── requirements.txt                # Python dependencies
├── .gitignore                      # excludes big index files, venv, etc.
└── README.md                       # this file
