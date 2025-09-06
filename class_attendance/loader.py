from django.db import transaction
import requests
import re
import logging
from .models import *
from django.contrib.auth import get_user_model 
import os

logger = logging.getLogger(__name__)

UNIVERSITY_ID_ENV = os.getenv("UNIVERSITY_ID_LOADER")
if not UNIVERSITY_ID_ENV:
    raise ValueError("UNIVERSITY_ID_LOADER environment variable is not set or empty")
UNIVERSITY_ID = int(UNIVERSITY_ID_ENV)

URL = os.getenv("URL_LOADER")
if not URL:
    raise ValueError("URL_LOADER environment variable is not set or empty")

def load_data():
    response = requests.get(URL)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    

def populate():
    UserModel = get_user_model()
    data = load_data()
    
    if 'disciplinas' not in data:
        logger.error("Invalid data format: 'disciplinas' key not found")
        return
    
    for disciplina in data['disciplinas']:
        with transaction.atomic():
            name = disciplina['name']

            courseIdentity = Course.objects.get_or_create(
                    label=name, 
                    university_id=UNIVERSITY_ID
                )[0]

            archive_school_classes_by_course(courseIdentity)
            courseIdentity.professors.clear()
            courseIdentity.save()

            for teacher in disciplina.get('teachers', []):
                email = teacher['email']
                nome = teacher['nome']
                
                if not email.endswith('@ulusofona.pt'):
                    logger.warning(f"Teacher has email {email} which does not end with @ulusofona.pt")
                
                profIdentity = UserModel.objects.get_or_create(email=email)[0]

                first_name, last_name = nome.split(" ", 1)
                profIdentity.first_name = first_name
                profIdentity.last_name = last_name

                profIdentity.save()
                courseIdentity.professors.add(profIdentity)
                courseIdentity.save()


def archive_school_classes_by_course(course_identity):
    try:
        with transaction.atomic():
            school_classes = SchoolClass.objects.filter(
                course=course_identity,
                is_archived=False
            )
            
            archived_count = school_classes.count()
            
            school_classes.update(is_archived=True)
            
            logger.info(f"Archived {archived_count} school classes for course: {course_identity.label}")
            return archived_count
            
    except Exception as e:
        logger.error(f"Error archiving school classes for course {course_identity}: {str(e)}")
        raise
