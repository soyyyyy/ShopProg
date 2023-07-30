from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing),
    path('about_us/', views.about_us),
    path('my_page/', views.my_page),
]