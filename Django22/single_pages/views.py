from django.shortcuts import render
from blog.models import Post

# Create your views here.
#함수 정의

def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]  # 0,1,2
    return render(request, 'single_pages/landing.html', {
        'recent_posts' : recent_posts
    })

def about_me(request):
    return render(request, 'single_pages/about_me.html')

#단순 html만 전달 -> blog.views와 다르게 인자 전달 필요가 X