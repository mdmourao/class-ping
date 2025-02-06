from django.db import models
from django.contrib.auth.models import User

class University(models.Model):
    label = models.CharField(max_length=50)
    image = models.ImageField(upload_to='university_images/')
    admins = models.ManyToManyField(User, related_name="universities")

    def __str__(self):
        return self.label


class SchoolClass(models.Model):
    label = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_archived = models.BooleanField(default=False)
    year = models.IntegerField()
    semester = models.IntegerField()

    professor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="classes")
    course = models.ForeignKey('Course', on_delete=models.PROTECT, related_name="classes")
    
    def __str__(self):
        return self.label

class Course(models.Model):
    label = models.CharField(max_length=50)

    professors = models.ManyToManyField(User, related_name="courses")
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

