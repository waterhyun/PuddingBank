from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer
from .models import Article, Comment

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def article_list_create(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializers = ArticleListSerializer(articles, many=True)
        return Response(serializers.data)
    
    elif request.method == 'POST':
        # context에 request를 추가하여 serializer 생성
        serializer = ArticleSerializer(
            data=request.data, 
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])  # GET은 누구나, PUT/DELETE는 인증된 사용자만
def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if request.method == 'GET':
        article_serializer = ArticleSerializer(article)
        comments = Comment.objects.filter(article=article)
        comment_serializer = CommentSerializer(comments, many=True)
        data = article_serializer.data
        data['comments'] = comment_serializer.data
        return Response(data)

    # PUT, DELETE 요청에 대해서만 인증 확인
    if not request.user.is_authenticated:
        raise PermissionDenied("Authentication required for this action.")

    # 작성자 본인만 수정/삭제 가능
    if request.method in ['PUT', 'DELETE']:
        if article.user != request.user:
            raise PermissionDenied("You do not have permission to modify this article.")
        
        if request.method == 'PUT':
            serializer = ArticleSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        
        elif request.method == 'DELETE':
            article.delete()
            return Response({"message": "Article deleted successfully"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    serializer = CommentSerializer(
        data=request.data,
        context={
            'request': request,
            'article': article
        }
    )
    if serializer.is_valid(raise_exception=True):
        serializer.save(
            article=article,
            user=request.user
        )
        return Response(serializer.data, status=201)
    


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_id):
    try:
        comment = get_object_or_404(Comment, pk=comment_id)
    except Comment.DoesNotExist:
        return Response(
            {"error": "Comment not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # 요청자가 댓글 작성자인지 확인
    if comment.user != request.user:
        raise PermissionDenied("You do not have permission to modify this comment.")

    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        comment.delete()
        return Response({"message": "Comment deleted successfully"})
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def article_like(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    
    # 현재 사용자가 이미 좋아요를 눌렀는지 확인
    if request.user in article.like_users.all():
        # 좋아요 취소
        article.like_users.remove(request.user)
        liked = False
    else:
        # 좋아요 추가
        article.like_users.add(request.user)
        liked = True
    
    return Response({
        'liked': liked,
        'like_count': article.like_users.count()
    })