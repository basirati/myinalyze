from django.urls import path, include, re_path
from . import views

app_name = 'riaapp'
urlpatterns = [
   	path('', views.IndexView.as_view(), name='index'),
    path('loadfile/analyze/', views.analyze, name='analyze'),
    path('loadfile/depslist/', views.depslist, name='depslist'),
    path('loadfile/sresults/', views.searchresults, name='searchresults'),
    re_path(r'^getreqs/$', views.getReqs, name='getreqs'),
    re_path(r'^getlp/$', views.getLP, name='getlp'),
    re_path(r'^loadfile/$', views.loadfile, name='loadfile'),
    re_path(r'^addreq/$', views.addReq, name='addreq'),
    re_path(r'^addlearninstance/$', views.addLearnInstance, name='addlearninstance'),
    re_path(r'^getreqdeps/$', views.getReqDeps, name='getreqdeps')
]