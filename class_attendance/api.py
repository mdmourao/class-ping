from ninja import NinjaAPI
from django.shortcuts import get_object_or_404
import pyotp, uuid
from .decorators import login_required
from .models import *
from django.db.models import Q
import json

api = NinjaAPI()

@api.api_operation(["HEAD", "GET"], "/")
def index(request):
    return {"success": "Ok"}

@api.api_operation(["HEAD", "GET"], "/ping")
def index(request):
    return {"ping": "pong"}

@login_required
@api.post("/courses/{course_id}/school-classes/{school_class_id}/sessions/create")
def create_session(request, course_id, school_class_id):
    course = get_object_or_404(
        Course.objects.filter(Q(professors=request.user) | Q(university__admins=request.user)).distinct(),
        id=course_id
    )
    school_class = get_object_or_404(SchoolClass, course=course, id=school_class_id)

    session = Session(
        uuid=str(uuid.uuid4()),
        school_class=school_class,
        secret=pyotp.random_base32(),
        opened_by=request.user
    )
    session.save()

    # close all other sessions
    school_class.sessions.filter(is_active=True).exclude(uuid=session.uuid).update(is_active=False)

    return {"success": True, "session_uuid": session.uuid}


@login_required
@api.get("/sessions/{session_uuid}/students")
def get_students(request, session_uuid: str):
    session = get_object_or_404(
        Session.objects.filter(Q(school_class__course__professors=request.user) | Q(school_class__course__university__admins=request.user)).distinct(),
        uuid=session_uuid
    )

    students = session.students.all()
    student_details = [{"first_name": student.first_name, "last_name": student.last_name, "number": student.number} for student in students]

    for i, student in enumerate(students):
        student_details[i]["joined_at"] = session.sessionstudent_set.get(student=student).joined_at

    return {"students": student_details}

@login_required
@api.put("/sessions/{session_uuid}/status")
def update_session_status(request, session_uuid: str):
    session = get_object_or_404(
        Session.objects.filter(Q(school_class__course__professors=request.user) | Q(school_class__course__university__admins=request.user)).distinct(),
        uuid=session_uuid
    )

    session.is_active = not session.is_active
    session.save()

    return {"success": True}


@login_required
@api.delete("/sessions/{session_uuid}/delete")
def delete_session(request, session_uuid: str):
    session = get_object_or_404(
        Session.objects.filter(Q(school_class__course__professors=request.user) | Q(school_class__course__university__admins=request.user)).distinct(),
        uuid=session_uuid
    ) 
    # dont delete the session, just remove the school_class...
    session.school_class = None
    session.save()
    return {"success": True}


@login_required
@api.patch("/students/{student_number}")
def update_student(request, student_number: str):
    print(student_number)
    student = get_object_or_404(Student, number=student_number)

    if not student.sessionstudent_set.filter(session__school_class__course__professors=request.user).exists() or not student.university.admins.filter(id=request.user.id).exists():
        return {"success": False, "error": "Student not found."}, 404

    body = request.body
    if isinstance(body, bytes):
        body = body.decode("utf-8")
    data = json.loads(body)

    if 'first_name' in data:
        student.first_name = data['first_name']
    if 'last_name' in data:
        student.last_name = data['last_name']
    
    student.save()
    return {"success": True}

@login_required
@api.delete("/sessions/{session_uuid}/students/{student_number}")
def remove_student(request, session_uuid: str, student_number: str):
    session = get_object_or_404(
        Session.objects.filter(Q(school_class__course__professors=request.user) | Q(school_class__course__university__admins=request.user)).distinct(),
        uuid=session_uuid
    )

    student = get_object_or_404(Student, number=student_number)
    session.students.remove(student)
    return {"success": True}
