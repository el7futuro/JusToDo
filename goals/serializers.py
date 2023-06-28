from rest_framework import serializers
from goals.models import GoalCategory
from core.serializers import ProfileSerializer


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user')