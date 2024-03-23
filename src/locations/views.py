from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render

from .models import Location


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("You are at the root of the locations app.")


def viewer(request: HttpRequest, location_id: int) -> HttpResponse:
    location: Location = get_object_or_404(Location, pk=location_id)
    context = {
        "location": location,
        "sub_locations": location.children.all(),
    }
    return render(request, "locations/viewer.jinja2", context=context)
