from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # 예금 상품 관련 URL
    path('deposits/', views.deposit_products, name='deposit_list'),  # 예금 상품 목록 및 생성
    path('deposits/<int:product_id>/', views.deposit_product_detail, name='deposit_detail'),  # 예금 상품 상세
    
    # 전세자금대출 상품 관련 URL
    path('loans/', views.rent_house_loans, name='loan_list'),  # 대출 상품 목록 및 생성
    path('loans/<int:loan_id>/', views.rent_house_loan_detail, name='loan_detail'),  # 대출 상품 상세
    
    # 상품 가입 관련 URL
    path('subscribe/<int:product_id>/', views.subscribe_product, name='subscribe'),  # 상품 가입
    
    # 금융감독원 API 데이터 업데이트
    path('update/deposits/', views.update_deposit_products, name='update_deposits'),  # 예금 상품 정보 업데이트
    path('update/loans/', views.update_rent_loans, name='update_loans'),  # 대출 상품 정보 업데이트
    
    # 상품 추천
    path('recommendations/', views.recommend_products, name='recommendations'),  # 상품 추천
    
    # 상품 검색 및 필터링
    path('search/', views.search_products, name='search'),  # 상품 검색
    path('filter/', views.filter_products, name='filter'),  # 상품 필터링
]