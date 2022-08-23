from django.contrib.auth import get_user_model
from rest_framework import viewsets

from users.serializers import UserSerializer


class UserView(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all().order_by('date_joined')
    serializer_class = UserSerializer
    permission_classes = []
