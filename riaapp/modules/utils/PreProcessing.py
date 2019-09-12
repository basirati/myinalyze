import pandas as pd 
import nltk
import re
from ..ml_modules import Feature_Extraction as fe
from spacy.tokens import Doc


def getDocFromBytes(doc_bytes):
    return Doc(fe.simple_doc.vocab).from_bytes(doc_bytes)

def importJiraCSV_bySentence(file_addr):
    data = pd.read_csv(file_addr, delimiter=';') 
    res = []
    for des in data['Description']:
        des = des.replace('\r', '.')
        des = des.replace('\n', '.')
        des = des.replace('\xa0', '')
        sents = nltk.sent_tokenize(des)
        for s in sents:
            s = s.replace('#', '')
            s = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', s) 
            s = re.sub('\!\|.*\!', '', s)
            res.append(s)
    return res

def importJiraCSV_byIssue(file_addr):
    data = pd.read_csv(file_addr, delimiter=';') 
    res = []
    for des in data['Description']:
        des = des.replace('\r', '.')
        des = des.replace('\n', '.')
        des = des.replace('\xa0', '')
        des = des.replace('#', '')
        des = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', des) 
        des = re.sub('\!\|.*\!', '', des)
        res.append(des)
    return res

def hasVerb(doc):
    for t in doc:
        if t.tag_.startswith('VB'):
            return True
    return False