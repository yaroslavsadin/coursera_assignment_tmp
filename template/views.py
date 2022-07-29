from django.shortcuts import render


# Create your views here.

def echo(request):
    if request.method == 'GET':
        context = {
            'method': 'get',
            'vars': request.GET
        }
    elif request.method == 'POST':
        context = {
            'method': 'post',
            'vars': request.POST
        }
    else:
        raise RuntimeError(f'Wrong method: {request.method}')
    context['statement'] = request.META.get('HTTP_X_PRINT_STATEMENT', 'empty')
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
