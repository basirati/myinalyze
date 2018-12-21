
# coding: utf-8

# In[89]:


import pandas as pd
import numpy as np
import spacy
import nltk
from nltk.corpus import wordnet


# In[90]:


model='en_core_web_sm'
nlp = spacy.load(model)


# In[91]:


class Req:
    def __init__(self, text):
        self.text = text
        self.nlp_doc = nlp(text)
        self.subjs = []
        self.objs = []
        self.root_verb = None
        self.size = 0
        self.noun_lemmas = []
        self.verb_lemmas = []
        self._load()
    
    def _load(self):
        counter = 0
        for t in self.nlp_doc:
            counter += 1
            
            if t.tag_.startswith('NN'):
                if not(self.isStopWord(t)):
                    self.noun_lemmas.append(t.lemma_)
            elif t.tag_.startswith('VB'):
                self.verb_lemmas.append(t.lemma_)
                
            if self.getOrigDep(t).endswith('subj'):
                self.subjs.append(t)
            elif self.getOrigDep(t).endswith('obj'):
                self.objs.append(t)
            elif t.dep_ == 'ROOT':
                self.root_verb = t
            else:
                continue
        self.size = counter
    
    def isStopWord(self, w):
        if w.pos_ == 'DET':
            return True 
        return False
    
    def getOrigDep(self, word):
        if (word.dep_ != 'conj'):
            return word.dep_
        return self.getOrigDep(word.head)


# In[92]:


def getSynAnt(word):
    synonyms = [] 
    antonyms = []
    for syn in wordnet.synsets(word): 
        for l in syn.lemmas(): 
            synonyms.append(l.name()) 
            if l.antonyms(): 
                antonyms.append(l.antonyms()[0].name()) 
    return synonyms, antonyms


# In[93]:


def getWUPSimilarity(t1, t2, w1, w2):
    if t1.lemma_ == t2.lemma_:
        return 1
    synonyms, _ = getSynAnt(w1)
    if w2 in synonyms:
        return 0.9
    synonyms, _ = getSynAnt(w2)
    if w1 in synonyms:
        return 0.9

    #NOUN
    synw1s = wordnet.synsets(w1, wordnet.NOUN)
    if len(synw1s) > 0:
        synw2s = wordnet.synsets(w2, wordnet.NOUN)
        if len(synw2s) > 0:
            return synw1s[0].wup_similarity(synw2s[0])
        synw2s = wordnet.synsets(w2, wordnet.VERB)
        if len(synw2s) > 0:
            return synw1s[0].wup_similarity(synw2s[0])
        synw2s = wordnet.synsets(w2, wordnet.ADJ)
        if len(synw2s) > 0:
            return synw1s[0].wup_similarity(synw2s[0])
        synw2s = wordnet.synsets(w2, wordnet.ADV)
        if len(synw2s) > 0:
            return synw1s[0].wup_similarity(synw2s[0])
    #VERB
    synw1s = wordnet.synsets(w1, wordnet.VERB)
    if len(synw1s) > 0:
        synw2s = wordnet.synsets(w2, wordnet.NOUN)
        if len(synw2s) > 0:
            return synw1s[0].wup_similarity(synw2s[0])
        synw2s = wordnet.synsets(w2, wordnet.VERB)
        if len(synw2s) > 0:
            return synw1s[0].wup_similarity(synw2s[0])
        synw2s = wordnet.synsets(w2, wordnet.ADJ)
        if len(synw2s) > 0:
            return synw1s[0].wup_similarity(synw2s[0])
        synw2s = wordnet.synsets(w2, wordnet.ADV)
        if len(synw2s) > 0:
            return synw1s[0].wup_similarity(synw2s[0])
    #ADJ
    synw1s = wordnet.synsets(w1, wordnet.ADJ)
    if len(synw1s) > 0:
        synw2s = wordnet.synsets(w2, wordnet.NOUN)
        if len(synw2s) > 0:
            return synw1s[0].wup_similarity(synw2s[0])
        synw2s = wordnet.synsets(w2, wordnet.VERB)
        if len(synw2s) > 0:
            return synw1s[0].wup_similarity(synw2s[0])
        synw2s = wordnet.synsets(w2, wordnet.ADJ)
        if len(synw2s) > 0:
            return synw1s[0].wup_similarity(synw2s[0])
        synw2s = wordnet.synsets(w2, wordnet.ADV)
        if len(synw2s) > 0:
            return synw1s[0].wup_similarity(synw2s[0])
    #ADV
    synw1s = wordnet.synsets(w1, wordnet.ADV)
    if len(synw1s) > 0:
        synw2s = wordnet.synsets(w2, wordnet.NOUN)
        if len(synw2s) > 0:
            return synw1s[0].wup_similarity(synw2s[0])
        synw2s = wordnet.synsets(w2, wordnet.VERB)
        if len(synw2s) > 0:
            return synw1s[0].wup_similarity(synw2s[0])
        synw2s = wordnet.synsets(w2, wordnet.ADJ)
        if len(synw2s) > 0:
            return synw1s[0].wup_similarity(synw2s[0])
        synw2s = wordnet.synsets(w2, wordnet.ADV)
        if len(synw2s) > 0:
            return synw1s[0].wup_similarity(synw2s[0])


# In[94]:


def getAntonymity(t1, t2, w1, w2): 
    antonyms = [] 
    for syn in wordnet.synsets(w1): 
        for l in syn.lemmas(): 
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name()) 
    if len(antonyms) < 1:
        return 0
    if w2 in antonyms:
        return 1
    avg = 0
    for a in antonyms:
        tmp = getWUPSimilarity(t2, nlp(a)[0], w2, a)
        if tmp == None:
            tmp = 0
        avg = avg + tmp
    if len(antonyms) > 0:
        avg = avg / len(antonyms)
    else:
        return 0
    return avg


# In[95]:


def normalizeSimAnt(sim):
    if sim == None:
        sim = 'nothing'
    elif sim < 0.2:
        sim = 'low'
    elif 0.2 <= sim < 0.4:
        sim = 'some'
    elif 0.4 <= sim < 0.6:
        sim = 'medium'
    elif 0.6 <= sim < 0.8:
        sim = 'much'
    elif 0.8 <= sim < 0.95:
        sim = 'high'
    elif 0.95 <= sim:
        sim = 'strong'
        
    return sim
    


# In[96]:


def normalizeSimAnt2(sim):
    if sim == None:
        sim = 0
    elif sim < 0.2:
        sim = 0
    elif 0.2 <= sim < 0.8:
        sim = 0.5
    elif 0.8 <= sim:
        sim = 1
        
    return sim


# In[97]:


def updateSimAnt(t1, t2, sfts, afts, state):
    similarity = normalizeSimAnt2(getWUPSimilarity(t1, t2, t1.text, t2.text))
    antonymity = normalizeSimAnt2(getAntonymity(t1, t2, t1.text, t2.text))
    if similarity > 0:
        if sfts[state] < similarity:
            sfts[state] = similarity
    if antonymity > 0:
        if afts['a'+state] < antonymity:
            afts['a'+state] = antonymity
    return sfts, afts

def getStcSubObjFeatures2(req1, req2):
    sfts = {'subjsubj' : 0, 'subjobj' : 0, 'objsubj' : 0, 'objobj' : 0}
    afts = {'asubjsubj' : 0, 'asubjobj' : 0, 'aobjsubj' : 0, 'aobjobj' : 0}
    for t1 in req1.subjs:
        for t2 in req2.subjs:
            sfts, afts = updateSimAnt(t1, t2, sfts, afts, 'subjsubj')
        for t2 in req2.objs:
            sfts, afts = updateSimAnt(t1, t2, sfts, afts, 'subjobj')
    for t1 in req1.objs:
        for t2 in req2.subjs:
            sfts, afts = updateSimAnt(t1, t2, sfts, afts, 'objsubj')
        for t2 in req2.objs:
            sfts, afts = updateSimAnt(t1, t2, sfts, afts, 'objobj')
    
    sfts.update(afts)
    return sfts


# In[98]:


def getNounSimilarityPortion(req1, req2):
    ns1 = req1.noun_lemmas
    ns2 = req2.noun_lemmas
    if len(ns1) < 1 or len(ns2) < 1:
        return 'low'
    num1 = 0
    for n in ns1:
        for m in ns2:
            if n == m:
                num1 = num1 + 1
                break
    if len(ns1) > 0:
        ovlap = num1/len(ns1)
    else:
        ovlap = 0
    if ovlap < 0.2:
        ovlap = 0
    elif 0.2 <= ovlap < 0.4:
        ovlap = 0.3
    elif 0.4 <= ovlap < 0.6:
        ovlap = 0.5
    elif 0.6 <= ovlap < 0.8:
        ovlap = 0.7
    elif 0.8 <= ovlap:
        ovlap = 1
    return ovlap


# In[99]:


def getNSPFeatures(r1, r2):
    res = {'noun_ovlap_1_2' : getNounSimilarityPortion(r1, r2), 'noun_ovlap_2_1' : getNounSimilarityPortion(r2, r1)}
    return res


# In[100]:


def getVerbSimilarityPortion(req1, req2):
    vs1 = req1.verb_lemmas
    vs2 = req2.verb_lemmas
    if len(vs1) < 1 or len(vs2) < 1:
        return 'low'
    num1 = 0
    for n in vs1:
        for m in vs2:
            if n == m:
                num1 = num1 + 1
                break
    if len(vs1) > 0:
        ovlap = num1/len(vs1)
    else:
        ovlap = 0
    if ovlap < 0.2:
        ovlap = 0
    elif 0.2 <= ovlap < 0.4:
        ovlap = 0.3
    elif 0.4 <= ovlap < 0.6:
        ovlap = 0.5
    elif 0.6 <= ovlap < 0.8:
        ovlap = 0.7
    elif 0.8 <= ovlap:
        ovlap = 1
    return ovlap


# In[101]:


def getVSPFeatures(r1, r2):
    res = {'verb_ovlap_1_2' : getVerbSimilarityPortion(r1, r2), 'verb_ovlap_2_1' : getVerbSimilarityPortion(r2, r1)}
    return res


# In[102]:


def getModalityType(req):
    doc = req.nlp_doc
    mvs = []
    root_lemma = 'nothing'
    for t in doc:
        if t.lemma_ == 'be':
            if t.dep_ == 'ROOT':
                return 'fact_be'
        elif t.lemma_ == 'have':
            if t.dep_ == 'ROOT':
                if doc[t.i + 1].lemma_ == 'to':
                    return 'obligatory'
                else:
                    return 'fact_hv'
        elif t.lemma_ == 'need':
            if t.dep_ == 'ROOT':
                return 'fact_need'
        elif t.tag_.startswith('MD'):
            if t.head.dep_ == 'ROOT':
                if t.lemma_ == 'must' or t.lemma_ == 'shall':
                    return 'obligatory'
                elif t.lemma_ == 'can' or t.lemma_ == 'could':
                    return 'ability'
                elif t.lemma_ == 'may':
                    return 'permission'
                elif t.lemma_ == 'should' or t.lemma_ == 'ought':
                    return 'advice'
                elif t.lemma_ == 'will':
                    return 'futurative'
    return 'unknown'
    


# In[103]:


def getModalityFeatures(req1, req2):
    res = {'M_1': getModalityType(req1), 'root_1': req1.root_verb.lemma_, 'M_2': getModalityType(req2), 'root_2': req2.root_verb.lemma_}
    return res


# In[104]:


def createFBag(req1, req2):
    fbag = getStcSubObjFeatures2(req1, req2)
    fbag.update(getNSPFeatures(req1, req2))
    fbag.update(getVSPFeatures(req1, req2))
    fbag.update(getModalityFeatures(req1, req2))
    return fbag


# In[106]:


import time
r1 = 'Setting the mode to its current value must have no effect.'
r2 = 'Users must be able to set the mode.'
req1 = Req(r1)
req2 = Req(r2)
x = time.time()
createFBag(req1, req2)
x = time.time() - x
print(x)
#createFBag('Mode must be either automatic or manual.', 'Users must be able to set the mode.')
#createFBag('Mode must be either automatic or manual.', 'Users must be able to select  automatic.')

