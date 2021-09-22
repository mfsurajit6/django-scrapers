from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('user.urls')),
    path('store/', include('store.urls')),
    path('scraper/', include('webscraper.urls')),
    path('admin/', admin.site.urls),
]
