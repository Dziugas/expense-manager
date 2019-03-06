from django.shortcuts import render, redirect
from django.http import Http404
from .models import Expenses, ExpenseTypes, Keeper
from .forms import ExpenseForm, ExpenseTypeForm, KeeperForm
from django.db.models import Sum

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

#data for charts

def expenditure_by_date_for_google_chart(keeper_id):
    all_expenses_for_current_keeper = Expenses.objects.filter(keeper=keeper_id).order_by('data')
    distinct_expense_dates_for_that_keeper = all_expenses_for_current_keeper.values('data').distinct()
    distinct_expense_dates_extracted = [date['data'] for date in distinct_expense_dates_for_that_keeper]
    list_for_chart = []
    for date in distinct_expense_dates_extracted:
        expenses_on_that_date = all_expenses_for_current_keeper.filter(data=date)
        sum_of_expenses_on_that_day = expenses_on_that_date.aggregate(Sum('suma'))
        sum_of_expenses_on_that_day_nicely_printed = sum_of_expenses_on_that_day['suma__sum']
        list_for_chart.append([date.strftime('%F'), float(sum_of_expenses_on_that_day_nicely_printed)])
    if list_for_chart:
        list_for_chart.insert(0, ['Date', 'EUR'])
    return list_for_chart

def expenditure_by_keepers_expense_types_for_google_chart(keeper_id):
    all_expense_types_for_current_keeper = ExpenseTypes.objects.filter(keeper=keeper_id).order_by('tipas')
    expense_type_names = [expense_type.tipas for expense_type in all_expense_types_for_current_keeper]
    list_for_chart = []
    for expense_type_name in expense_type_names:
        expenses_for_type = Expenses.objects.filter(tipas__tipas=expense_type_name, keeper=keeper_id)
        sum_of_expenses_for_type = expenses_for_type.aggregate(Sum('suma'))
        sum_of_expenses_for_type_nicely_printed = sum_of_expenses_for_type['suma__sum'] or 0.00
        list_for_chart.append([expense_type_name, float(sum_of_expenses_for_type_nicely_printed)])
    if list_for_chart:
        list_for_chart.insert(0, ['Expense type', 'Total Sum'])
    return list_for_chart


#Check if keeper instance is public and if the user is the creator of keeper instance
def get_keeper(keeper_id):
    try:
        keeper_ = Keeper.objects.get(id=keeper_id)
        return (keeper_)
    except Keeper.DoesNotExist:
        raise Http404("Keeper does not exist")

def check_if_user_is_owner(request, keeper):
    keeper_users = keeper.users.all()
    user = request.user
    if user not in keeper_users:
        raise PermissionDenied

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