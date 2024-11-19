from django.db import models

class Exchange(models.Model):
    result = models.IntegerField()  # 조회 결과
    cur_unit = models.CharField(max_length=10)  # 통화 코드
    cur_nm = models.CharField(max_length=100)  # 국가/통화명
    ttb = models.FloatField(null=True, blank=True)  # 전신환 매입율,  외화 → 원화 
    tts = models.FloatField(null=True, blank=True)  # 전신환 매도율
    deal_bas_r = models.FloatField(null=True, blank=True)  # 매매 기준율
    bkpr = models.FloatField(null=True, blank=True)  # 장부 가격
    yy_efee_r = models.FloatField(null=True, blank=True)  # 연 환가료율
    ten_dd_efee_r = models.FloatField(null=True, blank=True)  # 10일 환가료율
    kftc_bkpr = models.FloatField(null=True, blank=True)  # 서울외국환중개 장부가격
    kftc_deal_bas_r = models.FloatField(null=True, blank=True)  # 서울외국환중개 매매기준율
    update_date = models.DateField() # 데이터 불러온 날짜
    def __str__(self):
        return f"{self.cur_unit} - {self.cur_nm}"
    
    class Meta:
        db_table = 'exchanges'