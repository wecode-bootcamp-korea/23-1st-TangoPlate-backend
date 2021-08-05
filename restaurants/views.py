from django.shortcuts import render

from django.views         import View
from django.http          import JsonResponse

from restaurants.models   import Restaurant, Category, Location, ServingPrice, Menu
from users.models         import User, WishList, Rating
from reviews.models       import Review
from users.utils          import login_decorator

class RestaurantDetailView(View):
    @login_decorator
    def get(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id = restaurant_id)
            reviews = Review.objects.filter(restaurant_id = restaurant_id)
            is_wished  = restaurant.wishlist_set.filter(restaurant_id=restaurant_id).exists()
            results = []
            menus = restaurant.menu_set.filter(restaurant_id=restaurant.id)
            
            # ratings = Rating.objects.filter(restaurant_id=restaurant_id)
            # rating_list = [rating for rating in ratings]
            # a = []
            # for rating in rating_list:
            #     a.append(rating.rating)
            # rating = sum(a)/len(a)

            #Ratings.aggregate(Avg('rating'))

            # nickname = review.user_id.users.nickname
            # [review.user for review in reviews]

            results.append({
                "id"             : restaurant.id,
                "name"           : restaurant.name,
                # "rating"         : rating,
                "address"        : restaurant.address,
                "phone_number"   : restaurant.phone_number,
                "category"       : restaurant.category.name,
                "location"       : restaurant.location.area,
                "serving_price"  : restaurant.serving_price.price,
                "menus"          : [{"item" : menu.item, "item_price" : int(menu.item_price)} for menu in menus],
                "is_wished"      : is_wished,
                "review"         : [{
                    "user_id"    : review.user_id,
                    # "user_name"  : nickname,
                    "description": review.description,
                    # "rating"     : restaurant.ratings_set.rating,
                    "created_at" : review.created_at,
                    "images"     : {
                        # review.review_images_set.image
                    }
                } for review in reviews]
            })
            return JsonResponse({"results": results}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)