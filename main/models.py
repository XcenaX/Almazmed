from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
import os
#from wand.image import Image
from almazmed.settings import BASE_DIR
from datetime import date

class QualificationDocument(models.Model):
    name = models.TextField(default="")
    def __str__(self):
        return self.name
    
class City(models.Model):
    name = models.TextField(default="")
    def __str__(self):
        return self.name

class BranchPhone(models.Model):
    phone = models.TextField(default="")
    name = models.TextField(default="", blank=True, null=True)
    def __str__(self):
        return self.phone

class Branch(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    address = models.TextField(default="")
    latitude = models.DecimalField(decimal_places=14, max_digits=16, blank=True, null=True)
    longitude = models.DecimalField(decimal_places=14, max_digits=16, blank=True, null=True)
    phones = models.ManyToManyField(BranchPhone, null=True, blank=True)
    image = models.ImageField(upload_to='branches', blank=True, null=True)
    description = models.TextField(default="")
    def __str__(self):
        return self.address
    def get_tel(self):
        return self.phones.all()[0].phone.replace("-", "").replace("(","").replace(")","").replace(" ","")
    
class Partner(models.Model):
    name = models.TextField(default="")
    site = models.TextField(default="")
    image = models.ImageField(upload_to='partners', blank=True, null=True)
    def __str__(self):
        return self.name

class Letter(models.Model):
    person = models.TextField(default="")
    text = models.TextField(default="")
    letter = models.FileField(upload_to='letters', blank=True, null=True)
    def __str__(self):
        return self.person

class Position(models.Model):
    name = models.TextField(default="")
    def __str__(self):
        return self.name

class License(models.Model):
    lisence = models.FileField(upload_to='lisences')
    preview = models.ImageField(blank=True, null=True, upload_to="previews")

    # def save(self, *args, **kwargs):
    #     print(self.lisence.path)

    #     f = "somefile.pdf"
    #     with(Image(filename=self.lisence.path)) as source: 
    #         for i, image in enumerate(source.sequence):
    #             newfilename = BASE_DIR+'media/previews/preview'+str(self.id)+'.jpg'
    #             Image(image).save(filename=newfilename)
    #             break

    #     # pages = convert_from_path(self.lisence.path, 500)
    #     # first = pages[0]
    #     # image_path = BASE_DIR+'media/previews/preview'+str(self.id)+'.jpg'
    #     # first.save(image_path, 'JPG')
    #     self.preview = "media/previews/preview"+str(self.id)+".jpg"
    #     self.preview.save()
    #     super(lisence, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.id)

class Education(models.Model):
    name = models.TextField(default="", blank=True)
    def __str__(self):
        return self.name

class DirectionOfActivity(models.Model):
    name = models.TextField(default="")
    description = models.TextField(default="", blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.name
    

class Image(models.Model):
    img_url = models.TextField(default='')
    name = models.TextField(default='')
    absolute_path = models.TextField(default='')
    
    def delete_image(self, doctor_id):
        current_path = os.path.abspath(os.path.dirname(__file__))
        doctor = Doctor.objects.get(id=doctor_id)
        new_img_url = current_path + "\\static\\images\\doctors\\doctor" + str(doctor.id) + ".jpg"
        os.remove(new_img_url)
    def __str__(self):
        return self.name


class Doctor(models.Model):
    fullname = models.TextField(default='')
    qualification_category = models.TextField(default='', null=True, blank=True)
    work_experience = models.IntegerField(default=-1) 
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True)
    qualification = models.ManyToManyField(QualificationDocument, null=True, related_name='qualification_documents',  blank=True)
    direction_of_activity = models.ForeignKey(DirectionOfActivity, on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    education = models.ManyToManyField(Education, null=True, related_name='educations',  blank=True)
    image = models.ImageField(upload_to='doctors', blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.fullname
    def is_working(self):
        if not self.start_date:
            return True
        return self.start_date <= date.today()

class New(models.Model):
    title = models.TextField(default='')
    date = models.DateField(default='')
    description = models.TextField(default='')
    image = models.ImageField(upload_to='news', blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.title

class Nurse(models.Model):
    name = models.TextField(default="")
    def __str__(self):
        return self.name

class DistrictDoctor(models.Model):
    name = models.TextField(default="")
    def __str__(self):
        return self.name

class House(models.Model):
    name = models.TextField(default="")
    def __str__(self):
        return self.name

class Cabinet(models.Model):
    number = models.IntegerField(default=0)
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE, blank=True, null=True)
    district_doctor = models.ForeignKey(DistrictDoctor, on_delete=models.CASCADE, blank=True, null=True)
    houses = models.ManyToManyField(House, null=True, blank=True)
    def __str__(self):
        return str(self.number)

class HospitalBuilding(models.Model):
    number = models.IntegerField(default=0)
    cabinets = models.ManyToManyField(Cabinet, null=True, blank=True)
    def __str__(self):
        return str(self.number)

class Microdistrict(models.Model):
    name = models.TextField(default="")
    hospital_buildings = models.ManyToManyField(HospitalBuilding, null=True, blank=True)
    def __str__(self):
        return self.name

class HospitalSite(models.Model):
    name = models.TextField(default="")
    number = models.IntegerField(default=0)
    microdistricts = models.ManyToManyField(Microdistrict, null=True, blank=True)
    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.TextField(default="")
    price = models.IntegerField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    is_free = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class ServiceType(models.Model):
    services_types = models.ManyToManyField('ServiceType', null=True, blank=True)
    services = models.ManyToManyField(Service, null=True, blank=True)
    name = models.TextField(default="")
    is_top = models.BooleanField(default=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.name






    

