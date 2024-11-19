# locations/serializers.py
from rest_framework import serializers
from .models import Bank

class BankListSerializer(serializers.ModelSerializer):
    """은행 목록 조회용 시리얼라이저"""
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Bank
        fields = (
            'id',
            'place_name',
            'address_name',
            'road_address_name',
            'phone',
            'distance',
            'x',
            'y'
        )

    def get_distance(self, obj):
        """거리를 km 단위로 변환"""
        if obj.distance:
            return f"{obj.distance/1000:.1f}km"
        return None

class BankDetailSerializer(serializers.ModelSerializer):
    """은행 상세 정보 시리얼라이저"""
    class Meta:
        model = Bank
        fields = (
            'id',
            'place_name',
            'address_name',
            'road_address_name',
            'phone',
            'place_url',
            'category_name',
            'category_group_name',
            'x',
            'y',
            'distance'
        )

class KakaoLocalSerializer(serializers.Serializer):
    """카카오 로컬 API 응답 시리얼라이저"""
    place_name = serializers.CharField()
    address_name = serializers.CharField()
    road_address_name = serializers.CharField(allow_null=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    place_url = serializers.URLField()
    category_name = serializers.CharField()
    category_group_code = serializers.CharField()
    category_group_name = serializers.CharField()
    x = serializers.DecimalField(max_digits=20, decimal_places=16)
    y = serializers.DecimalField(max_digits=20, decimal_places=16)
    distance = serializers.IntegerField(allow_null=True)

    def create(self, validated_data):
        return Bank.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance