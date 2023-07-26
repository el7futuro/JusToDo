from rest_framework import serializers

from bot.models import TgUser



class TgUserSerializer(serializers.ModelSerializer):
    tg_id = serializers.IntegerField(source='chat_id', read_only=True)
    username = serializers.CharField(source='user.username', allow_null=True, read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    verification_code = serializers.CharField(write_only=True)

    class Meta:
        model = TgUser
        read_only_fields = ['tg_id', 'user_id', 'verification_code',  'username']
        fields = ['tg_id', 'user_id', 'username', 'verification_code']

    def validate_verification_code(self, code: str):
        try:
            TgUser.objects.get(verification_code=code)
        except TgUser.DoesNotExist:
            raise serializers.ValidationError('Verification code is incorrect')
        return code