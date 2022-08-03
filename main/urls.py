from . import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('view_inventory', views.view_inventory),
    path('add_item_page', views.add_item_page),
    path('create_item', views.create_item),
    path('item_sold_form/<int:item_id>', views.item_sold_form),
    path('complete_sell/<int:item_id>', views.complete_sell),
    path('finance_page', views.finance_page),
    path('add_to_backlog', views.add_to_backlog),
    path('mileage_sheet', views.mileage_sheet),
    path('login', views.login),
    path('logout', views.logout),
]