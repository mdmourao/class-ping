from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("class_attendance/", include("class_attendance.urls", namespace="class_attendance")),
    path("authentication/", include("authentication.urls")),
    path("", include("class_attendance.urls",  namespace="class_attendance_root")),
    path("qr-code/", include("qr_code.urls", namespace="qr_code")),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root= settings.MEDIA_ROOT,
)