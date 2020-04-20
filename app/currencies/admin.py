import logging

from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import path
from django.urls import reverse

from .models import Currency


# Register your models here.


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['char_code', 'nominal', 'name', 'value', 'num_code']
    change_list_template = "currencies/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('load_currencies/', self.load_currencies, name="load-currencies"),
        ]
        return my_urls + urls

    def load_currencies(self, request):
        try:
            Currency.cbr_load()
        except Currency.CbrLoadException as e:
            msg = f'Error while loading currencies: {e}'
            logging.error(msg)
            messages.add_message(request, messages.ERROR, msg)
        except Exception as e:
            msg = f'Unhandled error while loading currencies: {e}'
            logging.exception(msg, exc_info=True)
            messages.add_message(request, messages.ERROR, msg)
        else:
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Currencies loaded successfully')
        return redirect(reverse('admin:currencies_currency_changelist'))


admin.site.register(Currency, CurrencyAdmin)
