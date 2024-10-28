from django.contrib import admin
from .models import Category, Product, SliderImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']
    list_filter = ['category']

@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'order']

# Удалите эту строку, так как модель уже зарегистрирована через декоратор
# admin.site.register(SliderImage)