from http import HTTPStatus

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from notes.models import Note


ADD_NOTE_PAGE = reverse('notes:add')
# EDIT_NOTE_PAGE = reverse('notes:edit')
NOTE_CONTAINS = {'title': 'Название заметки', 'text': 'Текст заметки'}


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client()
        cls.user = User.objects.create_user(
            username='Имя пользователя',
            password='Пароль'
        )
        cls.note = Note.objects.create(
            title='Название заметки',
            text='Текст заметки',
            author=cls.user
        )
        return super().setUpTestData()

    def setUp(self):
        self.client.login(
            username='Имя пользователя',
            password='Пароль'
        )

    def test_create_note_logged_in(self):
        self.client.login(
            username='Имя пользователя',
            password='Пароль'
        )
        response = self.client.post(
            ADD_NOTE_PAGE,
            NOTE_CONTAINS)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        note = Note.objects.get(title='Название заметки')
        self.assertEqual(note.text, 'Текст заметки')
        self.assertEqual(note.author, self.user)

    def test_create_note_anonymous(self):
        initial_note_count = Note.objects.count()
        self.client.logout()
        response = self.client.post(
            ADD_NOTE_PAGE,
            NOTE_CONTAINS)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), initial_note_count)
        note = Note.objects.get(title='Название заметки')
        self.assertEqual(note.text, 'Текст заметки')
        self.assertEqual(note.author, self.user)

    def test_create_note_duplicate_slug(self):
        initial_note_count = Note.objects.count()
        self.client.login(username='Имя пользоателя', password='Пароль')
        response = self.client.post(
            ADD_NOTE_PAGE,
            NOTE_CONTAINS)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Note.objects.count(), initial_note_count)
        note = Note.objects.get(title='Название заметки')
        self.assertEqual(note.text, 'Текст заметки')
        self.assertEqual(note.author, self.user)

    def test_edit_note_own(self):
        self.client.login(username='Имя пользователя', password='Пароль')
        response = self.client.post(
            reverse('notes:edit', args=[self.note.id]),
            NOTE_CONTAINS)
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
            NOTE_CONTAINS)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
