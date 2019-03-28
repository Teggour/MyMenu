from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from .models import *


class AddIngredientsForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        fields = ('ingredient_name',)


AddIngredientsFormSet = formset_factory(AddIngredientsForm, extra=5)

AddIngredientsInOrderFormSet = modelformset_factory(Ingredients, form=AddIngredientsForm, fields=('ingredient_name', 'count'))


class AddDishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ('dish_name',)
        exclude = ('ingredients', 'author')


class AddOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('dish', 'author', 'ingredients')
