from rest_framework import serializers
from .models import Article, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    """댓글 시리얼라이저"""
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'article',
            'user',
            'username',
            'content',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('article', 'user')

class ArticleListSerializer(serializers.ModelSerializer):
    """게시글 목록 시리얼라이저"""
    username = serializers.CharField(source='user.username', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)

    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'username',
            'comment_count',
            'like_count',
            'created_at'
        )

class ArticleSerializer(serializers.ModelSerializer):
    """게시글 상세 시리얼라이저"""
    username = serializers.CharField(source='user.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like_users_count = serializers.IntegerField(source='like_users.count', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            'id',
            'user',
            'username',
            'title',
            'content',
            'comments',
            'like_users_count',
            'is_liked',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('user', 'like_users')

    def get_is_liked(self, obj):
        """현재 사용자의 좋아요 여부"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_users.filter(id=request.user.id).exists()
        return False