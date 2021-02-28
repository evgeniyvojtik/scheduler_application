from _multiprocessing import send
from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import send_mail
from event_manager.models import Event, Country, CountryHoliday
import arrow
from ics import Calendar
import requests
from scheduler_APP.celery import app

# @app.task
# def send_spam_email(user_email):
#     send(user_email)


@shared_task()
def remind_event():
    all_events = Event.objects.filter(notification=False)
    for every_event in all_events:
        if every_event.reminder_option:
            timezone = tz = datetime.now() + timedelta(hours=3)
            if every_event.reminder_time.timestamp() <= timezone.timestamp():
                subject = 'Вам направлено напоминание о событии'
                message = f'{every_event.user.username}, напоминаем Вам о следующем сохранённом событии. ' \
                          f'Событие: {every_event.event},' \
                          f'время начала: {every_event.date_time_start}, ' \
                          f'время окончания: {every_event.date_time_finish}.'
                send_mail(
                    subject,
                    message,
                    'lanser03051996@gmail.com',
                    [every_event.user.email]
                )
                Event.objects.filter(id=every_event.id).update(notification=True)
                print(every_event.id, 'ok')

@shared_task()
def update_holidays():
    CountryHoliday.objects.all().delete()
    all_countries = Country.objects.all()
    error = []
    for one_country in all_countries:
        try:
            url = "https://www.officeholidays.com/ics-clean/" + one_country.name_country
            holidays = list(Calendar(requests.get(url).text).events)
            for h in holidays:
                CountryHoliday.objects.create(
                    country_id=one_country.id,
                    holidays=h.name,
                    holiday_begin=arrow.get(h.begin).format("YYYY-MM-DD"),
                    holiday_end=arrow.get(h.end).format("YYYY-MM-DD"),
                )
        except Exception:
            error.append(one_country.name_country)
            continue