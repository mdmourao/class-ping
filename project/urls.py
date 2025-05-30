from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
import os
from class_attendance.api import api

urlpatterns = [
    path("class_attendance/", include("class_attendance.urls", namespace="class_attendance")),
    path("authentication/", include("authentication.urls")),
    path("", include("landing_page.urls")),
    path("qr-code/", include("qr_code.urls", namespace="qr_code")),
    path('accounts/', include('allauth.urls')),
    path("api/", api.urls, name="api"),
]

if os.getenv("DEBUG") == "True":
    urlpatterns += [
        path("admin/", admin.site.urls),
    ]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root= settings.MEDIA_ROOT,
)

handler404 = 'class_attendance.views.error_view'
handler500 = 'class_attendance.views.error_view'
