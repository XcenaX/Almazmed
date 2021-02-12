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

workbook = xlrd.open_workbook('example.xls')
worksheet = workbook.sheet_by_index(0)

CITY_NAME = "Павлодар"
city = City.objects.filter(name=CITY_NAME).first()
branch = Branch.objects.filter(city=city).first()

y = 0

while(worksheet.cell(y,0).value != xlrd.empty_cell.value):
    code = worksheet.cell(y,0).value
    name = worksheet.cell(y,1).value
    count = worksheet.cell(y,2).value
    int_count = int(count.split(" ")[0])
    price = worksheet.cell(y,3).value
    sub_services = []
    j = 4
    try:
        while(True):
            sub_services.append(worksheet.cell(y,j).value)
            j+=1
    except:
        pass
    
    length = len(sub_services)
    for i in range(0,length):
        service = ServiceType.objects.filter(name=sub_services[i]).first()
        if not service:
            if(i == 0):
                service = ServiceType.objects.create(name=sub_services[i], is_top=True, branch=branch)
            else:
                service = ServiceType.objects.create(name=sub_services[i], is_top=False, branch=branch)
        
        if(i > 0):
            previous_name = sub_services[i-1]
            previous = ServiceType.objects.filter(name=previous_name).first()
            previous.services_types.add(service)
        if(i == length - 1):
            service.services.add(Service.objects.create(name=name,price=int(price),count=int_count,code=code))
    y += 1
    break
    
        
