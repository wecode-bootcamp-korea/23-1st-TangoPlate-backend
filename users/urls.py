from django.urls import path

from users.views import SignUpView, SignInView, WishView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/restaurant/<int:restaurant_id>/wish', WishView.as_view()) 
]