#-*- coding:utf-8 -*-
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase

from blogpost.views import index, view_post
from blogpost.models import Blogpost
from datetime import datetime
# Create your tests here.
#######################################单元测试#################################
class HomePageTest(TestCase):
    #保证我们的route可以和我们的URL对应上
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)
    #测试页面的标题是不是我们想要的结果
    def test_home_page_returns_correct_html(self):
            request = HttpRequest()
            response = index(request)
            self.assertIn(b'<title>Welcome to my blog</title>', response.content)

class BlogpostTest(TestCase):
    #测试是否调用某个函数的方法
    def test_blogpost_url_resolves_to_blog_post_view(self):
        found = resolve('/blog/this_is_a_test.html')
        self.assertEqual(found.func, view_post)
    #创建一个数据，然后访问相应的页面来看是否正确。
    def test_blogpost_create_with_view(self):
        Blogpost.objects.create(title='hello', author='admin', slug='this_is_a_test', body='This is a blog',
                                posted=datetime.now)
        response = self.client.get('/blog/this_is_a_test.html')
        self.assertIn(b'This is a blog', response.content)
    #创建了一篇博客，然后在首页测试返回的内容中是否含有This is a blog。
    def test_blogpost_create_with_show_in_homepage(self):
        Blogpost.objects.create(title='hello', author='admin', slug='this_is_a_test', body='This is a blog',
                                posted=datetime.now)
        response = self.client.get('/')
        self.assertIn(b'This is a blog', response.content)

##########################################自动化测试################################
from django.test import LiveServerTestCase
from selenium import webdriver

class HomepageTestCase(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firfox()
        self.selenium.maximize_window()
        super(HomepageTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(HomepageTestCase, self).tearDown()

    def test_visit_homepage(self):
        self.selenium.get('%s%s'%(self.live_server_url, "/"))
        self.assertIn("Welcome to my blog", self.selenium.title)


class BlogpostDetailCase(LiveServerTestCase):
    def setUp(self):
        Blogpost.objects.create(
            title='hello',
            author='admin',
            slug='this_is_a_test',
            body='This is a blog',
            posted=datetime.now
        )

        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        super(BlogpostDetailCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(BlogpostDetailCase, self).tearDown()

    def test_visit_blog_post(self):
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/blog/this_is_a_test.html")
        )

        self.assertIn("hello", self.selenium.title)


class BlogpostFromHomepageCase(LiveServerTestCase):
    def setUp(self):
        Blogpost.objects.create(
            title='hello',
            author='admin',
            slug='this_is_a_test',
            body='This is a blog',
            posted=datetime.now
        )

        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        super(BlogpostFromHomepageCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(BlogpostFromHomepageCase, self).tearDown()

    def test_visit_blog_post(self):
        self.selenium.get(
            '%s%s' % (self.live_server_url,  "/")
        )

        self.selenium.find_element_by_link_text("hello").click()
        self.assertIn("hello", self.selenium.title)
