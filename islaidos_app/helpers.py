from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from . models import Expenses, ExpenseTypes, Keeper

# data for js charts

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