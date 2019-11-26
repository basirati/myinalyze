from ...models import Req, NLPDoc, DepLearnInstance, Issue, Project, Dep, DepType, DepIssue
from . import PreProcessing as pp
from ..ml_modules import Feature_Extraction as fe


def getReqsByProj(the_proj):
    if the_proj == None:
        return None
    res = None
    issues = Issue.objects.filter(proj=the_proj)
    first = True
    for iss in issues:
        if first:
            res = Req.objects.filter(issue=iss)
        else:
            res = res | Req.objects.filter(issue=iss)
        first = False
    return res


def getDepsByProj(the_proj):
    if the_proj == None:
        return None
    res = None
    types = DepType.objects.filter(proj=the_proj)
    first = True
    for t in types:
        if first:
            res = Dep.objects.filter(dep_type=t)
        else:
            res = res | Dep.objects.filter(dep_type=t)
        first = False
    return res

def getDepIssuesByProj(the_proj):
    if the_proj == None:
        return None
    res = None
    types = DepType.objects.filter(proj=the_proj)
    first = True
    for t in types:
        if first:
            res = DepIssue.objects.filter(dep_type=t)
        else:
            res = res | DepIssue.objects.filter(dep_type=t)
        first = False
    return res

def emptyProj(the_proj):
    try:
        issues = Issue.objects.filter(proj=the_proj)
        for iss in issues:
            Req.objects.filter(issue=iss).delete()
            iss.delete()

        dep_types = DepType.objects.filter(proj=the_proj)
        for dt in dep_types:
            DepIssue.objects.filter(dep_type=dt).delete()
            Dep.objects.filter(dep_type=dt).delete()
            dt.delete()

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
            #Inja bayad avaz she, alan line be line mirim jolo, vali kolan bayad issue by issue bashe, yani paragraph be paragraph
            addIssue(line_txt, 1, 'Task', 5, proj)
        return True
    except Exception as e:
        print(str(e))
        return False
    

def addIssue(txt, priority, itype, effort, proj):
    try:
        if txt == None:
            return None
        the_issue = Issue(text=txt, proj = proj, priority=priority, issue_type=itype, effort=effort)
        the_issue.save()

        docs = fe.nlp(txt)
        for sent in docs.sents:
            doc = sent.as_doc()
            addReqbyDoc(doc, the_issue)

        return the_issue
    except Exception as e:
        print('@addIssue: ', str(e))
        return None


def addReqbyDoc(doc, issue):
    try:
        doc_bytes = doc.to_bytes()
        the_nlp_doc = NLPDoc(doc = doc_bytes)
        the_nlp_doc.save()
        new_req = Req(text = doc.text, nlp_doc = the_nlp_doc, issue = issue)
        new_req.save()
        return new_req
    except Exception as e:
        print('@addReqByDoc: ', str(e))
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