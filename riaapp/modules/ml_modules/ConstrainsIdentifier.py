from joblib import dump, load
from sklearn.feature_extraction import DictVectorizer
from . import Feature_Extraction as fe

class ConstrainsIdentifier:
    clf = None
    vec = None
    def __init__(self):
        self.clf = load('riaapp/modules/ml_models/mentropy_constrains.joblib')
        self.vec = load('riaapp/modules/ml_models/vectorizer_constrains.joblib')
    
    def identify(self, req1, req2):
        x = fe.createFBag(req1, req2)
        xx = self.vec.transform(x)
        y =  self.clf.predict(xx)
        if y > 0:
            return True
        else:
            return False

    def parseReq(self, r):
        req = fe.Req(r)
        return req

