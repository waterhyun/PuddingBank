# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # 커스텀 프로필 관련 URLs만 포함
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/delete/', views.profile_delete, name='profile_delete'),
]