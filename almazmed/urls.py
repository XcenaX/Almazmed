from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from main import views as main_views
# from django.conf.urls.i18n import i18n_patterns 
# from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<slug:city>/', include('main.urls')),
    path('choose_city/', main_views.choose_city, name='choose_city'),
    path('download/(?P<path>.*)$', main_views.download, name="download"),
    path('setlang/', main_views.setlang, name="setlang"),
    path('', main_views.domain, name="domain"),
    #path('test/', main_views.test, name="test"),
    #url(r'^i18n/', include('django.conf.urls.i18n')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += i18n_patterns('',
#     (_(r'^dual-lang/'), include('duallang.urls')),
    
# )
