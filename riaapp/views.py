from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.http import JsonResponse
from django.core import serializers

from .models import Req, Dep, DepType, DepLearnInstance
from .forms import DocumentForm
from .modules.ml_modules import OverlapLib, DependencyIdentifier
from .modules.graph_modules import Graph_Analysis, REI_Graph_PathAnylsis
from .modules.utils import PreProcessing as pp

dependency_name = 'relates'

class IndexView(generic.ListView):
    template_name = 'riaapp/index.html'
    context_object_name = 'reqs'

    def get_queryset(self):
          return Req.objects.all()


###########################################################################

def loadReqs(doc):
    if doc.name.endswith('csv'):
        doc = pp.importJiraCSV_2(doc)
    for line in doc:
        if not(isinstance(line, str)):
            line_txt = line.decode("utf-8")
        else:
            line_txt = line
        if OverlapLib.hasVerb(line_txt):
            new_req = Req(text = line_txt)
            new_req.save()


def loadDeps(dep_type):
    c_id = DependencyIdentifier.DependencyIdentifier()
    for r1 in Req.objects.all():
        for r2 in Req.objects.all():
            if r1 == r2:
                continue
            if c_id.identify(r1, r2):
                new_dep = Dep(dep_type =dep_type, source = r1, destination = r2)
                new_dep.save()


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
    DepType.objects.all().delete()
    Dep.objects.all().delete()
    
    constrains_type = DepType(name=dependency_name)
    constrains_type.save()
    
    loadDeps(constrains_type)

    rgraph = Graph_Analysis.ReqGraph()
    rgraph = Graph_Analysis.calculateNodeDegrees(rgraph)
    size_limit = Req.objects.all().count()
    if size_limit > 10:
        size_limit = 9
    sortedReqs = Req.objects.all().order_by('-indeg')[:size_limit]

    #mainG = REI_Graph_PathAnylsis.importReqsToGraph()
    #dag = REI_Graph_PathAnylsis.transformToDAG(mainG)
    #longest_path = REI_Graph_PathAnylsis.getLongestPath(dag)

    response = {'req_count': Req.objects.all().count(), 'max_dependent': rgraph.max_indeg[0].text, 'max_influential': Req.objects.all().order_by('-indeg').reverse()[0], 'sortedReqs': sortedReqs}
    return render(request, 'riaapp/resadmin.html', response)

###################################################################

def searchresults(request):
    search_terms = request.GET.get('search_string').split()
    res = Req.objects
    for term in search_terms:
        res = res.filter(text__icontains=term)
    response = {'res': res}
    return render(request, 'riaapp/searchresults.html', response)

def depslist(request):
    response = {'deps': Dep.objects.all()}
    return render(request, 'riaapp/depslist.html', response)

def addLearnInstance(request):
    dep_id = request.GET.get('dep_id', None)
    the_dep = Dep.objects.get(pk=dep_id)
    the_positive = True if request.GET.get('positive', None) == 'true' else False
    if the_dep != None:
        existing_learn = DepLearnInstance.objects.filter(dep=the_dep)
        if len(existing_learn) == 0 :
            learn = DepLearnInstance.objects.create(dep=the_dep, positive=the_positive)
            learn.save()
        else:
            existing_learn[0].positive = the_positive
            existing_learn[0].save()
    res = {}
    return JsonResponse(res)

def resadmin(request):
    response = {'content': 'ok', 'reqs': Req.objects.all()}
    return render(request, 'riaapp/resadmin.html', response)

def addReq(request):
    new_req_text = request.GET.get('req', None)
    new_req = Req.objects.create(text=new_req_text)
    c_id = DependencyIdentifier.DependencyIdentifier()
    dep_type = DepType.objects.get(name=dependency_name)
    for r in Req.objects.all():
        if c_id.identify(new_req, r):
            new_dep = Dep(dep_type =dep_type, source = new_req, destination = r)
            new_dep.save()
        if c_id.identify(r, new_req):
            new_dep = Dep(dep_type =dep_type, source = r, destination = new_req)
            new_dep.save()

    success = False
    if new_req != None:
        success = True
    res = {'successful': success}
    return JsonResponse(res)

def getReqs(request):
    rs = []
    ds = []
    if request.method == 'GET':
        for r in Req.objects.all():
            rs.append(r.text)
        for d in Dep.objects.all():
            tmp = {'source': d.source.text, 'destination': d.destination.text}
            ds.append(tmp)
    res = {'jreqs': rs, 'jdeps': ds}
    return JsonResponse(res)

def getReqDeps(request):
    req_id = request.GET.get('req_id', None)
    the_req = Req.objects.get(pk=req_id)
    inf_objs = Dep.objects.filter(source=the_req)
    influencing = []
    for obj in inf_objs:
        influencing.append(obj.destination.text)
    depending_objs = Dep.objects.filter(destination=the_req)
    depending = []
    for obj in depending_objs:
        depending.append(obj.source.text)
    
    res = {'influencing': influencing, 'depending': depending}
    return JsonResponse(res)

def getLP(request):
    mainG = REI_Graph_PathAnylsis.importReqsToGraph()
    dag = REI_Graph_PathAnylsis.transformToDAG(mainG)
    longest_path = REI_Graph_PathAnylsis.getLongestPath(dag)
    print(longest_path)
    res = {'path': longest_path}
    return JsonResponse(res)

