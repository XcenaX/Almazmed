import os, sys, time
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','almazmed.settings')
django.setup()

from main.models import *
from datetime import datetime
import time

# for service in Service.objects.all():
#     service.delete()

# for service in Service.objects.all():
#     service.delete()

#current_service_type = ServiceType.objects.get(id=143)

consult = ServiceType.objects.get(id=191)
free_consult = ServiceType.objects.get(id=302)

for item in consult.services_types.all():
    item_services = item.services.all()
    item.pk=None
    item.save()
    for service in item_services:
        service.pk=None
        service.save()
        service.price = 0
        service.save()
        item.services.add(service)
    free_consult.services_types.add(item)


