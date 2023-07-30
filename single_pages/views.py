from django.shortcuts import render

from django.shortcuts import render
from shop.models import Item, Comment

# Create your views here.

def landing(request):
    recent_items = Item.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/landing.html', {
        'recent_items' : recent_items
    })

def about_us(request):
    return render(request, 'single_pages/about_us.html')

def my_page(request):
    comment_list = Comment.objects.order_by('-pk')
    return render(request, 'single_pages/my_page.html', {
        'comment_list' : comment_list
    })


