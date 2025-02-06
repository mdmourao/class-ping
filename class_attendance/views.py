from .decorators import login_required
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .forms import *
from formtools.wizard.views import SessionWizardView
from django.db.models import Q
from django.db import transaction
from django.utils.crypto import get_random_string

@login_required
def universities_view(request):
    # show universities where the user is an admin or a professor from a course
    universities = University.objects.filter(
        Q(admins=request.user) | Q(courses__professors=request.user)
    ).distinct()

    context = {
        "universities": universities
    }
    
    return render(request, "class_attendance/universities.html", context)

@login_required
def universities_edit_view(request, university_id):
    university = get_object_or_404(University, admins=request.user, id=university_id)
    
    if request.POST:
        form = UniversityForm(request.POST or None, request.FILES, instance=university)
        form_admin = AddAdminForm(request.POST or None)
        

        if 'form' in request.POST and form.is_valid():
            form.save()
            return redirect('/universities')
        
        if 'form_admin' in request.POST and form_admin.is_valid():
            admin_email = form_admin.cleaned_data['admin_email']
            if not User.objects.filter(email=admin_email).exists():
                raw_password = get_random_string(30) # the user must reset the password to login (we dont care about this password)
                user = User.objects.create_user(email=admin_email, username=admin_email, password=raw_password)
            else:
                user = User.objects.get(email=admin_email)

            university.admins.add(user)
            university.save()
            return redirect('/universities')
    else:
        form = UniversityForm(instance=university)
        form_admin = AddAdminForm()
        
    context = {
        'form': form,
        'form_admin': form_admin,
        'admins': university.admins.all(),
        'university': university

    }
    return render(request, 'class_attendance/universities_edit.html', context)

@login_required
def remove_admin_university_view(request, university_id, user_id):
    university = get_object_or_404(University, admins=request.user, id=university_id)
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        # the user can't remove himself
        return redirect('/universities')
    university.admins.remove(user)
    university.save()
    return redirect('/universities')


@login_required
def universities_new_view(request):
    form = UniversityForm(request.POST or None, request.FILES)
    if form.is_valid():
        with transaction.atomic():
            university = form.save(commit=False)
            university.save()
            university.admins.add(request.user)
        return redirect('/universities')

    context = {'form': form}
    return render(request, 'class_attendance/universities_new.html', context)

@login_required
def courses_view(request, university_id):
    # show courses where the user is a professor or one of the university's admins
    university = get_object_or_404(
        University.objects.filter(Q(admins=request.user) | Q(courses__professors=request.user)).distinct(),
        id=university_id
    )
    courses = Course.objects.filter(university=university).filter(
        Q(professors=request.user) | Q(university__admins=request.user)
    )
    context = {
        "courses": courses
    }

    return render(request, "class_attendance/courses.html" , context)

@login_required 
def courses_new_view(request,university_id):
    pass

@login_required
def courses_edit_view(request,university_id, course_id):
    pass

@login_required
def school_classes_view(request,course_id):
    course = Course.objects.get(id=course_id)
    course = get_object_or_404(
        Course.objects.filter(Q(professors=request.user) | Q(university__admins=request.user)),
        id=course_id
    )

    context = {
        "course": course,
        "school_classes": course.classes.all()
    }

    return render(request, "class_attendance/school_classes.html", context)

@login_required
def school_classes_new_view(request, course_id):
    pass

@login_required
def school_classes_edit_view(request, course_id, school_class_id):
    pass

@login_required
def sessions_view(request, course_id,school_class_id):
    course = get_object_or_404(
        Course.objects.filter(Q(professors=request.user) | Q(university__admins=request.user)),
        id=course_id
    )
    school_class = get_object_or_404(course.classes.all(), id=school_class_id)


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