from django.core.management.base import BaseCommand, CommandError
from aliments import dbInsert
from aliments.models import Category
from aliments.models import Store
from aliments.models import Products
import logging


class Command(BaseCommand):

    help = 'Closes the specified cron tache'

    def handle(self, *args, **options):
        # Get an instance of a logger
        logger = logging.getLogger(__name__)

        cat = Category.objects.all()

        if cat.exists():
            logger.info("Category table not empty")
            print("exist")
        else:
            dbInsert.insertCategory()

            store = Store.objects.all()
            if store.exists():
                logger.info("Store table not empty")
                print("exist")
            else:
                dbInsert.insertStore()
                products = Products.objects.all()
                if products.exists():
                    logger.info("Products table not empty")
                    print("exist")
                else:
                    dbInsert.insertProducts()

            self.stdout.write(self.style.SUCCESS('Successfully'))
