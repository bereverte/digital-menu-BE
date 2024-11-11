from rest_framework import serializers
from .models import Restaurant, RestaurantUser, Category, MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )
    category_names = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'is_available', 'categories', 'category_names']

    def get_category_names(self, obj):
        return [category.name for category in obj.categories.all()]

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']

class RestaurantSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    menuItems = serializers.SerializerMethodField()
    logo = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'hours', 'phone', 'logo', 'categories', 'menuItems']

    def get_menuItems(self, obj):
        menu_items = MenuItem.objects.filter(categories__restaurant=obj).distinct()
        return MenuItemSerializer(menu_items, many=True).data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print("Generated logo URL:", representation.get("logo"))  # Afegeix aquest print per veure la URL
        return representation

class RestaurantUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)

    class Meta:
        model = RestaurantUser
        fields = ['id', 'email', 'restaurant_name']