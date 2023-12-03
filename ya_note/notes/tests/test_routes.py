from http import HTTPStatus
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from notes.models import Note


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='Имя пользователя',
                                             password='Пароль')

    def test_home_page(self):
        response = self.client.get(reverse('notes:home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_notes_page(self):
        self.client.login(username='Пользователь', password='Пароль')
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_add_note(self):
        self.client.login(username='Пользователь', password='Пароль')
        response = self.client.get(reverse('notes:add'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_note_detail_page(self):
        self.client.login(username='Пользователь', password='Пароль')
        note = Note.objects.create(
            title='Название заметки',
            text='Текст заметки',
            author=self.user
        )
        response = self.client.get(reverse('notes:detail', args=[note.id]))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_edit_note(self):
        self.client.login(username='Пользователь', password='Пароль')
        note = Note.objects.create(
            title='Назание заметки',
            text='Текст заметки',
            author=self.user
        )
        response = self.client.get(reverse('notes:edit', args=[note.id]))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_delete_note(self):
        self.client.login(username='Пользователь', password='Пароль')
        note = Note.objects.create(
            title='Название заметки',
            text='Текст заметки',
            author=self.user
        )
        response = self.client.get(reverse('notes:delete', args=[note.id]))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_login_page(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)

    def test_logout_page(self):
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 200)
