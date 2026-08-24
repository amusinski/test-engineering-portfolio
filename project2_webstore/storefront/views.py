from django.shortcuts import render


def landing(request):
    context = {
        'store_name': 'Webstore',
        'tagline': 'Quality tested, one commit at a time.',
    }
    return render(request, 'storefront/landing.html', context)
