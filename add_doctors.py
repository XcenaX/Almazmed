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
    main_service_types = ServiceType.objects.filter(branch=branch, is_top=True)
    y = 0
    try:
        while(True):
            name = worksheet.cell(y,0).value
            sub_services = []
            j = 2
            try:
                while(True):
                    sub_services.append(worksheet.cell(y,j).value)
                    j+=1
            except:
                pass

            doctors = []
            j = 4
            try:
                while(True):
                    doctor_name = worksheet.cell(y,j).value
                    doctor = Doctor.objects.filter(fullname=doctor_name, branch=branch).first()
                    if doctor:
                        doctors.append(doctor)
                    j+=1
            except:
                pass
            for main_service in main_service_types:
                s1 = main_service.services_types.filter(name=sub_services[0]).first()
                if not s1:
                    print("Не найдено!" + " | " + sub_services[0])                    
                    continue
                s2 = s1.services_types.all().filter(name=sub_services[1]).first()
                if not s2:
                    print("Не найдено!" + " | " + sub_services[1])                    
                    continue
                service = s2.services.all().filter(name=name).first()
                if not service:   
                    continue
                print(service.name + " | " + str(len(doctors)))
                for doctor in doctors:
                    service.doctors.add(doctor)
                service.save()
            y += 1
    except Exception as error:
        print(error)

    
        
