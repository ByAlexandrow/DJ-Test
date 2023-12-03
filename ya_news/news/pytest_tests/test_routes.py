import pytest
from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
def test_home_page_available_for_anonymous_user(client):
    url = reverse('news:home')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_news_detail_page_available_for_anonymous_user(client, news):
    url = reverse('news:detail', args=[news.id])
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


# параметризовать
@pytest.mark.django_db
def test_comment_page_available_for_author(client, comment):
    url_edit = reverse('news:edit', args=[comment.id])
    url_delete = reverse('news:delete', args=[comment.id])
    client.force_login(comment.author)
    response_edit = client.get(url_edit)
    response_delete = client.get(url_delete)
    assert response_edit.status_code == HTTPStatus.OK
    assert response_delete.status_code == HTTPStatus.OK


# парамаетризовать
@pytest.mark.django_db
def test_comment_page_redirect_for_anonymous_user(client, comment):
    login_url = reverse('users:login')
    edit_url = reverse('news:edit', args=[comment.id])
    delete_url = reverse('news:delete', args=[comment.id])
    expected_login_edit_url = f'{login_url}?next={edit_url}'
    expected_login_delete_url = f'{login_url}?next={delete_url}'
    response_edit = client.get(edit_url)
    response_delete = client.get(delete_url)
    assert response_edit.status_code == HTTPStatus.FOUND
    assert response_delete.status_code == HTTPStatus.FOUND
    assertRedirects(response_edit, expected_login_edit_url)
    assertRedirects(response_delete, expected_login_delete_url)


# параметризовать
@pytest.mark.django_db
def test_comment_page_for_other_users(client, comment, user):
    edit_url = reverse('news:edit', args=[comment.id])
    delete_url = reverse('news:delete', args=[comment.id])
    client.force_login(user)
    response_edit = client.get(edit_url)
    response_delete = client.get(delete_url)
    assert response_edit.status_code == HTTPStatus.OK
    assert response_delete.status_code == HTTPStatus.OK


# параметризовать
@pytest.mark.django_db
def test_auth_pages_available_to_anonymous_user(client):
    register_url = reverse('users:signup')
    login_url = reverse('users:login')
    logout_url = reverse('users:logout')
    response_register = client.get(register_url)
    response_login = client.get(login_url)
    response_logout = client.get(logout_url)
    assert response_register.status_code == HTTPStatus.OK
    assert response_login.status_code == HTTPStatus.OK
    assert response_logout.status_code == HTTPStatus.OK
