from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from requests.exceptions import RequestException
import xml.etree.ElementTree as ET
import requests


class Currency(models.Model):

    class Meta:
        verbose_name_plural = "Currencies"

    class CbrLoadException(BaseException):
        pass

    num_code = models.PositiveSmallIntegerField(null=False, default=0)
    char_code = models.CharField(max_length=3,
                                 validators=[MinLengthValidator(3)],
                                 default='',
                                 unique=True
                                 )
    nominal = models.PositiveSmallIntegerField(null=False)
    name = models.CharField(null=False, max_length=50, default='')
    value = models.DecimalField(null=False, max_digits=7, decimal_places=4)

    @classmethod
    def _parse_valute(cls, valute: ET.Element):
        element_list = [
            'NumCode',
            'CharCode',
            'Nominal',
            'Name',
            'Value'
        ]

        parsed_valute = {}

        for k in element_list:
            el = valute.find(k)
            if not isinstance(el, ET.Element):
                raise cls.CbrLoadException(f'Missing value: "{k}"')
            parsed_valute[k] = el.text

        parsed_valute['Value'] = parsed_valute['Value'].replace(',', '.')
        return parsed_valute

    @classmethod
    def _parse_currencies(cls, content):
        try:
            et = ET.fromstring(content)
        except ET.ParseError:
            raise cls.CbrLoadException("Wrong payload")
        for ve in et.findall('.//Valute'):
            yield cls._parse_valute(ve)

    @classmethod
    def cbr_load(cls):
        try:
            response = requests.get(url=settings.CURRENCIES_URL)
        except RequestException as e:
            raise cls.CbrLoadException(f'Error requesting source: {e}')

        if response.status_code != 200:
            raise cls.CbrLoadException("Wrong resource response status code")

        added_codes = []

        for parsed_valute in cls._parse_currencies(response.content):
            Currency.objects.update_or_create(
                defaults={'char_code': parsed_valute['CharCode']},
                num_code=parsed_valute['NumCode'],
                char_code=parsed_valute['CharCode'],
                nominal=parsed_valute['Nominal'],
                name=parsed_valute['Name'],
                value=parsed_valute['Value']
            )
            added_codes.append(parsed_valute['CharCode'])

        Currency.objects.exclude(char_code__in=added_codes).delete()

    def __str__(self):
        return f"{self.nominal} {self.char_code}: {self.value} RUB"
