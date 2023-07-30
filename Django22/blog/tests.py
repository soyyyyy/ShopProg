from django.test import TestCase, Client

from bs4 import BeautifulSoup
from .models import Post, Category

from django.contrib.auth.models import User


# Create your tests here.
class TestView(TestCase):

    #TestCase 기본 설정
    def setUp(self):
        self.client = Client()    #Client 클래스를 통해 실제 경로의 뷰와 매치해서 테스트를 진행

        #매번 test할 때마다 생성하지 않고 미리 만들어 놓는 방법임
        self.user_kim = User.objects.create_user(username="kim", password="somepassword")
        self.user_lee = User.objects.create_user(username="lee", password="somepassword")

        self.category_com = Category.objects.create(name="computer", slug="computer")
        self.category_cul = Category.objects.create(name="culture", slug="culture")

        self.post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다.",
                                       author=self.user_kim,
                                       category=self.category_com)
        self.post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다.",
                                       author=self.user_lee,
                                       category=self.category_cul)
        self.post_003 = Post.objects.create(title="세번째 포스트", content="두번째 포스트입니다.",
                                       author=self.user_lee)


    # navbar가 정상적으로 보이는지
    def nav_test(self, soup):

        navbar = soup.nav
        #Blog, AboutMe라는 문구가 navbar에 있음
        self.assertIn('Blog', navbar.text)
        self.assertIn('AboutMe', navbar.text)

        #navbar 버튼 href 링크 연결하기
        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], "/")

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], "/blog/")

        about_btn = navbar.find('a', text='AboutMe')
        self.assertEqual(about_btn.attrs['href'], "/about_me/")

    def category_test(self, soup):
        category_card = soup.find('div', id='category-card')
        self.assertIn('Categories', category_card.text)
        self.assertIn(f'{self.category_com} ({self.category_com.post_set.count()})', category_card.text)
        self.assertIn(f'{self.category_cul} ({self.category_cul.post_set.count()})', category_card.text)
        self.assertIn(f'미분류 (1)', category_card.text)

    def test_post_list(self):
        #포스트 목록 가져오기
        response = self.client.get('/blog/')

        # response 결과가 정상적인지 확인 (정상 로드)
        self.assertEqual(response.status_code, 200) #안정된건지 test?

        # title이 정상적으로 보이는지  test, 페이지 title이 Blog
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')

        # navbar가 정상적으로 보이는지
        #navbar = soup.nav
        #self.assertIn('Blog', navbar.text)
        #self.assertIn('About Me', navbar.text)
        self.nav_test(soup)
        self.category_test(soup)

        #Post가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        main_area = soup.find('div', id="main-area")
        self.assertIn(self.post_001.title, main_area.text)
        self.assertIn(self.post_002.title, main_area.text)

        self.assertIn(self.post_001.author.username.upper(), main_area.text)
        self.assertIn(self.post_002.author.username.upper(), main_area.text)
        self.assertNotIn('아무 게시물이 없습니다.', main_area.text)


        #Post가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        main_area = soup.find('div', id="main-area")
        self.assertIn('아무 게시물이 없습니다.', main_area.text)
        
        #2. Post가 있는 경우
        #post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다.",
        #                               author=self.user_kim)
        #post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다.",
        #                               author=self.user_lee)


    def test_post_detail(self):
        #post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다",
        #                               author=self.user_kim)

        #포스트 url
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        #첫 번째 포스트 정상 접근 확인
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # navbar가 정상적으로 보이는지
        self.nav_test(soup)
        #navbar = soup.nav
        #self.assertIn('Blog', navbar.text)
        #self.assertIn('About Me', navbar.text)

        #첫 번째 포스트의 제목이 웹 브라우저 탭 타이틀에 있다.
        self.assertIn(self.post_001.title, soup.title.text)

        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.post_001.content, post_area.text)
        self.assertIn(self.post_001.author.username.upper(), post_area.text)

