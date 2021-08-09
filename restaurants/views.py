import json, re, bcrypt, jwt

from django.views         import View
from django.http          import JsonResponse
from django.db.models     import Q, Avg

from reviews.models       import Review, ReviewImage
from users.models         import User, WishList, Rating
from restaurants.models   import Category, Location, Menu, Restaurant

class SearchView(View):
    def get(self, request):
            search = request.GET.get('search', None)
            results = []
            if search:
                if Category.objects.filter(name__contains=search).exists():
                    categories = Category.objects.filter(name__contains=search)
                    for category in categories:
                        restaurants = Restaurant.objects.filter(category_id=category)
                        for restaurant in restaurants:
                            reviews = Review.objects.filter(restaurant_id=restaurant.id)
                            results.append(
                                {
                                    "id"      : restaurant.id,
                                    "name"    : restaurant.name,
                                    "rating"  : restaurant.rating_set.rating,
                                    "address" : restaurant.address,
                                    "review"  : [{
                                "description" : review.description,
                                "images"      : [{
                                "image_url"   : imageobject.image
                            } for imageobject in ReviewImage.objects.filter(review_id=review.id)]
                            } for review in reviews]
                            }
                            )

                if Menu.objects.filter(item__contains=search).exists():
                    menus = Menu.objects.filter(item__contains=search)
                    for menu in menus:
                        restaurants = Restaurant.objects.filter(id=menu.restaurant.id)
                        for restaurant in restaurants:
                            reviews = Review.objects.filter(restaurant_id=restaurant.id)
                            results.append(
                                {
                                    "id"      : restaurant.id,
                                    "name"    : restaurant.name,
                                    "rating"  : Rating.objects.filter(restaurant_id=restaurant.id).aggregate(Avg('rating')),
                                    "address" : restaurant.address,
                                    "review"  : [{
                            "description"     : review.description,
                            "images"          : [{
                            "image_url"       : imageobject.image
                            } for imageobject in ReviewImage.objects.filter(review_id=review.id)]
                            } for review in reviews]
                            }
                            )

                if Restaurant.objects.filter(address__contains=search, name__contains=search):
                    restaurants = Restaurant.objects.filter(address__contains=search, name__contains=search)
                    for restaurant in restaurants:
                        reviews = Review.objects.filter(restaurant_id=restaurant.id)
                        results.append(
                            {
                                "id"          : restaurant.id,
                                "name"        : restaurant.name,
                                "rating"      : Rating.objects.filter(restaurant_id=restaurant.id).aggregate(Avg('rating')),
                                "address"     : restaurant.address,
                                "review"      : [{
                                "description" : review.description,
                                "images"      : [{
                                "image_url"   : imageobject.image
                            } for imageobject in ReviewImage.objects.filter(review_id=review.id)]
                            } for review in reviews]
                            }
                        )

            return JsonResponse({'MESSAGE':results}, status=200)