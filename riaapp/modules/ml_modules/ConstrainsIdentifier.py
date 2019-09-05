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
        if isinstance(req1, str) and isinstance(req2, str):
            r1 = self.parseReq(req1)
            r2 = self.parseReq(req2)
        else:
            r1 = self.parseReq(req1.text)
            r2 = self.parseReq(req2.text)

        x = fe.createFBag(r1, r2)
        xx = self.vec.transform(x)
        y =  self.clf.predict(xx)
        if y > 0:
            return True
        else:
            return False

    def parseReq(self, r):
        req = fe.Req(r)
        return req

