from rest_framework import serializers

from rest_framework.serializers import ModelSerializer
from event_manager.models import Event, CountryHoliday


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ('event', 'date_time_start', 'date_time_finish', 'reminder_option',)


class HolidaySerializer(ModelSerializer):
    class Meta:
        model = CountryHoliday
        fields = ('holidays', 'holiday_begin', 'holiday_end',)


class GroupByDayEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['date_time_start', 'event']
