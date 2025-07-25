from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("news.urls")),
    path("accounts/", include("accounts.urls")),
]

if settings.DEBUG:
    # Django Debug Toolbar
    import debug_toolbar
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

    # media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
