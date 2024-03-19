from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("test", views.test, name="test"),
    path("viewf", views.viewFolders, name="viewFolders"),
    path("viewc", views.viewContents, name="viewContents"),
    path("stream", views.stream, name="stream")
]