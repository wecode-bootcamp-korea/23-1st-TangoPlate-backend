import json, re, bcrypt, jwt

from django.views         import View
from django.http          import JsonResponse
from django.db.models     import Avg, Q

from reviews.models       import Review, ReviewImage
from users.models         import User, WishList
from restaurants.models   import Restaurant
from users.utils          import login_decorator

class ReviewCreateView(View):
    @login_decorator
    def post(self, request, restaurant_id):
        try:
            data             = json.loads(request.body)
            user             = request.user
            
            if Review.objects.filter(user_id = user.id, restaurant_id = restaurant_id).exists():
                return JsonResponse({'MESSAGE':'ONE_REVIEW_PER_USER_ALLOWED'}, status=400)

            Review.objects.create(
                restaurant_id = restaurant_id,
                user_id       = user.id,
                description   = data['description'],
                rating        = data['rating']
            )

            review_id         = Review.objects.get(user_id = user.id, restaurant_id = restaurant_id).id

            ReviewImage.objects.create(
                review_id     = review_id,
                image         = data['image'],
            )
            return JsonResponse({'MESSAGE':'SUCCESS'},status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

class ReviewUpdateDeleteView(View):
    @login_decorator 
    def put(self, request, restaurant_id, review_id):
        try:
            data               =  json.loads(request.body)

            if not Review.objects.filter(id=review_id).exists():
                return JsonResponse({'MESSAGE':'NOT_EXISTS'}, status=400)
            
            user_reviews        =  Review.objects.filter(id = review_id)
            user_review         =  Review.objects.get(id = review_id)
            user_review_img     =  ReviewImage.objects.filter(review_id = review_id)

            if request.user.id == user_review.user_id:
                user_reviews.update(
                    description  = data['description'],
                    rating       = data['rating']
                    )
                user_review_img.update(
                    image        = data['image'],
                    )
                return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)

            return JsonResponse({'MESSAGE':'NOT_AUTHORIZED'}, status=403)
            
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

    @login_decorator
    def delete(self, request, restaurant_id, review_id):
        try:
            user_review         =  Review.objects.get(id = review_id)

            if not Review.objects.filter(id = review_id).exists():
                return JsonResponse({'MESSAGE':'NOT_EXISTS'}, status=400)
            
            if request.user.id == user_review.user_id:
                review_object = Review.objects.get(id = review_id)
                review_object.delete()
                return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)
            
            return JsonResponse({'MESSAGE':'NOT_AUTHORIZED'}, status=403)

            restaurant         = Restaurant.objects.get(id = restaurant_id)
            reviews            = restaurant.review_set.all()
            is_wished          = restaurant.wishlist_set.exists()
            menus              = restaurant.menu_set.all()
            rating_num         = restaurant.review_set.all().aggregate(rating = Avg('rating'))['rating']
            
            results = []
            results.append({
                "id"             : restaurant.id,
                "name"           : restaurant.name,
                "rating"         : rating_num,
                "restaurant_img" : restaurant.review_set.get(restaurant_id=restaurant.id).reviewimage_set.get().image,
                "address"        : restaurant.address,
                "phone_number"   : restaurant.phone_number,
                "category"       : restaurant.category.name,
                "location"       : restaurant.location.area,
                "serving_price"  : restaurant.serving_price.price,
                "menus"          : [{   
                                        "item"       : menu.item, 
                                        "item_price" : menu.item_price
                                    } for menu in menus],
                "is_wished"      : is_wished,
                "review"         : [{
                                        "review_id"  : review.id,
                                        "user_id"    : review.user.id,
                                        "user_name"  : review.user.nickname,
                                        "description": review.description,
                                        "rating"     : review.rating,
                                        "created_at" : review.created_at,
                                        "images url" : review.reviewimage_set.get().image, 
                } for review in reviews]
            })
            return JsonResponse({"results": results}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)