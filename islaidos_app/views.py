from django.shortcuts import render, redirect

from . models import Expenses, ExpenseTypes
from . forms import ExpenseForm, ExpenseTypeForm, KeeperForm
from django.db.models import Sum

from django.contrib.auth.decorators import login_required

from . helpers import expenditure_by_date_for_google_chart, expenditure_by_keepers_expense_types_for_google_chart, \
    check_if_user_is_owner, get_keeper

#Keeper views
def viewKeeper(request, keeper_id):
    keeper_ = get_keeper(keeper_id)

    if not keeper_.is_public == True:
        check_if_user_is_owner(request, keeper_)

    chart_data = expenditure_by_keepers_expense_types_for_google_chart(keeper_id)
    chart_data_2 = expenditure_by_date_for_google_chart(keeper_id)

    expense_types = ExpenseTypes.objects.filter(keeper=keeper_)
    for expense_type in expense_types:
        expenses = Expenses.objects.filter(tipas=expense_type)
        if expenses:
            expense_type.aktyvus =True
        else:
            expense_type.aktyvus = False
    expense_types.order_by('-aktyvus', 'tipas')
    expenses = Expenses.objects.filter(keeper=keeper_).order_by('data')
    expenses_total = list(expenses.aggregate(Sum('suma')).values())[0]
    return render(request, 'keeper.html', {'keeper':keeper_, 'expense_types':expense_types, 'expenses':expenses, \
                                           'chart_data':chart_data, 'expenses_total':expenses_total, 'chart_data_2':chart_data_2})

@login_required
def editKeeper(request, keeper_id):
    keeper = get_keeper(keeper_id)

    check_if_user_is_owner(request, keeper)

    form = KeeperForm(request.POST or None, instance=keeper)
    if form.is_valid():
        form.save()
        return redirect('islaidos_app:viewKeeper', keeper_id)
    return render(request, 'keeper-form.html', {'form':form, 'keeper':keeper})

@login_required
def deleteKeeper(request, keeper_id):
    keeper = get_keeper(keeper_id)

    check_if_user_is_owner(request, keeper)

    if request.method == 'POST':
        keeper.delete()
        return redirect('/')
    return render(request, 'confirm-keeper-deletion.html', {'keeper': keeper})

#Expense views
@login_required
def createExpense(request, keeper_id):
    keeper = get_keeper(keeper_id)
    form = ExpenseForm(request.POST or None, initial={'keeper':keeper_id})

    check_if_user_is_owner(request, keeper)

    form.fields['tipas'].queryset = ExpenseTypes.objects.filter(keeper=keeper)
    if form.is_valid():
        form.save()
        return redirect('islaidos_app:viewKeeper', keeper_id)
    return render(request, 'expense-form.html', {'form': form, 'keeper':keeper})

@login_required
def editExpense(request, keeper_id, expense_id):
    keeper = get_keeper(keeper_id)

    check_if_user_is_owner(request, keeper)

    expense = Expenses.objects.get(id=expense_id)
    form = ExpenseForm(request.POST or None, instance=expense)
    if form.is_valid():
         form.save()
         return redirect('islaidos_app:viewKeeper', keeper_id)
    return render(request, 'expense-form.html', {'form':form, 'expense': expense, 'keeper':keeper})

def deleteExpense(request, keeper_id, expense_id):
    keeper = get_keeper(keeper_id)

    check_if_user_is_owner(request, keeper)

    expense = Expenses.objects.get(id=expense_id)
    if request.method == 'POST':
        expense.delete()
        return redirect('islaidos_app:viewKeeper', keeper_id)
    return render(request, 'confirm-expense-deletion.html', {'expense': expense, "keeper": keeper})

#Expense type views
@login_required
def createType(request, keeper_id):
    keeper = get_keeper(keeper_id)

    check_if_user_is_owner(request, keeper)

    form = ExpenseTypeForm(request.POST or None, initial={'keeper':keeper_id})
    if form.is_valid():
        form.save()
        return redirect('islaidos_app:viewKeeper', keeper_id)
    return render(request, 'expense-type-form.html', {'form': form, 'keeper': keeper})

@login_required
def editType(request, keeper_id, type_id):
    keeper = get_keeper(keeper_id)

    check_if_user_is_owner(request, keeper)

    expense_type = ExpenseTypes.objects.get(keeper=keeper, id=type_id)
    form = ExpenseTypeForm(request.POST or None, instance=expense_type)
    if form.is_valid():
        form.save()
        return redirect('islaidos_app:viewKeeper', keeper_id)
    return render(request, 'expense-type-form.html', {'form': form, 'expense_type': expense_type, 'keeper': keeper})

@login_required
def deleteType(request, keeper_id, type_id):
    keeper = get_keeper(keeper_id)

    check_if_user_is_owner(request, keeper)

    expense_type = ExpenseTypes.objects.get(keeper=keeper, id=type_id)

    if request.method == 'POST':
        expense_type.delete()
        return redirect('islaidos_app:viewKeeper', keeper_id)

    return render(request, 'confirm-expense-type-deletion.html', {'expense_type': expense_type, "keeper": keeper})