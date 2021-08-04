from django.db          import models

from restaurants.models import Restaurant

class User(models.Model):
    nickname     = models.CharField(max_length=50, null=True)
    email        = models.EmailField(max_length=200)
    password     = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=45)

    class Meta:
        db_table = 'users'

class Rating(models.Model):
    user       = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE)
    rating     = models.IntegerField()

    class Meta:
        db_table = 'ratings'

class WishList(models.Model):
    user       = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE)

    class Meta:
        db_table = 'wishlist'
