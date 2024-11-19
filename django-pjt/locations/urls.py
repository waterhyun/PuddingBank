from django.urls import path
from . import views

app_name = 'locations'

urlpatterns = [
    path('banks/nearby/', views.search_nearby_banks, name='nearby-banks'),
    path('banks/search/', views.search_banks_by_keyword, name='search-banks'),
    path('banks/<int:bank_id>/', views.get_bank_detail, name='bank-detail'),
]