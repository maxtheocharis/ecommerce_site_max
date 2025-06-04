# backend/ecommerce/ecommerce/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from catalog.views import signup  # we kept the template‐based signup view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", signup, name="signup"),
    path("", include("catalog.urls")),         # your template pages
    path("api/", include("catalog.api_urls")),  # your DRF endpoints
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
