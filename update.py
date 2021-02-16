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


workbook = xlrd.open_workbook('example.xls')
worksheet = workbook.sheet_by_index(0)

CITY_NAME = "Тараз"
city = City.objects.filter(name=CITY_NAME).first()
branch = Branch.objects.filter(city=city).first()

y = 0
try:
    while(True):
        name = worksheet.cell(y,0).value
        count = 1
        print(name)
        
        price = worksheet.cell(y,2).value
        try:
            price = int(price)
        except:
            price = 0
        sub_services = []
        j = 3
        try:
            while(True):
                sub_services.append(worksheet.cell(y,j).value)
                j+=1
        except:
            pass
        
        length = len(sub_services)
        for i in range(0,length):
            service_name = sub_services[i]
            if not service_name:
                previous_name = sub_services[i-1]
                if not previous_name:
                    continue 
                previous = ServiceType.objects.filter(name=previous_name).first()
                if not previous:
                    previous = ServiceType.objects.create(name=previous_name, is_top=True)
                previous.services.add(Service.objects.create(name=name,price=int(price),count=count))
                continue
            
            

            print(service_name + " | " + str(len(service_name)))
            if service_name == " ":
                continue
            service = ServiceType.objects.filter(name=service_name).first()
            if not service:
                if(i == 0):
                    service = ServiceType.objects.create(name=service_name, is_top=True, branch=branch)
                else:
                    service = ServiceType.objects.create(name=service_name, is_top=False, branch=branch)
            
            if(i > 0):
                previous_name = sub_services[i-1]
                previous = ServiceType.objects.filter(name=previous_name).first()
                previous.services_types.add(service)
            if(i == length - 1):
                service.services.add(Service.objects.create(name=name,price=int(price),count=count))
        y += 1
except Exception as error:
    print(error)

    
        
