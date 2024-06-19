from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Location


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("You are at the root of the locations app.")


def viewer(request: HttpRequest, location_id: int) -> HttpResponse:
    location: Location = get_object_or_404(Location, pk=location_id)
    sub_locations = location.children.all()
    category_names = set()
    location.fill_with_category_names(category_names)
    context = {
        "location": location,
        "sub_locations": sub_locations,
        "category_names": category_names,
    }
    return render(request, "locations/viewer.jinja2", context=context)


def get_location(request: HttpRequest, location_id: int) -> HttpResponse:
    depth: int = int(request.GET.get("depth", default="0"))
    if not (0 <= depth <= 1):
        return HttpResponse(status=400, content="depth must be between 0 and 1")
    location: Location = get_object_or_404(Location, pk=location_id)
    content = {
        "id": location.id,
        "name": location.name,
        "parent": location.parent.id if location.parent else None,
        "subLocations": [],
    }
    if depth == 1:
        content["subLocations"] = [
            {
                "id": sub.id,
                "name": sub.name,
                "parent": sub.parent.id if sub.parent else None,
                "subLocations": [],
            }
            for sub in location.children.all()
        ]
    category_names = set()
    location.fill_with_category_names(category_names)
    content["categoryNames"] = list(category_names)
    return JsonResponse(content, headers={"Access-Control-Allow-Origin": "*"})
