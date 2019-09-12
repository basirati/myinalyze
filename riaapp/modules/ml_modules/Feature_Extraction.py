import pandas as pd
import numpy as np
import spacy
import nltk
from nltk.corpus import wordnet

import time

model='en_core_web_sm'
nlp = spacy.load(model)
simple_doc = nlp('This is a sentence for initialization.')

def isStopWord(w):
    if w.pos_ == 'DET':
        return True 
    return False
    
def getOrigDep(word):
    if (word.dep_ != 'conj'):
        return word.dep_
    return getOrigDep(word.head)

def getSynAnt(word):
    synonyms = [] 
    antonyms = []
    for syn in wordnet.synsets(word): 
        for l in syn.lemmas(): 
            synonyms.append(l.name()) 
            if l.antonyms(): 
                antonyms.append(l.antonyms()[0].name()) 
    return synonyms, antonyms


def getWUPSimilarity(t1, t2, w1, w2):
    try:
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
    except (BaseException) as e:
        print(str(e))
        return 0

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

def normalizeSimAnt(sim):
    if sim == None:
        sim = 0
    elif sim < 0.2:
        sim = 0
    elif 0.2 <= sim < 0.8:
        sim = 0.5
    elif 0.8 <= sim:
        sim = 1
        
    return sim

def updateSimAnt(t1, t2, sfts, afts, state):
    similarity = normalizeSimAnt(getWUPSimilarity(t1, t2, t1.text, t2.text))
    antonymity = normalizeSimAnt(getAntonymity(t1, t2, t1.text, t2.text))
    if similarity > 0:
        if sfts[state] < similarity:
            sfts[state] = similarity
    if antonymity > 0:
        if afts['a'+state] < antonymity:
            afts['a'+state] = antonymity
    return sfts, afts


def isSubject(token):
    return getOrigDep(token).endswith('subj')
def isObject(token):
    return getOrigDep(token).endswith('obj')

def getStcSubObjFeatures(req1, req2):
    sfts = {'subjsubj' : 0, 'subjobj' : 0, 'objsubj' : 0, 'objobj' : 0}
    afts = {'asubjsubj' : 0, 'asubjobj' : 0, 'aobjsubj' : 0, 'aobjobj' : 0}
    for t1 in req1:
        if isSubject(t1):
            for t2 in req2:
                if isSubject(t2):
                    sfts, afts = updateSimAnt(t1, t2, sfts, afts, 'subjsubj')
                elif isObject(t2):
                    sfts, afts = updateSimAnt(t1, t2, sfts, afts, 'subjobj')
        elif isObject(t1):
            for t2 in req2:
                if isSubject(t2):
                    sfts, afts = updateSimAnt(t1, t2, sfts, afts, 'objsubj')
                elif isObject(t2):
                    sfts, afts = updateSimAnt(t1, t2, sfts, afts, 'objobj')
    sfts.update(afts)
    return sfts

def getNounLemmas(doc):
    res = []
    for t in doc:
        if t.tag_.startswith('NN'):
            res.append(t.lemma_)
    return res

def getVerbLemmas(doc):
    res = []
    for t in doc:
        if t.tag_.startswith('VB'):
            res.append(t.lemma_)
    return res

def getRootLemma(doc):
    for t in doc:
        if t.dep_ == 'ROOT':
            return t.lemma_
    return None

def getNounSimilarityPortion(req1, req2):
    try:
        ns1 = getNounLemmas(req1)
        ns2 = getNounLemmas(req2)

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
    except (BaseException) as e:
        print(str(e))
        return 0

def getNSPFeatures(r1, r2):
    res = {'noun_ovlap_1_2' : getNounSimilarityPortion(r1, r2), 'noun_ovlap_2_1' : getNounSimilarityPortion(r2, r1)}
    return res


def getVerbSimilarityPortion(req1, req2):
    vs1 = getVerbLemmas(req1)
    vs2 = getVerbLemmas(req2)
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


def getVSPFeatures(r1, r2):
    res = {'verb_ovlap_1_2' : getVerbSimilarityPortion(r1, r2), 'verb_ovlap_2_1' : getVerbSimilarityPortion(r2, r1)}
    return res


def getModalityType(doc):
    try:
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
    except (BaseException) as e:
        print(str(e))
        return 'unknown'
    

def getModalityFeatures(req1, req2):
    res = {'M_1': getModalityType(req1), 'root_1': getRootLemma(req1), 'M_2': getModalityType(req2), 'root_2': getRootLemma(req1)}
    return res



def createFBag(req1_doc, req2_doc):
    #start_time = time.time()
    fbag = getStcSubObjFeatures(req1_doc, req2_doc)
    #print("AAA--- %s seconds ---" % (time.time() - start_time))
    fbag.update(getNSPFeatures(req1_doc, req2_doc))
    fbag.update(getVSPFeatures(req1_doc, req2_doc))
    fbag.update(getModalityFeatures(req1_doc, req2_doc))
    return fbag
