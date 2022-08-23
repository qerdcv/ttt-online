from rest_framework import viewsets, permissions

from games.models import Game
from games.serializers import GameSerializer


class GameView(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = []
