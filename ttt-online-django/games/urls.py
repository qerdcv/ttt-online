from django.urls import path, include
from rest_framework import routers

from games import views

router = routers.DefaultRouter()
router.register('games', views.GameView)

urlpatterns = [
    path('', include(router.urls)),
]
