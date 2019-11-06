from django.urls import path, include, re_path
from . import views

app_name = 'riaapp'
urlpatterns = [
   	path('', views.IndexView.as_view(), name='index'),
   	path('create', views.CreateProj.as_view(), name='create_proj'),
   	path('loadproj', views.LoadProj.as_view(), name='load_proj'),
    path('loadfile/analyze/', views.analyze, name='analyze'),
    path('loadfile/depslist/', views.depslist, name='depslist'),
    path('loadfile/sresults/', views.searchresults, name='searchresults'),
    path('loadfile/addload/', views.addreqspage, name='addreqspage'),
    path('loadfile/projconfig/', views.projconfig, name='projconfig'),
    
	#re_path(r'^loadfile/analyze/$', views.analyze, name='analyze'),
    re_path(r'^getallreqsanddeps/$', views.getAllReqsAndDeps, name='getallreqsanddeps'),
    re_path(r'^getlp/$', views.getLP, name='getlp'),
    re_path(r'^loadfile/$', views.loadfile, name='loadfile'),
    re_path(r'^addreq/$', views.addReq, name='addreq'),
    re_path(r'^addlearninstance/$', views.addLearnInstance, name='addlearninstance'),
    re_path(r'^getreqdeps/$', views.getReqDeps, name='getreqdeps'),
    re_path(r'^reset/$', views.resetAll, name='reset'),
    re_path(r'^delproj/$', views.deleteProj, name='delproj')
]