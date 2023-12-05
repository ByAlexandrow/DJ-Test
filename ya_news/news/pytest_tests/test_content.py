import pytest

from django.conf import settings
from django.urls import reverse
from news.forms import CommentForm


@pytest.fixture
@pytest.mark.django_db
def test_news_count_on_the_page(client, home_url):
    response = client.get(home_url)
    assert len(response.context['news']) == settings.CREATE_NEWS


@pytest.fixture
@pytest.mark.django_db
def test_news_order_on_the_page(client, home_url):
    response = client.get(home_url)
    news_list = response.context['news']
    news = response.context['news'].order_by('-date')
    assert news_list == news


@pytest.fixture
@pytest.mark.django_db
def test_news_detail_page_comments_order(client, detail_page_url):
    response = client.get(detail_page_url)
    comments_list = response.content['comment']
    comments = response.context['comments'].order_by('-date')
    assert comments_list == comments


@pytest.mark.django_db
def test_comment_form_anonymous_user(client, news):
    url = reverse('news:detail', args=[news.id])
    response = client.get(url)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_comment_form_authenticated_user(client, user, news):
    client.force_login(user)
    url = reverse('news:detail', args=[news.id])
    response = client.get(url)
    form = response.context.get('form')
    assert form is not None
    assert isinstance(form, CommentForm)
