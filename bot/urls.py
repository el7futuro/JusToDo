from django.urls import path
from bot import views

app_name = 'bot'
urlpatterns = [
    path("verify", views.VerifyBotView.as_view(), name='bot_verification'),
    ]