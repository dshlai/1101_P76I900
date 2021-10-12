
import os
from glob import glob
import xml.etree.cElementTree as ET
from prompt_toolkit.shortcuts.utils import clear
import yaml

from prompt_toolkit import HTML, PromptSession
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.formatted_text import FormattedText
import utility as utils

session = PromptSession()

# load configuration
def load_config():
    with open("config.yaml", "r") as reader:
        config = yaml.safe_load(reader)
    
    return config


def get_doc_folder(config):
    # Load and process configuration
    if config['APP']['FOLDER_USE_CONFIG'] is True:
        doc_folder = config['FOLDER']
    else:
        doc_folder = session.prompt("Enter the folder where the XML documents are located: ")
    
    return doc_folder


def main():
    
    config = load_config()
    
    doc_folder = get_doc_folder(config)
    
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
                formatted_title = FormattedText(art.get_formatted_title())
                print(formatted_title)
                print("")
            else:
                print(FormattedText([("#ffffff", art.article_title+"\n")]))
                
            if art.contain_abstract is True:
                formatted_abs = FormattedText(art.get_formatted_abstract())
                print(formatted_abs)
                print("")
            else:
                print(art.abstract_text)
            
            print("# of Words in Abstract: {}".format(art.num_of_words_in_abs))
            print("# of Characters in Abstract: {}".format(art.num_of_chr_abstract))
            print("# of Sentences in Abstract: {}\n".format(len(list(art.abstract_doc.sents))))
            print("--"*80+"\n")
        
    
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


def tests():
    config = load_config()
    folder = get_doc_folder(config)
    articles = load_documents(folder)
    
    assert articles[-1].article_title == "Qualitative study of the psychological experience of COVID-19 patients during hospitalization."

    terms = ["COVID-19", "patients"]

    articles[-1].check_terms(terms)
    assert articles[-1].contain_title is True
    assert articles[-1].contain_abstract is True
    
    formatted = FormattedText(articles[-1].get_formatted_abstract())
    
    print(formatted)
    
        
if __name__ == "__main__":
    main()