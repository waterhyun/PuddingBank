from rest_framework import serializers
from .models import BaseProduct, DepositProduct, RentHouseLoan, UserProduct

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

class RentHouseLoanSerializer(serializers.ModelSerializer):
    """전세자금대출 상품 정보 시리얼라이저"""
    product = BaseProductSerializer(read_only=True)
    
    class Meta:
        model = RentHouseLoan
        fields = (
            'product',
            'loan_rate_type',
            'loan_interest_rate',
            'max_loan_amount',
            'loan_period',
            'repayment_type',
            'requirement',
            'guarantee_type'
        )
        read_only_fields = ('product',)

    def create(self, validated_data):
        product_id = self.context.get('product_id')
        if product_id:
            base_product = BaseProduct.objects.get(id=product_id)
            rent_loan = RentHouseLoan.objects.create(
                product=base_product,
                **validated_data
            )
            return rent_loan
        raise serializers.ValidationError("BaseProduct ID is required")

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
        if user:
            user_product = UserProduct.objects.create(
                user=user,
                **validated_data
            )
            return user_product
        raise serializers.ValidationError("User is required")

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

class RentHouseLoanListSerializer(serializers.ModelSerializer):
    """전세자금대출 상품 목록 조회용 시리얼라이저"""
    product = BaseProductSerializer()
    
    class Meta:
        model = RentHouseLoan
        fields = (
            'product',
            'loan_rate_type',
            'loan_interest_rate',
            'max_loan_amount'
        )