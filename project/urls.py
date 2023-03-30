from django.urls import include, re_path, path
from . import views
urlpatterns = [
    path("", views.home_view ),
]