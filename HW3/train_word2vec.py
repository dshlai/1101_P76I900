import pandas as pd
from gensim.models import Word2Vec, Phrases
import spacy
from multiprocessing import Pool

nlp = spacy.load("en_core_web_md")
stop_words = nlp.Defaults.stop_words

def train():
    docs = pd.read_csv("../HW2/all_documents.csv", usecols=["title", "abstract"])

    titles = docs['title'].to_list()
    abs = docs['abstract'].to_list()

    texts = [t+" "+a for t, a in zip(titles, abs)]

    with Pool() as p:
        train_texts = p.map(tokenize_single_doc, texts)

    bigram = Phrases(train_texts)
    model = Word2Vec(bigram[train_texts], sg=0, min_count=8, workers=12)
    model.save("cbow_model_pubmed_covid_7000.bin")


def tokenize_single_doc(doc):
    doc = nlp(doc)
    tks = [tk.text for tk in doc if tk.is_alpha]
    tks = [tk for tk in tks if not tk in stop_words]
    return tks


def bin_to_kv():
    model = Word2Vec.load("skip_model_cord19_covid_55k.bin")
    wv = model.wv
    wv.save("skip_model_cord19_covid_55k.kv")


if __name__ == "__main__":
    bin_to_kv()