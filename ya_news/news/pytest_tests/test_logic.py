import pytest
from http import HTTPStatus
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_anonymous_user_cannot_post_comment(client, news):
    url = reverse('news:edit', args=[news.id])
    response = client.post(url, {'text': 'Текст комментария'})
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
def test_authenticated_user_can_post_comment(client, user, news):
    client.force_login(user)
    url = reverse('news:edit', args=[news.id])
    response = client.post(url, {'text': 'Какой-то текст'})
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_comment_with_bad_words_isnt_posted(client, user, news):
    client.force_login(user)
    url = reverse('news:edit', args=[news.id])
    response = client.post(url, {'text': 'Запрещенные слова'})
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_author_can_edit_his_own_comments(client, user, comment):
    client.force_login(user)
    url = reverse('news:edit', args=[comment.id])
    response = client.post(url, {'text': 'Отредактированный комментарий'})
    assert response.status_code == 302


@pytest.fixture
@pytest.mark.django_db
def test_user_cant_edit_other_comment(client, comment):
    other_user = User.objects.create_user(username='Имя пользователя',
                                          password='Пароль')
    client.force_login(other_user)
    url = reverse('news:edit', args=[comment.id])
    response = client.post(url, {'text': 'Отредактированный текст'})
    assert response.status_code == HTTPStatus.FORBIDDEN
