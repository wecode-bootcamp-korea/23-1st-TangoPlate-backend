from reviews.models import Review
from django.urls import path
from reviews.views import ReviewCreateView, ReviewUpdateDeleteView

urlpatterns = [
    path('<int:restaurant_id>/review', ReviewCreateView.as_view()),
    path('<int:restaurant_id>/review/<int:review_id>', ReviewUpdateDeleteView.as_view()),
]