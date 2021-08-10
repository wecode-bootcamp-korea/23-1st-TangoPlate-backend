import json, re, bcrypt, jwt

from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Avg, Q

from reviews.models         import Review, ReviewImage
from users.models           import User, WishList
from users.utils            import login_decorator
from restaurants.models     import Restaurant

class ReviewView(View):
    @login_decorator
    def post(self, request, restaurant_id):
        data    = json.loads(request.body)
        user    = request.user

        if Review.objects.filter(user_id = user.id, restaurant_id=restaurant_id).exists():
            return JsonResponse({'MESSAGE':'REVIEW_EXIST'}, status=400)

        review = Review.objects.create(
            restaurant_id = restaurant_id,
            user_id       = user.id,
            description   = data['description'],
            rating        = data['rating'],
        )

        ReviewImage.objects.create(
            review_id = review.id,
            image     = data['image'],
        )

        return JsonResponse({'MESSAGE':'SUCCESS'},status = 201)

    @login_decorator
    def patch(self, request, restaurant_id, review_id):
        data = json.loads(request.body)
        user = request.user

        if not Review.objects.filter(id=review_id).exists():
            return JsonResponse({'MESSAGE':'NOT_EXISTS'}, status=400)

        Review.objects.filter(id=review_id).update(
                restaurant_id = restaurant_id,
                user_id       = user.id,
                description   = data['description'],
                rating        = data['rating'],
                )

        ReviewImage.objects.filter(review_id = review_id).update(
            review_id = review_id,
            image     = data['image'],
            )

        return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)

    @login_decorator
    def delete(self, request, restaurant_id, review_id):
        user = request.user

        if not Review.objects.filter(id=review_id).exists():
            return JsonResponse({'MESSAGE':'NOT_EXISTS'}, status=400)

        Review.objects.get(id=review_id).delete()

        return JsonResponse({"MESSAGE": 'SUCCESS'}, status=204)
