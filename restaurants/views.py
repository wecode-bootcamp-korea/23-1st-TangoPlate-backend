import json, re, bcrypt, jwt

from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Avg, Q
from django.core.exceptions import FieldError

from users.models           import User, WishList
from restaurants.models     import Restaurant
from reviews.models         import Review, ReviewImage
from users.utils            import login_decorator
class RestaurantDetailView(View):
    @login_decorator
    def get(self, request, restaurant_id):
        try:
            user = request.user

            if not Restaurant.objects.filter(id = restaurant_id).exists():
                return JsonResponse({"MESSAGE": "NOT_EXIST"}, status=404)
                
            restaurant         = Restaurant.objects.get(id = restaurant_id)
            
            result = {
                "id"             : restaurant.id,
                "name"           : restaurant.name,
                "rating"         : restaurant.review_set.all().aggregate(rating = Avg('rating'))['rating'],
                "restaurant_img" : restaurant.review_set.last().reviewimage_set.last().image,
                "address"        : restaurant.address,
                "phone_number"   : restaurant.phone_number,
                "category"       : restaurant.category.name,
                "location"       : restaurant.location.area,
                "serving_price"  : restaurant.serving_price.price,
                "menus" : [{
                    "menu_id"    : menu.id,   
                    "item"       : menu.item, 
                    "item_price" : menu.item_price
                } for menu in restaurant.menu_set.all()],
                "is_wished"      : user.wishlist_set.filter(restaurant_id=restaurant.id).exists() if user else None,
                "reviews"        : [{
                    "id"         :  review.id,
                    "user" : {
                        "user_id" : review.user.id,
                        "email"   : review.user.email,
                        "name"    : review.user.nickname,
                    },
                    "description": review.description,
                    "rating"     : review.rating,
                    "created_at" : review.created_at,
                    "images_url" : review.reviewimage_set.last().image,
                } for review in restaurant.review_set.all()]
            }
            return JsonResponse({"result": result}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

class RestaurantListView(View):
    @login_decorator
    def get(self, request):
        try:
            category_id       = request.GET.get("categoryId")
            location_id       = request.GET.get("locationId")
            serving_price_id  = request.GET.get("servingPriceId")

            q = Q()

            if category_id:
                q &= Q(category_id = category_id)

            if location_id:
                q &= Q(location_id = location_id)

            if serving_price_id:
                q &= Q(serving_price_id = serving_price_id)

            restaurants = [{
                    "id"          : restaurant.id,
                    "name"        : restaurant.name,
                    "image"       : restaurant.review_set.filter(restaurant_id=restaurant.id)[0].reviewimage_set.last().image,
                    "rating"      : restaurant.review_set.all().aggregate(rating = Avg('rating'))['rating'],
                    "address"     : restaurant.address,
                    "is_wished"   : request.user.wishlist_set.filter(restaurant_id=restaurant.id).exists() if request.user else None,
                    "btn_toggle"  : False,
                    "review_id"   : restaurant.review_set.all().order_by('-created_at')[0].id if restaurant.review_set.all().order_by('-created_at')[0] else None,
                    "user_id"     : restaurant.review_set.all().order_by('-created_at')[0].user_id if restaurant.review_set.all().order_by('-created_at')[0] else None,
                    "user_name"   : restaurant.review_set.all().order_by('-created_at')[0].user.nickname if restaurant.review_set.all().order_by('-created_at')[0] else None,
                    "description" : restaurant.review_set.all().order_by('-created_at')[0].description if restaurant.review_set.all().order_by('-created_at')[0] else None,
                } for restaurant in Restaurant.objects.filter(q).order_by('name')]
            return JsonResponse({"restaurant" : restaurants}, status=200)

        except FieldError:
            return JsonResponse({"RESULT" : "FILTER_ERROR"}, status=404)
class SearchView(View):
    def get(self, request):
        search = request.GET.get('search', None)
        results = []
        restaurants = Restaurant.objects.none()

        if Category.objects.filter(name__contains=search).exists():
            restaurants = Restaurant.objects.filter(category__name__contains=search)

        if Menu.objects.filter(item__contains=search).exists():
            restaurants = restaurants.union(Restaurant.objects.filter(menu__item__contains=search))

        if Restaurant.objects.filter(address__contains=search).exists():
            restaurants = restaurants.union(Restaurant.objects.filter(address__contains=search))

        if Restaurant.objects.filter(name__contains=search).exists():
            restaurants = restaurants.union(Restaurant.objects.filter(name__contains=search))

        for restaurant in restaurants:
            results.append(
                {
                        "id"          : restaurant.id,
                        "name"        : restaurant.name,
                        "address"     : restaurant.address,
                        "is_wished"   : restaurant.wishlist_set.exists(),
                        "btn_toggle"  : False,
                        "rating"      : restaurant.review_set.all().aggregate(Avg('rating')),
                        "review"      : restaurant.first_review,
                }
            )

        return JsonResponse({'MESSAGE':results}, status=200)