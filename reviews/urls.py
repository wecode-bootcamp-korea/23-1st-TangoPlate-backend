from django.urls import path

from reviews.models import Review
from reviews.views import ReviewView

urlpatterns = [
    path('/<int:restaurant_id>', ReviewView.as_view()),
]