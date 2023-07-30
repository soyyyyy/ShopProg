"""myDjangoPrj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static

#장고 프로젝트의 url -> 각 앱에서 사용하는 url 주소를 리스트에 추가

urlpatterns = [ #IP주소/
    path('admin/', admin.site.urls),  # IP주소/admin  #앞 형태로 접속하면 뒤 주소로 연결함
    path('blog/', include('blog.urls')),   # IP주소/blog
    path('', include('single_pages.urls')),  # IP주소/
    path('accounts/', include('allauth.urls'))
]

#미디어 파일을 위한 url 저장하기
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#대문페이지 IP/
#블로그 목록 IP/blog
#블로그 상세 IP/blog/포스트 pk
#자기소기 IP/about_me

