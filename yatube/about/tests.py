from django.test import Client, TestCase
from http import HTTPStatus


class StaticPagesURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_url_template_location(self):
        templates_url_name = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }
        for path, template in templates_url_name.items():
            with self.subTest(path=path):
                response = self.guest_client.get(path)
                self.assertEquals(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)
