from django.urls import path
from .views import index, createExpense, editExpense, deleteExpense, createType, editType, deleteType

urlpatterns = [
    #BENDRAS PRADINIS
    path('', index, name='sarasas'),

    #IŠLAIDOS
    path('new-expense', createExpense, name='sukurti_is'),
    path('edit-expense/<int:id>/', editExpense, name='pakeisti_is'),
    path('delete-expense/<int:id>/', deleteExpense, name='istrinti_is'),

    #IŠLAIDŲ TIPAI
    path('new-type', createType, name='sukurti_tipa'),
    path('edit-type/<int:id>/', editType, name='pakeisti_tipa'),
    path('delete-type/<int:id>/', deleteType, name='istrinti_tipa'),
]

