from django.db import models
from django.conf import settings

class Article(models.Model):
    """게시글 모델"""
    CATEGORY_CHOICES = [
        ('NOTICE', '공지'),  
        ('FREE', '자유'),   
        ('QUESTION', '질문'),  
        ('RECOMMEND', '추천'), 
    ] 

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='FREE'  # 기본값 설정 (자유)
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_articles',
        blank=True
    )

    class Meta:
        db_table = 'articles'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

class Comment(models.Model):
    """댓글 모델"""
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'
        ordering = ['created_at']

    def __str__(self):
        return self.content[:30]