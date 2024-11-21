from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

User = get_user_model()

from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(required=True)
    birthdate = serializers.DateField(required=True)
    phone = serializers.CharField(required=False, allow_blank=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'name': self.validated_data.get('name', ''),
            'birthdate': self.validated_data.get('birthdate', ''),
            'phone': self.validated_data.get('phone', ''),
        })
        return data

    def save(self, request):
        user = super().save(request)
        user.name = self.validated_data.get('name', '')
        user.birthdate = self.validated_data.get('birthdate')
        user.phone = self.validated_data.get('phone', '')
        user.save()
        return user

    def validate(self, data):
        # 기본 유효성 검사
        data = super().validate(data)
        
        # birthdate 필수 필드 검사
        if not data.get('birthdate'):
            raise serializers.ValidationError({
                "birthdate": "생년월일은 필수 입력 항목입니다."
            })
            
        # name 필수 필드 검사
        if not data.get('name'):
            raise serializers.ValidationError({
                "name": "이름은 필수 입력 항목입니다."
            })

        # 이메일 중복 검사
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError({
                "email": "이미 사용 중인 이메일입니다."
            })
        
        # 이름 중복 검사
        if User.objects.filter(name=data.get('name')).exists():
            raise serializers.ValidationError({
                "name": "이미 사용 중인 이름입니다."
            })
            
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'name',
            'email',
            'birthdate',
            'phone',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'birthdate', 'name', 'phone')
        extra_kwargs = {
            'email': {'required': False},
            'birthdate': {'required': False},
            'name': {'required': False},
            'phone': {'required': False},
        }
        
    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("이미 사용 중인 이메일입니다.")
        return value
        
    def validate_name(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(name=value).exists():
            raise serializers.ValidationError("이미 사용 중인 이름입니다.")
        return value