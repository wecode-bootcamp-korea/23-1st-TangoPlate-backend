import json, re, bcrypt, jwt

from django.views         import View
from django.http          import JsonResponse

from reviews.models       import Review, ReviewImage
from users.models         import User, WishList, Rating
from users.utils          import login_decorator
from restaurants.models   import Restaurant

class Review_View(View):
    @login_decorator
    def post(self, request, restaurant_id):
        try:
            data    = json.loads(request.body)
            user    = request.user

            if Review.objects.filter(user_id = user.id, restaurant_id = restaurant_id).exists():
                return JsonResponse({'MESSAGE':'EXISTS'}, status=400)

            Review.objects.create(
                restaurant_id = restaurant_id,
                user_id       = user.id,
                description   = data['description'],
            )

            review_id = Review.objects.filter(user_id = user.id)
            review_id = review_id[0].id

            ReviewImage.objects.create(
                review_id = review_id,
                image     = data['image'],
            )

            Rating.objects.create(
                user_id       = user.id,
                restaurant_id = restaurant_id,
                rating        = data['rating']
            )

            return JsonResponse({'MESSAGE':'SUCCESS'},status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

    @login_decorator 
    def put(self, request, restaurant_id):
        try:
            data = json.loads(request.body)
            user = request.user

            user_review = Review.objects.filter(user_id = user.id, restaurant_id = restaurant_id)
            if not user_review.exists():
                return JsonResponse({'MESSAGE':'NOT_EXISTS'}, status=400)

            user_review.update(
                    restaurant_id = restaurant_id,
                    user_id       = user.id,
                    description   = data['description'],
                    )

            review_id = user_review[0].id

            ReviewImage.objects.filter(review_id = review_id).update(
                review_id = review_id,
                image     = data['image'],
                )
            
            Rating.objects.filter(user_id = user.id, restaurant_id = restaurant_id).update(
                user_id = user.id,
                restaurant_id = restaurant_id,
                rating = data['rating'],
            )

            return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

    @login_decorator
    def delete(self, request, restaurant_id):
        try:
            user = request.user

            if not Review.objects.filter(user_id = user.id, restaurant_id=restaurant_id).exists():
                return JsonResponse({'MESSAGE':'NOT_EXISTS'}, status=400)

            review_object = Review.objects.get(user_id = user.id, restaurant_id=restaurant_id)
            review_object.delete()
            
            rating_object = Rating.objects.get(user_id = user.id, restaurant_id=restaurant_id)
            rating_object.delete()

            return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
