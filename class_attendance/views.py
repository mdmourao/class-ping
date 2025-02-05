from django.shortcuts import render
from .decorators import login_required

@login_required
def courses_view(request):
    return render(request, "class_attendance/courses.html")

@login_required
def school_classes_view(request, course_id):
    return render(request, "class_attendance/school_classes.html")

@login_required
def sessions_view(request, course_id,school_class_id):
    return render(request, "class_attendance/sessions.html")

def join_session_view(request, session_uuid):
    return render(request, "class_attendance/join_session.html")