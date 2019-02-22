from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('users/<int:user_id>/', views.viewUser, name='viewUser'),
]