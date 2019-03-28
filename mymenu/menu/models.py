from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Ingredients(models.Model):
    ingredient_name = models.CharField(max_length=200, verbose_name=_('Название ингридиента'))
    count = models.IntegerField(verbose_name=_('Количество порций'), null=True)

    def __str__(self):
        return self.ingredient_name


class Dish(models.Model):
    dish_name = models.CharField(max_length=200, verbose_name=_('Название блюда'))
    ingredients = models.ManyToManyField(Ingredients, related_name='dishes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.dish_name

    def get_absolute_url(self):
        return reverse('ingredients', kwargs={'pk': self.pk})


class IngredientsInOrder(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Название ингридиента'))
    count = models.IntegerField(verbose_name=_('Количество порций'), null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(IngredientsInOrder)

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})
