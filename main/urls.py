from django.urls import path
from django.conf.urls import url, include

from . import views

app_name= "main"
urlpatterns = [
    path('', views.index, name='index'),
    
    path('news', views.news, name='news'),
    
    path('about', views.about, name='about'),
    path('director_blog', views.director_blog, name='director_blog'),
    path('lisences', views.lisences, name='lisences'),
    path('letters', views.letters, name='letters'),
    path('partners', views.partners, name='partners'),
    path('test', views.test, name='test'),
    
    path('patients', views.patients, name='patients'),
    path('serviced_area', views.serviced_area, name='serviced_area'),
    path('drug_supply', views.drug_supply, name='drug_supply'),
    path('gobmp', views.gobmp, name='gobmp'),
    path('osms', views.osms, name='osms'),
    path('question_answer', views.question_answer, name='question_answer'),
    path('goverment_services', views.goverment_services, name='goverment_services'),
    path('public_service_register', views.public_service_register, name='public_service_register'),

    path('news/<int:id>', views.one_new, name='one_new'),

    path('specialists', views.specialists, name='specialists'),
    path('specialists/activity/<int:id>', views.specialists_activity, name='specialists_activity'),
    path('specialists/<int:id>', views.specialist, name='specialist'),

    path('uslugi', views.uslugi, name='uslugi'),
    path('sub_uslugi/<int:id>', views.sub_uslugi, name='sub_uslugi'),
    

    path('search', views.search, name="search"),
    #url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),    
    
]
#