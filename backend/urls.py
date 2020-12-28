from django.urls import path , include
from django.contrib import admin
from api import urls
from api.views import homepage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urls)),
    path('',homepage)
    
]
