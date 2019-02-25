from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('users/<int:user_id>/not_authorized/', views.user_not_authorized, name='user_not_authorized'),
    path('users/<int:user_id>/', views.viewUser, name='viewUser'),
    path('in/', views.loggedIn, name='loggedIn'),
]