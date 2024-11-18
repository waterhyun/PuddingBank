from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.core.validators import MinValueValidator
from products.models import BaseProduct

# accounts/models.py
class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    birthdate = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 가입한 상품 조회를 위한 property
    @property
    def subscribed_products(self):
        return BaseProduct.objects.filter(
            product_users__user=self,
            product_users__status='ACTIVE'
        )

    class Meta:
        db_table = 'users'