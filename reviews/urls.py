from reviews.views  import ReviewView

from django.urls    import path

urlpatterns = [
    path('/<int:restaurant_id>/review', ReviewView.as_view()),
    path('/<int:restaurant_id>/review/<int:review_id>', ReviewView.as_view()),
]