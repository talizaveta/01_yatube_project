from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post
from ..forms import PostForm

User = get_user_model()


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(slug='test_slug')
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group
        )
        cls.form = PostForm()

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_form(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст из формы',
            'group': self.group.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.user.username}))
        self.assertEqual(Post.objects.count(), posts_count+1)
        self.assertTrue(
            Post.objects.filter(
                text='Текст из формы',
                group=self.group.id
            ).exists()
        )

    # при отправке валидной формы со страницы создания поста
    # reverse('posts:create_post')
    # создаётся новая запись в базе данных;
    # при отправке валидной формы со страницы редактирования поста
    # reverse('posts:post_edit', args=('post_id',))
    # происходит изменение поста с post_id в базе данных.
    def test_edit(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Отредактированный текст',
            'group': self.group.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        self.assertEquals(Post.objects.count(), posts_count)
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        self.assertTrue(
            Post.objects.filter(
                text='Отредактированный текст',
                group=self.group.id
            ).exists()
        )

    def test_guest_user(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст неавторизованного пользователя',
            'group': self.group.id
        }
        response = self.guest_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertFalse(
            Post.objects.filter(
                text='Текст неавторизованного пользователя',
                group=self.group.id
            ).exists()
        )
        self.assertEquals(Post.objects.count(), posts_count)
