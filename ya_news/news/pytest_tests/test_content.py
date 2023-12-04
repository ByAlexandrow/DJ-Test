import pytest

from django.urls import reverse
from news.forms import CommentForm


@pytest.fixture
@pytest.mark.django_db
def test_news_count_on_the_page(client, home_url):
    response = client.get(home_url)
    assert len(response.context['news']) == 10


@pytest.fixture
@pytest.mark.django_db
def test_news_order_on_the_page(client, home_url):
    response = client.get(home_url)
    news = response.context['news'].order_by('-date')
    for i in range(len(news) - 1):
        assert news[i].date > news[i + 1].date


@pytest.fixture
@pytest.mark.django_db
def test_news_detail_page_comments_order(client, detail_page_url):
    response = client.get(detail_page_url)
    comments = response.context['comments'].order_by('-date')
    for i in range(len(comments) - 1):
        assert comments[i].date > comments[i + 1].date


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
