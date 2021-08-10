from   itertools          import chain
import json, re, bcrypt, jwt

from django.views         import View
from django.http          import JsonResponse
from django.db.models     import Q, Avg


from reviews.models       import Review, ReviewImage
from users.models         import User, WishList
from restaurants.models   import Category, Location, Menu, Restaurant

class SearchView(View):
    def get(self, request):
        search = request.GET.get('search', None)
        category_restaurants = []
        menu_restaurants = []
        restaurants = []
        results = []

        if Category.objects.filter(name__contains=search).exists():
            categories = Category.objects.filter(name__contains=search)
            for category in categories:
                category_restaurants = Restaurant.objects.filter(category_id=category.id)

        if Menu.objects.filter(item__contains=search).exists():
            menus = Menu.objects.filter(item__contains=search)
            for menu in menus:
                menu_Restaurants = Restaurant.objects.filter(id=menu.restaurant.id)

        if Restaurant.objects.filter(address__contains=search, name__contains=search):
            restaurants = Restaurant.objects.filter(address__contains=search, name__contains=search)
        all_restaurant = list(chain(category_restaurants, menu_restaurants, restaurants))
        for restaurant in all_restaurant:
            reviews = Review.objects.filter(restaurant_id=restaurant.id)
            results.append(
                {
                    "id"          : restaurant.id,
                    "name"        : restaurant.name,
                    "address"     : restaurant.address,
                    "rating"      : reviews.aggregate(Avg('rating')),
                    "review"      : [{
                    "description" : review.description,
                    "images"      : [{
                    "image_url"   : imageobject.image
                } for imageobject in ReviewImage.objects.filter(review_id=review.id)]
                } for review in reviews]
                }
            )

        return JsonResponse({'MESSAGE':results}, status=200)
