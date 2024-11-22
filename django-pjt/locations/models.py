# locations/models.py
from django.db import models

class Bank(models.Model):
    """은행 정보 모델"""
    # id = models.AutoField(primary_key=True)  # 자동 증가하는 기본 키
    place_name = models.CharField(max_length=100)  # 은행명
    address_name = models.CharField(max_length=200)  # 전체 지번 주소
    road_address_name = models.CharField(max_length=200, null=True, blank=True)  # 전체 도로명 주소
    phone = models.CharField(max_length=20, null=True, blank=True)  # 전화번호
    place_url = models.URLField(max_length=200)  # 장소 상세페이지 URL
    category_name = models.CharField(max_length=100)  # 카테고리 이름
    category_group_code = models.CharField(max_length=10)  # 중요 카테고리만 그룹핑한 카테고리 그룹 코드
    category_group_name = models.CharField(max_length=100)  # 중요 카테고리만 그룹핑한 카테고리 그룹명
    x = models.DecimalField(max_digits=20, decimal_places=16)  # X 좌표값 (경도)
    y = models.DecimalField(max_digits=20, decimal_places=16)  # Y 좌표값 (위도)
    distance = models.IntegerField(null=True, blank=True)  # 중심좌표까지의 거리 (미터)

    class Meta:
        db_table = 'banks'
        ordering = ['distance']

    def __str__(self):
        return f"{self.place_name} ({self.address_name})"