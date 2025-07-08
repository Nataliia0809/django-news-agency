from django.contrib import admin
from django.urls import path, include

app_name = "news_agency"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("news.urls")),
    path("accounts/", include("accounts.urls")),
]
