from django.db import models


class BaseProduct(models.Model):
    """기본 금융 상품 정보"""
    fin_prdt_cd = models.CharField(max_length=100, unique=True)  # 금융 상품 코드
    kor_co_nm = models.CharField(max_length=100)  # 금융회사명
    fin_prdt_nm = models.CharField(max_length=100)  # 금융 상품명
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'base_products'

class DepositProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True) # 금융상품코드
    kor_co_nm = models.TextField()              # 금융회사명
    fin_prdt_nm = models.TextField()            # 금융상품명
    etc_note = models.TextField()               # 금융 상품 설명
    join_deny = models.IntegerField()           # 가입제한(1:제한없음, 2:서민전용, 3:일부제한)
    join_member = models.TextField()            # 가입대상
    join_way = models.TextField()               # 가입방법
    spcl_cnd = models.TextField()               # 우대조건

    class Meta:
        db_table = 'deposit_products'

class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)  # 외래키
    fin_prdt_cd = models.TextField()                                        # 금융 상품 코드
    intr_rate_type_nm = models.CharField(max_length=100)                    # 저축금리 유형명
    intr_rate = models.FloatField(default= -1)                                         # 저축금리
    intr_rate2 = models.FloatField(default= -1)                                        # 최고우대금리
    save_trm = models.IntegerField()                                        # 저축기간(단위: 개월)

    class Meta:
        db_table = 'deposit_options'

class SavingProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True) # 금융상품코드
    kor_co_nm = models.TextField()              # 금융회사명
    fin_prdt_nm = models.TextField()            # 금융상품명
    etc_note = models.TextField()               # 금융 상품 설명
    join_deny = models.IntegerField()           # 가입제한(1:제한없음, 2:서민전용, 3:일부제한)
    join_member = models.TextField()            # 가입대상
    join_way = models.TextField()               # 가입방법
    spcl_cnd = models.TextField()               # 우대조건

    class Meta:
        db_table = 'saving_products'

class SavingOptions(models.Model):
    product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE)  # 외래키
    fin_prdt_cd = models.TextField()                                        # 금융 상품 코드
    intr_rate_type_nm = models.CharField(max_length=100)                    # 저축금리 유형명
    intr_rate = models.FloatField(default= -1)                                         # 저축금리
    intr_rate2 = models.FloatField(default= -1)                                        # 최고우대금리
    save_trm = models.IntegerField()                                        # 저축기간(단위: 개월)

    class Meta:
        db_table = 'saving_options'


class Wishlist(models.Model):
    """유저가 찜한 상품 정보"""
    user = models.ForeignKey('accounts.User', 
                             on_delete=models.CASCADE)  # 사용자와 연결
    deposit_product = models.ForeignKey(
        DepositProducts, on_delete=models.CASCADE, null=True, blank=True
    )  # 예금 상품 (선택적)
    saving_product = models.ForeignKey(
        SavingProducts, on_delete=models.CASCADE, null=True, blank=True
    )  # 적금 상품 (선택적)
    added_at = models.DateTimeField(auto_now_add=True)  # 찜한 날짜

    class Meta:
        db_table = 'wishlist'
        unique_together = ('user', 'deposit_product', 'saving_product')  # 동일 사용자 중복 방지



# 주택담보대출
from django.db import models

class MortgageLoan(models.Model):
    """주택담보대출 상품 기본 정보"""
    fin_co_no = models.CharField(max_length=20, help_text='금융회사 코드')
    kor_co_nm = models.CharField(max_length=100, help_text='금융회사명')
    fin_prdt_cd = models.CharField(max_length=100, help_text='금융상품 코드')
    fin_prdt_nm = models.CharField(max_length=200, help_text='금융상품명')
    join_way = models.CharField(max_length=300, help_text='가입방법')
    loan_inci_expn = models.TextField(help_text='대출부대비용')
    erly_rpay_fee = models.TextField(help_text='중도상환수수료')
    dly_rate = models.TextField(help_text='연체이자율')
    loan_lmt = models.TextField(help_text='대출한도')
    dcls_strt_day = models.CharField(max_length=8, help_text='공시 시작일')
    dcls_end_day = models.CharField(max_length=8, null=True, blank=True, help_text='공시 종료일')
    fin_co_subm_day = models.CharField(max_length=8, help_text='금융회사 제출일')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('fin_co_no', 'fin_prdt_cd')
        indexes = [
            models.Index(fields=['fin_co_no', 'fin_prdt_cd']),
        ]

    def __str__(self):
        return f"{self.kor_co_nm} - {self.fin_prdt_nm}"

class MortgageLoanOption(models.Model):
    """주택담보대출 상품 옵션 정보"""
    MORTGAGE_TYPES = (
        ('A', '아파트'),
        ('E', '아파트외')
    )
    
    REPAY_TYPES = (
        ('D', '분할상환방식'),
        ('S', '만기일시상환방식')
    )
    
    RATE_TYPES = (
        ('F', '고정금리'),
        ('C', '변동금리')
    )

    loan = models.ForeignKey(
        MortgageLoan, 
        on_delete=models.CASCADE, 
        related_name='options'
    )
    
    fin_prdt_cd = models.CharField(
        max_length=100,
        help_text='금융상품 코드'
    )
    
    mrtg_type = models.CharField(
        max_length=1, 
        choices=MORTGAGE_TYPES,
        help_text='담보유형'
    )
    rpay_type = models.CharField(
        max_length=1, 
        choices=REPAY_TYPES,
        help_text='상환방식'
    )
    lend_rate_type = models.CharField(
        max_length=1, 
        choices=RATE_TYPES,
        help_text='금리유형'
    )
    lend_rate_min = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='최저금리'
    )
    lend_rate_max = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='최고금리'
    )
    lend_rate_avg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='평균금리'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['loan', 'fin_prdt_cd', 'mrtg_type', 'rpay_type', 'lend_rate_type']),
        ]

    def __str__(self):
        return f"{self.loan.fin_prdt_nm} - {self.get_mrtg_type_display()} {self.get_rpay_type_display()}"

# 전세자금대출
class LeaseLoan(models.Model):
    """전세자금대출 상품 기본 정보"""
    fin_co_no = models.CharField(max_length=20, help_text='금융회사 코드')
    kor_co_nm = models.CharField(max_length=100, help_text='금융회사명')
    fin_prdt_cd = models.CharField(max_length=100, help_text='금융상품 코드')
    fin_prdt_nm = models.CharField(max_length=200, help_text='금융상품명')
    join_way = models.CharField(max_length=300, help_text='가입방법')
    loan_inci_expn = models.TextField(help_text='대출부대비용')
    erly_rpay_fee = models.TextField(help_text='중도상환수수료')
    dly_rate = models.TextField(help_text='연체이자율')
    loan_lmt = models.TextField(help_text='대출한도')
    dcls_strt_day = models.CharField(max_length=8, help_text='공시 시작일')
    dcls_end_day = models.CharField(max_length=8, null=True, blank=True, help_text='공시 종료일')
    fin_co_subm_day = models.CharField(max_length=8, help_text='금융회사 제출일')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products_leaseloan'
        indexes = [
            models.Index(fields=['fin_co_no', 'fin_prdt_cd']),
        ]

    def __str__(self):
        return f"{self.kor_co_nm} - {self.fin_prdt_nm}"

class LeaseLoanOption(models.Model):
    """전세자금대출 상품 옵션 정보"""    
    REPAY_TYPES = (
        ('D', '분할상환방식'),
        ('S', '만기일시상환방식')
    )
    
    RATE_TYPES = (
        ('F', '고정금리'),
        ('C', '변동금리')
    )

    loan = models.ForeignKey(
        LeaseLoan, 
        on_delete=models.CASCADE, 
        related_name='options'
    )
    
    fin_prdt_cd = models.CharField(
        max_length=100,
        help_text='금융상품 코드'
    )
    
    rpay_type = models.CharField(
        max_length=1, 
        choices=REPAY_TYPES,
        help_text='상환방식'
    )
    lend_rate_type = models.CharField(
        max_length=1, 
        choices=RATE_TYPES,
        help_text='금리유형'
    )
    lend_rate_min = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='최저금리'
    )
    lend_rate_max = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='최고금리'
    )
    lend_rate_avg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='평균금리'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products_leaseloan_option'
        indexes = [
            models.Index(fields=['loan', 'fin_prdt_cd', 'rpay_type', 'lend_rate_type']),
        ]

    def __str__(self):
        return f"{self.loan.fin_prdt_nm} - {self.get_rpay_type_display()} {self.get_lend_rate_type_display()}"
