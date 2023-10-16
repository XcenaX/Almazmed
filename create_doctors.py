import os, sys, time
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','almazmed.settings')
django.setup()

from main.models import *
from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup as BS
import time
from django.utils import timezone
import xlrd

# for service in Service.objects.all():
#     service.delete()

# for service in Service.objects.all():
#     service.delete()


workbook = xlrd.open_workbook('taraz_doctors.xls')
worksheet = workbook.sheet_by_index(0)
#Тараз
CITY_NAME = "Тараз"
city = City.objects.filter(name=CITY_NAME).first()



if not city:
    print("Нет города")
else:
    branch = Branch.objects.filter(city=city).first()
    #main_service_types = ServiceType.objects.filter(branch=branch, is_top=True)
    y = 0
    try:
        while(True):       
            activity_name = worksheet.cell(y,2).value
            position_name = worksheet.cell(y,3).value
            position = Position.objects.filter(name=position_name).first()
            if not position:
                position = Position.objects.create(name=position_name)
                position.save()

            activity = DirectionOfActivity.objects.filter(name=activity_name).first()
            if not activity:
                activity = DirectionOfActivity.objects.create(name=activity_name)
                activity.save()

            doctors = []
            j = 4
            try:
                while(True):
                    doctor_name = worksheet.cell(y,j).value
                    doctor = Doctor.objects.filter(fullname=doctor_name, branch=branch).first()
                    if not doctor:
                        doctor = Doctor.objects.create(fullname=doctor_name, branch=branch, position=position, direction_of_activity=activity)                
                        doctor.save()
                    j+=1
            except:
                pass
            
            

            y += 1
    except Exception as error:
        print(error)

    
        
