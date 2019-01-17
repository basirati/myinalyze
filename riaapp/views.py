from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic

from django.http import JsonResponse

from .models import Req, IntDep, IntDepType
from .forms import DocumentForm
from .modules.ml_modules import OverlapLib, ConstrainsIdentifier
from .modules.graph_modules import Graph_Analysis 

class IndexView(generic.ListView):
    template_name = 'riaapp/index.html'
    context_object_name = 'reqs'

    def get_queryset(self):
          return Req.objects.all()

###########################################################################

def detail(request):
    response = {'content': 22, 'reqs': 33}
    return render(request, 'riaapp/detail.html', response)

###########################################################################

def loadReqs(doc):
    for line in doc:
        line_txt = line.decode("utf-8")
        if OverlapLib.hasVerb(line_txt):
            new_req = Req(text = line_txt)
            new_req.save()


def loadInterDeps(dep_type):
    cid = ConstrainsIdentifier.ConstrainsIdentifier()
    for r1 in Req.objects.all():
        req1 = cid.parseReq(r1.text)
        for r2 in Req.objects.all():
            if r1 == r2:
                continue
            req2 = cid.parseReq(r2.text)
            if cid.identify(req1, req2):
                new_idep = IntDep(typ =dep_type, fro = r1, to = r2)
                new_idep.save()


def loadfile(request):
    content = "Successfull"
    if request.method == 'POST':
        Req.objects.all().delete()
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = request.FILES['reqs_file']
            loadReqs(doc)
    else:
        content = "Uploading File Failed!"
    response = {'content': content, 'size': Req.objects.count()}
    return render(request, 'riaapp/index.html', response)

def analyze(request):
    IntDepType.objects.all().delete()
    IntDep.objects.all().delete()
    
    constrains_type = IntDepType(name="constrains")
    constrains_type.save()
    
    loadInterDeps(constrains_type)

    rgraph = Graph_Analysis.ReqGraph()
    rgraph = Graph_Analysis.calculateNodeDegrees(rgraph)
    sortedReqs = Req.objects.all().order_by('-indeg')

    response = {'req_count': Req.objects.all().count(), 'max_dependent': rgraph.max_indeg[0].text, 'sortedReqs': sortedReqs}
    return render(request, 'riaapp/resadmin.html', response)


####################################################################

def resadmin(request):
    response = {'content': 'ok', 'reqs': Req.objects.all()}
    return render(request, 'riaapp/resadmin.html', response)


def getReqs(request):
    rs = []
    ds = []
    if request.method == 'GET':
        for r in Req.objects.all():
            rs.append(r.text)
        for d in IntDep.objects.all():
            tmp = {'source': d.fro.text, 'destination': d.to.text}
            ds.append(tmp)
    res = {'jreqs': rs, 'jdeps': ds}
    return JsonResponse(res)
