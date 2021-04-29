from django.shortcuts import render

#from .forms import UserForm, CommentForm, BlogForm
from .models import *

from django.shortcuts import redirect
from django.urls import reverse

#from .modules.hashutils import check_pw_hash, make_pw_hash

#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils import timezone

#import smtplib, ssl

#from .modules.sendEmail import send_email
import itertools
from django.http import HttpResponse, JsonResponse, Http404

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
#from .tokens import account_activation_token
#from django.core.mail import EmailMessage
from django import template
import os
from django.conf import settings

#from django.db.models import Q
from datetime import datetime
#FUNCTIONS
#from django.template.Library import filter
#from django.utils.translation import gettext
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db.models.functions import Lower

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
COUNT_BLOG_ON_PAGE=50


from django.views.decorators.csrf import csrf_exempt

def get_paginated_blogs(request, paginator):
    page = request.GET.get('page')
    try:
        page = int(page)
    except:
        page = 1
    a = ""
    block = ""
    pages=[]
    if page:
        try:
            block = paginator.page(page)
        except EmptyPage:
            block = paginator.page(paginator.num_pages)
            page = paginator.num_pages

        for i in range(page-2, page+3):
            try:
                a = paginator.page(i)
                pages.append(i)
            except:
                continue
        print(pages)
        if pages[-1] != paginator.num_pages:
            pages.append(paginator.num_pages)

        if pages[0] != 1:
            pages.insert(0, 1)
    else:
        pages = [1,2,3,4,5,paginator.num_pages]
        block = paginator.page(1)
    return block, pages


class make_incrementor(object):
    count = 0

    def __init__(self, start):
        self.count = start

    def inc(self, jump=1):
        self.count += jump
        return self.count

    def res(self):
        self.count = 0
        return self.count

def sort_doctors(city):
    branches = Branch.objects.filter(city=city)
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    all_doctors = []
    for activity in activities:
        doctors = Doctor.objects.filter(direction_of_activity=activity, branch__in=branches)
        if(len(doctors) > 0): 
            all_doctors.append({"activity": activity, "doctors": doctors})
    return all_doctors



def get_parameter(request, name):
    try:
        return request.GET[name]
    except:
        return None 

def post_parameter(request, name):
    try:
        return request.POST[name]
    except:
        return None 

def post_file(request, name):
    try:
        return request.FILES.getlist(name)
    except:
        return None

def session_parameter(request, name):
    try:
        return request.session[name]
    except:
        return None

#VIEWS

def index(request, city):
    news = New.objects.all()[:4]
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    doctors = Doctor.objects.filter(branch__in=branches, has_appointment=True)[:6]
    cities = City.objects.all()
    partners = Partner.objects.all()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    services_types = ServiceType.objects.filter(name__icontains="Бесплатные", branch__in=branches).first()
    free_services_types = None
    if services_types:
        free_services_types = services_types.services_types.all()[0:4]
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    return render(request, "index.html", {
        "news":news,
        "city": current_city,
        "branches": branches,
        "all_branches": Branch.objects.all(),
        "doctors": doctors,
        "cities": cities,
        "partners": partners,
        "activities": activities,
        "leaders": leaders,
        "current_lang": session_parameter(request,"lang"),
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
        "free_services_types": free_services_types,
    })

def about(request, city):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    current_branch = Branch.objects.filter(city=current_city).first()
    cities = City.objects.all()
    
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    return render(request, "about.html", {
        "path": [{"О поликлинике": request.META.get('PATH_INFO', None)}],
        "leaders": leaders,
        "activities": activities,
        "city": current_city,
        "current_branch": current_branch,
        "cities": cities,
        "current_lang": session_parameter(request,"lang"),
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
        "branches": branches,
    })

def specialists(request, city):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    doctors = sort_doctors(current_city)
    cities = City.objects.all()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    return render(request, "specialists.html", {
        "path": [{"Специалисты": request.META.get('PATH_INFO', None)}],
        "activities": activities,
        "doctors": doctors,
        "city": current_city,
        "cities": cities,
        "leaders": leaders,
        "current_lang": session_parameter(request,"lang"),
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
        "branches": branches,
    })

def specialists_activity(request, city, id):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    current_activity = None
    try:
        current_activity = DirectionOfActivity.objects.get(id=id)
    except:
        return redirect(reverse("main:specialists"))
    branches = Branch.objects.filter(city=current_city)
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    doctors = Doctor.objects.filter(direction_of_activity=current_activity, branch__in=branches)
    all_doctors = [{"activity": current_activity, "doctors": doctors}]
    cities = City.objects.all()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    return render(request, "specialists.html", {
        "path": [{"Специалисты": "/"+current_city.en_name+"/specialists"}, {current_activity.name: request.META.get('PATH_INFO', None)}],
        "activities": activities,
        "doctors": all_doctors,
        "current_activity": current_activity,
        "city": current_city,
        "cities": cities,
        "leaders": leaders,
        "current_lang": session_parameter(request,"lang"),
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
        "branches": branches,
    })

def specialist(request, city, id):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    current_doctor = None
    try:
        current_doctor = Doctor.objects.get(id=id)
    except:
        return redirect(reverse("main:index"))
    cities = City.objects.all()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    return render(request, "specialist.html", {
        "path": [{"Специалисты": "/"+current_city.en_name+"/specialists"}, {current_doctor.fullname: request.META.get('PATH_INFO', None)}],
        "activities": activities,
        "current_doctor": current_doctor,
        "city": current_city,
        "cities": cities,
        "leaders": leaders,
        "current_lang": session_parameter(request,"lang"),
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
        "branches": branches,
    })

def sub_uslugi(request, city, id):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    cities = City.objects.all()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    service_type = ServiceType.objects.filter(id=id).first()
    services_types = ServiceType.objects.filter(is_top=True, branch__in=branches)
    parent_service_type = ServiceType.objects.filter(services_types=service_type).first()
    if parent_service_type:
        if not parent_service_type.is_top:
            services_types = parent_service_type.services_types.all()
        else:
            services_types = ServiceType.objects.filter(is_top=True, branch__in=branches)
        parent_service_type2 = ServiceType.objects.filter(services_types=parent_service_type).first()
        if parent_service_type2:
            services_types = parent_service_type2.services_types.all()
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    return render(request, "uslugi-i-tseny.html", {
        "cities": cities,
        "city": current_city,
        "leaders": leaders,
        "activities": activities,
        "current_lang": session_parameter(request,"lang"),
        "service_type": service_type,
        "services_types": services_types,
        "path": [{"Услуги и цены": "/"+current_city.en_name+"/uslugi"}, {service_type.name: request.META.get('PATH_INFO', None)}],
        "branches": branches,
    })

def uslugi(request, city):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    cities = City.objects.all()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    services_types = ServiceType.objects.filter(is_top=True, branch__in=branches)
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    return render(request, "uslugi-i-tseny.html", {
        "path": [{"Услуги и цены": request.META.get('PATH_INFO', None)}],
        "cities": cities,
        "city": current_city,
        "activities": activities,
        "leaders": leaders,  
        "current_lang": session_parameter(request,"lang"),
        "services_types": services_types,
        "branches": branches,
    })

def choose_doctor(request, city, id):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    cities = City.objects.all()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    service = Service.objects.get(id=id)
    service_type = ServiceType.objects.filter(services=service  ).first()
    services_types = ServiceType.objects.filter(services_types=service_type).first().services_types.all()
    print(service.doctors.all())
    return render(request, "choose_doctor.html", {
        "path": [{"Услуги и цены": request.META.get('PATH_INFO', None)}, {service_type.name:"/"+current_city.en_name+"/sub_uslugi/"+str(service_type.id)}, {service.name: "/"+current_city.en_name+"/uslugi/"+str(service_type.id)+ "/choose_doctor"}],
        "cities": cities,
        "city": current_city,
        "activities": activities,
        "leaders": leaders,  
        "current_lang": session_parameter(request,"lang"),
        "services_types": services_types,
        "branches": branches,
        "doctors": service.doctors.all(),
    })

@csrf_exempt
def setlang(request):
    if request.method=="POST":
        lang = post_parameter(request, "lang")
        request.session["lang"] = lang
        return JsonResponse({"success": True})
    return HttpResponse("GET method not allowed! But I can tell you joke. There is cheese on the table.<p>-Fucking cheese.</p><p>-Why fucking?</p><p>-Do you see the holes retard?<p>AHAHAHHAHAHAHAHAHAH\nthis is bad joke")

def news(request, city):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    news = New.objects.filter(branch__in=branches)
    year = get_parameter(request, "year")
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    if(year):
        start = str(year)+'-01-01'
        end = str(year)+'-12-30'
        
        news = New.objects.filter(date__gte=start, date__lte=end)
    cities = City.objects.all()
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    return render(request, "news.html", {
        "path": [{"Новости": request.META.get('PATH_INFO', None)}],
        "news": news,
        "year": year,
        "cities": cities,
        "activities": activities,
        "city": current_city,
        "current_lang": session_parameter(request,"lang"),
        "leaders": leaders,
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
    })

def one_new(request, city, id):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    current_new = New.objects.get(id=id)
    cities = City.objects.all()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    return render(request, "one_new.html", {
        "path": [{"Новости":"/"+current_city.en_name+"/news"}, {current_new.title: request.META.get('PATH_INFO', None)}],
        "current_new": current_new,
        "cities": cities,
        "city": current_city,
        "current_lang": session_parameter(request,"lang"),
        "leaders": leaders,
        "branches": branches,
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
        "activities": activities,
    })


def director_blog(request, city):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    cities = City.objects.all()
    position = Position.objects.filter(name__contains="Директор").first()
    director = DirectorBlog.objects.filter(branch__in=branches).first()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    return render(request, "director_blog.html", {
        "path": [{"О поликлинике":"/"+current_city.en_name+ "/about"}, {"Блог директора филиала": request.META.get('PATH_INFO', None)}],
        "director": director,
        "activities": activities,
        "cities": cities,
        "city": current_city,
        "leaders": leaders,
        "branches": branches,
        "current_lang": session_parameter(request,"lang"),
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
    })


def lisences(request, city):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    cities = City.objects.all()
    all_lisences = License.objects.all()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    return render(request, "lisences.html", {
        "path": [{"О поликлинике": "/"+current_city.en_name+"/about"}, {"Лицензии и Сертификаты": request.META.get('PATH_INFO', None)}],
        "cities": cities,
        "city": current_city,
        "leaders": leaders,
        "lisences": all_lisences,
        "branches": branches,
        "activities": activities,
        "current_lang": session_parameter(request,"lang"),
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
    })

def partners(request, city):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    cities = City.objects.all()
    all_partners = Partner.objects.all()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    return render(request, "partners.html", {
        "path": [{"О поликлинике": "/"+current_city.en_name+"/about"}, {"Партнеры": request.META.get('PATH_INFO', None)}],
        "cities": cities,
        "city": current_city,
        "leaders": leaders,
        "partners": all_partners,
        "activities": activities,
        "branches": branches,
        "current_lang": session_parameter(request,"lang"),
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
    })

def letters(request, city):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    cities = City.objects.all()
    all_letters = Letter.objects.all()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    return render(request, "letters.html", {
        "path": [{"О поликлинике": "/"+current_city.en_name+"/about"}, {"Отзывы клиентов": request.META.get('PATH_INFO', None)}],
        "cities": cities,
        "city": current_city,
        "leaders": leaders,
        "letters": all_letters,
        "branches": branches,
        "activities": activities,
        "current_lang": session_parameter(request,"lang"),
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
    })

def patients(request, city):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    cities = City.objects.all()
    all_lisences = License.objects.all()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    return render(request, "patients.html", {
        "path": [{"Пациенту": request.META.get('PATH_INFO', None)}],
        "cities": cities,
        "city": current_city,
        "leaders": leaders,
        "activities": activities,
        "branches": branches,
        "current_lang": session_parameter(request,"lang"),
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
    })



def serviced_area(request, city):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    cities = City.objects.all()
    all_lisences = License.objects.all()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    iterator = make_incrementor(0)
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    return render(request, "serviced_area.html", {
        "path": [{"Пациенту": "/"+current_city.en_name+"/patients"},{"Обслуживаемая территория": request.META.get('PATH_INFO', None)}],
        "cities": cities,
        "city": current_city,
        "leaders": leaders,
        "activities": activities,
        "iterator": iterator,
        "branches": branches,
        "current_lang": session_parameter(request,"lang"),
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
    })

def drug_supply(request, city):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    cities = City.objects.all()
    all_lisences = License.objects.all()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    return render(request, "drug_supply.html", {
        "path": [{"Пациенту": "/"+current_city.en_name+"/patients"},{"Лекарственное обеспечение": request.META.get('PATH_INFO', None)}],
        "cities": cities,
        "city": current_city,
        "leaders": leaders,
        "branches": branches,
        "activities": activities,
        "current_lang": session_parameter(request,"lang"),
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
    })

def gobmp(request, city):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    cities = City.objects.all()
    all_lisences = License.objects.all()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    return render(request, "gobmp.html", {
        "path": [{"Пациенту": "/"+current_city.en_name+"/patients"},{"ГОБМП": request.META.get('PATH_INFO', None)}],
        "cities": cities,
        "city": current_city,
        "leaders": leaders,
        "branches": branches,
        "activities": activities,
        "current_lang": session_parameter(request,"lang"),
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
    })

def osms(request, city):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    cities = City.objects.all()
    all_lisences = License.objects.all()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    return render(request, "osms.html", {
        "path": [{"Пациенту": "/"+current_city.en_name+"/patients"},{"ОСМС": request.META.get('PATH_INFO', None)}],
        "cities": cities,
        "city": current_city,
        "leaders": leaders,
        "branches": branches,
        "activities": activities,
        "current_lang": session_parameter(request,"lang"),
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
    })

def question_answer(request, city):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    cities = City.objects.all()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    return render(request, "question_answer.html", {
        "path": [{"Пациенту": "/"+current_city.en_name+"/patients"},{"Вопрос ответ": request.META.get('PATH_INFO', None)}],
        "cities": cities,
        "city": current_city,
        "leaders": leaders,
        "branches": branches,
        "activities": activities,
        "current_lang": session_parameter(request,"lang"),
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
    })

def goverment_services(request, city):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    cities = City.objects.all()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    branch = Branch.objects.filter(city=current_city).first()
    phone = branch.phones.first().phone
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    return render(request, "goverment_services.html", {
        "path": [{"Пациенту": "/"+current_city.en_name+"/patients"},{"Государственные услуги": request.META.get('PATH_INFO', None)}],
        "cities": cities,
        "city": current_city,
        "leaders": leaders,
        "phone": phone,
        "branches": branches,
        "activities": activities,
        "current_lang": session_parameter(request,"lang"),
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
    })

def public_service_register(request, city):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branches = Branch.objects.filter(city=current_city)
    cities = City.objects.all()
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branches).first()
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    return render(request, "public_service_register.html", {
        "path": [{"Пациенту": "/"+current_city.en_name+"/patients"},{"Реестр государственных услуг": request.META.get('PATH_INFO', None)}],
        "cities": cities,
        "city": current_city,
        "leaders": leaders,
        "branches": branches,
        "activities": activities,
        "current_lang": session_parameter(request,"lang"),
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
    })

@csrf_exempt
def choose_city(request):
    if request.method == "POST":
        city_id = post_parameter(request, "city")
        city = None
        try:
            city = City.objects.get(id=int(city_id))
        except:
            return JsonResponse({"error": "city with id " + city_id + " not found!"})
        request.session["city"] = city_id
        city = city
        return redirect(reverse("main:index"))
    elif request.method == "GET":
        cities = City.objects.all()
        
        city = None
        if city_id:
            city = City.objects.get(id=city_id)
        return render(request, "choose_city.html", {
            "cities": cities,
            "city": city,
            "current_lang": session_parameter(request,"lang"),
        })

def search(request, city):
    current_city = City.objects.filter(en_name=city).first()
    if not current_city:
        return redirect(reverse("main:index", kwargs={"city": City.objects.all().first().en_name}))
    branch = Branch.objects.filter(city=current_city)
    leaders = DirectionOfActivity.objects.filter(name="Руководители", branch__in=branch).first()

    q = get_parameter(request, "q")
    if not q:
        q = " "
    branches = Branch.objects.all()
    doctors = Doctor.objects.filter(Q(fullname__icontains=q) | Q(direction_of_activity__name__icontains=q))
    news = New.objects.filter(title__icontains=q)
    services_types = ServiceType.objects.filter(name__icontains=q)

    result = []
    for doctor in doctors:
        result.append({"type":"doctor", "item": doctor})
    for new in news:
        result.append({"type":"new", "item": new})
    for service in services_types:
        result.append({"type":"service_type", "item": service})

    paginator = Paginator(result, COUNT_BLOG_ON_PAGE)
    paginated_blocks, pages = get_paginated_blogs(request, paginator)
    activities = DirectionOfActivity.objects.filter(branch__in=branches)
    return render(request, "search.html", {
        "city": current_city,
        "branches": branches,
        "result": paginated_blocks,
        "pages": pages,
        "leaders": leaders,
        "activities": activities,
        "current_lang": session_parameter(request,"lang"),
        "q": q,
        "path": [{"Поиск": request.META.get('PATH_INFO', None)}],
        "services_types": ServiceType.objects.filter(is_top=True, branch__in=branches),
    })

def test(request, city):
    return render(request, "test.html", {
        
    })

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def domain(request):
    return redirect(reverse("main:index", kwargs={'city':City.objects.all().first().en_name}))