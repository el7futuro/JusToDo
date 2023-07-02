from django.db import models
from django.utils import timezone
from datetime import date
from core.models import User


class GoalCategory(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    def save(self, *args, **kwargs):
        if not self.id:  # Когда объект только создается, у него еще нет id
            self.created = timezone.now()  # проставляем дату создания
        self.updated = timezone.now()  # проставляем дату обновления
        return super().save(*args, **kwargs)


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
        verbose_name = 'Goal'
        verbose_name_plural = 'Goals'

    title = models.CharField(verbose_name='title', max_length=255)
    description = models.CharField(verbose_name='description', max_length=255)
    status = models.PositiveSmallIntegerField(verbose_name='status', choices=Status.choices,
                                              default=Status.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name='priority', choices=Status.choices,
                                                default=Priority.medium)
    user = models.ForeignKey(User, verbose_name='author', on_delete=models.PROTECT)
    category = models.ForeignKey(GoalCategory, verbose_name='category', on_delete=models.PROTECT, related_name='goals')
    due_date = models.DateField(verbose_name='deadline', default=date.today, null=True)
    created = models.DateTimeField(verbose_name='created at', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='updated at', auto_now=True)


class GoalComment(models.Model):
    class Meta:
        verbose_name = 'GoalComment'
        verbose_name_plural = 'GoalComments'

    goal = models.ForeignKey(Goal, verbose_name='goal', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='author', on_delete=models.CASCADE)
    text = models.CharField(verbose_name='text', max_length=255)
    created = models.DateTimeField(verbose_name='created at', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='updated at', auto_now=True)