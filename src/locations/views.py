from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404

from .models import Location


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("You are at the root of the locations app.")


def viewer(request: HttpRequest, location_id: int) -> HttpResponse:
    location: Location = get_object_or_404(Location, pk=location_id)
    sub_locations = location.children.all()
    return HttpResponse(f"""
        <h1>Location n°{location.pk} ({location.name})</h1>
        <p>
            <ul>
                {"".join(f"<li>{sl.name}</li>" for sl in sub_locations)}
            <ul>
        </p>
    """)
