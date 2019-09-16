from joblib import dump, load
import os
from sklearn.feature_extraction import DictVectorizer
from sklearn.base import clone

from django.core.files.storage import default_storage

from . import Feature_Extraction as fe
from ..utils import PreProcessing as pp
from ..utils import LoadData as ld

from ...models import Req, Dep, DepType, DepLearnInstance

class DependencyIdentifier:
    clf = None
    vec = None
    dep_type = None
    def __init__(self, type):
        self.clf = load('riaapp/modules/ml_models/mentropy_constrains.joblib')
        self.vec = load('riaapp/modules/ml_models/vectorizer_constrains.joblib')
        self.dep_type = type


    def learnAgain(self):
        #ld.loadLearnedInstancesFromCSV(self.dep_type, 'riaapp/modules/ml_models/500instances.csv', ';')
        y = []
        x = []
        for instance in DepLearnInstance.objects.all():
            r1doc = fe.nlp(instance.r1)
            r2doc = fe.nlp(instance.r2)
            x.append(fe.createFBag(r1doc, r2doc))
            if instance.positive == True:
                y.append(1)
            else:
                y.append(-1)
        
        self.vec = DictVectorizer()
        self.vec.fit(x)
        xx = self.vec.transform(x).toarray()
        self.clf = clone(self.clf)
        self.clf.fit(xx, y)

        vec_name = 'vec_' + self.dep_type.name
        vec_path = default_storage.location + os.sep + vec_name + '.joblib'
        dump(self.vec, vec_path)
        clf_name = 'clf_' + type(self.clf).__name__
        clf_path = default_storage.location + os.sep + clf_name + '.joblib'
        dump(self.clf, clf_path)
        #save the model
        #load the model
        #reload the deps
        #baadan bayad in poshte sahne hey ejra she

    def loadDeps(self):
        for r1 in Req.objects.all():
            r1doc = pp.getDocFromBytes(r1.nlp_doc.doc)
            for r2 in Req.objects.all():
                if r1 == r2:
                    continue
                r2doc = pp.getDocFromBytes(r2.nlp_doc.doc)
                if self.identifyDOC(r1doc, r2doc):
                    new_dep = Dep(dep_type=self.dep_type, source = r1, destination = r2)
                    new_dep.save()

    def updateDepsByNewReq(self, new_req):
        new_deps = []
        new_r_doc = pp.getDocFromBytes(new_req.nlp_doc.doc)
        for r in Req.objects.all():
            r2doc = pp.getDocFromBytes(r.nlp_doc.doc) 
            if self.identifyDOC(new_r_doc, r2doc):
                new_dep = Dep(dep_type =self.dep_type, source = new_req, destination = r)
                new_dep.save()
                new_deps.append(new_dep)
            if self.identifyDOC(r2doc, new_r_doc):
                new_dep = Dep(dep_type =self.dep_type, source = r, destination = new_req)
                new_dep.save()
                new_deps.append(new_dep)
        return new_deps


    def identifyOBJ(self, req1, req2):
        r1doc = pp.getDocFromBytes(req1.nlp_doc.doc)
        r2doc = pp.getDocFromBytes(req2.nlp_doc.doc)
        return self.identifyDOC(req1doc, req2doc)


    def identifyDOC(self, req1doc, req2doc):
        x = fe.createFBag(req1doc, req2doc)
        xx = self.vec.transform(x)
        y =  self.clf.predict(xx)
        if y > 0:
            return True
        else:
            return False

