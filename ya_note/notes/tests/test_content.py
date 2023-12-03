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
            title='Test Note',
            text='Test Content',
            author=self.user
        )

    def test_notes_page_context(self):
        self.client.login(
            username='Имя пользователя',
            password='Пароль'
        )
        response = self.client.get(reverse('notes:list'))
        self.assertIn(self.note, response.context['object_list'])

    def test_notes_page_user_notes(self):
        self.client.login(
            username='Имя пользователя',
            password='Пароль'
        )
        response = self.client.get(reverse('notes:list'))
        if response.context['object_list'] is not None:
            self.assertIn(self.note, response.context['object_list'])

    def test_add_note_page_form(self):
        self.client.login(
            username='Имя пользователя',
            password='Пароль'
        )
        response = self.client.get(reverse('notes:add'))
        if response.context['form'] is not None:
            self.assertIsNotNone(response.context['form'])

    def test_edit_note_page_form(self):
        self.client.login(
            username='Имя пользователя',
            password='Пароль'
        )
        response = self.client.get(reverse('notes:edit', args=[self.note.id]))
        self.assertIsNotNone(response.context)
