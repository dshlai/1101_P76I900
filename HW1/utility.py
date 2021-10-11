### Utility functions and classes
import spacy
from spacy.lang.en import English
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
                        
        # Get article's title in string
        self.__article_title = article_title_node.text

        # Gather all text string in abstract node and concate into a single string
        self.__abstract_text = self.parse_abstract_text()

        self.__title_doc = NLP(self.__article_title)
        self.__abstract_doc = NLP(self.__abstract_text)

        self.contain_title = False
        self.contain_abstract = False
        
        self.__title_tokenized = [tk for tk in self.__title_doc]
        self.__abstract_tokenized = [tk for tk in self.__abstract_doc]
        
        self.num_of_chr_abstract = self.count_abstract_chrs()
        
        self.__title_matches = []
        self.__abstract_matches = []
        
    @property
    def article_title(self):
        return self.__article_title
    
    @property
    def abstract_text(self):
        print("\"Getting concatnated abstract text ... \"")
        return self.__abstract_text
    
    @property
    def abstract_doc(self):
        return self.__abstract_doc
    
    @property
    def title_doc(self):
        return self.__title_doc
    
    @property
    def num_of_words_in_abs(self):
        return len(list(self.__abstract_tokenized))
    
    def get_formatted_title(self):
        
        formatted_title = []
        begin = 0
        
        for _, start, end in self.__title_matches:
            # no style applied
            formatted_title.append(("#ffffff bold", self.title_doc[begin:start].text_with_ws))
            
            # apply style to matched text
            formatted_title.append(("#aa9922 bold", self.title_doc[start:end].text_with_ws))
            begin = end
            
        return formatted_title
    
    def get_formatted_abstract(self):
        
        formatted_text = []
        begin = 0
        
        for _, start, end in self.__abstract_matches:
            
            # no style apply for this portion
            formatted_text.append(("", self.abstract_doc[begin:start].text_with_ws))
        
            # apply style to matched text
            formatted_text.append(("#ff0066", self.abstract_doc[start:end].text_with_ws))
            begin = end
            
        return formatted_text
    
    def count_abstract_chrs(self):
        tk_string = "".join([tk.text for tk in self.__abstract_tokenized])
    
        return len(tk_string)
    
    def check_terms(self, terms):
        
        self.__title_matches = match(terms, self.__article_title)
        
        self.__abstract_matches = match(terms, self.__abstract_text)
    
        if len(self.__title_matches) > 0:
            self.contain_title = True
        
        if len(self.__abstract_matches) > 0:
            self.contain_abstract = True
    
    def parse_abstract_text(self):
        
        if self.__abstract_node is None:
            return ""
        
        text_list = self.__abstract_node.findall(".//AbstractText")
        text = ""
        
        for node in text_list:
            text += node.text + "\n\n"

        return text


def match(terms, text):
    
    matcher = PhraseMatcher(NLP.vocab, attr="LOWER")
    
    patterns = [NLP.make_doc(tx) for tx in terms]
    matcher.add("TerminologyList", patterns)
    
    doc = NLP(text)
    
    matches = matcher(doc)
    
    return matches    



def get_object_from_article(tag_name, node):
    return node.find(".//{}".format(tag_name))

