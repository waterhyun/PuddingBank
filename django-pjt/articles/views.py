from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer
from .models import Article, Comment

# Create your views here.
@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 허용
def article_list_create(request):
    # 전체 게시글 조회
    if request.method == 'GET':
        articles = Article.objects.all()
        serializers = ArticleListSerializer(articles, many=True)
        return Response(serializers.data)
    # 게시글 추가 
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save() 
            return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, article_id):
    """게시글 조회, 수정, 삭제 및 댓글 조회"""

    # 게시글 가져오기
    article = get_object_or_404(Article, pk=article_id)

    if request.method == 'GET':
            # 게시글 및 댓글 조회
            article_serializer = ArticleSerializer(article)
            comments = Comment.objects.filter(article=article)
            comment_serializer = CommentSerializer(comments, many=True)
            data = article_serializer.data
            data['comments'] = comment_serializer.data
            return Response(data)

    elif request.method == 'PUT':
        # 게시글 수정
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save() # 추가 user=request.user
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


    elif request.method == 'DELETE':
        # 게시글 삭제
        article.delete() 
        return Response({"message": "Article deleted successfully"})

@api_view(['POST'])
# @permission_classes([IsAuthenticated])  # 로그인 사용자만 접근 가능
def comment_create(request, article_id):
    """댓글 추가"""
    article = get_object_or_404(Article, pk=article_id)  # 게시글 가져오기
    serializer = CommentSerializer(data=request.data)  # 요청 데이터 직렬화
    if serializer.is_valid(raise_exception=True):
        serializer.save(article=article)  # 댓글 생성 시 게시글 연결 # 추가 : user=request.user
        return Response(serializer.data, status=201)  # 성공 응답

@api_view(['PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])  # 로그인 사용자만 접근 가능
def comment_detail(request, comment_id):
    """댓글 수정 및 삭제"""
    comment = get_object_or_404(Comment, pk=comment_id)

    # 요청자가 댓글 작성자인지 확인
    # if comment.user != request.user:
    #     raise PermissionDenied("You do not have permission to modify or delete this comment.")

    if request.method == 'PUT':
        # 댓글 수정
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        # 댓글 삭제
        comment.delete()
        return Response({"message": "Comment deleted successfully"})