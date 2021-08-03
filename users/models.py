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
    user_id       = models.ForeignKey('User', on_delete=models.SET_NULL, db_column='user_id')
    restaurant_id = models.ForeignKey('Restaurant', on_delete=models.CASCADE, db_column='restaurant_id')
    rating         = models.IntegerField()

    class Meta:
        db_table = 'ratings'

class WishList(models.Model):
    user_id       = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_id')
    restaurant_id = models.ForeignKey('Restaurant', on_delete=models.CASCADE, db_column='restaurant_id')

    class Meta:
        db_table = 'wishes'
