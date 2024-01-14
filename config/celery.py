# import os
#
# from celery import Celery
#
# # Set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
#
# app = Celery('config')
#
#
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
#
# app.autodiscover_tasks()
#
# #app.conf.beat_schedule = {'add-every-60-seconds': {'task': 'habit.tasks.habits_notification', 'schedule': 60}, }
import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

app.conf.beat_schedule = {'add-every-60-seconds': {'task': 'habits.tasks.habits_to_telegram', 'schedule': 60}, }


# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')