from django import forms
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class FormModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            slug='test_slug'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group
        )

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """View-функции используют ожидаемые HTML-шаблоны"""
        templates_urls_names = {
            (reverse('posts:index')): 'posts/index.html',
            (reverse('posts:group_list', kwargs={'slug': self.group.slug})):
                'posts/group_list.html',
            (reverse('posts:profile', kwargs={'username': self.user.username})):
                'posts/profile.html',
            (reverse('posts:post_detail', kwargs={'post_id': self.post.id})):
                'posts/post_detail.html',
            (reverse('posts:post_create')): 'posts/create_post.html',
            (reverse('posts:post_edit', kwargs={'post_id': self.post.id})):
                'posts/create_post.html',
        }
        for reverse_name, template in templates_urls_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон сформирован с правильным контекстом."""
        reverse_names = {
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user.username})
        }
        for reverse_name in reverse_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                first_object = response.context['page_obj'][0]
                post_author_0 = str(first_object.author)
                post_text_0 = str(first_object.text)
                post_group_0 = str(first_object.group)
                post_image_0 = str(first_object.image)
                self.assertEqual(post_author_0, f'{FormModelTest.post.author}')
                self.assertEqual(post_text_0, f'{FormModelTest.post.text}')
                self.assertEqual(post_group_0, f'{FormModelTest.post.group}')
                self.assertEqual(post_image_0, f'{FormModelTest.post.image}')

    def test_view(self):
        pages_names_filters = {
            (reverse('posts:group_list', kwargs={'slug': self.group.slug}),
             'group', self.group),
            (reverse('posts:profile', kwargs={'username': self.user.username}),
             'author', self.post.author),
            (reverse('posts:post_detail', kwargs={'post_id': self.post.id}),
             'post', self.post),
        }
        for reverse_name, context_name, expected in pages_names_filters:
            response = self.authorized_client.get(reverse_name)
            self.assertEqual(response.context.get(context_name), expected)

    def test_view_create(self):
        reverse_name = reverse('posts:post_create')
        response = self.authorized_client.get(reverse_name)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_view_edit(self):
        reverse_name = reverse('posts:post_edit', kwargs={'post_id': self.post.id})
        response = self.authorized_client.get(reverse_name)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_create(self):
        """При создании поста с группой, он появляется на страницах"""
        reverse_names = {
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user.username})
        }
        for reverse_name in reverse_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(len(response.context['page_obj']), 1)

    def test_post_not(self):
        Group.objects.create(slug="test_slug_2")
        reverse_name = reverse('posts:group_list', kwargs={'slug': 'test_slug_2'})
        response = self.authorized_client.get(reverse_name)
        self.assertEqual(len(response.context['page_obj']), 0)


class PaginatorViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        cls.group = Group.objects.create(slug='test_slug')
        for i in range(13):
            Post.objects.create(
                author=cls.user,
                group=cls.group
            )

    def setUp(self) -> None:
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_paginator(self):
        post_amount = 10
        reverse_names = {
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user.username})
        }
        for reverse_name in reverse_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(len(response.context['page_obj']), post_amount)

    def test_second_page_contains_three_records(self):
        post_amount = 3
        reverse_names = {
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user.username})
        }
        for reverse_name in reverse_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name + '?page=2')
                self.assertEqual(len(response.context['page_obj']), post_amount)


class CacheTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        cls.group = Group.objects.create(slug='test_slug')
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group
        )

    def setUp(self) -> None:
        self.guest_client = Client()
        cache.clear()

    def test_cache(self):
        """Тестирование кеширования главной страницы."""
        response = self.guest_client.get(reverse('posts:index'))
        self.post.delete()
        response_2 = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(response.content, response_2.content)
        cache.clear()
        response_3 = self.guest_client.get(reverse('posts:index'))
        self.assertNotEqual(response.content, response_3.content)
