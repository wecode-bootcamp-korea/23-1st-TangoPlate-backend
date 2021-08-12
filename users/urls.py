from django.urls import path

from users.views import SignUpView, SignInView, WishListView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/wishlist', WishListView.as_view()),
]