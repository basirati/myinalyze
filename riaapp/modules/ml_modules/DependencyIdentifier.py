from joblib import dump, load
from sklearn.feature_extraction import DictVectorizer
from . import Feature_Extraction as fe

from .models import Req, Dep, DepType, DepLearnInstance

class DependencyIdentifier:
    clf = None
    vec = None
    dep_type = None
    def __init__(self, type):
        self.clf = load('riaapp/modules/ml_models/mentropy_constrains.joblib')
        self.vec = load('riaapp/modules/ml_models/vectorizer_constrains.joblib')
        dep_type = type


    def learnAgain():
        #learn
        #save the model
        #load the model
        #reload the deps

        #baadan bayad in poshte sahne hey ejra she

    def loadDeps():
        for r1 in Req.objects.all():
            for r2 in Req.objects.all():
                if r1 == r2:
                    continue
                if this.identify(r1, r2):
                    new_dep = Dep(dep_type =dep_type, source = r1, destination = r2)
                    new_dep.save()
    
    def identify(self, req1, req2):
        #inja harbar nlp run mishe ru reqs
        #bayad aval hame nlp shan o fe.bage shoon amade she tu preprocessing
        #ye fucntion bayad bashe ke aval preprocess kone
        #shayad bayad nlp doc ro serilize kard va as json ei chizi tu model save kard
        #function nlp mitune to preprocessing py bashe ehtemalan

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

