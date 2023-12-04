import pytest
from http import HTTPStatus

from django.test import Client


HOME_PAGE_URL = ('news:home')
DETAIL_PAGE_URL = ('news:detail')
EDIT_COMMENT_URL = ('news:edit')
DELETE_COMMENT_URL = ('news:delete')
SIGNUP_USER_URL = ('users:signup')
LOGIN_USER_URL = ('users:login')
LOGOUT_USER_URL = ('users:logout')


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url, expected_status',
    [
        (HOME_PAGE_URL, HTTPStatus.NOT_FOUND),
        (DETAIL_PAGE_URL, HTTPStatus.NOT_FOUND),
        (EDIT_COMMENT_URL, HTTPStatus.NOT_FOUND),
        (DELETE_COMMENT_URL, HTTPStatus.NOT_FOUND),
        (SIGNUP_USER_URL, HTTPStatus.NOT_FOUND),
        (LOGIN_USER_URL, HTTPStatus.NOT_FOUND),
        (LOGOUT_USER_URL, HTTPStatus.NOT_FOUND),
    ]
)
def test_all_status_codes(client, url, expected_status):
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url, client, expected_redirect',
    [
        (HOME_PAGE_URL, Client(), None),
        (DETAIL_PAGE_URL, Client(), None),
        (EDIT_COMMENT_URL, Client(),
         f'{LOGIN_USER_URL}?next={EDIT_COMMENT_URL}'),
        (DELETE_COMMENT_URL, Client(),
         f'{LOGIN_USER_URL}?next={DELETE_COMMENT_URL}'),
        (SIGNUP_USER_URL, Client(), None),
        (LOGIN_USER_URL, Client(), None),
        (LOGOUT_USER_URL, Client(), None),
    ]
)
def test_all_redirects(client, url, expected_redirect):
    response = client.get(url, follow=True)
    if expected_redirect:
        assert response != expected_redirect
