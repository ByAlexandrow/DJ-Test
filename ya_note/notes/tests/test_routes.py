from http import HTTPStatus

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


HOME_PAGE = reverse('notes:list')
ADD_NOTE_PAGE = reverse('notes:add')
EDIT_NOTE_PAGE = reverse('notes:edit', args=('slug',))
DELETE_NOTE_PAGE = reverse('notes:delete', args=('slug',))
DETAIL_NOTE_PAGE = reverse('notes:detail', args=('slug',))
SIGNUP_PAGE = reverse('users:signup')
LOGIN_PAGE = reverse('users:login')
LOGOUT_PAGE = reverse('users:logout')


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client()
        cls.user = User.objects.create_user(
            username='Имя пользователя',
            password='Пароль'
        )
        return super().setUpTestData()

    def setUp(self):
        self.client.login(
            username='Имя пользователя',
            password='Пароль'
        )

    def test_pages(self):
        test_cases = [
            [HOME_PAGE, self.client, HTTPStatus.OK],
            [ADD_NOTE_PAGE, self.client, HTTPStatus.OK],
            [SIGNUP_PAGE, self.client, HTTPStatus.OK],
            [LOGIN_PAGE, self.client, HTTPStatus.OK],
            [LOGOUT_PAGE, self.client, HTTPStatus.OK],
        ]

        for url, client, expected_status in test_cases:
            with self.subTest(url=url):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_redirects(self):
        test_cases = [
            [reverse('notes:edit', args=[1]), self.client,
             HTTPStatus.NOT_FOUND, '/login/?next=/notes/1/edit/'],
            [reverse('notes:delete', args=[1]), self.client,
             HTTPStatus.NOT_FOUND, '/login/?next=/notes/1/delete/'],
            [reverse('notes:detail', args=[1]), self.client,
             HTTPStatus.NOT_FOUND, '/login/?next=/notes/1/'],
        ]
        for url, client, expected_status, expected_url in test_cases:
            with self.subTest(url=url):
                response = client.get(url)
                if expected_status == HTTPStatus.FOUND:
                    self.assertRedirects(response, expected_url,
                                         status_code=expected_status)
                else:
                    self.assertEqual(response.status_code, expected_status)
