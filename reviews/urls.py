from reviews.views  import ReviewCreateView, ReviewUpdateDeleteView
from django.urls    import path

urlpatterns = [
    path('/<int:restaurant_id>/review', ReviewCreateView.as_view()),
    path('/<int:restaurant_id>/review/<int:review_id>', ReviewUpdateDeleteView.as_view()),
]