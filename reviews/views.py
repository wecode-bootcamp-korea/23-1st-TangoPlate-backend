import json, re, bcrypt, jwt
from django.views         import View
from django.http          import JsonResponse
from reviews.models       import Review, ReviewImage
from users.models         import User
from users.models         import WishList
from users.utils          import login_decorator
from restaurants.models   import Restaurant
# Create your views here.
class ReviewView(View):
    @login_decorator
    def post(self, request, restaurant_id):
        try:
            data = json.loads(request.body)
            user = request.user
            reviews = Review.objects.filter(user_id = user.id)
            for review in reviews:
                if review.restaurant_id == restaurant_id:
                    return JsonResponse({'MESSAGE':'EXISTS'}, status=400)
            Review.objects.create(
                restaurant_id = restaurant_id,
                user_id      = User.objects.get(id=user.id).id,
                description   = data['description'],
            )
            review_id = Review.objects.filter(user_id = user)
            review_id = review_id[0].id
            ReviewImage.objects.create(
                review_id = review_id,
                image     = data['image'],
            )
            return JsonResponse({'MESSAGE':'SUCCESS'},status = 201)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
