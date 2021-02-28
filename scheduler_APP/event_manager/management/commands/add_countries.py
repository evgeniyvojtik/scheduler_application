import requests
from django.core.management import BaseCommand
from bs4 import BeautifulSoup

from event_manager.models import Country


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
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



