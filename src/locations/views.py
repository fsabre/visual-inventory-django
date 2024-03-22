from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("You are at the root of the locations app.")
