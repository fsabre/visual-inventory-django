from django.urls import path

from . import views

urlpatterns = [
    path("", view=views.index, name="index"),
    path("<int:location_id>", view=views.viewer, name="viewer"),
]
