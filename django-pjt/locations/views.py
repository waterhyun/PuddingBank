from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import requests

from .models import Bank
from .serializers import BankListSerializer, BankDetailSerializer, KakaoLocalSerializer

@api_view(['GET'])
def search_nearby_banks(request):
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    radius = request.GET.get('radius', 1000)
    
    if not all([latitude, longitude]):
        return Response({'error': '위도와 경도가 필요합니다.'}, status=400)
    
    url = 'https://dapi.kakao.com/v2/local/search/category.json'
    headers = {'Authorization': f'KakaoAK {settings.KAKAO_MAP_API_KEY}'}
    params = {
        'category_group_code': 'BK9',
        'x': longitude,
        'y': latitude,
        'radius': radius,
        'sort': 'distance'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # 각 문서에 대해 개별적으로 serializer 검증
        serialized_data = []
        for document in data['documents']:
            serializer = KakaoLocalSerializer(data=document)
            if serializer.is_valid():
                serialized_data.append(serializer.validated_data)
            else:
                print(f"Validation error for document: {serializer.errors}")
                
        return Response({
            'banks': serialized_data,
            'meta': data['meta']
        })
    except requests.RequestException as e:
        return Response({'error': f'카카오 API 요청 실패: {str(e)}'}, status=400)
    
@api_view(['GET'])
def get_bank_detail(request, bank_id):
    """특정 은행 상세 정보 조회"""
    bank = get_object_or_404(Bank, pk=bank_id)
    serializer = BankDetailSerializer(bank)
    return Response(serializer.data)

@api_view(['GET'])
def search_banks_by_keyword(request):
    """키워드로 은행 검색 (지도 범위 고려)"""
    keyword = request.GET.get('keyword')
    sw_lat = request.GET.get('sw_lat')  # 남서쪽 위도
    sw_lng = request.GET.get('sw_lng')  # 남서쪽 경도
    ne_lat = request.GET.get('ne_lat')  # 북동쪽 위도
    ne_lng = request.GET.get('ne_lng')  # 북동쪽 경도
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 15))  # 한 페이지당 결과 수

    if not keyword:
        return Response({'error': '검색어를 입력해주세요.'}, status=400)

    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    headers = {
        'Authorization': f'KakaoAK {settings.KAKAO_MAP_API_KEY}'
    }
    
    params = {
        'query': keyword,
        'category_group_code': 'BK9',
        'page': page,
        'size': size
    }

    if all([sw_lat, sw_lng, ne_lat, ne_lng]):
        params.update({
            'rect': f"{sw_lng},{sw_lat},{ne_lng},{ne_lat}"
        })

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get('documents'):
            return Response(data)
        else:
            return Response({
                'documents': [],
                'meta': {
                    'total_count': 0,
                    'pageable_count': 0,
                    'is_end': True,
                    'current_page': page
                }
            })
            
    except requests.RequestException as e:
        return Response({
            'error': f'검색 중 오류가 발생했습니다: {str(e)}'
        }, status=400)
    
# @api_view(['GET'])
# def search_banks_by_keyword(request):
#     """키워드로 은행 검색 (위치 정보 포함)"""
#     keyword = request.GET.get('keyword')
#     latitude = request.GET.get('latitude')
#     longitude = request.GET.get('longitude')
#     radius = request.GET.get('radius', 5000)  # 기본 반경 5km

#     if not keyword:
#         return Response({'error': '검색어를 입력해주세요.'}, status=400)

#     url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
#     headers = {
#         'Authorization': f'KakaoAK {settings.KAKAO_MAP_API_KEY}'
#     }
    
#     # 기본 검색 파라미터
#     params = {
#         'query': keyword,
#         'category_group_code': 'BK9'
#     }

#     # 위치 정보가 있는 경우 위치 기반 검색 추가
#     if latitude and longitude:
#         params.update({
#             'x': longitude,
#             'y': latitude,
#             'radius': radius,
#             'sort': 'distance'  # 거리순 정렬
#         })

#     try:
#         response = requests.get(url, headers=headers, params=params)
#         response.raise_for_status()
#         data = response.json()
        
#         # 검색 결과가 있는 경우
#         if data.get('documents'):
#             return Response(data)
#         else:
#             return Response({
#                 'documents': [],
#                 'meta': {
#                     'total_count': 0,
#                     'pageable_count': 0,
#                     'is_end': True
#                 }
#             })
            
#     except requests.RequestException as e:
#         return Response({
#             'error': f'검색 중 오류가 발생했습니다: {str(e)}'
#         }, status=400)