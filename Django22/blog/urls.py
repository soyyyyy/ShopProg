from django.urls import path
from . import views

#리스트에 연결할거? 명시해주기 / 새로운 페이지에 대해 url먼저 선언해야함

urlpatterns = [ # IP주소/blog
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),    #/blog/pk -> 정수 형태의 pk일 경우 PostDetail 클래스 사용
    path('<int:pk>/new_comment/', views.new_comment),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('category/<str:slug>/', views.category_page),  #카테고리 url연결 - IP주소/blog/category/slug
    path('tag/<str:slug>/', views.tag_page),    #IP주소/blog/tag/slug
    path('search/<str:q>/', views.PostSearch.as_view())




    #FBV방법
    #path('', views.index),
    #path('<int:pk>/', views.single_post_page)
]

