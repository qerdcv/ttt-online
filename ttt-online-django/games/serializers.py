from rest_framework import serializers

from games.models import Game


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'current_state', 'field']
