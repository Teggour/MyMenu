from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from .models import *
from .forms import *


# Create your views here.
class HomeView(ListView):
    model = Dish
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_dish'] = Dish.objects.all()
        return context


class ShowIngredientsInDish(DetailView):
    model = Dish
    template_name = 'ingredients_in_dish.html'

    def get_context_data(self, **kwargs):
        context = super(ShowIngredientsInDish, self).get_context_data(**kwargs)
        context['dishes'] = self.model.objects.all()
        context['dish'] = self.get_object()
        context['all_ingredients'] = self.get_object().ingredients.all()

        return context


class AddDishView(CreateView):
    model = Dish
    add_dish_form = AddDishForm()
    template_name = 'add_dish.html'

    def get(self, request, *args, **kwargs):
        add_dish_form = AddDishForm
        add_ingredients_form = AddIngredientsFormSet
        context = {'add_dish_form': add_dish_form, 'add_ingredients_form': add_ingredients_form}

        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        add_dish_form = AddDishForm(request.POST)
        add_ingredients_form = AddIngredientsFormSet(request.POST)
        context = {'add_dish_form': add_dish_form, 'add_ingredients_form': add_ingredients_form}

        if add_dish_form.is_valid():
            dish = add_dish_form.save(commit=False)
            dish.author = request.user
            dish.save()

            for form in add_ingredients_form:
                if form.is_valid():
                    ingredients = form.save(commit=False)
                    ingredients.save()
                    dish.ingredients.add(ingredients)
                    dish.save()

            return redirect('home')
        return render(self.request, self.template_name, context)


class AddOrderView(CreateView):
    template_name = 'add_order.html'

    def get(self, request, *args, **kwargs):
        order_dish = Dish.objects.get(id=self.kwargs['dish_id'])
        add_order_form = AddOrderForm()
        add_ingredient_form = AddIngredientsInOrderFormSet(queryset=Ingredients.objects.filter(dishes=self.kwargs['dish_id']))
        context = {'add_order_form': add_order_form,
                   'order_dish': order_dish,
                   'add_ingredient_form': add_ingredient_form, }
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        order_dish = Dish.objects.get(id=self.kwargs['dish_id'])
        add_order_form = AddOrderForm(request.POST)
        add_ingredient_form = AddIngredientsInOrderFormSet(request.POST)
        context = {'add_order_form': add_order_form,
                   'order_dish': order_dish,
                   'add_ingredient_form': add_ingredient_form, }
        if add_order_form.is_valid():
            order = add_order_form.save(commit=False)
            order.dish = order_dish
            order.author = request.user
            order.save()

            for form in add_ingredient_form:
                if form.is_valid():
                    ingredient = form.save(commit=False)
                    ingredient_in_order = IngredientsInOrder(name=ingredient.ingredient_name, count=ingredient.count)
                    ingredient_in_order.save()
                    order.ingredients.add(ingredient_in_order)
                    order.save()

            return redirect('orders')
        return render(self.request, self.template_name, context)


class OrdersView(ListView):
    model = Order
    template_name = 'all_orders.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(author_id=user_id)
        return context


class OrderView(DetailView):
    model = Order
    template_name = 'ingredients_in_order.html'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['orders'] = self.model.objects.all()
        context['order'] = self.get_object()
        context['ingredients'] = self.get_object().ingredients.all()
        return context
