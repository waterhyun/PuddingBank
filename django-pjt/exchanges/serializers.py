from rest_framework import serializers
from .models import Exchange


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'  # 모든 필드를 포함
        # ['cur_unit', 'cur_nm', 'deal_bas_r']
