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
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']
    

class RestaurantSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    menuItems = serializers.SerializerMethodField()
    logo = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'hours', 'phone', 'logo', 'categories', 'menuItems']

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Restaurant name is required.")
        return value

    def get_menuItems(self, obj):
        menu_items = MenuItem.objects.filter(categories__restaurant=obj).distinct()
        return MenuItemSerializer(menu_items, many=True).data


class RestaurantUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)

    class Meta:
        model = RestaurantUser
        fields = ['id', 'email', 'restaurant_name']