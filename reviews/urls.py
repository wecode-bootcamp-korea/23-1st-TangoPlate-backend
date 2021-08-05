from reviews.models import Review
from django.urls import path

from reviews.views import Review_View

urlpatterns = [
    path('/<int:restaurant_id>', Review_View.as_view()),
    path('/<int:restaurant_id>', Review_View.as_view()),
    path('/<int:restaurant_id>', Review_View.as_view()),
]