from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home_organizer.views import dashboard, redirect_on_login


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('redirect-on-login/', redirect_on_login, name='redirect_on_login'),
    path('', dashboard, name='dashboard'),
    path('staff/', include('staff.urls')),
    path('kitchen/', include('kitchen.urls')),
    path('tasks/', include('tasks_app.urls')),
    path('notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
