from django.db import transaction
import requests
import re
from .models import *
from django.contrib.auth import get_user_model 
import os

UNIVERSITY_ID = int(os.getenv("UNIVERSITY_ID_LOADER"))
URL = os.getenv("URL_LOADER")

def load_data():
    response = requests.get(URL)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    

def populate():
    UserModel = get_user_model()
    data = load_data()
    for course in data:
        with transaction.atomic():
            courseIdentity = Course.objects.get_or_create(label=course, university_id=UNIVERSITY_ID)[0]

            for prof in data[course]:
                nome = prof['nome']
                numero = prof['numero']
                
                if not re.match(r'^p\d{4}$', numero):
                    continue
                    
                email = f"{numero}@ulusofona.pt"

                profIdentity = UserModel.objects.get_or_create(email=email)[0]

                first_name, last_name = nome.split(" ", 1)
                profIdentity.first_name = first_name
                profIdentity.last_name = last_name

                profIdentity.save()
                courseIdentity.professors.add(profIdentity)
                courseIdentity.save()
                print(f"Professor {profIdentity} added to course {courseIdentity}")
