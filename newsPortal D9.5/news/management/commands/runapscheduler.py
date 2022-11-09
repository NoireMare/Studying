import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import Post, UserCategory
from NewsPortal.settings import DEFAULT_FROM_EMAIL

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
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


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='mon'),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")