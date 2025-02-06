from django.urls import path, re_path
from .views import *
from .api import api
from .forms import *

app_name = "class_attendance"

urlpatterns = [
    path("", courses_view, name="courses"),

    path("universities", universities_view, name="universities"),
    path("universities/edit", universities_edit_view, name="universities-edit"),

    path("courses", courses_view, name="courses"),
    path("courses/new", courses_new_view, name="courses-new"),
    path("courses/<int:course_id>/edit", courses_edit_view, name="courses-edit"),

    path("courses/<int:course_id>/school-classes", school_classes_view, name="school-classes"),
    path("courses/<int:course_id>/school-classes/new", school_classes_new_view, name="school-classes-new"),
    path("courses/<int:course_id>/school-classes/<int:school_class_id>/edit", school_classes_edit_view, name="school-classes-edit"),
    path("courses/<int:course_id>/school-classes/<int:school_class_id>/sessions", sessions_view, name="sessions"),

    path("sessions/<uuid:session_uuid>/presentation", presentation_session_view, name="session-presentation"),
    path("sessions/<uuid:session_uuid>/join", JoinSessionView.as_view(), name="session-join"),

    path("api/", api.urls),
]