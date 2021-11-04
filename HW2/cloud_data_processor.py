import os
import pandas as pd
import toml
import collection_processor as cp
from multiprocessing import Pool
import spacy

configs = toml.load("configs.toml")

nlp = spacy.load("en_core_web_sm")
stop_words = nlp.Defaults.stop_words


def load_cloud_abstract(url):
    df = pd.read_csv(url, usecols=["title", "abstract"])
    df = df.dropna(subset=["abstract"])
    return df


def process_counted(counted):
    counted = pd.concat(counted)
    counted = counted.groupby('word').sum('freq').sort_values('freq', ascending=False)
    
    return counted


def output_lemma_words(abs_list):
    
    with Pool() as p:
        counted = p.map(cp.process_single_abstract, abs_list)
    
    #cleanup = stop_words_cleanup(counted)
    counted = process_counted(counted)
    
    counted.to_csv("test_cloud_lemma.csv")
    #cleanup.to_csv("test_cloud_cleanup.csv")


def stop_words_cleanup(counted):
    df_stop = pd.DataFrame(list(stop_words), columns=['word'])
    df = counted[~counted['word'].isin(df_stop['word'])]
    return df


def output_stemmed_words(abs_list):
    
    with Pool() as p:
        stemmed = p.map(cp.stemming_single_abstract, abs_list)

    stemmed = process_counted(stemmed)
    stemmed.to_csv("test_cloud_porter.csv")
    
def main():
    
    doc_path = "all_documents.csv"
    
    if os.path.exists(doc_path):
        df = pd.read_csv(doc_path)
    else:
        df_list = []
        
        base_url = configs["Cloud"]["url"]
        df_list = [base_url+"{}.csv".format(fn) for fn in range(1, 1001)]
        
        with Pool() as p:
            counted = p.map(load_cloud_abstract, df_list)
        
        df = pd.concat(counted)
        df.to_csv("all_documents.csv")

    print("Done loading documents!")
    
    abs_list = df["abstract"].to_list()
    output_lemma_words(abs_list)
    
    abs_list = df["abstract"].to_list()
    #output_stemmed_words(abs_list)
        

if __name__ == '__main__':
    main()