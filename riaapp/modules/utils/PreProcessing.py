import pandas as pd 
import nltk
import re
from ..ml_modules import Feature_Extraction as fe
from spacy.tokens import Doc


def getDocFromBytes(doc_bytes):
    return Doc(fe.simple_doc.vocab).from_bytes(doc_bytes)

def cleanText(txt):
    txt = txt.replace('\r', '.')
    txt = txt.replace('\n', '.')
    txt = txt.replace('\xa0', '')
    txt = txt.replace('#', '')
    txt = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', txt) 
    txt = re.sub('\!\|.*\!', '', txt)
    return txt

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
        res.append(cleanText(des))
    return res

class IssueHolder():
    title = "No Title" 
    text = "Empty"
    issue_type = 'task'
    priority = 1
    status = "ToDo"
    effort = 1
    creator = "Someone"
    created_date = None
    def printMe(self):
        print('------------')
        print(self.title)
        print(self.issue_type, self.priority, self.status, self.effort, self.creator, self.created_date)
        print(self.text)

def normalizePriority(txt_priority):
    if txt_priority == 'High':
        return 3
    if txt_priority == 'Medium':
        return 2
    return 1

def importJiraCSV_byIssue_Complete(file_addr):
    data = pd.read_csv(file_addr, delimiter=';') 
    res = []
    for i in range(len(data)):
        the_issue = IssueHolder()
        the_issue.title = cleanText(data['Summary'][i])
        the_issue.text = cleanText(data['Description'][i])
        the_issue.issue_type = data['Issue Type'][i]
        the_issue.priority = normalizePriority(data['Priority'][i])
        the_issue.status = data['Status'][i]
        the_issue.effort = data['Custom field (Story Points)'][i]
        if the_issue.effort < 1:
            the_issue.effort = 1
        the_issue.creator = data['Creator'][i]
        try:
            tmp_date = data['Created'][i].split()[0]
            splited = tmp_date.split('.')
            tmp_date = splited[2] + '-' + splited[1] + '-' + splited[0]
        except:
            tmp_date = '0000-00-00'
        the_issue.created_date = tmp_date
        res.append(the_issue)
    return res


def hasVerb(doc):
    for t in doc:
        if t.tag_.startswith('VB'):
            return True
    return False