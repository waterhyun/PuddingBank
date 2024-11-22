from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

import requests

from .models import (
    # BaseProduct, 
    DepositProducts,
    DepositOptions,
    SavingProducts, 
    SavingOptions,
    Wishlist
    # RentHouseLoan,
    # UserProduct
)
from .serializers import (
    # BaseProductSerializer,
    DepositProductsSerializer,
    DepositOptionsSerializer,
    DepositProductWithOptionSerialzier,
    SavingProductsSerializer,
    SavingOptionsSerializer,
    SavingProductWithOptionSerialzier
    # RentHouseLoanSerializer
)


@api_view(['GET'])
def save_deposit_product(request):
    api_key = settings.FSS_API_KEY
    api_url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(api_url).json()
    # print(response.get('result').get('baseList'))
    
    for li in response.get('result').get('baseList'):
        fin_prdt_cd = li.get('fin_prdt_cd')
        kor_co_nm = li.get('kor_co_nm')
        fin_prdt_nm = li.get('fin_prdt_nm')
        etc_note = li.get('etc_note')
        join_deny = li.get('join_deny')
        join_member = li.get('join_member')
        join_way = li.get('join_way')
        spcl_cnd = li.get('spcl_cnd')

        if DepositProducts.objects.filter(fin_prdt_cd = fin_prdt_cd).exists():
            continue

        save_data = {
            'fin_prdt_cd' : fin_prdt_cd, 
            'kor_co_nm' : kor_co_nm,
            'fin_prdt_nm' : fin_prdt_nm, 
            'etc_note' : etc_note,
            'join_deny' : join_deny,
            'join_member' : join_member,
            'join_way' : join_way,
            'spcl_cnd' : spcl_cnd
        }

        serializer = DepositProductsSerializer(data=save_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for li in response.get('result').get('optionList'):
        fin_prdt_cd = li.get('fin_prdt_cd')
        intr_rate_type_nm = li.get('intr_rate_type_nm')
        if li.get('intr_rate') == None:
            intr_rate = -1
        else :
            intr_rate = li.get('intr_rate')

        if li.get('intr_rate2') == None:
            intr_rate2 = -1
        else :
            intr_rate2 = li.get('intr_rate2')

        save_trm = li.get('save_trm')

        if DepositOptions.objects.filter(fin_prdt_cd = fin_prdt_cd, intr_rate_type_nm=intr_rate_type_nm, save_trm=save_trm).exists():
            continue

        save_data = {
            'fin_prdt_cd' : fin_prdt_cd,
            'intr_rate_type_nm' : intr_rate_type_nm,
            'intr_rate' : intr_rate,
            'intr_rate2' : intr_rate2,
            'save_trm' : save_trm
        }

        serializer = DepositOptionsSerializer(data=save_data)

        product = DepositProducts.objects.get(fin_prdt_cd = fin_prdt_cd)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(product = product)

    return Response({ 'message' : 'data save success'})

@api_view(['GET'])
def get_deposit_products_with_options(request):
    """모든 예금 상품과 옵션 정보를 반환"""
    products = DepositProducts.objects.prefetch_related('depositoptions_set').all()  
    serializer = DepositProductWithOptionSerialzier(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def deposit_product_detail(request, product_id):
    """특정 예금 상품 상세 정보와 옵션 조회"""
    product = get_object_or_404(DepositProducts, pk=product_id)
    serializer = DepositProductWithOptionSerialzier(product)  
    return Response(serializer.data)



@api_view(['GET'])
def save_saving_product(request):
    api_key = settings.FSS_API_KEY
    api_url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(api_url).json()
    # print(response.get('result').get('baseList'))
    
    for li in response.get('result').get('baseList'):
        fin_prdt_cd = li.get('fin_prdt_cd')
        kor_co_nm = li.get('kor_co_nm')
        fin_prdt_nm = li.get('fin_prdt_nm')
        etc_note = li.get('etc_note')
        join_deny = li.get('join_deny')
        join_member = li.get('join_member')
        join_way = li.get('join_way')
        spcl_cnd = li.get('spcl_cnd')

        if SavingProducts.objects.filter(fin_prdt_cd = fin_prdt_cd).exists():
            continue

        save_data = {
            'fin_prdt_cd' : fin_prdt_cd, 
            'kor_co_nm' : kor_co_nm,
            'fin_prdt_nm' : fin_prdt_nm, 
            'etc_note' : etc_note,
            'join_deny' : join_deny,
            'join_member' : join_member,
            'join_way' : join_way,
            'spcl_cnd' : spcl_cnd
        }

        serializer = SavingProductsSerializer(data=save_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for li in response.get('result').get('optionList'):
        fin_prdt_cd = li.get('fin_prdt_cd')
        intr_rate_type_nm = li.get('intr_rate_type_nm')
        if li.get('intr_rate') == None:
            intr_rate = -1
        else :
            intr_rate = li.get('intr_rate')

        if li.get('intr_rate2') == None:
            intr_rate2 = -1
        else :
            intr_rate2 = li.get('intr_rate2')

        save_trm = li.get('save_trm')

        if SavingOptions.objects.filter(fin_prdt_cd = fin_prdt_cd, intr_rate_type_nm=intr_rate_type_nm, save_trm=save_trm).exists():
            continue

        save_data = {
            'fin_prdt_cd' : fin_prdt_cd,
            'intr_rate_type_nm' : intr_rate_type_nm,
            'intr_rate' : intr_rate,
            'intr_rate2' : intr_rate2,
            'save_trm' : save_trm
        }

        serializer = SavingOptionsSerializer(data=save_data)

        product = SavingProducts.objects.get(fin_prdt_cd = fin_prdt_cd)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(product = product)

    return Response({ 'message' : 'data save success'})

@api_view(['GET'])
def get_saving_products_with_options(request):
    """모든 적금 상품과 옵션 정보를 반환"""
    products = SavingProducts.objects.prefetch_related('savingoptions_set').all()  
    serializer = SavingProductWithOptionSerialzier(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def saving_product_detail(request, product_id):
    """특정 적금 상품 상세 정보와 옵션 조회"""
    product = get_object_or_404(SavingProducts, pk=product_id)
    serializer = SavingProductWithOptionSerialzier(product)  
    return Response(serializer.data)

# Helper 함수: product_type에 따라 상품 가져오기
def get_product(product_type, product_id):
    if product_type == 'deposit':
        return get_object_or_404(DepositProducts, id=product_id)
    elif product_type == 'saving':
        return get_object_or_404(SavingProducts, id=product_id)
    else:
        return None

# 찜하기 추가
# @login_required
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request, product_type, product_id):
    product = get_product(product_type, product_id)
    if not product:
        return Response({'error': 'Invalid product type'}, status=400)

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        deposit_product=product if product_type == 'deposit' else None,
        saving_product=product if product_type == 'saving' else None
    )

    if created:
        return Response({'message': '상품이 찜 목록에 추가되었습니다.'}, status=201)
    return Response({'message': '상품이 이미 찜 목록에 있습니다.'}, status=200)

# 찜하기 제거
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, product_type, product_id):
    product = get_product(product_type, product_id)
    if not product:
        return Response({'error': 'Invalid product type'}, status=400)

    deleted = Wishlist.objects.filter(
        user=request.user,
        deposit_product=product if product_type == 'deposit' else None,
        saving_product=product if product_type == 'saving' else None
    ).delete()

    if deleted[0] > 0:  # 삭제된 항목이 있는 경우
        return Response({'message': '상품이 찜 목록에서 제거되었습니다.'}, status=200)
    return Response({'error': '상품이 찜 목록에 없습니다.'}, status=404)

# 찜 목록 조회
# @login_required
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    data = []
    for item in wishlist_items:
        if item.deposit_product:
            data.append({
                "id": item.deposit_product.id,
                "type": "deposit",
                "name": item.deposit_product.fin_prdt_nm,
                "bank": item.deposit_product.kor_co_nm,
            })
        elif item.saving_product:
            data.append({
                "id": item.saving_product.id,
                "type": "saving",
                "name": item.saving_product.fin_prdt_nm,
                "bank": item.saving_product.kor_co_nm,
            })
    return Response(data, status=200)


# @api_view(['GET', 'POST'])
# def rent_house_loans(request):
#     """전세자금대출 상품 목록 조회 및 저장"""
#     if request.method == 'GET':
#         loans = RentHouseLoan.objects.all()
#         serializer = RentHouseLoanSerializer(loans, many=True)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         # 금융감독원 API에서 전세자금대출 데이터 가져오기
#         url = f'http://finlife.fss.or.kr/finlifeapi/rentHouseLoanProductsSearch.json'
#         params = {
#             'auth': settings.FSS_API_KEY,
#             'topFinGrpNo': '020000',
#             'pageNo': 1
#         }
#         response = requests.get(url, params=params)
        
#         if response.status_code == 200:
#             data = response.json()
#             base_list = data.get('result').get('baseList')
            
#             for base in base_list:
#                 if not BaseProduct.objects.filter(fin_prdt_cd=base['fin_prdt_cd']).exists():
#                     base_serializer = BaseProductSerializer(data=base)
#                     if base_serializer.is_valid(raise_exception=True):
#                         base_product = base_serializer.save()
                        
#                         loan_data = {
#                             'product': base_product.pk,
#                             'loan_rate_type': base.get('loan_rate_type', ''),
#                             'loan_interest_rate': base.get('loan_interest_rate', 0),
#                             'max_loan_amount': base.get('max_loan_amount', 0),
#                             'loan_period': base.get('loan_period', 0),
#                             'repayment_type': base.get('repayment_type', ''),
#                             'requirement': base.get('requirement', ''),
#                             'guarantee_type': base.get('guarantee_type', '')
#                         }
                        
#                         loan_serializer = RentHouseLoanSerializer(data=loan_data)
#                         if loan_serializer.is_valid(raise_exception=True):
#                             loan_serializer.save()
            
#             return Response({'message': '데이터 저장 완료'}, status=status.HTTP_201_CREATED)
#         return Response({'message': 'API 요청 실패'}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def rent_house_loan_detail(request, loan_id):
#     """전세자금대출 상품 상세 정보 조회"""
#     loan = get_object_or_404(RentHouseLoan, pk=loan_id)
#     serializer = RentHouseLoanSerializer(loan)
#     return Response(serializer.data)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def subscribe_product(request, product_id):
#     """상품 가입하기"""
#     product = get_object_or_404(BaseProduct, pk=product_id)
#     user = request.user
    
#     # UserProduct를 통해 이미 가입한 상품인지 확인
#     if not UserProduct.objects.filter(user=user, product=product).exists():
#         UserProduct.objects.create(
#             user=user,
#             product=product,
#             status='ACTIVE',
#             product_type='savings' if hasattr(product, 'savingsproduct') else 'RENT_LOAN'
#         )
#         return Response({'message': '상품 가입이 완료되었습니다.'}, status=status.HTTP_201_CREATED)
#     return Response({'message': '이미 가입한 상품입니다.'}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def update_savings_products(request):
#     """예금 상품 정보 업데이트"""
#     return savings_products(request)

# @api_view(['POST'])
# def update_rent_loans(request):
#     """전세자금대출 상품 정보 업데이트"""
#     return rent_house_loans(request)

# @api_view(['GET'])
# def recommend_products(request):
#     """상품 추천"""
#     # 추후 구현
#     return Response({'message': '추천 시스템 준비 중'})

# @api_view(['GET'])
# def search_products(request):
#     """상품 검색"""
#     # 추후 구현
#     return Response({'message': '검색 시스템 준비 중'})

# @api_view(['GET'])
# def filter_products(request):
#     """상품 필터링"""
#     # 추후 구현
#     return Response({'message': '필터링 시스템 준비 중'})



