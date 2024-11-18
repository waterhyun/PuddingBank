from django.urls import path
from . import views


urlpatterns = [
    path('finance_services/', views.article_list),
    path('finance_services/articles/', views.article_list),
    # path('finance_services/<int:article_pk>/', views.article_detail),
]
