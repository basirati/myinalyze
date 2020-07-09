from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('web-view/', views.webview, name='web-view'),
    path('web-view/trend/<str:trend>/', views.trend, name='trend'),
]