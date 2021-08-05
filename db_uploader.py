import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tangoplate.settings")
django.setup()

from restaurants.models import *

CSV_PATH_LOCATION = 'menus.csv'

def insert_restaurants():
    with open(CSV_PATH_LOCATION) as in_file:
        data_reader = csv.reader(in_file)
        for row in data_reader:
            Restaurant.objects.create(
                name = row[1], 
                address = row[2], 
                phone_number=row[3], 
                category_id = int(row[4]), 
                location_id = int(row[5]), 
                serving_price_id = int(row[6])
            )

def insert_menus():
    with open(CSV_PATH_LOCATION) as in_file:
        data_reader = csv.reader(in_file)
        for row in data_reader:
            Menu.objects.create(
                item=row[0], 
                item_price=row[1],
                restaurant_id=row[2]
            )


insert_menus()