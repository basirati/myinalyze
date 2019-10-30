from ...models import Req, NLPDoc, DepLearnInstance, Issue, Project, Dep, DepType
from . import PreProcessing as pp
from ..ml_modules import Feature_Extraction as fe



def getReqsByProj(the_proj):
    res = []
    issues = Issue.objects.filter(proj=the_proj)
    for iss in issues:
        res = res + Req.objects.filter(issue=iss)
    res = set(res)
    return res

def emptyProj(the_proj):
    try:
        issues = Issue.objects.filter(proj=the_proj)
        for iss in issues:
            Req.objects.filter(issue=iss).delete()
            iss.delete()

        Dep.objects.all().delete()
        DepType.objects.all().delete()
        return True
    except Exception as e:
        print(str(e))
        return False



def loadReqs(doc, proj):
    try:
        if doc.name.endswith('csv'):
            doc = importJiraCSV_byIssue(doc)
        for line in doc:
            if not(isinstance(line, str)):
                line_txt = line.decode("utf-8")
            else:
                line_txt = line
            addReq(line_txt, -1, proj)
        return True
    except Exception as e:
        print(str(e))
        return False
    

def addReq(txt, issue_id, proj):
    try:
        doc = fe.nlp(txt)
        doc_bytes = doc.to_bytes()
        the_nlp_doc = NLPDoc(doc = doc_bytes)
        the_nlp_doc.save()

        the_issue = None
        #from django.shortcuts import get_object_or_404
        #comment = get_object_or_404(Comment, pk=comment_id)
        if issue_id == None or issue_id == -1:
            the_issue = Issue(proj = proj)
            the_issue.save()
        else:
            the_issue = Issue.objects.get(pk=issue_id)

        new_req = Req(text = txt, nlp_doc = the_nlp_doc, issue = the_issue)
        new_req.save()
        return new_req
    except Exception as e:
        print(str(e))
        return None


def loadLearnedInstancesFromCSV(dep_type, filename, seperator):
    try:
        data = open(filename, encoding="ANSI").read()
        for i, line in enumerate(data.split("\n")):
            if line != '' and line.isspace() != True:
                content = line.split(seperator)
                positive = True
                if content[0].lower() == 'false':
                    positive = False
                r1 = content[1]
                r2 = content[2]
                instance = DepLearnInstance.objects.create(dep_type=dep_type, r1=r1, r2=r2, positive=positive)
                instance.save()
        return True
    except Exception as e:
        print(str(e))
        return False




            #doc = fe.nlp(line_txt)
            #if pp.hasVerb(doc):
            #    doc_bytes = doc.to_bytes()
            #    the_nlp_doc = NLPDoc(doc = doc_bytes)
            #    the_nlp_doc.save()
            #    new_req = Req(text = line_txt, nlp_doc = the_nlp_doc)
            #    new_req.save()