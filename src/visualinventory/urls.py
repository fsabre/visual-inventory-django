from django.urls import path

from . import views

urlpatterns = [
    path("location/<int:location_id>", view=views.get_location, name="getLocation"),
    path("category", view=views.get_categories, name="getCategories"),
]
