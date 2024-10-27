from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Location, Category


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
    depth: int = int(request.GET.get(key="depth", default="0"))
    include_categories: bool = int(request.GET.get(key="categories", default="0")) > 0
    if not (0 <= depth):
        return JsonResponse({"error": "depth must be positive"}, status=400)
    location: Location = get_object_or_404(Location, pk=location_id)
    content = location.to_json(depth=depth, include_categories=include_categories)
    return JsonResponse(content, headers={"Access-Control-Allow-Origin": "*"})


def get_categories(request: HttpRequest) -> HttpResponse:
    content = [cat.to_json() for cat in Category.objects.all()]
    return JsonResponse(content, safe=False, headers={"Access-Control-Allow-Origin": "*"})
