import pytest

from django.urls import reverse

from news.models import Comment, News


@pytest.fixture
@pytest.mark.django_db
def test_news_count_on_the_page(client):
    for i in range(11):
        News.objects.create(title=f'Какое-то название новости {i}',
                            text='какая-то новость')
    url = reverse('news:home')
    response = client.get(url)
    assert len(response.context['news']) <= 10


@pytest.fixture
@pytest.mark.django_db
def test_news_order_on_the_page(client):
    for i in range(10):
        News.objects.create(title=f'Какое-то название новости {i}',
                            text='какая-то новость')
    url = reverse('home')
    response = client.get(url)
    news = response.context['news']
    assert news[0].title == 'Новость №1'


@pytest.fixture
@pytest.mark.django_db
def test_news_detail_page_comments_order(client, news):
    for i in range(10):
        Comment.objects.create(news=news, content=f'Какой-то комментарий {i}')
    url = reverse('news:detail', args=[news.id])
    response = client.get(url)
    comments = response.context['comments']
    assert comments[0].content == 'Последний комментарий'


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
    assert 'form' in response.context
