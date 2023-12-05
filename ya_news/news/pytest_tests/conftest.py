import pytest

from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from news.models import News, Comment


User = get_user_model()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def auth_client(client, user):
    auth_user = client.force_login(user)
    return auth_user


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
def home_url():
    reverse('news:home')


@pytest.fixture
def detail_page_url():
    reverse('news:detail', args=[news.id])


@pytest.fixture
def edit_comment_url():
    reverse('news:edit', args=[comment.id])


@pytest.fixture
def delete_comment_url():
    reverse('news:delete', args=[comment.id])


@pytest.fixture
def sign_up_user_url():
    reverse('users:signup')


@pytest.fixture
def login_user_url():
    reverse('users:login')


@pytest.fixture
def logout_user_url():
    reverse('users:logout')


@pytest.fixture
def create_news(title, text):
    return News.objects.create(title=title, text=text)


@pytest.fixture
def news_list():
    news = [News(title=f'Какое-то название новости {i}',
                 text='какая-то новость') for i in range(settings.CREATE_NEWS)]
    return News.objects.bulk_create(news)
