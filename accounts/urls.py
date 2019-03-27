from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('users/<int:user_id>/', views.viewUser, name='viewUser'),
    path('users/<int:user_id>/edit/', views.editUser, name='editUser'),
    path('in/', views.loggedIn, name='loggedIn'),
]