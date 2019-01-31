from django.urls import path
from . import views

urlpatterns = [
    #Home
    path('', views.home, name='home'),

    #Keepers
    path('keepers/<int:keeper_id>/', views.viewKeeper, name='viewKeeper'),
    path('keepers/<int:keeper_id>/delete/', views.deleteKeeper, name='deleteKeeper'),
    path('keepers/<int:keeper_id>/edit/', views.editKeeper, name='editKeeper'),

    #Expenses
    path('keepers/<int:keeper_id>/new-expense/', views.createExpense, name='create_expense'),
    path('keepers/<int:keeper_id>/edit-expense/<int:expense_id>/', views.editExpense, name='edit_expense'),
    path('keepers/<int:keeper_id>/delete-expense/<int:expense_id>/', views.deleteExpense, name='delete_expense'),

    #Expense Types
    path('keepers/<int:keeper_id>/new-type', views.createType, name='create_type'),
    path('keepers/<int:keeper_id>/edit-type/<int:type_id>/', views.editType, name='edit_type'),
    path('keepers/<int:keeper_id>/delete-type/<int:type_id>/', views.deleteType, name='delete_type'),
]

