from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


# тесты для:
# verbose_name
# help_text
# __str__  - это строчка с содержимым group.title
# __str__ для post
class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create()
        cls.post = Post.objects.create(
            text='Длиииинный тестовый текст',
            author=cls.user,
            group=cls.group
        )

    def test_verbose_name(self):
        """Verbose_name полей модели Post совпадает с ожидаемым"""
        post = PostModelTest.post
        group = PostModelTest.group
        field_verboses = {
            ('text', 'Текст поста', post),
            ('pub_date', 'Дата публикации', post),
            ('author', 'Автор', post),
            ('group', 'Группа', post),
            ('title', 'Название', group),
            ('slug', 'Слаг', group),
            ('description', 'Описание', group)
        }
        for field, expected_value, class_name in field_verboses:
            with self.subTest(field=field):
                verbose = class_name._meta.get_field(field).verbose_name
                self.assertEquals(verbose, expected_value)

    def test_help_text(self):
        """Help_text полей модели Post совпадает с ожидаемым"""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                help_text = post._meta.get_field(field).help_text
                self.assertEquals(help_text, expected_value)

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        group = PostModelTest.group
        post = PostModelTest.post
        expected_str = {
            group: group.title,
            post: post.text[:15]
        }
        for obj, expected in expected_str.items():
            with self.subTest(obj=obj):
                self.assertEquals(expected, str(obj))
