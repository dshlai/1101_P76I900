"""
Usually we need to run collection_processor before the main app to process the whole collection of texts
and collect the data we need from the corpus
"""


import pandas as pd
import spacy
import toml
from collections import Counter
from multiprocessing import Pool
import time

from nltk.stem.snowball import SnowballStemmer

nlp = spacy.load("en_core_web_sm")

configs = toml.load("configs.toml")
collection_path = configs['Collection']['path']
num_of_rows = None


def load_abstracts():
    cols_for_metadata = ["title", "journal", "authors", "abstract"]
    metadata_df = pd.read_csv(collection_path, usecols=cols_for_metadata, nrows=num_of_rows)

    # get subset with abstract included in the metadata.csv
    df_abstract = metadata_df.dropna(subset=["abstract"])
    
    return df_abstract


def process_single_abstract(text):
    """
    Process a single abstract using spacy and Counter
    return: Dataframe of counted words
    """
    doc = nlp(text)
    
    # eliminate number and punctuation and lemmatize
    words = [tk.lemma_ for tk in doc if tk.is_alpha]
    
    # count freq using python Counter
    counter = Counter(words)
    
    counter = [(w, freq) for w, freq in counter.items()]
    counter_df = pd.DataFrame(counter, columns=['word', 'freq'])
    
    return counter_df


def stemming_single_abstract(text):
    sstemer = SnowballStemmer(language='english')
    doc = nlp(text)
    
    stemmed = [sstemer.stem(tk.text) for tk in doc if tk.is_alpha]
    counter = Counter(stemmed)
    
    counter = [(w, freq) for w, freq in counter.items()]
    counter_df = pd.DataFrame(counter, columns=['word', 'freq'])
    
    return counter_df
    

def main():
    begin = time.time()
    df = load_abstracts()
    
    loading_time = time.time() - begin
    print("Finished Load Abstracts")
    print("Loading metadata.csv takes: {}".format(loading_time))

    abs_list = df['abstract'].tolist()
    
    with Pool() as p:
        results = p.map(process_single_abstract, abs_list)
    
    print("{} abstracts in metadata.csv".format(len(abs_list)))
    print("Processed All Abstracts")
    proc_time = time.time() - loading_time
    print("Process time: {}".format(proc_time))

    result = pd.concat(results)
    result = result.groupby('word').sum('freq').sort_values('freq', ascending=False)
    
    result.to_csv("test.csv")
    end = time.time()
    dur = end - begin
    print("Runtime: {}".format(dur))

if __name__ == "__main__":
    main()
