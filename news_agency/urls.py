from django.contrib import admin
from django.urls import path

app_name = 'news_agency'

urlpatterns = [
    path('admin/', admin.site.urls),
]
