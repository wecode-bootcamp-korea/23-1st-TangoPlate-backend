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
            reviews = Review.objects.filter(restaurant_id=restaurant.id)
            results.append(
                {
                    "id"          : restaurant.id,
                    "name"        : restaurant.name,
                    "address"     : restaurant.address,
                    "is_wished"   : restaurant.wishlist_set.exists(),
                    "rating"      : reviews.aggregate(Avg('rating')),
                    "review"      : [{
                        "description" : review.description,
                        "images"      : [{"url" : image.url} for image in review.image_set.all()]
                    } for review in restaurant.review_set.all()]
                }
            )

        return JsonResponse({'MESSAGE':results}, status=200)