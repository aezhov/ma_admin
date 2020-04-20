from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Currency


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['char_code', 'nominal', 'name', 'value', 'num_code']


admin.site.register(Currency, CurrencyAdmin)