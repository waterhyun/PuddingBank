from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.core.validators import MinValueValidator
from datetime import date

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    birthdate = serializers.DateField()

    class Meta:
        model = User
        fields = (
            'id', 
            'username', 
            'password',
            'password_confirm',
            'email',
            'birthdate',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at',)

    def validate(self, data):
        # 비밀번호 일치 검증
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        
        # 생년월일 유효성 검사
        if data.get('birthdate'):
            if data['birthdate'] > date.today():
                raise serializers.ValidationError("올바른 생년월일을 입력해주세요.")
            
        return data

    def create(self, validated_data):
        # password_confirm 필드 제거
        validated_data.pop('password_confirm', None)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            birthdate=validated_data.get('birthdate'),
        )
        Token.objects.create(user=user)
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    """사용자 정보 수정을 위한 시리얼라이저"""
    class Meta:
        model = User
        fields = (
            'email',
            'birthdate',
        )


# accounts/serializers.py에 UserUpdateSerializer 추가
class UserUpdateSerializer(serializers.ModelSerializer):
    """사용자 정보 수정을 위한 시리얼라이저"""
    class Meta:
        model = User
        fields = ('email', 'birthdate')
        
    def validate_email(self, value):
        """이메일 중복 검사"""
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("이미 사용 중인 이메일입니다.")
        return value

    def update(self, instance, validated_data):
        """사용자 정보 업데이트"""
        instance.email = validated_data.get('email', instance.email)
        instance.birthdate = validated_data.get('birthdate', instance.birthdate)
        instance.save()
        return instance