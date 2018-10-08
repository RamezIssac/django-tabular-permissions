try:
    from django.conf.urls import url
except ImportError:
    from django.urls import url

from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
]


