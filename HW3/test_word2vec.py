from gensim.models import Word2Vec, KeyedVectors
import argparse

from pandas.io import parsers

parser = argparse.ArgumentParser(description="Find most similar phrase using Word2Vec")
parser.add_argument("phrase", type=str, help="Input some test phrase")

args = parser.parse_args()

def test():

    wv = KeyedVectors.load("cbow_kv_pubmed_covid_7000.kv")

    try:
        topn = wv.most_similar(args.phrase, topn=10)
        print("")
        for w, sim in topn:
            print("-".join(w.split("_")) + ": {:0.2}".format(sim))
        print("")

    except KeyError:
        print("Cannot find similar word")


def to_kv_file():
    model = Word2Vec.load("cbow_model_pubmed_covid_7000.bin")
    wv = model.wv
    wv.save("cbow_kv_pubmed_covid_7000.kv")


if __name__ == "__main__":
    test()