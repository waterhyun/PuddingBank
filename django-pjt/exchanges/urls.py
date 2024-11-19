from django.urls import path
from . import views

app_name = 'exchanges'

urlpatterns = [
    # 환율 관련 URL
    path('', views.exchange, name='exchange'),  # 환율 목록 및 생성
]