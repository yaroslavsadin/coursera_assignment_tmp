from django.http import HttpResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from django.utils.datastructures import MultiValueDictKeyError

@require_http_methods(['GET'])
def simple_route(request: HttpRequest):
    return HttpResponse('')


def slug_route(request: HttpRequest, *, slug):
    return HttpResponse(slug)


def sum_route(request: HttpRequest, *, a, b):
    return HttpResponse(int(a) + int(b))


@require_http_methods(['GET'])
def sum_get_method(request: HttpRequest):
    try:
        return HttpResponse(int(request.GET['a']) + int(request.GET['b']))
    except (MultiValueDictKeyError, ValueError):
        return HttpResponse(status=400)


@require_http_methods(['POST'])
def sum_post_method(request: HttpRequest):
    try:
        return HttpResponse(int(request.POST['a']) + int(request.POST['b']))
    except (MultiValueDictKeyError, ValueError):
        return HttpResponse(status=400)
