from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, UserUpdateSerializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.http import JsonResponse


User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """프로필 조회"""
    try:
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': '프로필 조회 중 오류가 발생했습니다.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profile_update(request):
    """프로필 수정"""
    serializer = UserUpdateSerializer(
        request.user, 
        data=request.data, 
        partial=True,
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def profile_delete(request):
    """회원 탈퇴"""
    try:
        user = request.user
        user.delete()
        return Response(
            {'message': '회원 탈퇴가 완료되었습니다.'}, 
            status=status.HTTP_204_NO_CONTENT
        )
    except Exception as e:
        return Response(
            {'error': '회원 탈퇴 처리 중 오류가 발생했습니다.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """비밀번호 변경"""
    try:
        user = request.user
        old_password = request.data.get('old_password')
        new_password1 = request.data.get('new_password1')
        new_password2 = request.data.get('new_password2')
        
        # 현재 비밀번호 확인
        if not user.check_password(old_password):
            return Response(
                {'error': '현재 비밀번호가 일치하지 않습니다.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 새 비밀번호 일치 여부 확인
        if new_password1 != new_password2:
            return Response(
                {'error': '새 비밀번호가 일치하지 않습니다.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user.set_password(new_password1)
        user.save()
        
        return Response(
            {'message': '비밀번호가 성공적으로 변경되었습니다.'}, 
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': '비밀번호 변경 중 오류가 발생했습니다.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def login_view(request):
    # 로그인 로직 처리 후
    token = Token.objects.get(user=user)
    # 세션에 토큰 저장
    request.session['auth_token'] = token.key
    return JsonResponse({'token': token.key})