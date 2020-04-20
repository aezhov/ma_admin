import os
import requests_mock
from requests.exceptions import Timeout, RequestException
from django.conf import settings
from django.test import TestCase

from .models import Currency
# Create your tests here.


class CurrencyTestCase(TestCase):
    def setUp(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_data_dir = os.path.join(base_dir, 'test_data')

    def test_load_currencies_service(self):
        payload_filename = os.path.join(self.test_data_dir,
                                        'currencies_payload.xml')
        payload = open(payload_filename, 'r').read()

        payload_filename_missing_value = os.path.join(self.test_data_dir,
                                                      'currencies_payload_missing.xml')
        payload_missing_value = open(payload_filename_missing_value, 'r').read()

        with requests_mock.Mocker() as m:
            m.get(settings.CURRENCIES_URL, text=payload)
            Currency.cbr_load()
            self.assertEqual(Currency.objects.count(), 34)

            with self.assertRaises(Currency.CbrLoadException, msg='Wrong payload'):
                m.get(settings.CURRENCIES_URL, text='{payload: not xml}')
                Currency.cbr_load()

            with self.assertRaisesRegex(Currency.CbrLoadException,
                                        expected_regex='Missing value: "Value"'):
                m.get(settings.CURRENCIES_URL, text=payload_missing_value)
                Currency.cbr_load()

            with self.assertRaises(Currency.CbrLoadException,
                                   msg="Wrong resource response status code"):
                m.get(settings.CURRENCIES_URL, status_code=403, text=payload)
                Currency.cbr_load()

            with self.assertRaisesRegex(Currency.CbrLoadException,
                                        expected_regex='^Error requesting source:.*'):
                m.get(settings.CURRENCIES_URL, exc=RequestException)
                Currency.cbr_load()

    def test_update_logic(self):
        payload_whole_filename = os.path.join(self.test_data_dir, 'currencies_payload.xml')
        payload_part_1_filename = os.path.join(self.test_data_dir, 'currencies_payload_half_1.xml')
        payload_part_2_filename = os.path.join(self.test_data_dir, 'currencies_payload_half_2.xml')

        payload_whole = open(payload_whole_filename, 'r').read()
        payload_part_1 = open(payload_part_1_filename, 'r').read()
        payload_part_2 =  open(payload_part_2_filename, 'r').read()

        with requests_mock.Mocker() as m:
            # tests correct model creation
            m.get(settings.CURRENCIES_URL, text=payload_part_1)
            Currency.cbr_load()
            self.assertEqual(Currency.objects.count(), 22)

            m.get(settings.CURRENCIES_URL, text=payload_part_2)
            Currency.cbr_load()
            self.assertEqual(Currency.objects.count(), 12)

            m.get(settings.CURRENCIES_URL, text=payload_whole)
            Currency.cbr_load()
            self.assertEqual(Currency.objects.count(), 34)
