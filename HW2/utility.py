### Utility functions and classes
import spacy
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher


NLP = spacy.load("en_core_web_sm")


class PubmedArticle(object):
    
    def __init__(self, article):
        
        self.is_json = False
        
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
        return self.__abstract_text
    
    @property
    def abstract_doc(self):
        return self.__abstract_doc
    
    @property
    def title_doc(self):
        return self.__title_doc
    
    @property
    def num_of_words_in_abs(self):
        return token_count(self.abstract_text)
    
    def explain(self):
        tok_exp = NLP.tokenizer.explain(self.abstract_text)
        
        tk_count = 0
        sf_count = 0
        pf_count = 0
        if_count = 0
        
        for tok in tok_exp:
            print(tok[1] + "\t" + tok[0])
            if tok[0] == "SUFFIX":
                sf_count += 1
            elif tok[0] == "PREFIX":
                pf_count += 1
            elif tok[0] == "TOKEN":
                tk_count += 1
            elif tok[0] == "INFIX":
                if_count += 1
        
        print("Token#: {}, SUFFIX_#: {}, PREFIX_#: {}, INFIX_#:{}, TOTAL: {}".format(tk_count, 
                                                                                  sf_count, pf_count, if_count, 
                                                                                  tk_count+sf_count+pf_count+if_count))
    
    def get_formatted_title(self):
        
        formatted_title = []
        begin = 0
        
        for _, start, end in self.__title_matches:
            # no style applied
            formatted_title.append(("#ffffff bold", self.title_doc[begin:start].text_with_ws))
            
            # apply style to matched text
            formatted_title.append(("#aa9922 bold", self.title_doc[start:end].text_with_ws))
            begin = end
        
        formatted_title.append(("#ffffff bold", self.title_doc[end:].text_with_ws))
            
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
        
        formatted_text.append(("", self.abstract_doc[end:].text_with_ws))
        
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


class JsonArticle(object):
    def __init__(self, jo):
        jo = jo[0]
        self.name = jo['username']
        self.__raw_text = " ".join([v for v in jo.values()])
        self.__text = jo['tweet_text']
        
        self.__raw_doc = NLP(self.__raw_text)
        self.__doc = NLP(self.__text)
        
        self.article_title = self.name
        self.contain_title = False
        self.contain_abstract = False
        
        self.is_json = True
        
    @property
    def text(self):
        return self.__doc.text
    
    @property
    def number_of_word_in_tweet(self):
        return token_count(self.__text)

    @property
    def number_of_sents(self):
        return len(list(self.__doc.sents))
    
    def check_terms(self, terms):
        self.contain_text = False
        self.__text_matches = match(terms, self.__text)
        if len(self.__text_matches) > 0:
            self.contain_text = True


def token_count(text):
    tok_exp = NLP.tokenizer.explain(text)
    tk_count = 0
    
    for tk in tok_exp:
        if tk[0] == "TOKEN":
            tk_count +=1
    
    return tk_count


def match(terms, text):
    
    matcher = PhraseMatcher(NLP.vocab, attr="LOWER")
    
    patterns = [NLP.make_doc(tx) for tx in terms]
    matcher.add("TerminologyList", patterns)
    
    doc = NLP(text)
    
    matches = matcher(doc)
    
    return matches    



def get_object_from_article(tag_name, node):
    return node.find(".//{}".format(tag_name))


# A Dynamic Programming based Python program for edit
# distance problem


def editDistDP(str1, str2, m, n):
	# Create a table to store results of subproblems
	dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

	# Fill d[][] in bottom up manner
	for i in range(m + 1):
		for j in range(n + 1):

			# If first string is empty, only option is to
			# insert all characters of second string
			if i == 0:
				dp[i][j] = j # Min. operations = j

			# If second string is empty, only option is to
			# remove all characters of second string
			elif j == 0:
				dp[i][j] = i # Min. operations = i

			# If last characters are same, ignore last char
			# and recur for remaining string
			elif str1[i-1] == str2[j-1]:
				dp[i][j] = dp[i-1][j-1]

			# If last character are different, consider all
			# possibilities and find minimum
			else:
				dp[i][j] = 1 + min(dp[i][j-1],	 # Insert
								dp[i-1][j],	 # Remove
								dp[i-1][j-1]) # Replace

	return dp[m][n]


# Driver code
#str1 = "sunday"
#str2 = "saturday"

#print(editDistDP(str1, str2, len(str1), len(str2)))
# This code is contributed by Bhavya Jain

