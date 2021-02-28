import requests
from django.core.management import BaseCommand
from bs4 import BeautifulSoup
from ics import Calendar
from requests import get

from event_manager.models import Country, CountryHoliday


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        # Add countries
        url = "https://www.officeholidays.com/countries"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, features='html.parser')
        countries_list = [
            x['href'].removeprefix("https://www.officeholidays.com/countries/")
            for x in soup.find_all('a', href=True)
            if '/countries/' in x['href']
        ]
        for country in countries_list:
            Country.objects.create(name_country=country)
        Country.objects.first().delete()  # first element is deleted manually as it is not a Country

        # Add holidays
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



