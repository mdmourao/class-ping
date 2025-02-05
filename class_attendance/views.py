from .decorators import login_required
from .models import *
from django.shortcuts import render, get_object_or_404, get_list_or_404

@login_required
def courses_view(request):
    courses = get_list_or_404(Course, user=request.user)

    context = {
        "courses": courses
    }

    return render(request, "class_attendance/courses.html" , context)

@login_required
def school_classes_view(request, course_id):
    course = get_object_or_404(Course, user=request.user, id=course_id)

    context = {
        "course": course,
        "school_classes": course.classes.all( )
    }

    return render(request, "class_attendance/school_classes.html", context)

@login_required
def sessions_view(request, course_id,school_class_id):
    course = get_object_or_404(Course, user=request.user, id=course_id)
    school_class = get_object_or_404(SchoolClass, course=course, id=school_class_id)

    context = {
        "course": course,
        "school_class": school_class,
        "sessions": school_class.sessions.all()
    }
    return render(request, "class_attendance/sessions.html", context)


def join_session_view(request, session_uuid):
    return render(request, "class_attendance/join_session.html")