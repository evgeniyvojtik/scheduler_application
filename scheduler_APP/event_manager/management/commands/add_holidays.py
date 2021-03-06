import requests
from django.core.management import BaseCommand
from requests import get
from ics import Calendar

from event_manager.models import Country, CountryHoliday


class Command(BaseCommand):
    def handle(self, *args, **options):
        countries = Country.objects.all()
        holidays_name_set = []

        for country in countries:
            try:
                url = "https://www.officeholidays.com/ics-clean/" + country.name_country
                holidays = Calendar(get(url).text)
                for holiday in holidays.events:
                    if holiday.name not in holidays_name_set:
                        CountryHoliday.objects.create(
                            country_id=country.id,
                            holidays=holiday.name,
                            holiday_start=holiday._begin.date(),
                            holiday_finish=holiday._end_time.date()
                        )
                        holidays_name_set.append(holiday.name)
            except Exception as error:
                print(country.name_country)
                continue