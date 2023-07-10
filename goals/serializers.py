from django.db import transaction
from rest_framework import serializers

from core.models import User
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant
from core.serializers import ProfileSerializer
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user", "board")
        fields = "__all__"

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")

        return value

    def create(self, validated_data):
        board_id = self.initial_data.pop('board', None)
        board = get_object_or_404(Board, pk=board_id)

        if not board.participants.filter(user=self.context['request'].user.pk, role__in=[1, 2]).exists():
            raise PermissionDenied({'non_field_errors': ["You don't have write permission"]})

        category = GoalCategory.objects.create(**validated_data, board=board)
        return category


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user', 'board')


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    description = serializers.CharField(max_length=255, required=False, allow_blank=True)

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')

    def validate_category(self, value: GoalCategory):
        if value.is_deleted:
            raise serializers.ValidationError('not allowed in deleted category')
        if not value.board.participants.filter(role__in=[1, 2], user=self.context['request'].user):
            raise PermissionDenied({'non_field_errors': ["You don't have write permission"]})

        return value


class GoalSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')

    def validate_goal(self, value: Goal):
        if value.status == 4:
            raise serializers.ValidationError('not allowed in archived goal')
        if not value.category.board.participants.filter(role__in=[1, 2], user=self.context['request'].user):
            raise PermissionDenied({'non_field_errors': ["You don't have write permission"]})

        return value


class CommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', 'goal')


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def create(self, validated_data):
        with transaction.atomic():
            user = validated_data.pop("user")
            board = Board.objects.create(**validated_data)
            BoardParticipant.objects.create(
                user=user, board=board, role=BoardParticipant.Role.owner
            )
            return board

class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.Role.choices)
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'board')


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True, required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    title = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated')

    def update(self, instance, validated_data: dict):

        with transaction.atomic():
            instance.participants.exclude(user=self.context["request"].user).delete()
            if 'participants' in validated_data.keys():
                for participant in validated_data["participants"]:
                    BoardParticipant.objects.create(
                        user_id=participant["user"].id,
                        role=participant["role"],
                        board_id=instance.pk
                    )

            if validated_data["title"]:
                instance.title = validated_data["title"]
                instance.save(update_fields=("title",))

        return instance


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ("id", "created", "updated")