from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
import json

from .models import Req, Dep, DepType, DepLearnInstance, NLPDoc
from .forms import DocumentForm
from .modules.ml_modules.DependencyIdentifier import DependencyIdentifier
from .modules.graph_modules import Graph_Analysis, REI_Graph_PathAnylsis
from .modules.utils import LoadData as ld

dependency_name = 'relates'
di = DependencyIdentifier(None)
max_size = 10

class IndexView(generic.ListView):
    template_name = 'riaapp/index.html'
    context_object_name = 'reqs'
    def get_queryset(self):
          return None


def loadfile(request):
    content = "Successfull"
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = request.FILES['reqs_file']
            Req.objects.all().delete()
            DepType.objects.all().delete()
            Dep.objects.all().delete()
            NLPDoc.objects.all().delete()
            DepLearnInstance.objects.all().delete()
            ld.loadReqs(doc)
    else:
        content = "Uploading File Failed!"
    response = {'content': content, 'size': Req.objects.count()}
    return render(request, 'riaapp/index.html', response)

def analyze(request):
    if not DepType.objects.all().exists():
        thetype = DepType(name=dependency_name)
        thetype.save()
        di.dep_type = thetype
        di.loadDeps()
        rgraph = Graph_Analysis.ReqGraph()
        rgraph = Graph_Analysis.calculateNodeDegrees(rgraph)
        #mainG = REI_Graph_PathAnylsis.importReqsToGraph()
        #dag = REI_Graph_PathAnylsis.transformToDAG(mainG)
        #longest_path = REI_Graph_PathAnylsis.getLongestPath(dag)

    size_limit = min(Req.objects.all().count(), max_size)
    sortedReqs = Req.objects.all().order_by('-indeg')[:size_limit]
    response = {'sortedReqs': sortedReqs}
    return render(request, 'riaapp/resadmin.html', response)


def searchresults(request):
    search_terms = request.GET.get('search_string')
    isNone = False
    if search_terms == None:
        isNone = True

    if isNone or search_terms == []:
        response = {'res': Req.objects.all()}
        return render(request, 'riaapp/searchresults.html', response)
    else:
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
        existing_learn = DepLearnInstance.objects.filter(r1=the_dep.source.text).filter(r2=the_dep.destination.text)
        if len(existing_learn) == 0 :
            learn = DepLearnInstance.objects.create(dep_type=the_dep.dep_type, r1=the_dep.source.text, r2=the_dep.destination.text, positive=the_positive)
            learn.save()
        else:
            existing_learn[0].positive = the_positive
            existing_learn[0].save()
    res = {'success': 'true'}
    return JsonResponse(res)

def resadmin(request):
    response = {'reqs': Req.objects.all()}
    return render(request, 'riaapp/resadmin.html', response)

def addReq(request):
    new_req_text = request.GET.get('req', None)
    new_req = ld.addReq(new_req_text)
    if new_req != None:
        new_deps = di.updateDepsByNewReq(new_req)
        new_req.indeg = Graph_Analysis.calNodeInDegree(new_req)
        new_req.outdeg = Graph_Analysis.calNodeOutDegree(new_req)
        new_req.save()
        
        size_limit = min(Req.objects.all().count(), max_size)
        sortedReqs = []
        for r in Req.objects.all().order_by('-indeg')[:size_limit]:
            sortedReqs.append(json.dumps(model_to_dict(r)))
        new_depends_txt = []
        new_influences_txt = []
        for d in new_deps:
            if d.source == new_req:
                new_influences_txt.append(d.destination.text)
            else:
                new_depends_txt.append(d.source.text)
        new_req_json = json.dumps(model_to_dict(new_req))
        res = {'successful': True, 'sortedReqs': sortedReqs, 'new_depends': new_depends_txt, 'new_influences': new_influences_txt,'new_req':new_req_json}
    else:
        res = {'successful': False}
    
    return JsonResponse(res)

def getAllReqsAndDeps(request):
    rs = []
    ds = []
    if request.method == 'GET':
        for r in Req.objects.all():
            rs.append(json.dumps(model_to_dict(r)))
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

