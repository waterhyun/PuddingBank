from django.shortcuts import render, get_object_or_404
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

import requests
from datetime import datetime, timedelta

# 모델/시리얼라이즈 
from .models import Exchange
from .serializers import ExchangeSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def exchange(request):
    if request.method == 'GET':
        # 모든 환율 데이터 조회
        exchange_result = Exchange.objects.all()
        serializer = ExchangeSerializer(exchange_result, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # 현재 날짜를 YYYYMMDD 형식으로 포맷팅

        def get_adjusted_date(date):
            """
            입력된 날짜가 토요일(5) 또는 일요일(6)일 경우 금요일 날짜로 변경
            :param date: datetime 객체
            :return: YYYYMMDD 형식의 날짜 문자열
            """
            # 요청 시간 검사 로직 추가
            if date.hour < 11:
                date -= timedelta(days=1)

            # 요일 확인 (월요일: 0, ... 금요일: 4, 토요일: 5, 일요일: 6)
            if date.weekday() == 5:  # 토요일
                date -= timedelta(days=1)  # 금요일로 변경
            elif date.weekday() == 6:  # 일요일
                date -= timedelta(days=2)  # 금요일로 변경

            # YYYYMMDD 형식으로 반환
            return date.strftime('%Y%m%d')
        today = datetime.now()
        formatted_date = get_adjusted_date(today)
        dateform_date = datetime.strptime(formatted_date, "%Y%m%d").strftime("%Y-%m-%d")

        # API 호출 정보
        url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
        params = {
            'authkey': settings.EXCHANGE_API_KEY,
            'data': 'AP01',
            'searchdate': formatted_date
        }

        try:
            # 외부 API 요청
            response = requests.get(url, params=params)
            response.raise_for_status()  # 요청 실패 시 예외 발생
            data = response.json()  # JSON 데이터 파싱

             # 데이터 전처리: 쉼표 제거 후 숫자 변환
            def parse_float(value):
                """쉼표를 제거하고 float로 변환"""
                if value is None or value == '':
                    return None
                return float(value.replace(',', ''))

            for item in data:
                item['ttb'] = parse_float(item.get('ttb'))
                item['tts'] = parse_float(item.get('tts'))
                item['deal_bas_r'] = parse_float(item.get('deal_bas_r'))
                item['bkpr'] = parse_float(item.get('bkpr'))
                item['kftc_bkpr'] = parse_float(item.get('kftc_bkpr'))
                item['kftc_deal_bas_r'] = parse_float(item.get('kftc_deal_bas_r'))
                item['update_date'] = dateform_date
        # 데이터 저장

            # API 데이터 처리 및 저장
            created_entries = []
            skipped_entries = []
            for item in data:
                # 중복 데이터 확인
                existing_entry = Exchange.objects.filter(
                    cur_unit=item.get('cur_unit'),
                    update_date=dateform_date
                ).exists()

                if existing_entry:
                    skipped_entries.append(item)  # 저장 건너뛴 데이터
                    continue

                # 데이터 직렬화 및 저장
                serializer = ExchangeSerializer(data=item)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    created_entries.append(serializer.data)


            return Response({
                'message': '데이터 처리 완료',
                'created_entries': created_entries,
                'skipped_entries': skipped_entries
            }, status=status.HTTP_201_CREATED)

        except requests.RequestException as e:
            # API 요청 실패 시 응답 처리
            return Response({
                'message': 'API 요청 실패',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # 기타 예외 처리
            return Response({
                'message': '데이터 저장 실패',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def update_exchange(request):
    """환율 정보 업데이트"""
    return exchange(request)

