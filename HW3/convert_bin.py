from gensim.models import Word2Vec
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("bin", help="Path to gensim .bin file")
parser.add_argument("kv", help="Path to save .kv file")

args = parser.parse_args()

def convert(binfile, kvfile):

    model = Word2Vec.load(binfile)
    wv = model.wv
    wv.save(kvfile)
    print("Finish Convert ... ")


if __name__ == "__main__":
    convert(args.bin, args.kv)
