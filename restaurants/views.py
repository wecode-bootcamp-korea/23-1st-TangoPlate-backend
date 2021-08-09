from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Avg, Q
from django.core.exceptions import FieldError

from restaurants.models     import Restaurant, Category, Location, ServingPrice, Menu
from users.models           import User, WishList, Rating
from reviews.models         import Review, ReviewImage
from users.utils            import login_decorator

class RestaurantDetailView(View):
    @login_decorator
    def get(self, request, restaurant_id):
        try:
            restaurant         = Restaurant.objects.get(id = restaurant_id)
            
            # reviews          = Review.objects.filter(restaurant_id = restaurant_id)
            reviews            = restaurant.review_set.all()
            
            is_wished          = restaurant.wishlist_set.filter(restaurant_id=restaurant_id).exists()
            menus              = restaurant.menu_set.filter(restaurant_id=restaurant.id)
            restaurant_ratings = Rating.objects.filter(restaurant_id=restaurant_id)
            # if  Rating.objects.get(user_id = request.user.id, restaurant_id=restaurant_id).exist():
            #     user_rating    = Rating.objects.get(user_id = request.user.id, restaurant_id=restaurant_id)
            rating_num         = restaurant_ratings.aggregate(rating = Avg('rating'))['rating']

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
                                        #"rating"     : review.user.rating_set.get(restaurant_id=restaurant_id).rating,
                                        "created_at" : review.created_at,
                                        "images"     : [{
                                                            "image_url" : imageobject.image
                                                        } for imageobject in ReviewImage.objects.filter(review_id=review.id)]
                } for review in reviews]
            })
            return JsonResponse({"results": results}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

class RestaurantFilterView(View):
    def get(self, request):
        # restaurants  = Restaurant.objects.all().order_by("rating")
        # category_id = request.GET.get('category', None)
        # location_id = request.GET.get('location', None)
        # category_id_list = request.GET.getlist('category', None)
        # restaurants_all = Restaurant.objects.all()

        # filtered_restaurants = restaurants_all.filter(category=category_id)
        # filtered_restaurants = filtered_restaurants.filter(location=location_id)

        # category_filtered_list__in 
        # location_filter = Location.objects.filter(location__in=category_filter)

        try:
            category_id = request.GET.get("category")
            location_id  = request.GET.get("location")
            serving_price_id  = request.GET.get("serving_price")

            q        = Q()

            if category_id:
                q &= Q(category=category_id)

            if location_id:
                q &= Q(location=location_id)

            if serving_price_id:
                q &= Q(serving_price=serving_price_id)

            restaurants = [{
                    "id"          : restaurant.id,
                    "name"        : restaurant.name,
                    "rating"      : Rating.objects.filter(restaurant_id=restaurant.id).aggregate(rating = Avg('rating'))['rating'],
                    "address"     : restaurant.address,
                    "is_wished"   : restaurant.wishlist_set.filter(restaurant_id=restaurant.id).exists(),
                    "btn_toggle"  : False,
                    "review_id"   : Review.objects.filter(restaurant_id=restaurant.id)[0].id,
                    "user_id"     : Review.objects.filter(restaurant_id=restaurant.id)[0].user.id,
                    "user_name"   : Review.objects.filter(restaurant_id=restaurant.id)[0].user.nickname,
                    "description" : Review.objects.filter(restaurant_id=restaurant.id)[0].description,
                } for restaurant in Restaurant.objects.filter(q).order_by("rating")]
            return JsonResponse({"restaurant" : restaurants}, status=200)

        except FieldError:
            return JsonResponse({"RESULT" : "FILTER_ERROR"}, status=404)

        #=====================================================================

        # result = []
        # for restaurant in filtered_restaurants:
        #     result.append({
        #         # "image"      : ReviewImage.objects.filter(review_id=review_id), 
        #         "id"           : restaurant.id,
        #         "name"         : restaurant.name,
        #         "rating"       : Rating.objects.filter(restaurant_id=restaurant.id).aggregate(rating = Avg('rating'))['rating'],
        #         "address"      : restaurant.address,
        #         "is_wished"    : restaurant.wishlist_set.filter(restaurant_id=restaurant.id).exists(),
        #         "review_id"    : Review.objects.filter(restaurant_id=restaurant.id)[0].id,
        #         # "user_id"    : review.user.id,
        #         # "user_name"  : review.user.nickname,
        #         # "description": review.description,
        #     })
        # return JsonResponse({"response":result}, status=200)
