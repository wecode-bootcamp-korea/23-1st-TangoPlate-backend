from django.db          import models
from users.models       import User
from restaurants.models import Restaurant

class Review(models.Model):
    restaurants_id = models.ForeignKey('restaurants.Restaurant', on_delete=CASCADE, db_column='restaurants_id')
    users_id       = models.ForeignKey('users.User', on_delete=CASCADE, db_column='users_id')
    desc           = models.CharField(max_length=500, null=True)
    created_at     = models.DateField(auto_now_add=True)
    updated_at     = models.DateField(auto_now=True, null=True)

    class Meta:
        db_table = 'reviews'

class ReviewImage(models.Model):
    reviews_id    = models.ForeignKey('Review',on_delete=CASCADE, db_column='reviews_id')
    image         = models.CharField(max_length=500)
    
    class Meta:
        db_table = 'reviews_images'