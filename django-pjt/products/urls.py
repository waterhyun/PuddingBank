from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # 예금 상품 관련 URL
    path('deposits/', views.deposit_products, name='deposit_list'),  # 예금 상품 목록 및 생성
    path('deposits/<int:product_id>/', views.deposit_product_detail, name='deposit_detail'),  # 예금 상품 상세
        
    # # 금융감독원 API 데이터 업데이트
    # path('update/deposits/', views.update_deposit_products, name='update_deposits'),  # 예금 상품 정보 업데이트
    # path('update/loans/', views.update_rent_loans, name='update_loans'),  # 대출 상품 정보 업데이트

    # # 상품 검색 및 필터링
    # path('search/', views.search_products, name='search'),  # 상품 검색
    # path('filter/', views.filter_products, name='filter'),  # 상품 필터링

    ###########################################

    # 주택담보대출 관련 URL
    path('mortgage/', views.mortgage_loans, name='mortgage_list'),  # 주택담보대출 상품 목록 조회
    path('mortgage/<str:loan_id>/', views.mortgage_loan_detail, name='mortgage_detail'),  # 주택담보대출 상품 상세
    
    # 전세자금대출 관련 URL
    path('lease/', views.lease_loans, name='lease_list'),  # 전세자금대출 상품 목록 조회
    path('lease/<str:loan_id>/', views.lease_loan_detail, name='lease_detail'),  # 전세자금대출 상품 상세
    
    # MBTI 검사 및 추천
    path('mbti/recommendation/', views.loan_recommendation, name='mbti_recommendation'),  # MBTI 검사 및 추천

]