from django.urls import path
from .views import sarasas, sukurti_is, pakeisti_is, istrinti_is, sukurti_tipa, pakeisti_tipa, istrinti_tipa

urlpatterns = [
    #BENDRAS PRADINIS
    path('', sarasas, name='sarasas'),

    #IŠLAIDOS
    path('naujos_islaidos', sukurti_is, name='sukurti_is'),
    path('pakeisti_islaidas/<int:id>/', pakeisti_is, name='pakeisti_is'),
    path('istrinti_islaidas/<int:id>/', istrinti_is, name='istrinti_is'),

    #IŠLAIDŲ TIPAI
    path('naujas_tipas', sukurti_tipa, name='sukurti_tipa'),
    path('pakeisti_tipa/<int:id>/', pakeisti_tipa, name='pakeisti_tipa'),
    path('istrinti_tipa/<int:id>/', istrinti_tipa, name='istrinti_tipa'),
]

