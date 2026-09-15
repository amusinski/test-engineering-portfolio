from django.shortcuts import render


def landing(request):
    context = {
        'store_name': 'Little Apple Nutrition',
        'tagline': 'Little Apple, Big Impact',
    }
    return render(request, 'storefront/landing.html', context)
