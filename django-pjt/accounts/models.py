from django.db import models
from django.contrib.auth.models import AbstractUser
from products.models import BaseProduct

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    # username은 AbstractUser에서 이미 제공하므로 재정의 불필요
    name = models.CharField(max_length=100, unique=True)      # 화면 표시용 이름
    # email은 AbstractUser에서 이미 제공
    # password는 AbstractUser에서 이미 제공
    birthdate = models.DateField(null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # AbstractUser의 불필요한 필드 제거
    first_name = None
    last_name = None

    @property
    def subscribed_products(self):
        return BaseProduct.objects.filter(
            product_users__user=self,
            product_users__status='ACTIVE'
        )

    class Meta:
        db_table = 'users'
        # dj-rest-auth를 위한 설정 추가
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username