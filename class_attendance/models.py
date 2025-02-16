from django.db import models
from django.conf import settings

class University(models.Model):
    label = models.CharField(max_length=50)
    image = models.ImageField(upload_to='university_images/')
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="universities")

    def __str__(self):
        return self.label


class SchoolClass(models.Model):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6
    
    WEEKDAY_CHOICES = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    ]

    label = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    
    is_archived = models.BooleanField(default=False)
    year = models.IntegerField()
    semester = models.IntegerField()
    class_id = models.CharField(max_length=50, blank=True, null=True)

    professor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="classes")
    course = models.ForeignKey('Course', on_delete=models.PROTECT, related_name="classes")
    
    def __str__(self):
        return self.label

class Course(models.Model):
    label = models.CharField(max_length=50)

    professors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="courses")
    university = models.ForeignKey(University, on_delete=models.PROTECT, related_name="courses")

    def __str__(self):
        return self.label

class Student(models.Model):
    number = models.IntegerField()
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)

    university = models.ForeignKey(University, on_delete=models.PROTECT, related_name="students")

    def __str__(self):
        return f"{self.number}: {self.first_name}"

class Session(models.Model):
    uuid = models.UUIDField()
    open_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    secret = models.CharField(max_length=200)
    opened_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="sessions")
    
    students = models.ManyToManyField(Student, through='SessionStudent')
    school_class = models.ForeignKey(SchoolClass, on_delete=models.PROTECT, related_name="sessions")

    def __str__(self):
        return f"Session at {self.open_time}"

class SessionStudent(models.Model):
    session = models.ForeignKey(Session, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} joined {self.session} at {self.joined_at}"

