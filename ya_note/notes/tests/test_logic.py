from http import HTTPStatus
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from notes.models import Note


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='Имя пользователя',
            password='Пароль'
        )
        self.note = Note.objects.create(
            title='Название заметки',
            text='Текст',
            author=self.user
        )

    def test_create_note_logged_in(self):
        self.client.login(
            username='Имя пользователя',
            password='Пароль'
        )
        response = self.client.post(
            reverse('notes:add'),
            {'title': 'Название заметки', 'text': 'Текст заметки'})
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_note_anonymous(self):
        self.client.logout()
        response = self.client.post(
            reverse('notes:add'),
            {'title': 'Имя заметки', 'text': 'Текст заметки'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_create_note_duplicate_slug(self):
        self.client.login(username='Имя пользоателя', password='Пароль')
        response = self.client.post(
            reverse('notes:add'),
            {'title': 'Имя заметки', 'text': 'Текст заметки'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_edit_note_own(self):
        self.client.login(username='Имя пользователя', password='Пароль')
        response = self.client.post(
            reverse('notes:edit', args=[self.note.id]),
            {'title': 'Имя заметки', 'text': 'Текст заметки'})
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_edit_note_other(self):
        other_user = User.objects.create_user(
            username='Новый пользователь',
            password='Пароль'
        )
        other_note = Note.objects.create(
            title='Имя заметки',
            text='Текст заметки',
            author=other_user
        )
        self.client.login(username='Имя пользователя', password='Пароль')
        response = self.client.post(
            reverse('notes:edit', args=[other_note.id]),
            {'title': 'Название заметки', 'text': 'Текст заметки'})
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
