
import os
from glob import glob
import xml.etree.cElementTree as ET
import yaml

from prompt_toolkit import HTML, PromptSession
from prompt_toolkit import print_formatted_text as print
import utility as utils

session = PromptSession()

# load configuration
def load_config():
    with open("config.yaml", "r") as reader:
        config = yaml.safe_load(reader)
    
    return config

def main():
    
    config = load_config()
    
    # Load and process configuration
    if config['APP']['FOLDER_USE_CONFIG'] is True:
        doc_folder = config['FOLDER']
    else:
        doc_folder = session.prompt("Enter the folder where the XML documents are located: ")
    
    articles = load_documents(doc_folder)

    keywords = session.prompt("\nEnter Keyword to Search: ")
    terms = keywords.strip(" ").split(",")
    
    contain_list = []
    
    for art in articles:
        
        art.check_terms(terms)
        
        if art.contain_title is True :
            contain_list.append(art)
        elif art.contain_abstract is True:
            contain_list.append(art)
        else:
            pass
    
    print("")
    for art in contain_list:
        if art.contain_title is True:
            pass
        else:
            print(art.article_title+"\n")
            print("# of Words in Abstract: {}".format(art.num_of_words_in_abs))
            print("# of Characters in Abstract: {}".format(art.num_of_chr_abstract))
            print("# of Sentences in Abstract: {}\n".format(len(list(art.abstract_doc.sents))))

def get_ptk_formatted_text(doc):

    text = [token.text for token in doc]
    
    
def load_documents(folder):

    file_list = []
    
    for f in glob("{}/*.xml".format(folder)):
        file_list.append(f)
    
    doc_list = []

    for f in file_list:
        tree = ET.parse(f)
        root = tree.getroot()
        doc_list.append(root)
    
    article_list = []
    
    for doc in doc_list:
        articles = doc.findall(".//PubmedArticle")
        article_list.extend(articles)

    article_list = [utils.PubmedArticle(at) for at in article_list]
    
    return article_list
    
def test_load_documents():
    folder = session.prompt("Enter Test Document Folder: ")
    articles = load_documents(folder)
    
    print("")
    print(articles[-1].article_title)
    print("")

    text = articles[-1].abstract_text
    
    if text is not None:
        test_lemmatize = utils.lemmatize(text)
        
    terms = ["COVID-19", "patients"]

    utils.match(terms, text)
    
    articles[-1].check_terms(terms)
    print(articles[-1].contain_title)
    print(articles[-1].contain_abstract)

if __name__ == "__main__":
    main()