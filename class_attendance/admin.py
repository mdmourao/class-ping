from django.contrib import admin 
from .models import *

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(SchoolClass)
admin.site.register(Session)
admin.site.register(SessionStudent)

