import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

class Preprocessor:
    def __init__(self, lowercase=True, remove_stop=True, stem=True):
        self.lowercase = lowercase
        self.remove_stop = remove_stop
        self.stem = stem
        self.stemmer = PorterStemmer()
        self.stopset = set(stopwords.words('english'))

    def tokenize(self, text):
        return re.findall(r"\w+", text)

    def process(self, text):
        if self.lowercase:
            text = text.lower()
        tokens = self.tokenize(text)
        if self.remove_stop:
            tokens = [t for t in tokens if t not in self.stopset]
        if self.stem:
            tokens = [self.stemmer.stem(t) for t in tokens]
        return tokens