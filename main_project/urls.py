from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from main_project import settings
from my_app.views import pageNotFound

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('my_app.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
urlpatterns += [
    path('captcha/', include('captcha.urls')),
]

handler404 = pageNotFound
