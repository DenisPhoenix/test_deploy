import requests
from rest_framework import status

from config import settings
import json
from datetime import datetime, timedelta
from django_celery_beat.models import PeriodicTask, IntervalSchedule


def convert_currencies(rub_price):
    """Конвертация валюты"""
    usd_price = 0

    response = requests.get(f"{settings.CUR_API_URL}api/?apikey={settings.CUR_API_KEY}")

    if response.status_code == status.HTTP_200_OK:
        usd_rate = response.json()["data"]["RUB"]["value"]
        usd_price = rub_price * usd_rate
    return usd_price


def set_schedule(*args, **kwargs):
    # Создаем интервал для повтора
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.SECONDS,
    )

    # Создаем задачу для повторения
    PeriodicTask.objects.create(
        interval=schedule,
        name='Importing contacts',
        task='proj.tasks.import_contacts',
        args=json.dumps(['arg1', 'arg2']),
        kwargs=json.dumps({
            'be_careful': True,
        }),
        expires=datetime.utcnow() + timedelta(seconds=30)
    )

