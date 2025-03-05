from .decorators import login_required
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .forms import *
from formtools.wizard.views import SessionWizardView
from django.db.models import Q
from django.db import transaction
from .utils import *
import csv
from django.http import HttpResponse
from django.contrib.auth import get_user_model 
from datetime import datetime


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
def universities_update_view(request, university_id):
    university = get_object_or_404(University, admins=request.user, id=university_id)
    
    if request.POST:
        form = UniversityForm(request.POST or None, request.FILES, instance=university)
        form_admin = AddEmailForm(request.POST or None)
        

        if 'form' in request.POST and form.is_valid():
            form.save()
            return redirect('/universities')
        
        if 'form_admin' in request.POST and form_admin.is_valid():
            email = form_admin.cleaned_data['email']
            user = getUserOrCreate(email)

            university.admins.add(user)
            university.save()
            return redirect('/universities')
    else:
        form = UniversityForm(instance=university)
        form_admin = AddEmailForm()
        
    context = {
        'form': form,
        'form_admin': form_admin,
        'admins': university.admins.all(),
        'university': university

    }
    return render(request, 'class_attendance/universities_update.html', context)

@login_required
def remove_admin_university_view(request, university_id, user_id):
    university = get_object_or_404(University, admins=request.user, id=university_id)
    UserModel = get_user_model()
    user = get_object_or_404(UserModel, id=user_id)
    if user == request.user:
        # the user can't remove himself
        return redirect('/universities')
    university.admins.remove(user)
    university.save()
    return redirect('/universities')


@login_required
def universities_create_view(request):
    form = UniversityForm(request.POST or None, request.FILES)
    if form.is_valid():
        with transaction.atomic():
            university = form.save(commit=False)
            university.save()
            university.admins.add(request.user)
        return redirect('/universities')

    context = {'form': form}
    return render(request, 'class_attendance/universities_create.html', context)

@login_required
def courses_view(request, university_id):
    # show courses where the user is a professor or one of the university's admins
    university = get_object_or_404(
        University.objects.filter(Q(admins=request.user) | Q(courses__professors=request.user)).distinct(),
        id=university_id
    )

    is_admin = university.admins.filter(id=request.user.id).exists()

    search = request.GET.get('search', '')

    if search:
        courses = Course.objects.filter(university=university).filter(
            Q(professors=request.user) | Q(university__admins=request.user)
        ).filter(
            Q(label__icontains=search)
        ).distinct()
    else:
        courses = Course.objects.filter(university=university).filter(
            Q(professors=request.user) | Q(university__admins=request.user)
        ).distinct()
    context = {
        "courses": courses,
        "university": university,
        "is_admin": is_admin
    }

    return render(request, "class_attendance/courses.html" , context)

@login_required 
def courses_create_view(request,university_id):
    university = get_object_or_404(University, admins=request.user, id=university_id)

    form = CourseForm(request.POST or None)
    if form.is_valid():
        course = form.save(commit=False)
        course.university = university
        course.save()
        return redirect(f'/universities/{university_id}/courses')

    context = {'form': form}
    return render(request, 'class_attendance/courses_create.html', context)

@login_required
def courses_update_view(request,university_id, course_id):
    university = get_object_or_404(University, admins=request.user, id=university_id)
    course = get_object_or_404(Course, university=university, id=course_id)
    
    if request.POST:
        form = CourseForm(request.POST or None, request.FILES, instance=course)
        form_email = AddEmailForm(request.POST or None)
        

        if 'form' in request.POST and form.is_valid():
            form.save()
            return redirect(f'/universities/{university_id}/courses')
        
        if 'form_admin' in request.POST and form_email.is_valid():
            email = form_email.cleaned_data['email']
            user = getUserOrCreate(email)
            course.professors.add(user)
            return redirect(f'/universities/{university_id}/courses')
    else:
        form = CourseForm(instance=course)
        form_email = AddEmailForm()
        
    context = {
        'form': form,
        'form_admin': form_email,
        'professors': course.professors.all(),
        'course': course,
        'university': university
    }
    return render(request, 'class_attendance/courses_update.html', context)

@login_required
def remove_professor_course_view(request, university_id, course_id, user_id):
    university = get_object_or_404(University, admins=request.user, id=university_id)
    course = get_object_or_404(Course, university=university, id=course_id)
    UserModel = get_user_model()
    user = get_object_or_404(UserModel, id=user_id)
    course.professors.remove(user)
    course.save()
    return redirect(f'/universities/{university_id}/courses')

@login_required
def school_classes_view(request,course_id):
    course = get_object_or_404(
        Course.objects.filter(Q(professors=request.user) | Q(university__admins=request.user)).distinct(),
        id=course_id
    )
    user = request.user
    filter_professor = request.GET.get('filter_professor', 'true').lower() == 'true'
    search = request.GET.get('search', '')

    if search:
        if filter_professor:
            school_classes = SchoolClass.objects.filter(
                course=course,
                professor=user
            ).filter(
                Q(label__icontains=search) | Q(class_id__icontains=search)
            )
        else:
            school_classes = SchoolClass.objects.filter(course=course).filter(
                Q(label__icontains=search) | Q(class_id__icontains=search)
            )
    else:
        if filter_professor:
            school_classes = SchoolClass.objects.filter(course=course, professor=user)
        else:
            school_classes = SchoolClass.objects.filter(course=course)


    university = course.university

    context = {
        "course": course,
        "school_classes": school_classes,
        "user": request.user,
        "university": university,
        "filter_professor": filter_professor,
    }

    return render(request, "class_attendance/school_classes.html", context)

@login_required
def school_classes_create_view(request, course_id):
    course = get_object_or_404(
        Course.objects.filter(Q(professors=request.user) | Q(university__admins=request.user)).distinct(),
        id=course_id
    )

    initial_data = {'email_professor': request.user.email, 'year': datetime.now().year}
    form = SchoolClassForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        with transaction.atomic():
            school_class = form.save(commit=False)
            school_class.course = course
            user = getUserOrCreate(form.cleaned_data['email_professor'])
            school_class.professor = user
            school_class.save()
            if user not in course.professors.all():
                course.professors.add(user)
                course.save()
        return redirect(f'/courses/{course_id}/school-classes')

    context = {'form': form}
    return render(request, 'class_attendance/school_classes_create.html', context)

@login_required
def school_classes_update_view(request, course_id, school_class_id):
    course = get_object_or_404(
        Course.objects.filter(Q(professors=request.user) | Q(university__admins=request.user)).distinct(),
        id=course_id
    )
    school_class = get_object_or_404(course.classes.all(), id=school_class_id)
    
    if request.POST:
        form = SchoolClassForm(request.POST or None, instance=school_class)
        
        if form.is_valid():
            with transaction.atomic():
                school_class = form.save(commit=False)
                user = getUserOrCreate(form.cleaned_data['email_professor'])
                school_class.professor = user
                school_class.save()
                if user not in course.professors.all():
                    course.professors.add(user)
                    course.save()
            return redirect(f'/courses/{course_id}/school-classes')
    else:
        initial_data = {'email_professor':school_class.professor}
        form = SchoolClassForm(instance=school_class, initial=initial_data)
        
    context = {
        'form': form,
        'school_class': school_class,
        'course': course
    }
    return render(request, 'class_attendance/school_classes_update.html', context)

@login_required
def sessions_view(request, course_id,school_class_id):
    course = get_object_or_404(
        Course.objects.filter(Q(professors=request.user) | Q(university__admins=request.user)).distinct(),
        id=course_id
    )
    school_class = get_object_or_404(course.classes.all(), id=school_class_id)


    context = {
        "course": course,
        "school_class": school_class,
        "sessions": school_class.sessions.all().order_by("-open_time"),
        "university": course.university 
    }
    return render(request, "class_attendance/sessions.html", context)


@login_required
def download_course_report_view(request, course_id):
    course = get_object_or_404(
        Course.objects.filter(professors=request.user),
        id=course_id
    )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="report_{course.label.replace(" ", "_")}.csv"'

    writer = csv.writer(response)
    school_classes = course.classes.all()

    actual_sessions = Session.objects.filter(school_class__in=school_classes).order_by("open_time")
    
    class_sessions = {}
    class_session_counts = {}
    
    for session in actual_sessions:
        if session.school_class.id not in class_sessions:
            class_sessions[session.school_class.id] = []
            class_session_counts[session.school_class.id] = 0
        
        class_session_counts[session.school_class.id] += 1
        
        class_sessions[session.school_class.id].append({
            'session': session,
            'session_number': class_session_counts[session.school_class.id]
        })
    
    max_sessions = max(class_session_counts.values()) if class_session_counts else 0
    
    expected_sessions = []
    
    for school_class in school_classes:
        class_count = class_session_counts.get(school_class.id, 0)
        if class_count < max_sessions:
            for session_number in range(class_count + 1, max_sessions + 1):
                reference_date = None
                for other_class_id, sessions in class_sessions.items():
                    for s in sessions:
                        if s['session_number'] == session_number:
                            reference_date = s['session'].open_time.date()
                            break
                    if reference_date:
                        break
                
                if not reference_date and actual_sessions:
                    reference_date = actual_sessions.last().open_time.date()
                
                expected_sessions.append({
                    'school_class': school_class,
                    'session_number': session_number,
                    'expected_date': reference_date,
                    'is_missing': True
                })
    
    all_sessions = []
    
    for class_id, sessions in class_sessions.items():
        for session_info in sessions:
            all_sessions.append({
                'session': session_info['session'],
                'school_class': session_info['session'].school_class,
                'date': session_info['session'].open_time.date(),
                'session_number': session_info['session_number'],
                'is_missing': False
            })
    
    for expected in expected_sessions:
        all_sessions.append({
            'session': None,
            'school_class': expected['school_class'],
            'date': expected['expected_date'],
            'session_number': expected['session_number'],
            'is_missing': True
        })
    
    all_sessions.sort(key=lambda x: (x['date'], x['session_number'], x['school_class'].class_id or ""))

    header = ["Student Number", "Name", "Attendance Count"]
    for session_info in all_sessions:
        school_class = session_info['school_class']
        session_num = session_info['session_number']
        date_str = session_info['date'].strftime('%Y-%m-%d') if session_info['date'] else "N/A"
        
        if session_info['is_missing']:
            header.append(f"{school_class.class_id or 'NA'} - Week {session_num} - MISSING ({date_str})")
        else:
            session = session_info['session']
            header.append(f"{school_class.class_id or 'NA'} - Week {session_num} ({date_str})")
    
    writer.writerow(header)

    students = Student.objects.filter(session__school_class__course=course).distinct()

    for student in students:
        attended_count = 0
        total_sessions = 0
        
        for session_info in all_sessions:
            if not session_info['is_missing']:
                total_sessions += 1
                if session_info['session'].students.filter(id=student.id).exists():
                    attended_count += 1
        
        attendance_rate = f"{attended_count}"
        
        row = [student.number, f"{student.first_name} {student.last_name}", attendance_rate]
        
        for session_info in all_sessions:
            if session_info['is_missing']:
                row.append("N/A")
            else:
                row.append("X" if session_info['session'].students.filter(id=student.id).exists() else "")
        
        writer.writerow(row)
    return response


@login_required
def download_school_class_report_view(request, course_id, school_class_id):
    school_class = get_object_or_404(
        SchoolClass.objects.filter(course__professors=request.user).distinct(),
        id=school_class_id
    )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="report_{school_class.class_id}.csv"'

    writer = csv.writer(response)
    sessions = school_class.sessions.all().order_by("open_time")
    header = ["Student Number"] + ["Name"] + [session.open_time for session in sessions]
    writer.writerow(header)

    students = Student.objects.filter(session__school_class=school_class).distinct()
    for student in students:
        row = [student.number, f"{student.first_name} {student.last_name}"]  
        for session in sessions:
            row.append("X" if session.students.filter(id=student.id).exists() else "")
        writer.writerow(row)

    return response



@login_required
def presentation_session_view(request, session_uuid):
    session = get_object_or_404(Session, uuid=session_uuid)

    if not session.is_active:
        context = {
            "session": session,
            "students": session.students.all(),
            "course": session.school_class.course,
            "school_class": session.school_class,
            "university": session.school_class.course.university
        }
        return render(request, "class_attendance/session_students.html", context)
    
    current_url = request.build_absolute_uri().replace("presentation", "join")
    context = {
        "session": session,
        "join_url": current_url,
        "otp_interval": settings.OTP_INTERVAL,
        "course": session.school_class.course,
        "school_class": session.school_class,   
        "university": session.school_class.course.university  
    }

    return render(request, "class_attendance/presentation_session.html", context)

@login_required
def host_session_view(request, session_uuid):
    session = get_object_or_404(Session, uuid=session_uuid)
    
    current_url = request.build_absolute_uri().replace("presentation", "join")
    context = {
        "session": session,
        "students": session.students.all(),
        "join_url": current_url,
        "otp_interval": settings.OTP_INTERVAL,
        "course": session.school_class.course,
        "school_class": session.school_class,   
        "university": session.school_class.course.university  
    }

    return render(request, "class_attendance/session_students.html", context)


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

    def dispatch(self, request, *args, **kwargs):
        session = get_object_or_404(Session, uuid=kwargs.get("session_uuid"))
        if not session.is_active:
            return render(request, "class_attendance/session_closed.html")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step == "code" or step == "student_number": 
            session = get_object_or_404(Session, uuid=self.kwargs.get("session_uuid"))
            kwargs.update({"session": session, "university": session.school_class.course.university})
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
                university=University.objects.get(courses__classes__sessions__uuid=self.kwargs.get("session_uuid"))
            )

        session = get_object_or_404(Session, uuid=self.kwargs.get("session_uuid"))
        if not session.is_active:
            return render(self.request, "class_attendance/session_closed.html")
        
        session.students.add(student)
        session.save()

        return render(self.request, "class_attendance/done.html", {"form_data": form_data})
    

@login_required
def history_sessions_view(request):
    sessions = Session.objects.filter(school_class__course__professors=request.user).order_by("-open_time")[:50]
    context = {
        "sessions": sessions
    }
    return render(request, "class_attendance/history_sessions.html", context)