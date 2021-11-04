import pandas as pd
from spacy.matcher import PhraseMatcher
import spacy
from prompt_toolkit import HTML, PromptSession
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.formatted_text import FormattedText
import utility as utils

session = PromptSession()
NLP = spacy.load("en_core_web_md")
THRES = 0.9
DIST_THRES = 4

def main():
    docs = pd.read_csv("all_documents.csv", index_col="title", usecols=['title', 'abstract'])
    
    keywords = session.prompt("\nEnter Keyword to Search: ")
    print("")
    terms = keywords.strip(" ").split(",")

    match_list = []

    idx = 0
    
    for row in docs.iterrows():
        #matches = match(terms, row[1]['abstract'])
        #matches = similarity_match(terms, row[1]['abstract'])
        matches = edit_match(terms, row[1]['abstract'])
        
        if len(matches) > 0:
            match_list.append((row, matches))
        
        #match = edit_match(terms, row[0])
        #if match > 0:
        #    match_list.append(row)
        
        if idx > 20:
            break
        idx +=1
    
    #match_list = [o[1] for o in match_list]
    for row, matches in match_list:
        t, r = row
        text = r['abstract']
        text = get_formatted_abstract(text, matches)
        print(FormattedText([("#1144ff",  "{}.  \n".format(t))]))
        print(FormattedText(text))
        print("")


def get_formatted_abstract(abs, matches):
        
        formatted_text = []
        begin = 0
        
        doc = NLP(abs)
        
        for _, start, end in matches:
            
            # no style apply for this portion
            formatted_text.append(("", doc[begin:start].text_with_ws))
        
            # apply style to matched text
            formatted_text.append(("#ff0066", doc[start:end].text_with_ws))
            begin = end
        
        formatted_text.append(("", doc[end:].text_with_ws))
        
        return formatted_text
    

def match(terms, text):
    
    matcher = PhraseMatcher(NLP.vocab, attr="LOWER")
    
    patterns = [NLP.make_doc(tx) for tx in terms]
    matcher.add("TerminologyList", patterns)
    
    doc = NLP(text)
    
    matches = matcher(doc)
    
    return matches    

def similarity_match(terms, text):
    
    doc = NLP(text)
    tokens = [tk for tk in doc if tk.is_alpha]
    
    matcher = PhraseMatcher(NLP.vocab, attr="LOWER")
    
    match_list = []
    
    for t in terms:
        t = NLP(t)
        for tk in tokens:
            if t.similarity(tk) > THRES:
                match_list.append(NLP(tk.text))
    
    matcher.add("TerminologyList", match_list)
    matches = matcher(doc)
    
    return matches

def edit_match(terms, text):
    
    match_list = []
    doc = NLP(text)
    tokens = [tk.text for tk in doc if tk.is_alpha]
    
    for t in terms:
        t = t.lower()
        for tk in tokens:
            tk = tk.lower()
            dist = utils.editDistDP(t, tk, len(t), len(tk))
            if dist < DIST_THRES:
                match_list.append(NLP((tk)))
    
    matcher = PhraseMatcher(NLP.vocab, attr="LOWER")
    matcher.add("TerminologyList", match_list)
    matches = matcher(doc)
    
    return matches

if __name__ == '__main__':
    main()
    