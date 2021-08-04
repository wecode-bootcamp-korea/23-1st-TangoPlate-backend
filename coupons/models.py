from django.db          import models

from restaurants.models import Restaurant

class Coupon(models.Model):
    name           = models.CharField(max_length=40)
    restaurant     = models.ForeignKey('Restaurant', on_delete=models.SET_NULL, null=True)
    price          = models.DecimalField(max_digits= 6, decimal_places=1)
    description    = models.CharField(max_length=500, null=True)
    start_date     = models.DateField()
    end_date       = models.DateField()

    class Meta:
        db_table = 'coupons'

class CouponImage(models.Model):
    coupon        = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True)
    image         = models.URLField(max_length=500)

    class Meta:
        db_table = 'coupon_images'
