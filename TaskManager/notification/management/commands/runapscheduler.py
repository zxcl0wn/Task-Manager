import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.db import connection
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from notification.models import Notification
from tasks.models import Task
from user.middleware import get_current_user
from time import gmtime, strftime
logger = logging.getLogger(__name__)
import datetime


def my_job():
    logger.info("Выполняется задача my_job")
    try:
        all_tasks = Task.objects.all()
        for task in all_tasks:
            deadline = task.deadline_date
            showtime = strftime("%Y-%m-%d")
            showtime_datetime = datetime.datetime.strptime(showtime, "%Y-%m-%d").date()
            time_diff = deadline - showtime_datetime

            if time_diff.total_seconds() <= 86400:
                new_content = f'Ваша задача "{task.title}" подходит к концу сроку выполнения!"'
                try:
                    exist_notification = Notification.objects.get(task=task.id)
                    continue
                except:
                    new_task = task
                    new_is_read = False
                    Notification.objects.create(
                        content=new_content,
                        task=new_task,
                        is_read=new_is_read
                    )
                    logger.info("Добавлено новое оповещение")

    except Exception as e:
        print(e)
    finally:
        connection.close()  # Закрываем соединение


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """Удаление старых записей о выполнении задач"""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Запускает APScheduler для выполнения периодических задач"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Добавляем задачу my_job, которая будет выполняться каждую минуту
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # Каждую минуту
            id="my_job",
            max_instances=1,
            replace_existing=True,
            coalesce=True,
        )
        logger.info("Добавлена задача 'my_job' с запуском каждую минуту")

        # Добавляем задачу очистки старых записей (раз в неделю)
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена еженедельная задача очистки старых записей")

        try:
            logger.info("Запуск планировщика задач...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Остановка планировщика...")
            scheduler.shutdown()
            logger.info("Планировщик успешно остановлен")