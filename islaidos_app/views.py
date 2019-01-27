from django.shortcuts import render, redirect
from .models import Expenses, ExpenseTypes, Keeper
from .forms import ExpenseForm, ExpenseTypeForm, KeeperForm
from django.db.models import Sum


def data_for_the_google_chart(keeper_id):
    all_expense_types_for_one_keeper = ExpenseTypes.objects.filter(keeper=keeper_id)
    expense_type_names = [islaidu_tipas.tipas for islaidu_tipas in all_expense_types_for_one_keeper]
    list_for_chart = [['Expense type', 'Total Sum']]
    for expense_type_name in expense_type_names:
        expenses_for_type = Expenses.objects.filter(tipas__tipas=expense_type_name, keeper=keeper_id)
        sum_of_expenses_for_type = expenses_for_type.aggregate(Sum('suma'))
        sum_of_expenses_for_type_nycely_printed = sum_of_expenses_for_type['suma__sum'] or 0.00
        list_for_chart.append([expense_type_name, float(sum_of_expenses_for_type_nycely_printed)])
    return list_for_chart

def home(request):
    keepers = Keeper.objects.all()
    if request.method == 'POST':
        form = KeeperForm(request.POST)
        if form.is_valid():
            new_keeper = form.save()
            return redirect(f'/keepers/{new_keeper.id}/')
    else:
        form = KeeperForm()
    return render(request, 'home.html', {'keepers':keepers, 'form':form})

def viewKeeper(request, keeper_id):
    chart_data = data_for_the_google_chart(keeper_id)
    keeper_ = Keeper.objects.get(id=keeper_id)
    expense_types = ExpenseTypes.objects.filter(keeper=keeper_).order_by('-aktyvus', 'tipas')
    expenses = Expenses.objects.filter(keeper=keeper_).order_by('-data')
    expenses_total = list(expenses.aggregate(Sum('suma')).values())[0]
    return render(request, 'keeper.html', {'keeper':keeper_, 'expense_types':expense_types, 'expenses':expenses, \
                                           'chart_data':chart_data, 'expenses_total':expenses_total})

def createExpense(request, keeper_id):
    form = ExpenseForm(request.POST or None, initial={'keeper':keeper_id})
    keeper_ = Keeper.objects.get(id=keeper_id)
    form.fields['tipas'].queryset = ExpenseTypes.objects.filter(keeper=keeper_)
    if form.is_valid():

        form.save()
        return redirect('viewKeeper', keeper_id)

    return render(request, 'islaidos-form.html', {'form': form})

def editExpense(request, keeper_id, expense_id):
    expense = Expenses.objects.get(id=expense_id)
    form = ExpenseForm(request.POST or None, instance=expense)

    if form.is_valid():
         form.save()
         return redirect('viewKeeper', keeper_id)

    return render(request, 'islaidos-form.html', {'form':form, 'expense': expense})

def deleteExpense(request, keeper_id, expense_id):
    expense = Expenses.objects.get(id=expense_id)

    if request.method == 'POST':
        expense.delete()
        return redirect('viewKeeper', keeper_id)

    return render(request, 'islaidu-istrynimo-patvirtinimas.html', {'expense': expense})


#Expense type views
def createType(request, keeper_id):
    form = ExpenseTypeForm(request.POST or None, initial={'keeper':keeper_id})

    if form.is_valid():
        form.save()
        return redirect('viewKeeper', keeper_id)

    return render(request, 'tipas-form.html', {'form': form})

def editType(request, keeper_id, type_id):
    keeper_ = Keeper.objects.get(id=keeper_id)
    expense_type = ExpenseTypes.objects.get(keeper=keeper_, id=type_id)
    form = ExpenseTypeForm(request.POST or None, instance=expense_type)

    if form.is_valid():
        form.save()
        return redirect('viewKeeper', keeper_id)

    return render(request, 'tipas-form.html', {'form': form, 'expense_type': expense_type})

def deleteType(request, keeper_id, type_id):
    keeper_ = Keeper.objects.get(id=keeper_id)
    expense_type = ExpenseTypes.objects.get(keeper=keeper_, id=type_id)

    if request.method == 'POST':
        expense_type.delete()
        return redirect('viewKeeper', keeper_id)

    return render(request, 'tipo-istrynimo-patvirtinimas.html', {'expense_type': expense_type})







