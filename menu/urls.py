from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, RestaurantUserViewSet, CategoryViewSet, MenuItemViewSet, RegisterView

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'restaurants/(?P<restaurant_id>\d+)/categories', CategoryViewSet, basename='category')
router.register(r'restaurants/(?P<restaurant_id>\d+)/menuItems', MenuItemViewSet, basename='menuitem')
router.register(r'restaurants/(?P<restaurant_id>\d+)/users', RestaurantUserViewSet, basename='restaurant-users')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register_user'),  # Ruta para registro
]