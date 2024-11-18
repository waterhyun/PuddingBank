from django.db import models
from django.core.validators import MinValueValidator

class BaseProduct(models.Model):
    """기본 금융 상품 정보"""
    fin_prdt_cd = models.CharField(max_length=100, unique=True)  # 금융 상품 코드
    kor_co_nm = models.CharField(max_length=100)  # 금융회사명
    fin_prdt_nm = models.CharField(max_length=100)  # 금융 상품명
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'base_products'

class DepositProduct(models.Model):
    """정기예금 상품 정보"""
    product = models.OneToOneField(
        BaseProduct,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    interest_rate = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )  # 기본 금리
    max_interest_rate = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )  # 최고 우대금리
    save_trm = models.IntegerField()  # 저축 기간 (단위: 개월)
    intr_rate_type_nm = models.CharField(max_length=100)  # 저축금리유형
    intr_rate2 = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )  # 최고 우대금리
    join_way = models.TextField()  # 가입방법
    join_member = models.TextField()  # 가입대상
    etc_note = models.TextField()  # 기타 유의사항

    class Meta:
        db_table = 'deposit_products'

class RentHouseLoan(models.Model):
    """전세자금대출 상품 정보"""
    product = models.OneToOneField(
        BaseProduct,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    loan_rate_type = models.CharField(max_length=100)  # 대출금리유형
    loan_interest_rate = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )  # 대출금리
    max_loan_amount = models.IntegerField(
        validators=[MinValueValidator(0)]
    )  # 최대대출한도
    loan_period = models.IntegerField(
        validators=[MinValueValidator(0)]
    )  # 대출기간
    repayment_type = models.CharField(max_length=100)  # 상환방식
    requirement = models.TextField()  # 가입요건
    guarantee_type = models.CharField(max_length=100)  # 담보유형

    class Meta:
        db_table = 'rent_house_loans'

class UserProduct(models.Model):
    """사용자 가입 상품 정보"""
    STATUS_CHOICES = [
        ('ACTIVE', '유지중'),
        ('EXPIRED', '만기'),
        ('CANCELED', '해지')
    ]
    PRODUCT_CHOICES = [
        ('DEPOSIT', '정기예금'),
        ('RENT_LOAN', '전세자금대출')
    ]

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='user_products'
    )
    product = models.ForeignKey(
        BaseProduct,
        on_delete=models.CASCADE,
        related_name='product_users'
    )
    subscription_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )
    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_CHOICES
    )

    class Meta:
        db_table = 'user_products'