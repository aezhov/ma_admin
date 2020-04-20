from django.core.management.base import BaseCommand, CommandError
from currencies.models import Currency


class Command(BaseCommand):

    help = 'Load currencies from www.cbr.ru'

    def handle(self, *args, **options):
        try:
            Currency.cbr_load()
        except Currency.CbrLoadException as e:
            raise CommandError(f'Error while loading currencies: {e}')
        except Exception as e:
            raise CommandError(f'Unhandled error while loading currencies: {e}')
        else:
            self.stdout.write(self.style.SUCCESS("Currencies loaded successfully"))
            for c in Currency.objects.all():
                self.stdout.write(f"{c}\n")
