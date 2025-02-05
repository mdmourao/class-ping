from .decorators import login_required
from .models import *
from django.shortcuts import render, get_object_or_404, get_list_or_404
import pyotp
from django.conf import settings


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


def presentation_session_view(request, session_uuid):
    session = get_object_or_404(Session, uuid=session_uuid)
    current_url = request.build_absolute_uri()

    context = {
        "session": session,
        "current_url": current_url,
        "otp_interval": settings.OTP_INTERVAL
    }

    return render(request, "class_attendance/presentation_session.html", context)

def join_session_view(request, session_uuid):
    session = get_object_or_404(Session, uuid=session_uuid)

    base_url = request.build_absolute_uri('/')
    join_url = f"{base_url}sessions/{session.uuid}/join"
    msg = ""

    if request.method == "POST":
        code = request.POST.get("code")
        totp = pyotp.TOTP(session.secret, interval=settings.OTP_INTERVAL)

        if totp.verify(code):
            student_id = request.POST.get("student_id")
            student = Student.objects.filter(number=student_id).first()
            if not student:
                student = Student.objects.create(number=student_id)
            
            session.students.add(student)
            session.save()
            msg = "Success" 
        else:
            msg = "Invalid code"
        
    context = {
        "session": session,
        "join_url": join_url,
        "error": msg,
    }

    return render(request, "class_attendance/join_session.html", context)