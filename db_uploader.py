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
            r_name = row[1]
            r_address = row[2]
            r_phone_number= row[3]
            r_category_id = int(row[4])
            r_location_id = int(row[5])
            r_serving_price_id = int(row[6])
            Restaurant.objects.create(name = r_name, address = r_address, phone_number=r_phone_number, category_id = r_category_id, location_id = r_location_id, serving_price_id = r_serving_price_id)

def insert_menus():
    with open(CSV_PATH_LOCATION) as in_file:
        data_reader = csv.reader(in_file)
        for row in data_reader:
            Menu.objects.create(item=row[0], item_price=row[1],restaurant_id=row[2])

insert_menus()