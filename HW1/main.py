
import os
from glob import glob
import xml.etree.cElementTree as ET
from prompt_toolkit.shortcuts.utils import clear
import yaml
import json

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
    json_articles = load_json_docs(doc_folder)

    keywords = session.prompt("\nEnter Keyword to Search: ")
    terms = keywords.strip(" ").split(",")
    
    contain_list = []
    xml_doc_list = []
    json_doc_list = []
    
    for art in articles:
        
        art.check_terms(terms)
        
        if art.contain_title is True :
            contain_list.append(art)
            xml_doc_list.append(art)
        elif art.contain_abstract is True:
            contain_list.append(art)
            xml_doc_list.append(art)
        else:
            pass
    
    for ja in json_articles:
        ja.check_terms(terms)
        if ja.contain_text is True:
            contain_list.append(ja)
            json_doc_list.append(ja)
    
    
    print("")
    print("Number of Matched PubMed articles Found: {}".format(len(xml_doc_list)))
    print("Number of Twitter text Matched: {}".format(len(json_doc_list)))
    print("")
    
    counter = 1
    for art in contain_list:

            title_len = len(art.article_title) + 5
            sep = "-"*title_len+"\n"
            print(sep)
            
            if art.contain_title is True:
                formatted_title = [("", "{}.  ".format(counter))]
                formatted_title.extend(art.get_formatted_title())
                formatted_title = FormattedText(formatted_title)
                title_len = len(formatted_title)
                print(formatted_title)  
            else:
                print(FormattedText([("#ffffff",  "{}.  ".format(counter)+art.article_title+"\n")]))
                
            print("")
            print(sep)
            print("")
            
            if art.is_json is True:
                print(art.text+"\n")
                print("# of Words in Tweet: {}".format(art.number_of_word_in_tweet))
                print("# of Sentences in Twiiter: {}\n".format(art.number_of_sents))
                counter += 1
                continue
            
            if art.contain_abstract is True:
                formatted_abs = FormattedText(art.get_formatted_abstract())
                print(formatted_abs)
            else:
                print(art.abstract_text)
            
            print("# of Words in Abstract: {}".format(art.num_of_words_in_abs))
            print("# of Characters in Abstract: {}".format(art.num_of_chr_abstract))
            print("# of Sentences in Abstract: {}\n".format(len(list(art.abstract_doc.sents))))
            print("")
            
            counter += 1

    #print(contain_list[0].explain())

def load_json_docs(folder):
    json_list = []
    for f in glob("{}/*.json".format(folder)):
        json_list.append(f)
        
    json_doc_list = []
    
    for fp in json_list:
        with open(fp) as reader:
            data = json.load(reader)
            j_doc = utils.JsonArticle(data)
            json_doc_list.append(j_doc)

    return json_doc_list
    
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