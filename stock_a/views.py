from django.shortcuts import render


def driver(request):

    context = {
        'text': 'Hola Aliens'
    }

    return render(request, 'base.html', context)
