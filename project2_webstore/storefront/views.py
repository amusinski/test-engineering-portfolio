from django.shortcuts import render


def landing(request):
    context = {
        'store_name': 'Little Apple Nutrition',
        'tagline': '',
    }
    return render(request, 'storefront/landing.html', context)
