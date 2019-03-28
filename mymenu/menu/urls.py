from django.urls import path, include
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('add_dish/', AddDishView.as_view(), name='add_dish'),

    path('dish/<int:pk>', ShowIngredientsInDish.as_view(), name='ingredients'),

    path('add_order/<int:dish_id>', AddOrderView.as_view(), name='add_order'),

    path('orders/', OrdersView.as_view(), name='orders'),

    path('orders/<int:pk>', OrderView.as_view(), name='order_detail'),

]
