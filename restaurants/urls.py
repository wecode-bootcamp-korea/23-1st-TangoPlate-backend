from restaurants.models import Restaurant
from django.urls       import path

from restaurants.views import SearchView

urlpatterns = [
    path("search", SearchView.as_view()),
]