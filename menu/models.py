from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    hours = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    logo = models.ImageField(upload_to='restaurant_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

class RestaurantUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Restaurant User"
        verbose_name_plural = "Restaurant Users"

    def clean(self):
        # Si no es superuser o staff, el restaurante es obligatorio
        if not self.user.is_superuser and not self.user.is_staff and self.restaurant is None:
            raise ValidationError("A Restaurant User must be associated with a restaurant.")

    def __str__(self):
        if self.restaurant:
            return f'{self.user.username} ({self.restaurant.name})'
        else:
            return self.user.username
    
class Category(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f'{self.restaurant.name} - {self.name}'
    
class MenuItem(models.Model):
    categories = models.ManyToManyField(Category, related_name='items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        category_names = ", ".join([category.name for category in self.categories.all()])
        return f'{self.name} - Categories: {category_names}'
    
    def clean(self):
        if self.price <= 0:
            raise ValidationError("Price must be greater than zero.")