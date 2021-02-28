from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, datetime, time

from scheduler_APP.settings import REMIND_OPTIONS


class Event(models.Model):

    event = models.TextField(max_length=2000, verbose_name='Событие', null=True)
    user = models.ForeignKey('MyUser', on_delete=models.CASCADE, related_name='user_event', null=True)
    date_time_start = models.DateTimeField(null=True)
    date_time_finish = models.DateTimeField(null=True, blank=True)
    reminder_option = models.CharField(max_length=30, choices=REMIND_OPTIONS, null=True, blank=True)
    reminder_time = models.DateTimeField(null=True, blank=True)
    notification = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.event

    def save(self, **kwargs):
        if self.date_time_finish is None:
            self.date_time_finish = self.date_time_start
        if self.reminder_option:
            self.reminder_time = self.date_time_start - self.reminder_option

        super().save(**kwargs)


class Country(models.Model):
    name_country = models.TextField()

    def __str__(self):
        return self.name_country


class MyUser(AbstractUser):
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True,
        blank=True, related_name='country_user',
        verbose_name='Страна'
    )
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True, blank=False)
    REQUIRED_FIELDS = ['username']


class CountryHoliday(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True,
                                blank=True, related_name='country_holiday',
                                )
    holidays = models.TextField(null=True)
    holiday_start = models.DateField(null=True)
    holiday_finish = models.DateField(null=True)


