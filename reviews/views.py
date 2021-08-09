import json, re, bcrypt, jwt

from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Avg, Q

from reviews.models         import Review, ReviewImage
from users.models           import User, WishList, Rating
from users.utils            import login_decorator
from restaurants.models     import Restaurant

class ReviewView(View):
    @login_decorator
    def post(self, request, restaurant_id):
        try:
            data    = json.loads(request.body)
            user    = request.user

            q = Q()
            q.add(Q(user_id = user.id), Q.AND)
            q.add(Q(restaurant_id=restaurant_id),Q.AND)

            if Review.objects.filter(q).exists():
                return JsonResponse({'MESSAGE':'REVIEW_EXIST'}, status=400)

            review = Review.objects.create(
                restaurant_id = restaurant_id,
                user_id       = user.id,
                description   = data['description'],
            )

            ReviewImage.objects.create(
                review_id = review.id,
                image     = data['image'],
            )

            Rating.objects.create(
                user_id       = user.id,
                restaurant_id = restaurant_id,
                rating        = data['rating'],
            )

            return JsonResponse({'MESSAGE':'SUCCESS'},status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

    @login_decorator 
    def put(self, request, restaurant_id):
        try:
            data = json.loads(request.body)
            user = request.user

            q = Q()
            q.add(Q(user_id = user.id), Q.AND)
            q.add(Q(restaurant_id=restaurant_id),Q.AND)

            user_review = Review.objects.filter(q)
            if not user_review.exists():
                return JsonResponse({'MESSAGE':'NOT_EXISTS'}, status=400)

            review = user_review.update(
                    restaurant_id = restaurant_id,
                    user_id       = user.id,
                    description   = data['description'],
                    )

            ReviewImage.objects.filter(review_id = review.id).update(
                review_id = review.id,
                image     = data['image'],
                )
            
            Rating.objects.filter(q).update(
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
            q = Q()
            q.add(Q(user_id = user.id), Q.AND)
            q.add(Q(restaurant_id=restaurant_id),Q.AND)

            review = Review.objects.filter(q)

            if not review.exists():
                return JsonResponse({'MESSAGE':'NOT_EXISTS'}, status=400)

            review_object = Review.objects.get(q)
            review_object.delete()
            
            rating_object = Rating.objects.get(q)
            rating_object.delete()

            return JsonResponse({"MESSAGE": 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
