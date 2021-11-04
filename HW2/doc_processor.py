from os import closerange
import pandas as pd
import spacy
import utility as utils
from multiprocessing import Pool
from collections import Counter

nlp = spacy.load("en_core_web_sm")
stop_words = nlp.Defaults.stop_words

def build_index():
    docs = pd.read_csv("all_documents.csv", usecols=["title", "abstract"])
    words = pd.read_csv("test_cloud_lemma.csv", usecols=['word'])
    
    stop_words = nlp.Defaults.stop_words
    
    # remove stop words
    df_stop = pd.DataFrame(stop_words, columns=['word'])
    words = words[~words['word'].isin(df_stop['word'])]
    
    words.dropna(inplace=True, axis=0)
    word_list = words['word'].to_list()
    doc_list = docs['abstract'].to_list()
    
    len_of_section = 700
    
    print("Processing Start ... ")    
    counted_list = []
    
    for s in range(int(len(doc_list)/len_of_section)+1):
        start = s * len_of_section
        end = start + len_of_section
        docs_to_proc = doc_list[start:end]
        proc_list = [(doc, word_list) for doc in docs_to_proc]
        
        with Pool() as p:
            results = p.starmap(find_docs, proc_list)
        
        df = pd.concat(results, axis=0)
        df = df.reset_index()
        df = df.fillna(0)
        df.to_csv("word_freq_in_docs_{}.csv".format(s))
    

def find_docs(doc, terms):
    matches = utils.match(terms, doc)
    doc = nlp(doc)
    spans = [doc[start:end] for _, start, end in matches]
    spans = [w.text for w in spans if not w.text.lower() in stop_words]
    counter = Counter(spans)
    
    counter = dict(counter)
    counted = pd.DataFrame.from_dict(counter, orient='index').transpose()
    return counted


def remove_stop_words(text):
    doc = nlp(text)
    isalpha = [w.lemma_ for w in doc if w.is_alpha]
    lemmatized = [w for w in isalpha if not w in stop_words]
    return lemmatized


if __name__ == '__main__':
    build_index()
    