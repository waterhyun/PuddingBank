# accounts/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404


@api_view(['POST'])
@permission_classes([AllowAny])  # 인증되지 않은 사용자도 접근 가능
def signup(request):
    """
    회원가입 View
    POST 요청으로 username, password, email을 받아 새로운 사용자 생성
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user=user)
        # 성공 응답 반환 (201 Created)
        return Response({
            'token': token.key,
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny]) # 인증되지 않은 사용자도 접근 가능
def login(request):
    """
    로그인 View
    POST 요청으로 username과 password를 받아 사용자 인증
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    # username이나 password가 없는 경우
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                    status=status.HTTP_400_BAD_REQUEST)
    
     # 사용자 인증
    user = authenticate(username=username, password=password)
    
    # 인증 실패 시
    if not user:
        return Response({'error': 'Invalid credentials'},
                    status=status.HTTP_404_NOT_FOUND)
    
    # 토큰 가져오기 또는 생성 (이미 있으면 가져오고, 없으면 새로 생성)
    token, _ = Token.objects.get_or_create(user=user)
    
    # 사용자 정보 직렬화
    serializer = UserSerializer(user)
    
    # 성공 응답 반환
    return Response({
        'token': token.key,
        'user': serializer.data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    로그아웃 View
    현재 사용자의 인증 토큰을 삭제
    """
    request.user.auth_token.delete()
    return Response({'message': '로그아웃되었습니다.'}, 
                   status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    프로필 조회 View
    현재 로그인된 사용자의 정보를 반환
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profile_update(request):
    """
    프로필 수정 View
    현재 로그인된 사용자의 정보를 수정
    """
    serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def profile_delete(request):
    """
    회원 탈퇴 View
    현재 로그인된 사용자의 계정을 삭제
    """
    user = request.user
    user.delete()
    return Response({'message': '회원 탈퇴가 완료되었습니다.'}, 
                   status=status.HTTP_204_NO_CONTENT)