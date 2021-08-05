from django.urls import path
from .views      import ReviewView

urlpatterns = [
    # path("/restaurant/?no=<int:restaurant_id>", RestaurantDetailView.as_view()),
    path("/<int:restaurant_id>", ReviewView.as_view()),
]