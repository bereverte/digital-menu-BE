from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from menu.models import MenuItem, Category, Restaurant, RestaurantUser
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class RegisterViewSetTests(TestCase):

    def setUp(self):
        
        self.client = APIClient()

        self.register_data = {
            "restaurant_name": "Test Restaurant",
            "email": "test@example.com",
            "password": "securepassword123"
        }

    def test_register_user_and_create_restaurant(self):

        response = self.client.post("/api/register/", self.register_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "User and restaurant created successfully.")

        #Comprovar que s'ha creat be a la base de dades
        restaurant = Restaurant.objects.get(name="Test Restaurant")
        self.assertIsNotNone(restaurant)
        self.assertEqual(restaurant.name, "Test Restaurant")

        # Comprovar que el restaurant està associat amb un usuari
        restaurant_user = RestaurantUser.objects.get(restaurant=restaurant)
        self.assertIsNotNone(restaurant_user)
        self.assertEqual(restaurant_user.user.email, "test@example.com")

    def test_register_missing_fields(self):

        self.invalid_data = {
            "restaurant_name": "",
            "email": "test@example.com",
            "password": "securepassword123"
        }

        response = self.client.post("/api/register/", self.invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "All fields are required.")

    def test_register_user_email_already_exists(self):

        User.objects.create_user(username="test@example.com", email="test@example.com", password="securepassword123")

        response = self.client.post("/api/register/", {
            "restaurant_name": "Another Restaurant",
            "email": "test@example.com",
            "password": "securepassword123"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Email already in use.")


class RestaurantViewSetTests(TestCase):

    def setUp(self):
        
        self.client = APIClient()

        self.restaurant = Restaurant.objects.create(name="Test Restaurant", phone=123456789)

        user = User.objects.create_user(username="test@example.com", email="test@example.com", password="securepassword123")
        self.user = RestaurantUser.objects.create(user=user, restaurant=self.restaurant)
        
        self.token = Token.objects.create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.updated_data = {
            "name": "Updated Restaurant",
            "phone": "123123123",
            "hours": "19:30 - 23:00"
        }

    def test_update_restaurant(self):

        response = self.client.put(f"/api/restaurants/{self.restaurant.id}/", self.updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Restaurant")
        self.assertEqual(response.data["phone"], "123123123")
        self.assertIsNone(response.data["address"])
        self.assertEqual(response.data["hours"], "19:30 - 23:00")

    def test_update_restaurant_without_authentication(self):
        
        self.client.credentials()

        response = self.client.put(f"/api/restaurants/{self.restaurant.id}/", self.updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CategoryViewSetTests(TestCase):

    def setUp(self):
    
        self.client = APIClient()

        self.restaurant = Restaurant.objects.create(name="Test Restaurant", phone=123456789)

        user = User.objects.create_user(username="test@example.com", email="test@example.com", password="securepassword123")
        self.user = RestaurantUser.objects.create(user=user, restaurant=self.restaurant)
        
        self.token = Token.objects.create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.category_data = {"name": "Pizzes"}

    def test_get_category(self):

        Category.objects.create(**self.category_data, restaurant=self.restaurant)
        response = self.client.get(f"/api/restaurants/{self.restaurant.id}/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_categories(self):

        response = self.client.post(f"/api/restaurants/{self.restaurant.id}/categories/", self.category_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_categories_without_name(self):

        self.invalid_category = {"name": ""}

        response = self.client.post(f"/api/restaurants/{self.restaurant.id}/categories/", self.invalid_category, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_category(self):

        category = Category.objects.create(**self.category_data, restaurant=self.restaurant)
        self.updated_category_data = {"name": "Pizzes Cassolanes"}

        response = self.client.put(f"/api/restaurants/{self.restaurant.id}/categories/{category.id}/", self.updated_category_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Pizzes Cassolanes")


    def test_check_categoty_exists(self):

        self.client.post(f"/api/restaurants/{self.restaurant.id}/categories/", self.category_data, format="json")
        response = self.client.get(f"/api/restaurants/{self.restaurant.id}/categories/check/?name=Pizzes")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['exists'])

    def test_check_category_not_exists(self):

        response = self.client.get(f"/api/restaurants/{self.restaurant.id}/categories/check/?name=Pasta")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['exists'])

    def test_category_without_authentication(self):
        
        self.client.credentials()

        response = self.client.post(f"/api/restaurants/{self.restaurant.id}/categories/", self.category_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MenuItemViewSetTests(TestCase):

    def setUp(self):
    
        self.client = APIClient()

        self.restaurant = Restaurant.objects.create(name="Test Restaurant", phone=123456789)

        self.category = Category.objects.create(name="Pizzes", restaurant=self.restaurant)

        user = User.objects.create_user(username="test@example.com", email="test@example.com", password="securepassword123")
        self.user = RestaurantUser.objects.create(user=user, restaurant=self.restaurant)
        
        self.token = Token.objects.create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.menu_item_data = {"name": "Pizza Margherita",
                               "categories": [self.category.id],
                               "description": "Pizza amb tomàquet i mozzarella",
                               "price": "10.50"}
        
        self.menu_item = MenuItem.objects.create(name="Pizza Margherita",
                                                 description="Pizza amb tomàquet i mozzarella",
                                                 price=10.50)
        self.menu_item.categories.add(self.category)
        
    def test_get_menu_item(self):
        
        response = self.client.get(f"/api/restaurants/{self.restaurant.id}/menuItems/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_create_menu_item(self):

        response = self.client.post(f"/api/restaurants/{self.restaurant.id}/menuItems/", self.menu_item_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Pizza Margherita")

    def test_create_menu_item_without_name(self):

        self.invalid_menu_item = {"name": "",
                                  "categories": [self.category.id],
                                  "description": "Pizza amb tomàquet i mozzarella",
                                  "price": "10.50"}

        response = self.client.post(f"/api/restaurants/{self.restaurant.id}/menuItems/", self.invalid_menu_item, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_menu_item(self):

        updated_menu_item_data = {"name": "Pizza Margherita",
                                  "categories": [self.category.id],
                                  "description": "Pizza amb tomàquet i mozzarella",
                                  "price": "12.50"}
        
        response = self.client.put(f"/api/restaurants/{self.restaurant.id}/menuItems/{self.menu_item.id}/", updated_menu_item_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Pizza Margherita")
        self.assertEqual(response.data['price'], "12.50")

    def test_check_menu_item_exists(self):

        response = self.client.get(f"/api/restaurants/{self.restaurant.id}/menuItems/check/?name=Pizza Margherita&categories={self.category.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['exists'])

    def test_delete_menu_item(self):

        response = self.client.delete(f'/api/restaurants/{self.restaurant.id}/menuItems/{self.menu_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MenuItem.objects.count(), 0)

    def test_update_menu_item_availability(self):

        self.assertTrue(self.menu_item.is_available)

        response = self.client.patch(f'/api/restaurants/{self.restaurant.id}/menuItems/{self.menu_item.id}/toggle-availability/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["is_available"], False)

        response = self.client.patch(f'/api/restaurants/{self.restaurant.id}/menuItems/{self.menu_item.id}/toggle-availability/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["is_available"], True)

    def test_menu_item_without_authentication(self):
        
        self.client.credentials()

        response = self.client.post(f"/api/restaurants/{self.restaurant.id}/menuItems/", self.menu_item_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RestaurantUserViewSetTests(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.restaurant = Restaurant.objects.create(name="Test Restaurant", phone=123456789)

        user = User.objects.create_user(username="test@example.com", email="test@example.com", password="securepassword123")
        self.user = RestaurantUser.objects.create(user=user, restaurant=self.restaurant)
        
        self.token = Token.objects.create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_authenticated_user(self):
        
        response = self.client.get(f"/api/restaurants/{self.restaurant.id}/users/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_get_authenticated_user_without_authentication(self):
        
        self.client.credentials()
        response = self.client.get(f"/api/restaurants/{self.restaurant.id}/users/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_restaurant_user(self):
        
        response = self.client.get(f"/api/restaurants/{self.restaurant.id}/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_restaurant_user_not_found(self):
        
        response = self.client.get(f"/api/restaurants/{self.restaurant.id}/restaurantusers/{99999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)