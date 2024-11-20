"""
URL configuration for base project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    # API 버전 1
    path('api/v1/', include([
        # 게시글 관련
        path('articles/', include('articles.urls')),
        # 금융 상품 관련
        path('products/', include('products.urls')),
        # 위치 서비스 관련
        path('locations/', include('locations.urls')),
        # 환율 정보 관련
        path('exchanges/', include('exchanges.urls')),
        # dj-rest-auth URLs
        path('accounts/', include([
            path('', include('dj_rest_auth.urls')),
            path('signup/', include('dj_rest_auth.registration.urls')),
            path('', include('accounts.urls')),
        ])),
    ])),
]