from datetime import datetime, timedelta, timezone
import requests
from celery import shared_task
from habits.models import Habit
from django.conf import settings
from datetime import datetime
import pytz
from celery import shared_task
import requests

from users.services import tg_send_message

TOKEN = settings.TELEGRAM_TOKEN

@shared_task
def habits_to_telegram():
    timezone = pytz.timezone('Asia/Irkutsk')
    current_time_yek = datetime.now(timezone)
    current_time = current_time_yek.strftime('%H:%M')
    now_date = datetime.now().date()
    habits = Habit.objects.all()  # Получяем объекты Habit по фильтру раз в день

    for habit in habits:
        print(now_date)
        action = habit.get_habit  # что делаем
        location = habit.place_habit  # место привычки
        reminder_time = habit.time_habit  # время привычки
        chat_id = habit.owner.chat_id  #

        if habit.period_habit == "Каждый день":  # каждые 24 часа
            if current_time == habit.time_habit.strftime('%H:%M'):  # проверяем чч:мм отправки
                tg_send_message(chat_id, f'Напоминание: нужно {action} в {location} в {reminder_time}')
                print(f'Сообщение отправлено')

        if habit.period_habit == "Раз в два дня":
            if (now_date - habit.create_time).days > 2:  # каждые 48 часов раз в два дня
                if current_time == habit.time_habit.strftime('%H:%M'):  ## проверяем чч:мм отправки
                    habit.time_habit = timezone.now()
                    tg_send_message(chat_id, f'Напоминание: нужно {action} в {location} в {reminder_time}')
                    print(f'Сообщение отправлено')

        if habit.period_habit == "Раз в три дня":
            if (current_time_yek - habit.create_time).days > 3:  # каждые 72 часа раз в 3 дня
                if current_time == habit.time_habit.strftime('%H:%M'):  # проверяем чч:мм отправки
                    habit.time_habit = now_date
                    tg_send_message(chat_id, f'Напоминание: нужно {action} в {location} в {reminder_time}')
                    print(f'Сообщение отправлено')
