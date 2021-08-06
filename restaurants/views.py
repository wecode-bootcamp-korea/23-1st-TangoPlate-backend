from django.shortcuts import render

from django.views         import View
from django.http          import JsonResponse
from django.db.models     import Avg

from restaurants.models   import Restaurant, Category, Location, ServingPrice, Menu
from users.models         import User, WishList, Rating
from reviews.models       import Review, ReviewImage
from users.utils          import login_decorator

class RestaurantDetailView(View):
    @login_decorator
    def get(self, request, restaurant_id):
        try:
            restaurant        = Restaurant.objects.get(id = restaurant_id)
            reviews           = Review.objects.filter(restaurant_id = restaurant_id)
            is_wished         = restaurant.wishlist_set.filter(restaurant_id=restaurant_id).exists()
            menus             = restaurant.menu_set.filter(restaurant_id=restaurant.id)
            retaurant_ratings = Rating.objects.filter(restaurant_id=restaurant_id)
            user_rating       = Rating.objects.get(user_id = request.user.id, restaurant_id=restaurant_id)
            rating_num = retaurant_ratings.aggregate(rating = Avg('rating'))['rating']

            results = []
            results.append({
                "id"             : restaurant.id,
                "name"           : restaurant.name,
                "rating"         : rating_num,
                "address"        : restaurant.address,
                "phone_number"   : restaurant.phone_number,
                "category"       : restaurant.category.name,
                "location"       : restaurant.location.area,
                "serving_price"  : restaurant.serving_price.price,
                "menus"          : [{"item" : menu.item, "item_price" : int(menu.item_price)} for menu in menus],
                "is_wished"      : is_wished,
                "review"         : [{
                    "review_id"  : review.id,
                    "user_id"    : review.user.id,
                    "user_name"  : review.user.nickname,
                    "description": review.description,
                    "rating"     : user_rating.rating,
                    "created_at" : review.created_at,
                    "images"     : [{"image_url" : imageobject.image} for imageobject in ReviewImage.objects.filter(review_id=review.id)]
                } for review in reviews]
            })
            return JsonResponse({"results": results}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)