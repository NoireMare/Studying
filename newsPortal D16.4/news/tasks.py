

from celery import shared_task
from django.utils import timezone

from news.models import UserCategory
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from NewsPortal.settings import DEFAULT_FROM_EMAIL
from news.models import Post


@shared_task
def send_emails_to_subscribers(data):
    html_content = render_to_string(
        'account/email/news_to_subscribers.html',
        {
            'form': [data['title'], data['text'], data['id'], data['subscriber_username']],
        })
    msg = EmailMultiAlternatives(
        subject=f'{data["title"]}',
        body=f'{data["text"]}',
        from_email=DEFAULT_FROM_EMAIL,
        to=[data['subscriber_email']],  # это то же, что и recipients_list
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем


@shared_task
def week_news():
    now = timezone.now()
    week = now - timezone.timedelta(days=7)
    for user in list(set(UserCategory.objects.all().values_list('user_id', 'user_id__email', 'user_id__username'))):
        categories_subscribed = UserCategory.objects.filter(user_id=user[0]).values_list('category_id', flat=True)
        posts = list(set(Post.objects.filter(time_add__gte=week, type=True, category_post__in=categories_subscribed)))
        email = user[1]
        html_content = render_to_string(
            'account/email/week_news.html',
            {
                'form': [posts, user[2]]
            })
        msg = EmailMultiAlternatives(
            subject=f'Горячие новости!',
            body=f'{posts}',
            from_email=DEFAULT_FROM_EMAIL,
            to=[email],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем

