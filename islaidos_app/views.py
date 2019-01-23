from django.shortcuts import render, redirect
from .models import Expenses, ExpenseTypes
from .forms import IslaidosForm, TiekejaiForm
from django.db.models import Sum


def data_for_the_google_chart():
    visi_islaidu_tipai = ExpenseTypes.objects.all()
    islaidu_tipu_pavadinimai = [islaidu_tipas.tipas for islaidu_tipas in visi_islaidu_tipai]
    l = [['Islaidu tipas', 'Total Suma']]
    for islaidu_tipo_pavadinimas in islaidu_tipu_pavadinimai:
        islaidos_tipui = Expenses.objects.filter(tipas__tipas=islaidu_tipo_pavadinimas)
        islaidu_tipui_suma = islaidos_tipui.aggregate(Sum('suma'))
        tvarkinga_islaidu_tipui_suma = islaidu_tipui_suma['suma__sum'] or 0.00
        l.append([islaidu_tipo_pavadinimas, float(tvarkinga_islaidu_tipui_suma)])
    return l

#Main page view
def index(request):
    chart_data = data_for_the_google_chart()
    islaidos = Expenses.objects.all().order_by('-data')
    islaidu_tipai = ExpenseTypes.objects.all().order_by('-aktyvus', 'tipas')
    islaidu_suma = list(Expenses.objects.aggregate(Sum('suma')).values())[0]
    return render(request, 'sarasas.html', \
                  {'islaidos': islaidos, 'islaidu_tipai':islaidu_tipai, 'islaidu_suma':islaidu_suma, 'chart_data':chart_data})


#Expense views
def createExpense(request):
    form = IslaidosForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('sarasas')

    return render(request, 'islaidos-form.html', {'form': form})

def editExpense(request, id):
    islaidu_irasas = Expenses.objects.get(id=id)
    form = IslaidosForm(request.POST or None, instance=islaidu_irasas)

    if form.is_valid():
         form.save()
         return redirect('sarasas')

    return render(request, 'islaidos-form.html', {'form':form, 'islaidu_irasas': islaidu_irasas})

def deleteExpense(request, id):
    islaidu_irasas = Expenses.objects.get(id=id)

    if request.method == 'POST':
        islaidu_irasas.delete()
        return redirect('sarasas')

    return render(request, 'islaidu-istrynimo-patvirtinimas.html', {'islaidu_irasas': islaidu_irasas})


#Expense type views
def createType(request):
    form = TiekejaiForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('sarasas')

    return render(request, 'tipas-form.html', {'form': form})

def editType(request, id):
    islaidu_tipas = ExpenseTypes.objects.get(id=id)
    form = TiekejaiForm(request.POST or None, instance=islaidu_tipas)

    if form.is_valid():
        form.save()
        return redirect('sarasas')

    return render(request, 'tipas-form.html', {'form': form, 'islaidu_tipas': islaidu_tipas})

def deleteType(request, id):
    islaidu_tipas = ExpenseTypes.objects.get(id=id)

    if request.method == 'POST':
        islaidu_tipas.delete()
        return redirect('sarasas')

    return render(request, 'tipo-istrynimo-patvirtinimas.html', {'islaidu_tipas': islaidu_tipas})







