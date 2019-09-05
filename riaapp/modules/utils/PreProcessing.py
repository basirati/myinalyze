import pandas as pd 
import nltk
import re

def importJiraCSV(file_addr):
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

def importJiraCSV_2(file_addr):
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

