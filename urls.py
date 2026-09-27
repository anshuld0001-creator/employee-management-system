from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path("add/", views.addEmp, name="add"),
    path("show/", views.showEmp, name="show"),
    path("edit/<eid>", views.updateEmp, name="edit"),
    path("del/<eid>", views.delEmp, name="delete"),
]