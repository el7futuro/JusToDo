import json

from rest_framework import permissions
from rest_framework import serializers

from rest_framework.generics import UpdateAPIView, GenericAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient
from core.models import User


class VerifyBotView(GenericAPIView):
    model = TgUser
    serializer_class = TgUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        tg_user = TgUser.objects.filter(verification_code=request.data["verification_code"])
        if tg_user:
            tg_user.update(user=request.user.id)
            TgClient().send_message(chat_id=tg_user[0].chat_id, text='Аккаунт успешно подтвержден')
            return Response(data=TgUserSerializer(tg_user[0]).data, status=200)
        else:
            raise serializers.ValidationError("incorrect code")