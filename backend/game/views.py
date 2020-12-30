from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from ClockLife.socket import sio
from game.models import Game


class GameViewSerializer(serializers.Serializer):
    sid = serializers.CharField()
    password = serializers.CharField()


class GameView(APIView):
    queryset = Game.objects.all()
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GameViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        game, created = Game.objects.create_or_join(
            data["sid"],
            data["password"],
        )

        if not created:
            sio.emit("game_ready", room=game.room_id)
            status = 200
        else:
            status = 201

        return Response(
            {
                "room_id": game.room_id,
                "game_ready": (not created),
            },
            status=status,
        )
