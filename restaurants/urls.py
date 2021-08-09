from django.urls import path

from .views      import RestaurantDetailView, RestaurantFilterView

urlpatterns = [
    path("/<int:restaurant_id>", RestaurantDetailView.as_view()),
    path("", RestaurantFilterView.as_view()),
]