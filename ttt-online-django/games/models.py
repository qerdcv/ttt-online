from django.db import models
from django.contrib.auth import get_user_model


def default_field() -> list:
    return [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]


class Game(models.Model):

    class State(models.TextChoices):
        PENDING = 'pending',
        IN_GAME = 'in_game',
        DONE = 'done'

    owner_id = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL),
    opponent_id = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, default=None),
    current_player_id = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, default=None),
    step_count = models.IntegerField(),
    winner_id = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, default=None),
    field = models.JSONField(default=default_field),
    current_state = models.TextField(choices=State.choices, default=State.PENDING)
