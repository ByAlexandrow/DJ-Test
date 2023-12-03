import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model
from news.models import News, Comment


User = get_user_model()


@pytest.fixture
def client():
    from django.test.client import Client
    return Client()


@pytest.fixture
def news():
    return News.objects.create(title='Заголовок', text='Что-то здесь')


@pytest.fixture
def comment(news, user):
    return Comment.objects.create(news=news, author=user,
                                  text='Какой-то комментарий')


@pytest.fixture
def user():
    return User.objects.create_user(username='Имя пользоателя',
                                    password='какой-то пароль')


@pytest.fixture
def url_edit(comment):
    return reverse('news:edit', args=[comment.id])


@pytest.fixture
def url_delete(comment):
    return reverse('news:delete', args=[comment.id])
