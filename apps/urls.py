import django
from django.conf.urls import include, url
from django.conf import settings
from django.views.generic import RedirectView
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
import xadmin
xadmin.ROOT_PATH_NAME = 'xadmin'
settings.XADMIN_EXCLUDE_PLUGINS = ['bookmark','topnav']
xadmin.DEFAULT_RELFIELD_STYLE = {'fk': 'fk_select', 'm2m': 'm2m_select2'}
xadmin.autodiscover()
from xadmin import defs
defs.EMPTY_CHANGELIST_VALUE = None

# from xadmin.plugins import xversion
# xversion.register_models()

from django.contrib import admin
admin.autodiscover()

from callc import views
from rests import interfaces

urlpatterns = [
    url(r'^$',RedirectView.as_view(url='/xadmin/')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^xadmin/', include(xadmin.site.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
