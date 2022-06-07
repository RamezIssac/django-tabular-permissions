try:
    from django.conf.urls import url
except ImportError:
    from django.urls import path

from django.contrib import admin


urlpatterns = [
    path(r'^admin/', admin.site.urls),
]


