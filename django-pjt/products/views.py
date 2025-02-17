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
    Wishlist,
    # RentHouseLoan,
    # UserProduct
    MortgageLoan,
    MortgageLoanOption,
    LeaseLoan,
    LeaseLoanOption
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
def mortgage_loans(request):
    """주택담보대출 상품 목록 조회 및 DB 저장"""
    url = 'http://finlife.fss.or.kr/finlifeapi/mortgageLoanProductsSearch.json'
    params = {
        'auth': settings.FSS_API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': request.GET.get('page', '1')
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        base_list = data.get('result', {}).get('baseList', [])
        option_list = data.get('result', {}).get('optionList', [])
        
        # DB에 데이터 저장
        for base in base_list:
            loan, created = MortgageLoan.objects.update_or_create(
                fin_co_no=base['fin_co_no'],
                fin_prdt_cd=base['fin_prdt_cd'],
                defaults={
                    'kor_co_nm': base['kor_co_nm'],
                    'fin_prdt_nm': base['fin_prdt_nm'],
                    'join_way': base['join_way'],
                    'loan_inci_expn': base['loan_inci_expn'],
                    'erly_rpay_fee': base['erly_rpay_fee'],
                    'dly_rate': base['dly_rate'],
                    'loan_lmt': base['loan_lmt'],
                    'dcls_strt_day': base['dcls_strt_day'],
                    'dcls_end_day': base['dcls_end_day'],
                    'fin_co_subm_day': base['fin_co_subm_day'],
                }
            )
            
            # 해당 상품의 옵션 정보 저장
            product_options = [opt for opt in option_list if opt['fin_prdt_cd'] == base['fin_prdt_cd']]
            for option in product_options:
                MortgageLoanOption.objects.update_or_create(
                    loan=loan,
                    fin_prdt_cd=option['fin_prdt_cd'],
                    mrtg_type=option['mrtg_type'],
                    rpay_type=option['rpay_type'],
                    lend_rate_type=option['lend_rate_type'],
                    defaults={
                        'lend_rate_min': option['lend_rate_min'],
                        'lend_rate_max': option['lend_rate_max'],
                        'lend_rate_avg': option['lend_rate_avg'] if option['lend_rate_avg'] else None,
                    }
                )
        
        # 저장된 데이터 조회하여 반환
        loans = MortgageLoan.objects.all().prefetch_related('options')
        result = []
        for loan in loans:
            loan_data = {
                'fin_co_no': loan.fin_co_no,
                'kor_co_nm': loan.kor_co_nm,
                'fin_prdt_nm': loan.fin_prdt_nm,
                'options': list(loan.options.values())
            }
            result.append(loan_data)
            
        return Response(result)
        
    except requests.RequestException as e:
        return Response({
            'message': 'API 요청 실패',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def mortgage_loan_detail(request, loan_id):
    """주택담보대출 상품 상세 정보 조회"""
    loan = get_object_or_404(MortgageLoan, id=loan_id)
    
    result = {
        'fin_prdt_cd': loan.fin_prdt_cd,  # 추가
        'fin_co_no': loan.fin_co_no,
        'kor_co_nm': loan.kor_co_nm,
        'fin_prdt_nm': loan.fin_prdt_nm,
        'join_way': loan.join_way,
        'loan_inci_expn': loan.loan_inci_expn,
        'erly_rpay_fee': loan.erly_rpay_fee,
        'dly_rate': loan.dly_rate,
        'loan_lmt': loan.loan_lmt,
        'dcls_strt_day': loan.dcls_strt_day,
        'dcls_end_day': loan.dcls_end_day,
        'options': [{
            'mrtg_type': opt.mrtg_type,
            'mrtg_type_nm': opt.get_mrtg_type_display(),
            'rpay_type': opt.rpay_type,
            'rpay_type_nm': opt.get_rpay_type_display(),
            'lend_rate_type': opt.lend_rate_type,
            'lend_rate_type_nm': opt.get_lend_rate_type_display(),
            'lend_rate_min': opt.lend_rate_min,
            'lend_rate_max': opt.lend_rate_max,
            'lend_rate_avg': opt.lend_rate_avg,
        } for opt in loan.options.all()]
    }
    
    return Response(result)

# 전세자금대출
@api_view(['GET'])
def lease_loans(request):
    """전세자금대출 상품 목록 조회 및 DB 저장"""
    url = 'http://finlife.fss.or.kr/finlifeapi/rentHouseLoanProductsSearch.json'
    params = {
        'auth': settings.FSS_API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': request.GET.get('page', '1')
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        base_list = data.get('result', {}).get('baseList', [])
        option_list = data.get('result', {}).get('optionList', [])
        
        # DB에 데이터 저장
        for base in base_list:
            loan, created = LeaseLoan.objects.update_or_create(
                fin_co_no=base['fin_co_no'],
                fin_prdt_cd=base['fin_prdt_cd'],
                defaults={
                    'kor_co_nm': base['kor_co_nm'],
                    'fin_prdt_nm': base['fin_prdt_nm'],
                    'join_way': base['join_way'],
                    'loan_inci_expn': base['loan_inci_expn'],
                    'erly_rpay_fee': base['erly_rpay_fee'],
                    'dly_rate': base['dly_rate'],
                    'loan_lmt': base['loan_lmt'],
                    'dcls_strt_day': base['dcls_strt_day'],
                    'dcls_end_day': base['dcls_end_day'],
                    'fin_co_subm_day': base['fin_co_subm_day'],
                }
            )
            
            # 해당 상품의 옵션 정보 저장
            product_options = [opt for opt in option_list if opt['fin_prdt_cd'] == base['fin_prdt_cd']]
            for option in product_options:
                LeaseLoanOption.objects.update_or_create(
                    loan=loan,
                    fin_prdt_cd=option['fin_prdt_cd'],
                    rpay_type=option['rpay_type'],
                    lend_rate_type=option['lend_rate_type'],
                    defaults={
                        'lend_rate_min': option['lend_rate_min'],
                        'lend_rate_max': option['lend_rate_max'],
                        'lend_rate_avg': option.get('lend_rate_avg', None),
                    }
                )
        
        # 저장된 데이터 조회하여 반환
        loans = LeaseLoan.objects.all().prefetch_related('options')
        result = []
        for loan in loans:
            loan_data = {
                'id': loan.id,
                'fin_co_no': loan.fin_co_no,
                'kor_co_nm': loan.kor_co_nm,
                'fin_prdt_nm': loan.fin_prdt_nm,
                'join_way': loan.join_way,
                'loan_inci_expn': loan.loan_inci_expn,
                'erly_rpay_fee': loan.erly_rpay_fee,
                'dly_rate': loan.dly_rate,
                'loan_lmt': loan.loan_lmt,
                'dcls_strt_day': loan.dcls_strt_day,
                'dcls_end_day': loan.dcls_end_day,
                'fin_co_subm_day': loan.fin_co_subm_day,
                'options': list(loan.options.values())
            }
            result.append(loan_data)
            
        return Response(result)
        
    except requests.RequestException as e:
        return Response({
            'message': 'API 요청 실패',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def lease_loan_detail(request, loan_id):
    """전세자금대출 상품 상세 정보 조회"""
    loan = get_object_or_404(LeaseLoan, id=loan_id)
    
    result = {
        'fin_prdt_cd': loan.fin_prdt_cd,  # 추가
        'fin_co_no': loan.fin_co_no,
        'kor_co_nm': loan.kor_co_nm,
        'fin_prdt_nm': loan.fin_prdt_nm,
        'join_way': loan.join_way,
        'loan_inci_expn': loan.loan_inci_expn,
        'erly_rpay_fee': loan.erly_rpay_fee,
        'dly_rate': loan.dly_rate,
        'loan_lmt': loan.loan_lmt,
        'dcls_strt_day': loan.dcls_strt_day,
        'dcls_end_day': loan.dcls_end_day,
        'fin_co_subm_day': loan.fin_co_subm_day,
        'options': [{
            'rpay_type': opt.rpay_type,
            'rpay_type_nm': opt.get_rpay_type_display(),
            'lend_rate_type': opt.lend_rate_type,
            'lend_rate_type_nm': opt.get_lend_rate_type_display(),
            'lend_rate_min': opt.lend_rate_min,
            'lend_rate_max': opt.lend_rate_max,
            'lend_rate_avg': opt.lend_rate_avg,
        } for opt in loan.options.all()]
    }
    
    return Response(result)

### MBTI 검사
# 초기 질문 처리
def calculate_mbti_type(answers):
    """MBTI 유형 계산"""
    # 초기 질문으로 대출 종류 결정
    initial_scores = [answers.get(f'initial_q{i}', 2) for i in range(1, 4)]
    loan_type = determine_loan_type(initial_scores)
    
    try:
        if loan_type == 'M':
            return 'M' + calculate_mortgage_type(answers)
        else:
            return 'L' + calculate_lease_type(answers)
    except KeyError as e:
        raise ValueError(f'필수 답변이 누락되었습니다: {str(e)}')

# 대출 종류 결정
def determine_loan_type(initial_scores):
    """대출 종류 결정 (M/L)"""
    # 첫 번째 질문 점수가 높으면 주택담보대출
    # 세 번째 질문 점수가 높으면 전세자금대출
    mortgage_score = initial_scores[0]  # "내 소유의 집을 마련하는 것이 목표이다"
    lease_score = initial_scores[2]     # "전세 보증금 마련이 우선이다"
    
    return 'M' if mortgage_score > lease_score else 'L'

# 세부 유형 계산
# 주택담보대출인 경우
def calculate_mortgage_type(answers):
    """주택담보대출 MBTI 계산"""
    mbti = ''
    
    # F/V (Fixed/Variable) - 금리 선호도
    rate_scores = [
        answers.get('fv_q1', 2),  # "금리가 변동될 수 있다는 생각만으로도 불안하다"
        answers.get('fv_q2', 2),  # "원금이 조금 더 들더라도 고정금리가 좋다"
        answers.get('fv_q3', 2)   # "시장 금리가 떨어질 수 있는 기회는 포기하고 싶지 않다"
    ]
    # 마지막 질문은 역산
    rate_scores[2] = 4 - rate_scores[2]
    mbti += 'F' if sum(rate_scores) > 6 else 'V'
    
    # P/D (Payment/Divide) - 상환 방식
    payment_scores = [
        answers.get('pd_q1', 2),  # "매달 고정적으로 갚아나가는 것이 편하다"
        answers.get('pd_q2', 2),  # "대출 상환 계획은 처음부터 명확히 세우고 싶다"
        answers.get('pd_q3', 2)   # "목돈이 생기면 수시로 상환하고 싶다"
    ]
    # 마지막 질문은 역산
    payment_scores[2] = 4 - payment_scores[2]
    mbti += 'P' if sum(payment_scores) > 6 else 'D'
    
    # A/H (Apartment/House) - 담보 유형
    property_scores = [
        answers.get('ah_q1', 2),  # "아파트의 안정성이 가장 중요하다"
        answers.get('ah_q2', 2),  # "관리비를 내더라도 체계적인 관리가 필요하다"
        answers.get('ah_q3', 2)   # "단독주택이나 상가의 투자가치가 더 매력적이다"
    ]
    # 마지막 질문은 역산
    property_scores[2] = 4 - property_scores[2]
    mbti += 'A' if sum(property_scores) > 6 else 'H'
    
    return mbti

# 전세 자금 대출인 경우
def calculate_lease_type(answers):
    """전세자금대출 MBTI 계산"""
    mbti = ''
    
    # F/V (Fixed/Variable) - 금리 선호도 (주택담보대출과 동일한 질문 사용)
    rate_scores = [
        answers.get('fv_q1', 2),
        answers.get('fv_q2', 2),
        answers.get('fv_q3', 2)
    ]
    rate_scores[2] = 4 - rate_scores[2]
    mbti += 'F' if sum(rate_scores) > 6 else 'V'
    
    # T/S (Term/Short) - 기간
    term_scores = [
        answers.get('ts_q1', 2),  # "2년 이상 한 곳에 거주할 계획이다"
        answers.get('ts_q2', 2),  # "주거비용의 안정성이 가장 중요하다"
        answers.get('ts_q3', 2)   # "필요하면 언제든 이사할 수 있어야 한다"
    ]
    # 마지막 질문은 역산
    term_scores[2] = 4 - term_scores[2]
    mbti += 'T' if sum(term_scores) > 6 else 'S'
    
    # G/P (Government/Private) - 보증 유형
    guarantee_scores = [
        answers.get('gp_q1', 2),  # "보증료를 내더라도 안전한 상품이 좋다"
        answers.get('gp_q2', 2),  # "정부 지원 상품을 이용하고 싶다"
        answers.get('gp_q3', 2)   # "절차가 복잡해도 안전한게 중요하다"
    ]
    mbti += 'G' if sum(guarantee_scores) > 6 else 'P'
    
    return mbti


### 상품 추천 단계
# 1. API 데이터 조회
def calculate_avg_rate(scored_products):
    """평균 금리 계산"""
    if not scored_products:
        return 0
    
    total_rate = sum(
        float(product['product']['options'][0]['lend_rate_min'])
        for product in scored_products
    )
    return round(total_rate / len(scored_products), 2)

def validate_loan_data(data):
    """API 응답 데이터 유효성 검증"""
    # result 객체 확인
    if not data.get('result'):
        raise ValueError('유효하지 않은 API 응답: result 객체 없음')
    
    # baseList와 optionList 추출
    base_list = data.get('result', {}).get('baseList', [])
    option_list = data.get('result', {}).get('optionList', [])
    
    # 필수 데이터 존재 여부 확인
    if not base_list:
        raise ValueError('상품 기본 정보가 존재하지 않습니다')
    if not option_list:
        raise ValueError('상품 옵션 정보가 존재하지 않습니다')
    
    # 각 상품의 필수 필드 확인
    required_base_fields = ['fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm']
    required_option_fields = ['fin_prdt_cd', 'lend_rate_type', 'lend_rate_min', 'lend_rate_max']
    
    for base in base_list:
        if not all(field in base for field in required_base_fields):
            raise ValueError('상품 기본 정보에 필수 필드가 누락되었습니다')
            
    for option in option_list:
        if not all(field in option for field in required_option_fields):
            raise ValueError('상품 옵션 정보에 필수 필드가 누락되었습니다')
    
    return base_list, option_list

@api_view(['GET', 'POST'])
def loan_recommendation(request):
    """MBTI 검사 및 대출 상품 추천"""
    if request.method == 'POST':
        answers = request.data.get('answers', {})

    if not answers:
        return Response({
            'message': '답변이 제공되지 않았습니다.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # 1. MBTI 유형 계산
        mbti_type = calculate_mbti_type(answers)

        # 2. 대출 상품 추천
        # 대출 종류에 따른 URL 설정
        if mbti_type.startswith('M'):
            url = 'http://finlife.fss.or.kr/finlifeapi/mortgageLoanProductsSearch.json'
        else:
            url = 'http://finlife.fss.or.kr/finlifeapi/rentHouseLoanProductsSearch.json'
            
        params = {
            'auth': settings.FSS_API_KEY,
            'topFinGrpNo': '020000',
            'pageNo': '1'
        }
        
        # API 호출 및 데이터 가져오기
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # 데이터 유효성 검증
        base_list, option_list = validate_loan_data(data)
        
        # 상품 필터링 및 점수 계산
        scored_products = []
        for base in base_list:
            product_options = [opt for opt in option_list if opt['fin_prdt_cd'] == base['fin_prdt_cd']]
            if not product_options:
                continue
                
            base['options'] = product_options
            score = 0
            
            if mbti_type.startswith('M'):
                score = calculate_mortgage_score(mbti_type, base, product_options)
            else:
                score = calculate_lease_score(mbti_type, base, product_options)
                
            if score > 0:  # 최소 점수를 넘은 상품만 추가
                scored_products.append({
                    'product': base,
                    'score': score
                })

        # 점수순 정렬
        scored_products.sort(key=lambda x: x['score'], reverse=True)
            
        # 응답 데이터 구성
        response_data = {
            'mbti_result': {
                'mbti_type': mbti_type,
                'matching_criteria': get_matching_criteria(mbti_type)
            },
            'recommendations': {
                'total_count': len(scored_products),
                'products': [{
                    'product_info': item['product'],
                    'score': item['score'],
                    'matching_points': get_matching_points(mbti_type, item['product']),
                    'rate_analysis': analyze_rates(item['product']['options']),
                    'recommendation_reason': get_recommendation_reason(mbti_type, item['product'])
                } for item in scored_products[:3]]
            }
        }
        
        return Response(response_data)
        
    except requests.RequestException as e:
        return Response({
            'message': 'API 요청 실패',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'message': '처리 중 오류가 발생했습니다',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 2. 상품 점수 계산

def calculate_mortgage_score(mbti_type, product, options):
    """주택담보대출 상품 점수 계산"""
    score = 0
    max_score = 7  # 총 가중치 합
    
    # F/V (금리 유형) - 가중치 3
    rate_score = 3
    if 'F' in mbti_type:
        if any(opt['lend_rate_type'] == 'F' for opt in options):
            min_rate = min(float(opt['lend_rate_min']) for opt in options)
            rate_score = 3 if min_rate < 4.5 else 2  # 금리가 낮을수록 높은 점수
    elif 'V' in mbti_type:
        if any(opt['lend_rate_type'] == 'C' for opt in options):
            min_rate = min(float(opt['lend_rate_min']) for opt in options)
            rate_score = 3 if min_rate < 4.5 else 2
    
    score += rate_score
    
    # P/D (상환 방식) - 가중치 2
    if 'P' in mbti_type and any(opt['rpay_type'] == 'D' for opt in options):
        score += 2
    elif 'D' in mbti_type and any(opt['rpay_type'] == 'S' for opt in options):
        score += 2
    
    # A/H (담보 유형) - 가중치 2
    if 'A' in mbti_type and any(opt['mrtg_type'] == 'A' for opt in options):
        score += 2
    elif 'H' in mbti_type and any(opt['mrtg_type'] == 'E' for opt in options):
        score += 2
    
    return (score / max_score) * 100

def calculate_lease_score(mbti_type, product, options):
    """전세자금대출 상품 점수 계산"""
    score = 0
    max_score = 7  # 총 가중치 합
    
    # F/V (금리 유형) - 가중치 3
    rate_score = 3
    if 'F' in mbti_type:
        if any(opt['lend_rate_type'] == 'F' for opt in options):
            min_rate = min(float(opt['lend_rate_min']) for opt in options)
            rate_score = 3 if min_rate < 4.5 else 2  # 금리가 낮을수록 높은 점수
    elif 'V' in mbti_type:
        if any(opt['lend_rate_type'] == 'C' for opt in options):
            min_rate = min(float(opt['lend_rate_min']) for opt in options)
            rate_score = 3 if min_rate < 4.5 else 2
    
    score += rate_score
    
    # T/S (기간) - 가중치 2
    term_score = 0
    if 'T' in mbti_type and '장기' in product['fin_prdt_nm'].lower():
        term_score = 2
    elif 'S' in mbti_type and '단기' in product['fin_prdt_nm'].lower():
        term_score = 2
    score += term_score
    
    # G/P (보증 유형) - 가중치 2
    guarantee_score = 0
    if 'G' in mbti_type and '주택보증' in product['loan_inci_expn']:
        guarantee_score = 2
    elif 'P' in mbti_type and '신용보증' in product['loan_inci_expn']:
        guarantee_score = 2
    score += guarantee_score
    
    return (score / max_score) * 100

# 3. 필터링 계산

def filter_mortgage_type(mbti_type, product, options):
    """주택담보대출 MBTI 유형별 필터링"""
    if not options:
        return False
        
    score = 0
    weights = {
        'rate': 3,    # 금리 유형 가중치
        'repay': 2,   # 상환 방식 가중치
        'mortgage': 2 # 담보 유형 가중치
    }
    max_score = sum(weights.values())
    
    # F/V (금리 유형)
    if 'F' in mbti_type:
        if any(opt['lend_rate_type'] == 'F' for opt in options):
            min_rate = min(float(opt['lend_rate_min']) for opt in options)
            score += weights['rate'] if min_rate < 4.5 else weights['rate'] * 0.5
    elif 'V' in mbti_type:
        if any(opt['lend_rate_type'] == 'C' for opt in options):
            score += weights['rate']
    
    # P/D (상환 방식)
    if 'P' in mbti_type and any(opt['rpay_type'] == 'D' for opt in options):
        score += weights['repay']
    elif 'D' in mbti_type and any(opt['rpay_type'] == 'S' for opt in options):
        score += weights['repay']
    
    # A/H (담보 유형)
    if 'A' in mbti_type and any(opt['mrtg_type'] == 'A' for opt in options):
        score += weights['mortgage']
    elif 'H' in mbti_type and any(opt['mrtg_type'] == 'E' for opt in options):
        score += weights['mortgage']
    
    # 60% 이상 만족시 추천
    return (score / max_score) >= 0.6

def filter_lease_type(mbti_type, product, options):
    """전세자금대출 MBTI 유형별 필터링"""
    if not options:
        return False
        
    score = 0
    weights = {
        'rate': 3,     # 금리 유형 가중치
        'term': 2,     # 기간 가중치
        'guarantee': 2 # 보증 유형 가중치
    }
    max_score = sum(weights.values())
    
    # F/V (금리 유형)
    if 'F' in mbti_type:
        if any(opt['lend_rate_type'] == 'F' for opt in options):
            min_rate = min(float(opt['lend_rate_min']) for opt in options)
            score += weights['rate'] if min_rate < 4.5 else weights['rate'] * 0.5
    elif 'V' in mbti_type:
        if any(opt['lend_rate_type'] == 'C' for opt in options):
            score += weights['rate']
    
    # T/S (기간)
    if 'T' in mbti_type and '장기' in product['fin_prdt_nm'].lower():
        score += weights['term']
    elif 'S' in mbti_type and '단기' in product['fin_prdt_nm'].lower():
        score += weights['term']
    
    # G/P (보증 유형)
    if 'G' in mbti_type and '주택보증' in product['loan_inci_expn']:
        score += weights['guarantee']
    elif 'P' in mbti_type and '신용보증' in product['loan_inci_expn']:
        score += weights['guarantee']
    
    # 60% 이상 만족시 추천
    return (score / max_score) >= 0.6

# 4. 추천 결과 구성
def get_matching_criteria(mbti_type):
    """MBTI 유형별 매칭 기준 설명"""
    criteria = []
    
    if mbti_type.startswith('M'):  # 주택담보대출
        # 금리 선호도 (F/V)
        if 'F' in mbti_type:
            criteria.append('고정금리로 안정적인 이자 부담 선호')
        else:  # 'V'
            criteria.append('변동금리로 시장 금리 변동 기회 활용 선호')
        
        # 상환 방식 (P/D)
        if 'P' in mbti_type:
            criteria.append('매월 정해진 금액으로 계획적 상환 선호')
        else:  # 'D'
            criteria.append('자유로운 금액으로 유연한 상환 선호')
        
        # 담보 유형 (A/H)
        if 'A' in mbti_type:
            criteria.append('아파트의 안정성과 체계적 관리 선호')
        else:  # 'H'
            criteria.append('단독주택/상가의 자산가치 및 투자성 선호')
            
    else:  # 전세자금대출
        # 금리 선호도 (F/V)
        if 'F' in mbti_type:
            criteria.append('고정금리로 안정적인 이자 부담 선호')
        else:  # 'V'
            criteria.append('변동금리로 시장 금리 변동 기회 활용 선호')
        
        # 거주 기간 (T/S)
        if 'T' in mbti_type:
            criteria.append('2년 이상 장기 거주 계획')
        else:  # 'S'
            criteria.append('2년 미만 단기 거주 계획')
        
        # 보증 유형 (G/P)
        if 'G' in mbti_type:
            criteria.append('주택보증공사 등 정부 보증 상품 선호')
        else:  # 'P'
            criteria.append('민간 보증 상품 선호')
    
    return {
        'mbti_type': mbti_type,
        'criteria': criteria,
        'loan_type': '주택담보대출' if mbti_type.startswith('M') else '전세자금대출'
    }

## 기타
def get_matching_points(mbti_type, product):
    """상품과 MBTI 유형 간의 매칭 포인트 분석"""
    points = []
    
    if mbti_type.startswith('M'):  # 주택담보대출
        # 금리 분석
        if float(product['options'][0]['lend_rate_min']) < 4.5:
            points.append('낮은 금리 상품')
            
        # 상환 방식
        if 'P' in mbti_type and any(opt['rpay_type'] == 'D' for opt in product['options']):
            points.append('원리금균등분할상환 가능')
            
        # 담보 유형
        if 'A' in mbti_type and any(opt['mrtg_type'] == 'A' for opt in product['options']):
            points.append('아파트 담보 특화 상품')
    else:  # 전세자금대출
        # 금리 분석
        if float(product['options'][0]['lend_rate_min']) < 4.5:
            points.append('낮은 금리 상품')
            
        # 기간
        if 'T' in mbti_type and '장기' in product['fin_prdt_nm'].lower():
            points.append('장기 거주자 특화 상품')
            
        # 보증 유형
        if 'G' in mbti_type and '주택보증' in product['loan_inci_expn']:
            points.append('정부 보증 상품')
    
    return points

def analyze_rates(options):
    """금리 정보 분석"""
    return {
        'min_rate': min(float(opt['lend_rate_min']) for opt in options),
        'max_rate': max(float(opt['lend_rate_max']) for opt in options),
        'avg_rate': sum(float(opt['lend_rate_avg']) for opt in options if opt['lend_rate_avg']) / len(options) if any(opt['lend_rate_avg'] for opt in options) else None,
        'rate_type': options[0]['lend_rate_type_nm']
    }

def get_recommendation_reason(mbti_type, product):
    """추천 이유 설명"""
    reasons = []
    
    if mbti_type.startswith('M'):  # 주택담보대출
        if 'F' in mbti_type and any(opt['lend_rate_type'] == 'F' for opt in product['options']):
            reasons.append('고정금리로 안정적인 이자 부담')
        if 'P' in mbti_type and any(opt['rpay_type'] == 'D' for opt in product['options']):
            reasons.append('계획적인 상환으로 장기 재무 설계 가능')
        if 'A' in mbti_type and any(opt['mrtg_type'] == 'A' for opt in product['options']):
            reasons.append('아파트 담보의 안정성')
    else:  # 전세자금대출
        if 'F' in mbti_type and any(opt['lend_rate_type'] == 'F' for opt in product['options']):
            reasons.append('고정금리로 안정적인 이자 부담')
        if 'T' in mbti_type and '장기' in product['fin_prdt_nm'].lower():
            reasons.append('장기 거주자를 위한 안정적인 상품')
        if 'G' in mbti_type and '주택보증' in product['loan_inci_expn']:
            reasons.append('정부 보증으로 안전한 상품')
    
    return reasons

def get_best_options(mbti_type, scored_products):
    """최적 옵션 추천"""
    if not scored_products:
        return []
        
    # 점수순 정렬
    sorted_products = sorted(scored_products, key=lambda x: x['score'], reverse=True)
    
    best_options = []
    for product in sorted_products[:3]:  # 상위 3개 상품
        option = {
            'product_name': product['product']['fin_prdt_nm'],
            'company': product['product']['kor_co_nm'],
            'score': product['score'],
            'min_rate': min(float(opt['lend_rate_min']) for opt in product['product']['options'])
        }
        best_options.append(option)
    
    return best_options


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
