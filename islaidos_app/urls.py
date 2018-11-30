from django.urls import path
from .views import sarasas, sukurti, pakeisti, istrinti

urlpatterns = [
    path('', sarasas, name='sarasas'),
    path('naujas', sukurti, name='sukurti'),
    path('pakeisti/<int:id>/', pakeisti, name='pakeisti'),
    path('istrinti/<int:id>/', istrinti, name='istrinti'),
]

