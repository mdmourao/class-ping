from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("class_attendance/", include("class_attendance.urls")),
    path("authentication/", include("authentication.urls")),
    path("", include("class_attendance.urls")),
]
