import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import connection
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from notification.models import Notification
from projects.models import ProjectMember
from tasks.models import Task
from user.middleware import get_current_user
from time import gmtime, strftime
from django.db.models import Q
import datetime


logger = logging.getLogger(__name__)


def notification_cron():
    try:
        all_tasks = Task.objects.all()
        for task in all_tasks:
            deadline = task.deadline_date
            showtime = strftime("%Y-%m-%d")
            showtime_datetime = datetime.datetime.strptime(showtime, "%Y-%m-%d").date()
            time_diff = deadline - showtime_datetime

            if time_diff.total_seconds() <= 24*60*60:
                members_id = ProjectMember.objects.filter(project=task.project).select_related('user').values_list(
                    'user_id', flat=True)
                users = User.objects.filter(id__in=members_id)
                for user in users:
                    if not Notification.objects.filter(Q(task=task.id)&Q(user=user)).exists():
                        new_content = f'Ваша задача "{task.title}" подходит к концу сроку выполнения!"'
                        new_user = user
                        new_task = task
                        new_is_read = False
                        Notification.objects.create(
                            content=new_content,
                            task=new_task,
                            user=new_user,
                            is_read=new_is_read
                        )
    except Exception as e:
        pass
    finally:
        connection.close()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """Удаление старых записей о выполнении задач"""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Запускает APScheduler для выполнения периодических задач"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            notification_cron,
            trigger=CronTrigger(second="*/5"),  # Каждые 10 секунд
            id="my_job",
            max_instances=1,
            replace_existing=True,
            coalesce=True,
        )

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )

        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()