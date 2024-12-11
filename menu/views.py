from rest_framework import viewsets
from .models import Restaurant, RestaurantUser, Category, MenuItem
from .serializers import RestaurantSerializer, RestaurantUserSerializer, CategorySerializer, MenuItemSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        restaurant_user = RestaurantUser.objects.get(user=token.user)
        restaurant = restaurant_user.restaurant
        return Response({
            'token': token.key,
            'user_id': token.user.pk,
            'restaurant_id': restaurant_user.restaurant.id,
            'restaurant_name': restaurant.name,
            'email': token.user.email
        })

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        restaurant = self.get_object()
        data = request.data

        # Actualitza els camps que es permet modificar
        if 'name' in data:
            restaurant.name = data['name']

        if 'logo' in data:
            restaurant.logo = data['logo']

        if 'address' in data:
            restaurant.address = data['address']

        if 'phone' in data:
            restaurant.phone = data['phone']

        if 'hours' in data:
            restaurant.hours = data['hours']

        restaurant.save()

        serializer = self.get_serializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny], url_path='public')
    def get_public_restaurant(self, request, pk=None):
        restaurant = self.get_object()
        serializer = self.get_serializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        categories = Category.objects.filter(restaurant_id=restaurant_id)
        return categories

    def perform_create(self, serializer):
        restaurant_id = self.kwargs['restaurant_id']
        category_name = serializer.validated_data.get('name')
        
        if Category.objects.filter(restaurant_id=restaurant_id, name__iexact=category_name).exists():
            raise ValidationError({"error": "Category with this name already exists."})

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
        
        return Response({"exists": False}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='public', permission_classes=[AllowAny])
    def get_public_categories(self, request, restaurant_id=None):
        """
        Endpoint públic per obtenir categories d'un restaurant.
        """
        categories = Category.objects.filter(restaurant_id=restaurant_id)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)

class MenuItemViewSet(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return MenuItem.objects.filter(categories__restaurant_id=restaurant_id).distinct()

    @action(detail=True, methods=['patch'], url_path='toggle-availability')
    def toggle_availability(self, request, pk=None, restaurant_id=None):
        """
        Acción personalizada para alternar el estado de `is_available`.
        """
        try:
            menu_item = self.get_object()  # Obtiene el menú item por su ID
            menu_item.is_available = not menu_item.is_available  # Alterna el valor de is_available
            menu_item.save()
            # Devuelve la respuesta con el estado actualizado
            return Response({"id": menu_item.id, "is_available": menu_item.is_available}, status=status.HTTP_200_OK)
        except MenuItem.DoesNotExist:
            return Response({"error": "Menu item not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['get'], url_path='check')
    def check_menu_item_exists(self, request, restaurant_id=None):
        item_name = request.query_params.get('name')
        category_ids = request.query_params.get('categories', "").split(",")  # Lista de IDs de categorías

        if item_name and category_ids:
            category_ids = list(map(int, category_ids))  # Convertir les categories a una llista d'enters

            # Busquem ítems de menú amb el mateix nom (insensible a majúscules)
            menu_items = MenuItem.objects.filter(
                categories__restaurant_id=restaurant_id,
                name__iexact=item_name
            ).distinct()

            # Comprovar si alguna de les categories seleccionades coincideix amb les categories de l'ítem existent
            for item in menu_items:
                item_categories = list(item.categories.values_list('id', flat=True))
                if any(cat_id in item_categories for cat_id in category_ids):
                    return Response({"exists": True}, status=status.HTTP_200_OK)

            return Response({"exists": False}, status=status.HTTP_200_OK)
    
        return Response({"error": "Missing parameters or invalid values"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='public', permission_classes=[AllowAny])
    def get_public_menu_items(self, request, restaurant_id=None):
        """
        Endpoint públic per obtenir ítems del menú d'un restaurant.
        """
        menu_items = MenuItem.objects.filter(categories__restaurant_id=restaurant_id, is_available=True).distinct()
        serializer = self.get_serializer(menu_items, many=True)
        return Response(serializer.data)

class RestaurantUserViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return RestaurantUser.objects.filter(restaurant_id=restaurant_id)

    @action(detail=False, methods=['get'], url_path='me')
    def get_authenticated_user(self, request, restaurant_id=None):
        """
        Este endpoint devuelve el usuario actualmente autenticado.
        """
        try:
            user = request.user  # Obtener el usuario autenticado desde el token
            """ restaurant_id = self.kwargs['restaurant_id'] """
            restaurant_user = RestaurantUser.objects.get(user=user, restaurant__id=restaurant_id)
            serializer = self.get_serializer(restaurant_user)
            return Response(serializer.data)
        except RestaurantUser.DoesNotExist:
            return Response({"error": "Restaurant user not found"}, status=404)


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
