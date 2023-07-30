from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)   #사람이 읽을 수 있는 텍스트로 고유의 url을 만들고 싶을 때

    def __str__(self):
        return self.name

    def get_absolute_url(self):   #고유 url 부여
        return f'/blog/category/{self.slug}'

    class Meta:  #복수형 직접 지정
        verbose_name_plural = 'Categories'


class Post(models.Model):  #Post 모델은 models.Model 클래스를 확장해서 만든 클래스 -> settings.py에 생성한 앱 추가
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True) #중간 타이틀, 미리보기 제공
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    # %Y 2022(네자리 표현), %y 22(두자리 표현)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True) #새 글 작성시 현재 시간 자동 저장 -> post 작성시 시간 입력란이 안 보임
    updated_at = models.DateTimeField(auto_now=True)  #마지막 저장 시점 자동 저장

    #추후 author 작성
    #포스트와 유저 연결
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    #카테고리
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __str__(self):    #포스트 제목 등 목록에 출력
        return f'[{self.pk}] {self.title}:: {self.author} : {self.created_at}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name) #file 이름만 출력(경로x)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1] # '.' 기준으로 분리 -> 두개의 split이 배열형태로 전달
        #a.txt -> a txt
        #b.docx -> b docx
        #c.xlsx -> c xlsx
        #a.b.c.txt -> a b c txt [-1]: 제일 마지막 원소

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} : {self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'