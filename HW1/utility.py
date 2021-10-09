### Utility functions and classes
import spacy
from spacy.matcher import PhraseMatcher


NLP = spacy.load("en_core_web_sm")


class PubmedArticle(object):
    
    def __init__(self, article):
        
        # Store PubMed article node
        self.__article_node = article
        
        # Get article title node, not needed after initialization
        article_title_node = get_object_from_article("ArticleTitle", self.__article_node)
        
        # Get abstract node
        self.__abstract_node = get_object_from_article("Abstract", self.__article_node)
        
        # Get journal node
        self.__journal_node = get_object_from_article("Journal", self.__article_node)
                
        # Get journal's title in string
        self.__journal_title = get_object_from_article("Title", self.__journal_node).text
        
        # Get article's title in string
        self.__article_title = article_title_node.text

        # Gather all text string in abstract node and concate into a single string
        self.__abstract_text = self.parse_abstract_text()

        self.contain_title = False
        self.contain_abstract = False
        
    @property
    def article_title(self):
        return self.__article_title
    
    @property
    def abstract_text(self):
        print("\"Getting concatnated abstract text ... \"")
        return self.__abstract_text
    
    def check_terms(self, terms):
        
        title_match = match(terms, self.__article_title)
        
        abstract_match = match(terms, self.__abstract_text)
    
        if len(title_match) > 0:
            self.contain_title = True
        
        if len(abstract_match) > 0:
            self.contain_abstract = True
    
    def parse_abstract_text(self):
        
        if self.__abstract_node is None:
            return ""
        
        text_list = self.__abstract_node.findall(".//AbstractText")
        text = ""
        
        for node in text_list:
            text += node.text + " "

        return text
        

def lemmatize(text):
    lemmatizer = NLP.get_pipe("lemmatizer")
    print("Lemmatizer Mode: {}".format(lemmatizer.mode))
    
    doc = NLP(text)
    
    return [(token.text, token.lemma_) for token in doc]    


def match(terms, text):
    
    matcher = PhraseMatcher(NLP.vocab)
    
    patterns = [NLP.make_doc(tx) for tx in terms]
    matcher.add("TerminologyList", patterns)
    
    doc = NLP(text)
    
    matches = matcher(doc)
    
    return matches    



def get_object_from_article(tag_name, node):
    return node.find(".//{}".format(tag_name))

