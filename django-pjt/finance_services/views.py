from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404, render

# Create your views here.
@api_view(['GET', 'POST'])
def article_list_create(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializers = ArticleListSerializer(articles, many=True)
        return Response(serializers.data)
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
