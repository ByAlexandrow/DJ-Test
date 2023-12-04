from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm


HOME_PAGE = reverse('notes:list')
ADD_NOTE_PAGE = reverse('notes:add')
# EDIT_NOTE_PAGE = reverse('notes:edit')


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client()
        cls.user = User.objects.create_user(
            username='Имя пользователя',
            password='Пароль'
        )
        cls.note = Note.objects.create(
            title='Test Note',
            text='Test Content',
            author=cls.user
        )
        return super().setUpTestData()

    def setUp(self) -> None:
        self.client.login(
            username='Имя пользователя',
            password='Пароль'
        )
        return super().setUp()

    def test_notes_page_context(self):
        response = self.client.get(HOME_PAGE)
        self.assertIn(self.note, response.context['object_list'])

    def test_notes_page_user_notes(self):
        response = self.client.get(HOME_PAGE)
        if response.context['object_list'] is not None:
            self.assertIn(self.note, response.context['object_list'])

    def test_add_note_page_form(self):
        response = self.client.get(ADD_NOTE_PAGE)
        if response.context['form'] is not None:
            self.assertIsInstance(response.context['form'], NoteForm)

    def test_edit_note_page_form(self):
        response = self.client.get(reverse('notes:edit', args=[self.note.id]))
        self.assertIsNotNone(response.context)
