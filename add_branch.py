import os, sys, time
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','almazmed.settings')
django.setup()

from main.models import *

for branch in Branch.objects.all():
    for service_type in ServiceType.objects.filter(branch=branch):
        for service in service_type.services.all():
            service.branch = branch
            service.save()
