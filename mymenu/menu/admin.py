from django.contrib import admin
from .models import Ingredients, Dish, IngredientsInOrder, Order

# Register your models here.


class DishAdmin(admin.ModelAdmin):
    list_display = ('dish_name', 'author')


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('ingredient_name',)


admin.site.register(Dish, DishAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Order)
admin.site.register(IngredientsInOrder)
