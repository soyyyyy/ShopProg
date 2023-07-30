from django.contrib import admin
from .models import Post, Category, Tag, Comment

# Register your models here.
#admin 페이지에 모델 추가
admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )} #모델의 name 필드에 값이 입력됐을 때 자동으로 slug 생성

admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Tag, TagAdmin)

admin.site.register(Comment)