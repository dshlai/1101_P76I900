
import os
from glob import glob
import xml.etree.cElementTree as ET
from prompt_toolkit import print_formatted_text, HTML, PromptSession

import utility as utils

session = PromptSession()


def main():
    
    doc_folder = session.prompt("Enter the folder where the XML documents are located: ")
    articles = load_documents(doc_folder)

    keywords = session.prompt("Enter Keyword to Search: ")
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
        print(art.article_title + "\n")

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