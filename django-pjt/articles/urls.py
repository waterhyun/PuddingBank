from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # 전체 게시글 및 게시글 추가
    path('', views.article_list_create), 
    # 게시글 상세 및 댓글 포함(조회, 수정, 삭제)
    path('<int:article_id>/', views.article_detail, name='article_detail'),
    # 댓글 추가
    path('<int:article_id>/comments/', views.comment_create, name='comment_create'), 
    # 댓글 수정/ 삭제
    path('comments/<int:comment_id>/', views.comment_detail, name='comment_detail'),
    # 게시글 좋아요 토글
    path('<int:article_id>/like/', views.article_like, name='article_like'),
    # 내가 쓴 댓글
    path('my_comments/<int:user_id>/', views.my_comments, name='my_comments'),
]
