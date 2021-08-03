from django.db import models
from restaurants.models import Restaurant

class Coupon(models.Model):
    name           = models.CharField(max_length=40)
    restaurants_id = models.ForeignKey('Restaurant', on_delete=models.CASCADE, db_column='restaurants_id')
    price          = models.DecimalField(max_digits= 6, decimal_places=0)
    desc           = models.CharField(max_length=500)
    start_date     = models.DateField()
    end_date       = models.DateField()

    class Meta:
        db_table = 'coupons'

class CouponImage(models.Model):
    coupons_id    = models.ForeignKey('Coupon', on_delete=models.CASCADE, db_column='coupons_id')
    image         = models.URLField(max_length=500)

    class Meta:
        db_table = 'coupons_images'
