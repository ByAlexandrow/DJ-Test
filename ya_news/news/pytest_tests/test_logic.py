import pytest
from http import HTTPStatus
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_post_comment(client, news):
    initial_comment_count = Comment.objects.count()
    url = reverse('news:edit', args=[news.id])
    response = client.post(url, {'text': 'Текст комментария'})
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == initial_comment_count


@pytest.fixture
@pytest.mark.django_db
def test_authenticated_user_can_post_comment(auth_client, news):
    initial_comment_count = Comment.objects.count()
    url = reverse('news:edit', args=[news.id])
    response = auth_client.post(url, {'text': 'Какой-то текст'})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == initial_comment_count + 1
    comment = Comment.objects.last()
    assert comment.text == 'Какой-то текст'


@pytest.fixture
@pytest.mark.django_db
def test_comment_with_bad_words_isnt_posted(auth_client, news):
    initial_comment_count = Comment.objects.count()
    url = reverse('news:edit', args=[news.id])
    response = auth_client.post(url, {'text': 'Запрещенные слова'})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == initial_comment_count


@pytest.fixture
@pytest.mark.django_db
def test_author_can_edit_his_own_comments(auth_client, user,
                                          comment, news, date):
    url = reverse('news:edit', args=[comment.id])
    response = auth_client.post(url, {'text': 'Отредактированный комментарий'})
    assert response.status_code == HTTPStatus.FOUND
    comment.refresh_from_db()
    assert comment.text == 'Отредактированный комментарий'
    assert comment.author == user
    assert comment.news == news
    assert comment.date == date


@pytest.fixture
@pytest.mark.django_db
def test_user_cant_edit_other_comment(auth_client, comment):
    initial_text = comment.text
    url = reverse('news:edit', args=[comment.id])
    response = auth_client.post(url, {'text': 'Отредактированный текст'})
    assert response.status_code == HTTPStatus.FORBIDDEN
    comment.refresh_from_db()
    assert comment.text == initial_text


@pytest.fixture
@pytest.mark.django_db
def test_user_can_delete_his_own_comment(auth_client, comment):
    url = reverse('news:delete', args=[comment.id])
    response = auth_client.post(url)
    assert response.status_code == HTTPStatus.FOUND
    with pytest.raises(ObjectDoesNotExist):
        comment.refresh_from_db()


@pytest.fixture
@pytest.mark.django_db
def test_user_cant_delete_other_comment(auth_client, comment):
    url = reverse('news:delete', args=[comment.id])
    response = auth_client.post(url)
    assert response.status_code == HTTPStatus.FORBIDDEN
    comment.refresh_from_db()
    assert comment.text == 'Текст'
