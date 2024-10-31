from django.contrib import admin
from .models import Restaurant, RestaurantUser, Category, MenuItem

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    search_fields = ('name',)

# Registre del model RestaurantUser (perfil d'usuari)
@admin.register(RestaurantUser)
class RestaurantUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant')
    search_fields = ('user__username', 'restaurant__name')
    list_filter = ('restaurant',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant')
    search_fields = ('name',)
    list_filter = ('restaurant',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_categories', 'price')
    search_fields = ('name',)
    list_filter = ('categories',)

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    
    display_categories.short_description = 'Categories'