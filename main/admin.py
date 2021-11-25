from django.contrib import admin
from .models import *
from django.contrib import admin

class ServiceAdmin(admin.ModelAdmin):    
    search_fields = ['name', 'price']

class ServiceTypeAdmin(admin.ModelAdmin):    
    search_fields = ['name']

admin.site.register(Doctor)
admin.site.register(New)
admin.site.register(QualificationDocument)
admin.site.register(Image)
admin.site.register(DirectionOfActivity)
admin.site.register(Education)
admin.site.register(Position)
admin.site.register(Branch)
admin.site.register(BranchPhone)
admin.site.register(City)
admin.site.register(Partner)
admin.site.register(License)
admin.site.register(Letter)
admin.site.register(ServiceType, ServiceTypeAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(DirectorBlog)
admin.site.register(GovermentService)

