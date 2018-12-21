from django.urls import path, include, re_path
from . import views

app_name = 'riaapp'
urlpatterns = [
   	path('', views.IndexView.as_view(), name='index'),
    path('detail/', views.detail, name='detail'),
    path('loadfile/analyze/', views.analyze, name='analyze'),
    path('resadmin/', views.resadmin, name='resadmin'),
    re_path(r'^like/$', views.like, name='like'),
    re_path(r'^loadfile/$', views.loadfile, name='loadfile'),
]