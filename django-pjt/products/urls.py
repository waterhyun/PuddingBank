from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # 예금 상품 관련 URL
    # path('deposits/test/', views.save_deposit_product, name='deposit_test'),  # (테스트용)예금 상품 저장
    path('deposits/save/', views.save_deposit_product, name='deposit_save'),  # 예금 상품 저장
    path('deposits/', views.get_deposit_products_with_options, name='deposit_list'),  # 예금 상품 전체
    path('deposits/<int:product_id>/', views.deposit_product_detail, name='deposit_detail'),  # 예금 상품 상세

    # 주택담보대출 관련 URL
    path('mortgage/', views.mortgage_loans, name='mortgage_list'),  # 주택담보대출 상품 목록 조회
    path('mortgage/<str:loan_id>/', views.mortgage_loan_detail, name='mortgage_detail'),  # 주택담보대출 상품 상세
    
    # 전세자금대출 관련 URL
    path('lease/', views.lease_loans, name='lease_list'),  # 전세자금대출 상품 목록 조회
    path('lease/<str:loan_id>/', views.lease_loan_detail, name='lease_detail'),  # 전세자금대출 상품 상세
    
    # MBTI 검사 및 추천
    path('mbti/recommendation/', views.loan_recommendation, name='mbti_recommendation'),  # MBTI 검사 및 추천

    # 적금 상품 관련 URL
    path('savings/save/', views.save_saving_product, name='saving_save'),  # 적금 상품 목록 및 생성
    path('savings/', views.get_saving_products_with_options, name='saving_list'),  # 적금 상품 목록 및 생성
    path('savings/<int:product_id>/', views.saving_product_detail, name='saving_detail'),  # 적금 상품 상세
    
    # 찜 관련 URL
    path('wishlist/', views.my_wishlist, name='my_wishlist'),
    path('wishlist/add/<str:product_type>/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<str:product_type>/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]