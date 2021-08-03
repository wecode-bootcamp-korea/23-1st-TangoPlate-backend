from django.db          import models

from users.models       import User
from restaurants.models import Restaurant

class Review(models.Model):
    restaurant_id = models.ForeignKey('restaurants.Restaurant', on_delete=SET_NULL, db_column='restaurant_id', null=True)
    user_id       = models.ForeignKey('users.User', on_delete=SET_NULL, db_column='user_id', null=True)
    description   = models.CharField(max_length=500, null=True)
    created_at    = models.DateField(auto_now_add=True)
    updated_at    = models.DateField(auto_now=True, null=True)

    class Meta:
        db_table = 'reviews'

class ReviewImage(models.Model):
    reviews_id    = models.ForeignKey('Review',on_delete=SET_NULL, db_column='review_id')
    image         = models.URLField(max_length=500)
    
    class Meta:
        db_table = 'reviews_images'