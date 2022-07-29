from django.shortcuts import render


# Create your views here.

def echo(request):
    if request.method == 'GET':
        context = {
            'method': 'get',
            'vars': request.GET
        }
    else:
        context = {
            'method': 'post',
            'vars': request.POST
        }
    context['statement'] = request.META.get('X_PRINT_STATEMENT', 'empty')
    return render(request, 'echo.html', context)


def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 1),
        'b': request.GET.get('b', 1)
    })


def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })
