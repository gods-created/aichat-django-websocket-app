from django.urls import path
from .views import (
    chat_page,
)
from .views import (
    DialogStorage as DialogStorageView,
)

app_name = 'initchat'

urlpatterns = [
    path('', chat_page, name='Chat page'),
    path('api/dialog', DialogStorageView.as_view(), name='Dialog storage actions'),
] 