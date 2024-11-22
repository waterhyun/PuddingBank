from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # 예금 상품 관련 URL
    # path('deposits/test/', views.save_deposit_product, name='deposit_test'),  # (테스트용)예금 상품 저장
    path('deposits/save/', views.save_deposit_product, name='deposit_save'),  # 예금 상품 저장
    path('deposits/', views.get_deposit_products_with_options, name='deposit_list'),  # 예금 상품 전체
    path('deposits/<int:product_id>/', views.deposit_product_detail, name='deposit_detail'),  # 예금 상품 상세

    # 적금 상품 관련 URL
    path('savings/save/', views.save_saving_product, name='saving_save'),  # 적금 상품 목록 및 생성
    path('savings/', views.get_saving_products_with_options, name='saving_list'),  # 적금 상품 목록 및 생성
    path('savings/<int:product_id>/', views.saving_product_detail, name='saving_detail'),  # 적금 상품 상세
    
    # 찜 관련 URL
    path('wishlist/', views.my_wishlist, name='my_wishlist'),
    path('wishlist/add/<str:product_type>/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<str:product_type>/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    
    # 전세자금대출 상품 관련 URL
    # path('loans/', views.rent_house_loans, name='loan_list'),  # 대출 상품 목록 및 생성
    # path('loans/<int:loan_id>/', views.rent_house_loan_detail, name='loan_detail'),  # 대출 상품 상세
    
    # # 상품 가입 관련 URL
    # path('subscribe/<int:product_id>/', views.subscribe_product, name='subscribe'),  # 상품 가입
    
    # # 금융감독원 API 데이터 업데이트
    # # path('update/deposits/', views.update_deposit_products, name='update_deposits'),  # 예금 상품 정보 업데이트
    # # path('update/loans/', views.update_rent_loans, name='update_loans'),  # 대출 상품 정보 업데이트
    
    # # 상품 추천
    # path('recommendations/', views.recommend_products, name='recommendations'),  # 상품 추천
    
    # # 상품 검색 및 필터링
    # path('search/', views.search_products, name='search'),  # 상품 검색
    # path('filter/', views.filter_products, name='filter'),  # 상품 필터링
]