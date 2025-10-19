from django.db import transaction
import requests
import re
import logging
from .models import *
from django.contrib.auth import get_user_model 
import os
import csv

logger = logging.getLogger(__name__)

UNIVERSITY_ID = 37

def load_data():
    UserModel = get_user_model()
    with open('file.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
                with transaction.atomic():
                    name = lines[0][:50]
                    email = lines[1]
                    
                    courseIdentity = Course.objects.get_or_create(
                            label=name, 
                            university_id=UNIVERSITY_ID
                        )[0]

                    
                    profIdentity = UserModel.objects.get_or_create(email=email)[0]
                    courseIdentity.professors.add(profIdentity)
                    courseIdentity.save()


def populate():
    UserModel = get_user_model()
    data = load_data()
    