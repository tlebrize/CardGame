import random, string
from django.utils import timezone
from django.db import models
from django.db.models import F
from django.db import transaction
from ClockLife.socket import sio
from django.core.exceptions import ValidationError

letters_and_digits = string.printable[:62]


def validate_password(value):
    for char in value:
        if not (char in letters_and_digits):
            raise ValidationError(
                f"{char} is not a letter or digit",
            )


def validate_player_count(value):
    if 0 <= value <= 2:
        raise ValidationError(f"{value} must be between 0 and 2 inclusive.")


class GameManager(models.QuerySet):
    def create(self, **kwargs):
        kwargs["room_id"] = "".join(random.choices(string.hexdigits, k=32))
        game = super().create(**kwargs)
        return game

    def create_or_join(self, sid, password):
        with transaction.atomic():
            game, created = self.get_or_create(password=password)
            game.join(sid)
        return game, created


class Game(models.Model):
    objects = GameManager.as_manager()

    created_at = models.DateTimeField(
        default=timezone.now,
    )
    password = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            validate_password,
        ],
    )
    room_id = models.CharField(
        max_length=255,
    )
    players = models.IntegerField(
        default=0,
        validators=[validate_player_count],
    )

    def join(self, sid):
        if self.players >= 2:
            raise ValidationError("Room already has two players.")

        sio.enter_room(sid, self.room_id)
        self.players = F("players") + 1
        self.save()
        return self
