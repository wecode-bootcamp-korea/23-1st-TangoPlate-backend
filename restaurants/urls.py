from django.urls        import path

from restaurants.models import Restaurant
from .views             import RestaurantDetailView, RestaurantListView, SearchView

urlpatterns = [
    path("restaurant/<int:restaurant_id>", RestaurantDetailView.as_view()),
    path("", RestaurantListView.as_view()),
    path("search", SearchView.as_view()),
]