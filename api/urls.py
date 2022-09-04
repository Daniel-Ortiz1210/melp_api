from django.urls import path
from .views import RestaurantDetailView, RestaurantsView, StatisticsView



urlpatterns = [
    path('restaurants/<id>', RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('restaurants/', RestaurantsView.as_view(), name='restaurants'),
    path('restaurants/statistics/', StatisticsView.as_view(), name='statistics')
]