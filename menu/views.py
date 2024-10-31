from rest_framework import viewsets
from .models import Restaurant, RestaurantUser, Category, MenuItem
from .serializers import RestaurantSerializer, RestaurantUserSerializer, CategorySerializer, MenuItemSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        restaurant_user = RestaurantUser.objects.get(user=token.user)
        restaurant = restaurant_user.restaurant
        return Response({
            'token': token.key,
            'user_id': token.user.pk,
            'restaurant_id': restaurant_user.restaurant.id,  # Devolvemos el restaurant_id
            'restaurant_name': restaurant.name,
            'email': token.user.email
        })

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def update(self, request, *args, **kwargs):
        restaurant = self.get_object()
        data = request.data

        if 'name' in data:
            restaurant.name = data['name']

        if 'logo' in data:
            restaurant.logo = data['logo']

        restaurant.save()

        serializer = self.get_serializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return Category.objects.filter(restaurant_id=restaurant_id)

    def perform_create(self, serializer):
        restaurant_id = self.kwargs['restaurant_id']
        restaurant = Restaurant.objects.get(id=restaurant_id)
        serializer.save(restaurant=restaurant)
    
    @action(detail=False, methods=['get'], url_path='check')
    def check_category_exists(self, request, restaurant_id=None):
        """
        Verifica si una categoría con el mismo nombre ya existe en el restaurante.
        """
        category_name = request.query_params.get('name')

        if category_name:
            exists = Category.objects.filter(
                restaurant_id=restaurant_id,
                name__iexact=category_name
            ).distinct().exists()
            
            return Response({"exists": exists})
        
        return Response({"exists": False}, status=400)

class MenuItemViewSet(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return MenuItem.objects.filter(categories__restaurant_id=restaurant_id).distinct()

    
    @action(detail=False, methods=['get'], url_path='check')
    def check_menu_item_exists(self, request, restaurant_id=None):
        """
        Verifica si un ítem de menú con el mismo nombre y al menos una de las categorías ya existe.
        """
        item_name = request.query_params.get('name')
        category_ids = request.query_params.get('categories', "").split(",")  # Lista de IDs de categorías

        if item_name and category_ids:
            # Convertir las categorías a una lista de enteros
            category_ids = list(map(int, category_ids))

            # Buscar ítems de menú con el mismo nombre (insensible a mayúsculas)
            menu_items = MenuItem.objects.filter(
                categories__restaurant_id=restaurant_id,
                name__iexact=item_name  # Insensible a mayúsculas
            ).distinct()

            # Comprobar si alguna de las categorías seleccionadas coincide con las categorías del ítem existente
            for item in menu_items:
                item_categories = list(item.categories.values_list('id', flat=True))  # IDs de las categorías del ítem
                if any(cat_id in item_categories for cat_id in category_ids):
                    return Response({"exists": True})

            return Response({"exists": False})
    
        return Response({"exists": False}, status=400)  # 400 si faltan parámetros o son incorrectos


class RestaurantUserViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantUserSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return RestaurantUser.objects.filter(restaurant_id=restaurant_id)
    

class RegisterView(APIView):
    """
    Vista para registrar un nuevo usuario y su restaurante asociado.
    """

    permission_classes = [AllowAny]  # Permitir el acceso sin autenticación

    def post(self, request):
        restaurant_name = request.data.get('restaurant_name')
        email = request.data.get('email')
        password = request.data.get('password')

        # Verificar que los campos obligatorios estén presentes
        if not all([restaurant_name, email, password]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si ya existe un usuario con ese email
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already in use."}, status=status.HTTP_400_BAD_REQUEST)

        # Crear el restaurante
        restaurant = Restaurant.objects.create(name=restaurant_name)

        # Crear el usuario de Django
        user = User.objects.create_user(username=email, email=email, password=password)

        # Crear el RestaurantUser y asociarlo con el restaurante
        RestaurantUser.objects.create(user=user, restaurant=restaurant)

        return Response({"message": "User and restaurant created successfully."}, status=status.HTTP_201_CREATED)
    
class ProtectedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Authenticated successfully"})
