from django.contrib import admin
from .models import TgUser


class TGUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'tg_username', 'chat_id')
    readonly_fields = ['verification_code']
    search_fields = ['chat_id']


admin.site.register(TgUser, TGUserAdmin)
