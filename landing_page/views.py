from django.shortcuts import render

def landing_page_view(request):
    return render(request, "landing_page/landing_page.html")