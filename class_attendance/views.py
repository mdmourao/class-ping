from .decorators import login_required
from .models import *
from django.shortcuts import render, get_object_or_404, get_list_or_404
import pyotp
from django.conf import settings
from .forms import *
from formtools.wizard.views import SessionWizardView
from collections import OrderedDict

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


@login_required
def presentation_session_view(request, session_uuid):
    session = get_object_or_404(Session, uuid=session_uuid)
    current_url = request.build_absolute_uri()

    context = {
        "session": session,
        "current_url": current_url,
        "otp_interval": settings.OTP_INTERVAL
    }

    return render(request, "class_attendance/presentation_session.html", context)

class JoinSessionView(SessionWizardView):
    form_list = [
        ("student_number", StudentNumberForm),
        ("name", NameForm),
        ("code", CodeForm),
    ]
    template_name = "class_attendance/join_session.html"

    def student_needs_name(wizard):
        step0_data = wizard.get_cleaned_data_for_step("student_number") or {}
        student_number = step0_data.get("student_number")
        if student_number:
            return not Student.objects.filter(number=student_number).exists()
        return True
    
    condition_dict = {
        "name": student_needs_name,
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step == "code": 
            session = get_object_or_404(Session, uuid=self.kwargs.get("session_uuid"))
            kwargs.update({"session": session})
        return kwargs

    def done(self, form_list, **kwargs):
        form_data = {}
        for form in form_list:
            form_data.update(form.cleaned_data)

        student_number = form_data["student_number"]
        if Student.objects.filter(number=student_number).exists():
            student = Student.objects.get(number=student_number)
        else:
            student = Student.objects.create(
                number=student_number,
                first_name=form_data["first_name"],
                last_name=form_data["last_name"],
            )

        session = get_object_or_404(Session, uuid=self.kwargs.get("session_uuid"))
        session.students.add(student)
        session.save()

        return render(self.request, "class_attendance/done.html", {"form_data": form_data})