import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tangoplate.settings")
django.setup()

from restaurants.models import Restaurant, Menu
from reviews.models import Review
from users.models import Rating

CSV_PATH_LOCATION = 'ratings.csv'

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

def insert_review():
    with open(CSV_PATH_LOCATION) as in_file:
        data_reader = csv.reader(in_file)
        for row in data_reader:
            Review.objects.create(
                description=row[0], 
                created_at=row[1],
                updated_at=row[2],
                restaurant_id=row[3],
                user_id=row[4],
            )

def insert_review_img():
    with open(CSV_PATH_LOCATION) as in_file:
        data_reader = csv.reader(in_file)
        for row in data_reader:
            Review.objects.create(
                image=row[0], 
                review_id=row[1],
            )

def insert_rating():
    with open(CSV_PATH_LOCATION) as in_file:
        data_reader = csv.reader(in_file)
        for row in data_reader:
            Rating.objects.create(
                rating=row[0], 
                restaurant_id = row[1],
                user_id=row[2],
                review_id=row[3]
            )

insert_rating()