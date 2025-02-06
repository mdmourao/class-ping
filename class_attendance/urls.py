from django.urls import path, re_path
from .views import *
from .api import api
from .forms import *

app_name = "class_attendance"

urlpatterns = [
    path("universities", universities_view, name="universities"),
    path("universities/new", universities_new_view, name="universities-new"),
    path("universities/<int:university_id>/edit", universities_edit_view, name="universities-edit"),

    path("universities/<int:university_id>/admins/<int:user_id>/delete", remove_admin_university_view, name="universities-admins-delete"),

    path("universities/<int:university_id>/courses", courses_view, name="courses"),
    path("universities/<int:university_id>/courses/new", courses_new_view, name="courses-new"),
    path("universities/<int:university_id>/courses/<int:course_id>/edit", courses_edit_view, name="courses-edit"),
    path("universities/<int:university_id>/courses/<int:course_id>/professors/<int:user_id>/delete", remove_professor_course_view, name="courses-professors-delete"),


    path("courses/<int:course_id>/school-classes", school_classes_view, name="school-classes"),
    path("courses/<int:course_id>/school-classes/new", school_classes_new_view, name="school-classes-new"),
    path("courses/<int:course_id>/school-classes/<int:school_class_id>/edit", school_classes_edit_view, name="school-classes-edit"),
    path("courses/<int:course_id>/school-classes/<int:school_class_id>/sessions", sessions_view, name="sessions"),

    path("sessions/<uuid:session_uuid>/presentation", presentation_session_view, name="session-presentation"),
    path("sessions/<uuid:session_uuid>/join", JoinSessionView.as_view(), name="session-join"),

    path("api/", api.urls),
]