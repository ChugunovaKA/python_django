"""
mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    # Путь для смены языка, не зависящий от локали
    path('i18n/', include('django.conf.urls.i18n')),
    # Здесь можно добавить другие пути, не зависящие от языка
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('shopapp.urls', namespace='shopapp')),  # <-- добавлен маршрут корня сайта
    path('shop/', include('shopapp.urls', namespace='shopapp')),
    path('myauth/', include('myauth.urls', namespace='myauth')),
)

if settings.DEBUG:
    urlpatterns.extend(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
    urlpatterns.extend(
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    )