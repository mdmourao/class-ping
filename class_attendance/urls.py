from django.urls import path
from .views import *
from .api import api
from .forms import *

app_name = "class_attendance"

urlpatterns = [
    path("", universities_view, name="universities"),
    path("universities", universities_view, name="universities"),
    path("universities/create", universities_create_view, name="universities-create"),
    path("universities/<int:university_id>/update", universities_update_view, name="universities-update"),

    path("universities/<int:university_id>/admins/<int:user_id>/remove", remove_admin_university_view, name="universities-admins-remove"),

    path("universities/<int:university_id>/courses", courses_view, name="courses"),
    path("universities/<int:university_id>/courses/create", courses_create_view, name="courses-create"),
    path("universities/<int:university_id>/courses/<int:course_id>/update", courses_update_view, name="courses-update"),
    path("universities/<int:university_id>/courses/<int:course_id>/professors/<int:user_id>/remove", remove_professor_course_view, name="courses-professors-remove"),

    path("courses/<int:course_id>/download-report", download_course_report_view, name="download-report-course"),

    path("courses/<int:course_id>/school-classes", school_classes_view, name="school-classes"),
    path("courses/<int:course_id>/school-classes/create", school_classes_create_view, name="school-classes-create"),
    path("courses/<int:course_id>/school-classes/<int:school_class_id>/update", school_classes_update_view, name="school-classes-update"),
    path("courses/<int:course_id>/school-classes/<int:school_class_id>/sessions", sessions_view, name="sessions"),
    path("courses/<int:course_id>/school-classes/<int:school_class_id>/download-report", download_school_class_report_view, name="download-report-school-class"),
    

    path("sessions/<uuid:session_uuid>/presentation", presentation_session_view, name="session-presentation"),
    path("sessions/<uuid:session_uuid>/host", host_session_view, name="session-host"),

    path("sessions/<uuid:session_uuid>/join", JoinSessionView.as_view(), name="session-join"),


    path("sessions/history", history_sessions_view, name="history_sessions"),

    path("404", view_404, name="404"),

    path("api/", api.urls),
]