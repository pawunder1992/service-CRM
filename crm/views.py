

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render



from .models import Order, Client, Worker, ServiceCategory, Specialty




@login_required
def index(request):
    """View function for the home page of the site."""
    sum_all = sum(
        order.total_price for order in Order.objects.filter(is_completed=True)
    )
    sum_month = sum(
        order.total_price
        for order in Order.objects.filter(
            Q(is_completed=True) & Q(date__month=current_month)
        )
    )
    num_orders = Order.objects.filter(is_completed=False).count()
    num_worker = Worker.objects.filter(is_active=True).count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "sum_all": sum_all,
        "num_orders": num_orders,
        "num_worker": num_worker,
        "num_visits": num_visits + 1,
        "sum_month": sum_month,
    }

    return render(request, "crm/index.html", context=context)
