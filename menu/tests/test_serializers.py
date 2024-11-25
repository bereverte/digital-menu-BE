from rest_framework.exceptions import ValidationError
from django.test import TestCase
from menu.models import Restaurant, MenuItem, Category
from menu.serializers import MenuItemSerializer, CategorySerializer, RestaurantSerializer

class MenuItemSerializerTests(TestCase):

    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Test Restaurant")
        self.category = Category.objects.create(name="Pizzes", restaurant=self.restaurant)

    def test_valid_serializer_data(self):
        valid_data = {
            'name': "Pizza Margherita",
            'description': "Pizza amb tomàquet i mozzarella",
            'price': 10.50,
            'categories': [self.category.id]
        }

        serializer = MenuItemSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_price(self):
        invalid_data = {
            'name': "Pizza Margherita",
            'description': "Pizza amb tomàquet i mozzarella",
            'price': -10.50,  # Preu invàlid
            'categories': [self.category.id]
        }

        serializer = MenuItemSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'price'})

    def test_create_menu_item_without_name(self):
        invalid_data = {
            'name': "",  # Nom buit
            'description': "Pizza amb tomàquet i mozzarella",
            'price': 10.50,
            'categories': [self.category.id]
        }

        serializer = MenuItemSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'name'})


class CategorySerializerTests(TestCase):

    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Test Restaurant")
        self.category_data = {"name": "Pizzes"}

    def test_valid_category(self):
        serializer = CategorySerializer(data=self.category_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_category_without_name(self):
        invalid_data = {"name": ""}
        serializer = CategorySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'name'})

    def test_create_category(self):
        serializer = CategorySerializer(data=self.category_data)
        if serializer.is_valid():
            category = serializer.save(restaurant=self.restaurant)
            self.assertEqual(category.name, "Pizzes")
            self.assertEqual(category.restaurant, self.restaurant)


class RestaurantSerializerTests(TestCase):

    def setUp(self):
        self.restaurant_data = {
            'name': 'Test Restaurant',
            'address': '123 Test St',
            'hours': '10:00-22:00',
            'phone': '123456789'
        }

    def test_valid_restaurant(self):
        serializer = RestaurantSerializer(data=self.restaurant_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_restaurant_without_name(self):
        invalid_data = {'name': ''}
        serializer = RestaurantSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_create_restaurant(self):
        serializer = RestaurantSerializer(data=self.restaurant_data)
        if serializer.is_valid():
            restaurant = serializer.save()
            self.assertEqual(restaurant.name, 'Test Restaurant')
            self.assertEqual(restaurant.address, '123 Test St')