from django.db import models
from django.utils import timezone
from datetime import date
from core.models import User
from django.db.models import TextField


class DatesModelMixin(models.Model):
    class Meta:
        abstract = True  # for preventing table creation for this model

    created = models.DateTimeField(verbose_name='created at', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='updated at', auto_now=True)


class Board(DatesModelMixin):
    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class BoardParticipant(DatesModelMixin):
    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    board = models.ForeignKey(
        Board,
        verbose_name="Доска",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    role = models.PositiveSmallIntegerField(
        verbose_name="Роль", choices=Role.choices, default=Role.owner
    )


class GoalCategory(DatesModelMixin):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    board = models.ForeignKey(
        Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="categories"
    )
    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    def save(self, *args, **kwargs):
        if not self.id:  # Когда объект только создается, у него еще нет id
            self.created = timezone.now()  # проставляем дату создания
        self.updated = timezone.now()  # проставляем дату обновления
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Status(models.IntegerChoices):
    to_do = 1, "К выполнению"
    in_progress = 2, "В процессе"
    done = 3, "Выполнено"
    archived = 4, "Архив"


class Priority(models.IntegerChoices):
    low = 1, "Низкий"
    medium = 2, "Средний"
    high = 3, "Высокий"
    critical = 4, "Критический"


class Goal(models.Model):
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    title = models.CharField(verbose_name='Название', max_length=255)
    description = models.TextField(verbose_name='описание', max_length=255)
    status = models.PositiveSmallIntegerField(verbose_name='статус', choices=Status.choices,
                                              default=Status.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name='приоритет', choices=Status.choices,
                                                default=Priority.medium)
    user = models.ForeignKey(User, verbose_name='автор', on_delete=models.PROTECT)
    category = models.ForeignKey(GoalCategory, verbose_name='категория', on_delete=models.PROTECT, related_name='goals')
    due_date = models.DateField(verbose_name='дедлайн', default=date.today, null=True)
    created = models.DateTimeField(verbose_name='создано в', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='изменено в', auto_now=True)

    def __str__(self) -> str:
        return self.title


class GoalComment(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    goal = models.ForeignKey(Goal, verbose_name='цель', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='автор', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='текст', max_length=255)
    created = models.DateTimeField(verbose_name='создано в', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='изменено в', auto_now=True)

    def __str__(self) -> str:
        return self.title