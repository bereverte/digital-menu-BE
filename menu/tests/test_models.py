from django.test import TestCase
from menu.models import MenuItem, Category, Restaurant

class RestaurantModelTests(TestCase):
    
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Imagine Dragons", phone=621998450)

    def test_restaurant_creation(self):
        self.assertEqual(self.restaurant.name, "Imagine Dragons")
        self.assertEqual(self.restaurant.phone, 621998450)

class CategoryModelTests(TestCase):
    
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Imagine Dragons")
        self.category1 = Category.objects.create(name="Pizzes", restaurant=self.restaurant)
        self.category2 = Category.objects.create(name="Pasta", restaurant=self.restaurant)
        self.category3 = Category.objects.create(name="Plat del dia", restaurant=self.restaurant)

    def test_category_creation(self):
        self.assertEqual(self.category1.name, "Pizzes")
        self.assertEqual(self.category2.name, "Pasta")
        self.assertEqual(self.category3.name, "Plat del dia")

class MenuItemModelTests(TestCase):

    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Imagine Dragons")
        self.category1 = Category.objects.create(name="Pizzes", restaurant=self.restaurant)
        self.category2 = Category.objects.create(name="Pasta", restaurant=self.restaurant)
        self.category3 = Category.objects.create(name="Plat del dia", restaurant=self.restaurant)

        self.menu_item1 = MenuItem.objects.create(
            name="Pizza Margherita",
            description="Pizza amb tomàquet i mozzarella",
            price=10.50
        )
        self.menu_item1.categories.add(self.category1)

        self.menu_item2 = MenuItem.objects.create(
            name="Espaguetis Carbonara",
            description="Espaguetis amb ou, guanciale, formatge i pebre",
            price=13.00
        )
        self.menu_item2.categories.add(self.category2)
        self.menu_item2.categories.add(self.category3)

        self.menu_item3 = MenuItem.objects.create(
            name="Macarrons Bolonyesa",
            description="Macarrons amb tomata, carn picada i pastanaga",
            price=12.50
        )
        self.menu_item3.categories.add(self.category2)

    def test_menu_item_creation(self):
        self.assertEqual(self.menu_item1.name, "Pizza Margherita")
        self.assertEqual(self.menu_item2.price, 13.00)
        self.assertEqual(self.menu_item3.description, "Macarrons amb tomata, carn picada i pastanaga")

    def test_menu_item_category_association(self):
        self.assertIn(self.category1, self.menu_item1.categories.all())
        self.assertEqual(self.menu_item1.categories.count(), 1)

        self.assertIn(self.category2, self.menu_item2.categories.all())
        self.assertEqual(self.menu_item2.categories.count(), 2)

        self.assertIn(self.category2, self.menu_item3.categories.all())
        self.assertEqual(self.menu_item3.categories.count(), 1)