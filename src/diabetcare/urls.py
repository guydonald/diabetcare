
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('patients/', include('patients.urls')),
    path('nutritions/', include('nutritions.urls')),
    path('activities/', include('activities.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
