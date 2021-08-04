from django.db          import models

from users.models       import User
from restaurants.models import Restaurant

class Review(models.Model):
    user        = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    restaurant  = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    description = models.CharField(max_length=500, null=True)
    created_at  = models.DateField(auto_now_add=True)
    updated_at  = models.DateField(auto_now=True, null=True)

    class Meta:
        db_table = 'reviews'

class ReviewImage(models.Model):
    review     = models.ForeignKey('Review',on_delete=SET_NULL, null=True)
    image      = models.URLField(max_length=500)
    
    class Meta:
        db_table = 'review_images'