from django.urls import path

from users.views import SignUpView, SignInView, WishListView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/restaurant/<int:restaurant_id>/wish', WishListView.as_view()) 
]