from django.urls import path

from . import views
from . import util 

app_name= "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("wiki/newpage", views.newpage, name="newpage"),
    path("wiki/search", views.search, name="search"),
    path("edit/<str:title>/", views.editpage, name="editpage"),
    path("wiki/", views.rando, name="rando"),
]
