from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("metadata", views.metadataDownload, name="metadata"),
    path("viewf", views.viewFolders, name="viewFolders"),
    path("viewc", views.viewContents, name="viewContents"),
    path("stream", views.stream, name="stream")
]