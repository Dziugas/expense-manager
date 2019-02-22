from django.urls import path
from . import views

app_name = 'islaidos_app'

urlpatterns = [
    #Keepers
    path('<int:keeper_id>/', views.viewKeeper, name='viewKeeper'),
    path('<int:keeper_id>/delete/', views.deleteKeeper, name='deleteKeeper'),
    path('<int:keeper_id>/edit/', views.editKeeper, name='editKeeper'),

    #Expenses
    path('<int:keeper_id>/new-expense/', views.createExpense, name='create_expense'),
    path('<int:keeper_id>/edit-expense/<int:expense_id>/', views.editExpense, name='edit_expense'),
    path('<int:keeper_id>/delete-expense/<int:expense_id>/', views.deleteExpense, name='delete_expense'),

    #Expense Types
    path('<int:keeper_id>/new-type', views.createType, name='create_type'),
    path('<int:keeper_id>/edit-type/<int:type_id>/', views.editType, name='edit_type'),
    path('<int:keeper_id>/delete-type/<int:type_id>/', views.deleteType, name='delete_type'),
]

