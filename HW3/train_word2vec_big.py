import pandas as pd
from gensim.models import Word2Vec, Phrases
import spacy
from multiprocessing import Pool
import os

nlp = spacy.load("en_core_web_md")
stop_words = nlp.Defaults.stop_words

train_path = "../../models/P76I900/HW3/"
if not os.path.exists(train_path):
    print("Create model save path: {}".format(train_path))
    os.mkdir(train_path)

def train():
    
    docs = pd.read_csv("/disk/datassd/datasets/CORD19/metadata.csv", usecols=["abstract"])

    texts = docs['abstract'].dropna().to_list()

    with Pool() as p:
        train_texts = p.map(tokenize_single_doc, texts)

    bigram = Phrases(train_texts)
    model = Word2Vec(bigram[train_texts], sg=1, window=10,
                     vector_size=300, min_count=5, workers=12)

    model.save("{}skip_lemmatized_model_cord19_covid_55k.bin".format(train_path))


def tokenize_single_doc(doc):
    try:
        doc = nlp(doc)
    except TypeError:
        return []

    tks = [tk.lemma_ for tk in doc if tk.is_alpha]
    tks = [tk for tk in tks if not tk in stop_words]
    return tks


if __name__ == "__main__":
    train()