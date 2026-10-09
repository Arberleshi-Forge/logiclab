from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("", include("analyzer.urls")),
    path("algorithms/", include("algorithms.urls")),
    path("chatbot/", include("chatbot.urls")),
    path("uploads/", include("uploads.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
