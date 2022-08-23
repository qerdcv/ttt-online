from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v2/auth/', include('users.urls')),
    path('api/v2/games/', include('games.urls'))
]
