from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Avg, Q
from django.core.exceptions import FieldError

from restaurants.models     import Restaurant
from reviews.models         import Review, ReviewImage
from users.utils            import login_decorator

class RestaurantDetailView(View):
    def get(self, request, restaurant_id):
        try:
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
            return JsonResponse({"results": results}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

class RestaurantListView(View):
    def get(self, request):
        try:
            category_id       = request.GET.get("category")
            location_id       = request.GET.get("location")
            serving_price_id  = request.GET.get("serving_price")

            q        = Q()

            if category_id:
                q &= Q(category = category_id)

            if location_id:
                q &= Q(location = location_id)

            if serving_price_id:
                q &= Q(serving_price = serving_price_id)

            restaurants = [{
                    "id"          : restaurant.id,
                    "name"        : restaurant.name,
                    "rating"      : restaurant.review_set.all().aggregate(rating = Avg('rating'))['rating'],
                    "address"     : restaurant.address,
                    "is_wished"   : restaurant.wishlist_set.exists(),
                    "btn_toggle"  : False,
                    "review_id"   : restaurant.review_set.all().order_by('-created_at')[0].id,
                    "user_id"     : restaurant.review_set.all().order_by('-created_at')[0].user_id,
                    "user_name"   : restaurant.review_set.all().order_by('-created_at')[0].user.nickname,
                    "description" : restaurant.review_set.all().order_by('-created_at')[0].description,
                } for restaurant in Restaurant.objects.filter(q).order_by('name')]
            return JsonResponse({"restaurant" : restaurants}, status=200)

        except FieldError:
            return JsonResponse({"RESULT" : "FILTER_ERROR"}, status=404)
