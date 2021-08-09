from django.urls import path

from .views      import RestaurantDetailView, RestaurantListView

urlpatterns = [
    path("/<int:restaurant_id>", RestaurantDetailView.as_view()),
    path("", RestaurantListView.as_view()),
]