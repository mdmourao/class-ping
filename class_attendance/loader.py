from django.db import transaction
import logging
from .models import *
from django.contrib.auth import get_user_model 
import csv

logger = logging.getLogger(__name__)

def load_data(university_id):
    UserModel = get_user_model(university_id)
    with open('file.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
                with transaction.atomic():
                    name = lines[0][:50]
                    email = lines[1]
                    
                    courseIdentity = Course.objects.get_or_create(
                            label=name, 
                            university_id=university_id
                        )[0]

                    
                    profIdentity = UserModel.objects.get_or_create(email=email)[0]
                    courseIdentity.professors.add(profIdentity)
                    courseIdentity.save()


def archive(university_id):
    try:
        courses = Course.objects.filter(university_id=university_id)
        total_archived = 0
        
        for course in courses:
            school_classes = SchoolClass.objects.filter(
                course=course,
                is_archived=False
            )
            archived_count = school_classes.count()
            # school_classes.update(is_archived=True)
            total_archived += archived_count
            logger.info(f"Archived {archived_count} school classes for course: {course.label}")
        
        logger.info(f"Total archived: {total_archived} school classes for university ID: {university_id}")
        return total_archived
            
    except Exception as e:
        logger.error(f"Error archiving school classes for university {university_id}: {str(e)}")
        raise
    