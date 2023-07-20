import os

from django.db import models

# Create your models here.
from core.models import User


class TgUser(models.Model):
    chat_id = models.BigIntegerField(primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tg_username = models.CharField(max_length=255, null=True, blank=True)
    verification_code = models.CharField(max_length=255, null=True, unique=True, blank=True, default=None)


    def __str__(self):
        return f'{self.__class__.__name__}  ({self.chat_id})'

    # @staticmethod
    # def _generate_verification_code():
    #     return os.urandom(12).hex()
    #
    # def set_verification_code(self):
    #     self.verification_code = self._generate_verification_code()
    #     self.save(update_fields=['verification_code',])
    #     return self.verification_code


