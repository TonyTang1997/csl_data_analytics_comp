import pandas as pd
import re
import matplotlib.pyplot as plt
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
import spacy

def similarity(w1,w2):
    return sum(w1*w2) / sum(w1 *w2)**0.5/ sum(w2*w2)**0.5 

def english(sent):
    try:
        return len(re.findall('[A-z]',sent))/len(sent) > 0.5
    except:
        return False 
def tokenize(comment,nlp):  
    doc = nlp(str(comment))
    return doc

def entity(comment):
    comment = [(X.text, X.label_) for X in comment.ents]
    return comment
def keyword(sent):
    #https://pythonprogramming.net/natural-language-toolkit-nltk-part-speech-tagging/
    out = [] 
    sent = sent.split()
    sent = nltk.pos_tag(sent)
    for word in sent:
        try:
            word[1].index('JJ')
            out.append(word[0].lower())
        except:
            try:
                word[1].index('RB')
                out.append(word[0].lower())
            except:
                pass
    return out

def word(comment):
    return [ X for X in comment]

def stopword(sent,stop_list):
    sent = word_tokenize(sent)
    out = []
    for w in sent:
        if w not in stop_list and len(w) >2:
            out.append(str(w))
    return out
def clean(sent,lemma):
    out = []
    sent = nltk.pos_tag(sent)
    for word in sent:
        try:
            word[1].index('V')
            out.append(lemma.lemmatize(word[0],'v'))
        except:
            out.append(lemma.lemmatize(word[0]))
    return " ".join(out)


review = pd.read_csv('./Data/reviews.csv',nrows=100)
lemmatizer = WordNetLemmatizer()
stop_list = set(stopwords.words('english'))
nlp = en_core_web_sm.load()
print(review.shape)
print(review.columns)

review['eng'] = review['comments'].apply(english)
review['comments'] = review['comments'][review['eng'] == True].apply(stopword, args=(stop_list,))
review['comments'] = review['comments'][review['eng'] == True].apply(clean, args=(lemmatizer,))
review['comment_token'] = review['comments'][review['eng'] == True].apply(tokenize, args=(nlp,))
review['keyword'] = review['comments'][review['eng']== True].apply(keyword)
review['entities'] = review['comment_token'][review['eng'] == True].apply(entity)
review['words'] = review['comment_token'][review['eng'] == True].apply(word)


nlp = spacy.load('en_core_web_md')
doc = nlp("This is some text that I am processing with Spacy")
print(doc[1].vector)
print(type(doc[1].vector))

count = 0
out = []
bad = nlp('bad')[0].vector
small = nlp('small')[0].vector
dirty = nlp('dirty')[0].vector
unfriend = nlp('unfriendly')[0].vector
for i,words in review['keyword'][review['eng'] == True].iteritems():
    for word in words:
        vec = nlp(str(word))[0].vector
        if similarity(vec, bad) > 0.7:
            print("close to bad | ", word,similarity(vec, bad))
            count += 1
        if similarity(vec,small) > 0.8:
            print('close to small | ',word, similarity(vec, small))
        if similarity(vec, dirty) > 0.7:
            print("close to dirty | ", word, similarity(vec, dirty))
            count += 1
        if similarity(vec,unfriend) > 0.7:
            print('close to unfriend |',word), similarity(vec, unfriend)

    out.append(count)
out = pd.Series(out)
out.to_csv('./1026.csv')

            