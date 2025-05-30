from django.shortcuts import render, redirect

def landing_page_view(request):
    if request.user.is_authenticated:
        return redirect('/class_attendance/universities')
    
    return render(request, "landing_page/landing_page.html")