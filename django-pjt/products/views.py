from django.shortcuts import render, get_object_or_404
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

import requests

from .models import (
    BaseProduct, 
    DepositProduct, 
    RentHouseLoan,
    UserProduct
)
from .serializers import (
    BaseProductSerializer,
    DepositProductSerializer,
    RentHouseLoanSerializer
)

@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'GET':
        products = DepositProduct.objects.all()
        serializer = DepositProductSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
        params = {
            'auth': settings.FSS_API_KEY,
            'topFinGrpNo': '020000',
            'pageNo': 1
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # 오류 발생시 예외 발생
            data = response.json()
            
            base_list = data.get('result', {}).get('baseList', [])
            option_list = data.get('result', {}).get('optionList', [])
            
            created_products = []
            for base in base_list:
                base_product, created = BaseProduct.objects.get_or_create(
                    fin_prdt_cd=base['fin_prdt_cd'],
                    defaults={
                        'kor_co_nm': base['kor_co_nm'],
                        'fin_prdt_nm': base['fin_prdt_nm'],
                    }
                )
                
                product_options = [opt for opt in option_list if opt['fin_prdt_cd'] == base['fin_prdt_cd']]
                if product_options:
                    option = product_options[0]
                    deposit_data = {
                        'interest_rate': option.get('intr_rate', 0),
                        'max_interest_rate': option.get('intr_rate2', 0),
                        'save_trm': option.get('save_trm', 0),
                        'intr_rate_type_nm': option.get('intr_rate_type_nm', ''),
                        'intr_rate2': option.get('intr_rate2', 0),
                        'join_way': base.get('join_way', ''),
                        'join_member': base.get('join_member', ''),
                        'etc_note': base.get('etc_note', '')
                    }
                    
                    serializer = DepositProductSerializer(
                        data=deposit_data,
                        context={'product': base_product}
                    )
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        created_products.append(serializer.data)
            
            return Response({
                'message': '데이터 저장 완료',
                'created_products': created_products
            }, status=status.HTTP_201_CREATED)
            
        except requests.RequestException as e:
            return Response({
                'message': 'API 요청 실패',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def deposit_product_detail(request, product_id):
    """예금 상품 상세 정보 조회"""
    product = get_object_or_404(DepositProduct, pk=product_id)
    serializer = DepositProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def rent_house_loans(request):
    """전세자금대출 상품 목록 조회 및 저장"""
    if request.method == 'GET':
        loans = RentHouseLoan.objects.all()
        serializer = RentHouseLoanSerializer(loans, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # 금융감독원 API에서 전세자금대출 데이터 가져오기
        url = f'http://finlife.fss.or.kr/finlifeapi/rentHouseLoanProductsSearch.json'
        params = {
            'auth': settings.FSS_API_KEY,
            'topFinGrpNo': '020000',
            'pageNo': 1
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            base_list = data.get('result').get('baseList')
            
            for base in base_list:
                if not BaseProduct.objects.filter(fin_prdt_cd=base['fin_prdt_cd']).exists():
                    base_serializer = BaseProductSerializer(data=base)
                    if base_serializer.is_valid(raise_exception=True):
                        base_product = base_serializer.save()
                        
                        loan_data = {
                            'product': base_product.pk,
                            'loan_rate_type': base.get('loan_rate_type', ''),
                            'loan_interest_rate': base.get('loan_interest_rate', 0),
                            'max_loan_amount': base.get('max_loan_amount', 0),
                            'loan_period': base.get('loan_period', 0),
                            'repayment_type': base.get('repayment_type', ''),
                            'requirement': base.get('requirement', ''),
                            'guarantee_type': base.get('guarantee_type', '')
                        }
                        
                        loan_serializer = RentHouseLoanSerializer(data=loan_data)
                        if loan_serializer.is_valid(raise_exception=True):
                            loan_serializer.save()
            
            return Response({'message': '데이터 저장 완료'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'API 요청 실패'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def rent_house_loan_detail(request, loan_id):
    """전세자금대출 상품 상세 정보 조회"""
    loan = get_object_or_404(RentHouseLoan, pk=loan_id)
    serializer = RentHouseLoanSerializer(loan)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe_product(request, product_id):
    """상품 가입하기"""
    product = get_object_or_404(BaseProduct, pk=product_id)
    user = request.user
    
    # UserProduct를 통해 이미 가입한 상품인지 확인
    if not UserProduct.objects.filter(user=user, product=product).exists():
        UserProduct.objects.create(
            user=user,
            product=product,
            status='ACTIVE',
            product_type='DEPOSIT' if hasattr(product, 'depositproduct') else 'RENT_LOAN'
        )
        return Response({'message': '상품 가입이 완료되었습니다.'}, status=status.HTTP_201_CREATED)
    return Response({'message': '이미 가입한 상품입니다.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_deposit_products(request):
    """예금 상품 정보 업데이트"""
    return deposit_products(request)

@api_view(['POST'])
def update_rent_loans(request):
    """전세자금대출 상품 정보 업데이트"""
    return rent_house_loans(request)

@api_view(['GET'])
def recommend_products(request):
    """상품 추천"""
    # 추후 구현
    return Response({'message': '추천 시스템 준비 중'})

@api_view(['GET'])
def search_products(request):
    """상품 검색"""
    # 추후 구현
    return Response({'message': '검색 시스템 준비 중'})

@api_view(['GET'])
def filter_products(request):
    """상품 필터링"""
    # 추후 구현
    return Response({'message': '필터링 시스템 준비 중'})