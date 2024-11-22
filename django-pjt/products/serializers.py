from rest_framework import serializers
from .models import BaseProduct, DepositProduct, UserProduct, MortgageLoan, LeaseLoan

class BaseProductSerializer(serializers.ModelSerializer):
    """기본 금융 상품 정보 시리얼라이저"""
    class Meta:
        model = BaseProduct
        fields = (
            'id',
            'fin_prdt_cd',
            'kor_co_nm',
            'fin_prdt_nm',
            'created_at',
            'updated_at'
        )

class DepositProductSerializer(serializers.ModelSerializer):
    """정기예금 상품 정보 시리얼라이저"""
    product = BaseProductSerializer(read_only=True)
    
    class Meta:
        model = DepositProduct
        fields = (
            'product',
            'interest_rate',
            'max_interest_rate',
            'save_trm',
            'intr_rate_type_nm',
            'intr_rate2',
            'join_way',
            'join_member',
            'etc_note'
        )

    def create(self, validated_data):
        product = self.context.get('product')
        if not product:
            raise serializers.ValidationError("BaseProduct is required")
        
        deposit_product = DepositProduct.objects.create(
            product=product,
            **validated_data
        )
        return deposit_product


class UserProductSerializer(serializers.ModelSerializer):
    """사용자 가입 상품 정보 시리얼라이저"""
    product = BaseProductSerializer(read_only=True)
    
    class Meta:
        model = UserProduct
        fields = (
            'id',
            'user',
            'product',
            'subscription_date',
            'status',
            'product_type'
        )
        read_only_fields = ('user', 'subscription_date')


    def create(self, validated_data):
        user = self.context.get('user')
        if not user:
            raise serializers.ValidationError("User is required")
            
        user_product = UserProduct.objects.create(
            user=user,
            **validated_data
        )
        return user_product

class DepositProductListSerializer(serializers.ModelSerializer):
    """정기예금 상품 목록 조회용 시리얼라이저"""
    product = BaseProductSerializer()
    
    class Meta:
        model = DepositProduct
        fields = (
            'product',
            'interest_rate',
            'max_interest_rate',
            'save_trm'
        )

### 주택담보대출

class MortgageLoanOptionSerializer(serializers.Serializer):
    """주택담보대출 옵션 정보 시리얼라이저"""
    mrtg_type = serializers.CharField()  # 담보유형 코드
    mrtg_type_nm = serializers.CharField()  # 담보유형명
    rpay_type = serializers.CharField()  # 대출상환유형 코드
    rpay_type_nm = serializers.CharField()  # 대출상환유형명
    lend_rate_type = serializers.CharField()  # 대출금리유형 코드
    lend_rate_type_nm = serializers.CharField()  # 대출금리유형명
    lend_rate_min = serializers.DecimalField(max_digits=4, decimal_places=2)  # 대출금리_최저
    lend_rate_max = serializers.DecimalField(max_digits=4, decimal_places=2)  # 대출금리_최고
    lend_rate_avg = serializers.DecimalField(max_digits=4, decimal_places=2)  # 전월 취급 평균금리

class MortgageLoanSerializer(serializers.Serializer):
    """주택담보대출 상품 정보 시리얼라이저"""
    fin_prdt_cd = serializers.CharField()  # 금융상품코드
    kor_co_nm = serializers.CharField()  # 금융회사명
    fin_prdt_nm = serializers.CharField()  # 금융상품명
    loan_inci_expn = serializers.CharField()  # 대출부대비용
    erly_rpay_fee = serializers.CharField()  # 중도상환수수료
    dly_rate = serializers.CharField()  # 연체이자율
    loan_lmt = serializers.CharField()  # 대출한도
    options = MortgageLoanOptionSerializer(many=True)  # 옵션 정보

### 전세자금대출

class LeaseLoanOptionSerializer(serializers.Serializer):
    """전세자금대출 옵션 정보 시리얼라이저"""
    rpay_type = serializers.CharField()  # 대출상환유형 코드
    rpay_type_nm = serializers.CharField()  # 대출상환유형명
    lend_rate_type = serializers.CharField()  # 대출금리유형 코드
    lend_rate_type_nm = serializers.CharField()  # 대출금리유형명
    lend_rate_min = serializers.DecimalField(max_digits=4, decimal_places=2)  # 대출금리_최저
    lend_rate_max = serializers.DecimalField(max_digits=4, decimal_places=2)  # 대출금리_최고
    lend_rate_avg = serializers.DecimalField(max_digits=4, decimal_places=2)  # 전월 취급 평균금리

class LeaseLoanSerializer(serializers.Serializer):
    """전세자금대출 상품 정보 시리얼라이저"""
    fin_prdt_cd = serializers.CharField()  # 금융상품코드
    kor_co_nm = serializers.CharField()  # 금융회사명
    fin_prdt_nm = serializers.CharField()  # 금융상품명
    loan_inci_expn = serializers.CharField()  # 대출부대비용
    erly_rpay_fee = serializers.CharField()  # 중도상환수수료
    dly_rate = serializers.CharField()  # 연체이자율
    loan_lmt = serializers.CharField()  # 대출한도
    options = LeaseLoanOptionSerializer(many=True)  # 옵션 정보

### 추천 서비스

class LoanRecommendationSerializer(serializers.Serializer):
    """대출 상품 추천 결과 시리얼라이저"""
    mbti_type = serializers.CharField()  # MBTI 유형
    recommended_products = serializers.SerializerMethodField()

    def get_recommended_products(self, obj):
        if obj['mbti_type'].startswith('M'):
            return MortgageLoanSerializer(obj['products'], many=True).data
        return LeaseLoanSerializer(obj['products'], many=True).data