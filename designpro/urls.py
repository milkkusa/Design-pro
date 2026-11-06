from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('superadmin/', admin.site.urls), #как по тз опять же адрес
    path('', include('main.urls')),
]

if settings.DEBUG:#картинки
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

