from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='auth')
        cls.group = Group.objects.create(
            slug='test_slug'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            id=1111
        )

    def setUp(self) -> None:
        self.guest_client = Client()  # Создаем экземпляр клиента
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)  # Авторизуем пользователя

    def test_pages_exists_at_desired_location(self):
        """Страницы доступны пользователям"""
        urls = {
            '/': self.guest_client,
            '/groups/test_slug/': self.guest_client,
            '/profile/auth/': self.guest_client,
            '/posts/1111/': self.guest_client,
            '/create/': self.authorized_client,
            '/posts/1111/edit/': self.authorized_client
        }
        for path, client in urls.items():
            with self.subTest(path=path):
                response = client.get(path)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_redirect(self):
        """Редирект пользователей"""
        not_author = User.objects.create(username='not_auth')
        not_author_client = Client()
        not_author_client.force_login(not_author)
        urls = {
            ('/auth/login/?next=/create/', '/create/', self.guest_client,),
            ('/auth/login/?next=/posts/1111/edit/', '/posts/1111/edit/', self.guest_client),
            ('/posts/1111/', '/posts/1111/edit/', not_author_client),
            ('/profile/auth/', '/posts/1111/delete/', self.authorized_client),
        }
        for redirect, path, client in urls:
            with self.subTest(path=path):
                response = client.get(path, follow=True)
                self.assertRedirects(response, redirect)

    def test_unexisting_page(self):
        """Запрос к несуществующей странице"""
        response = self.guest_client.get('/unexisting_page/404/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_urls_names = {
            '/': 'posts/index.html',
            '/groups/test_slug/': 'posts/group_list.html',
            '/profile/auth/': 'posts/profile.html',
            '/posts/1111/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            '/posts/1111/edit/': 'posts/create_post.html'
        }
        for path, template_name in templates_urls_names.items():
            with self.subTest(path=path):
                response = self.authorized_client.get(path)
                self.assertTemplateUsed(response, template_name)
