import pandas as pd
import numpy as np
import spacy
import nltk
from nltk.corpus import wordnet as wn

model='en_core_web_sm'
nlp = spacy.load(model)

def isStopWord(w):
    if w.pos_ == 'DET':
        return True 
    return False


def getNounLemmas(s):
    res = []
    doc = nlp(s)
    for nc in doc.noun_chunks:
        for t in nc:
            if not(isStopWord(t)):
                res.append(t.lemma_)
    return res


def getVerbLemmas(s):
    res = []
    doc = nlp(s)
    for t in doc:
        if t.tag_.startswith('VB'):
            res.append(t.lemma_)
    return res


def getNounSimilarityPortion(r1, r2):
    ns1 = getNounLemmas(r1)
    ns2 = getNounLemmas(r2)
    if len(ns1) < 1 or len(ns2) < 1:
        return 0
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


def getVerbSimilarityPortion(r1, r2):
    vs1 = getVerbLemmas(r1)
    vs2 = getVerbLemmas(r2)
    if len(vs1) < 1 or len(vs2) < 1:
        return 0
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


def getOverlap(r1, r2):
    return getVerbSimilarityPortion(r1, r2) + getNounSimilarityPortion(r1, r2)

