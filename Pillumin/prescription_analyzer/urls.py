from django.urls import path
from . import views

urlpatterns=[
    path("",views.home,name="home"),
    path("analyze/", views.analyze_prescription, name="analyze_prescription"),

]