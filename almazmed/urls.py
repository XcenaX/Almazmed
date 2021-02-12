from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
# from django.conf.urls.i18n import i18n_patterns 
# from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    #url(r'^i18n/', include('django.conf.urls.i18n')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += i18n_patterns('',
#     (_(r'^dual-lang/'), include('duallang.urls')),
    
# )
