from django.urls import path

from game.views import GameView

urlpatterns = [
    path("game/", GameView.as_view(), name="create-game"),
    path("game/<password>/", GameView.as_view(), name="create-game"),
]
