
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import OrderSearchForm, OrderForm
from .models import Order, Client, Worker, ServiceCategory, Specialty

current_month = timezone.now().month


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

class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    context_object_name = "order_list"
    template_name = "crm/order_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        license_plate = self.request.GET.get("license_plate", "")
        context["search_form"] = OrderSearchForm(
            initial={"license_plate": license_plate}
        )
        return context

    def get_queryset(self):
        queryset = Order.objects.select_related("client", "category").order_by(
            "is_completed", "-date"
        )
        form = OrderSearchForm(self.request.GET)
        if form.is_valid() and form.cleaned_data.get("license_plate"):
            queryset = queryset.filter(
                client__license_plate__icontains=form.cleaned_data["license_plate"]
            )
        status = self.request.GET.get("status")
        if status == "completed":
            queryset = queryset.filter(is_completed=True).order_by("-id")
        elif status == "waiting":
            queryset = queryset.filter(is_completed=False).order_by("-id")
        elif status == "my_orders":
            queryset = queryset.filter(performers__id=self.request.user.id).distinct()
        return queryset


class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = OrderForm
    template_name = "crm/order_form.html"
    success_url = reverse_lazy("crm:order-list")

    def get_initial(self):
        initial = super().get_initial()

        client_id = self.request.session.pop("last_client_id", None)
        if client_id:
            initial["client"] = client_id
        return initial

class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = "crm/order_detail.html"


class OrderUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "crm/order_form.html"

    def get_success_url(self):

        return reverse_lazy("crm:order-detail", kwargs={"pk": self.object.pk})


class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Order
    template_name = "crm/order_confirm_delete.html"
    success_url = reverse_lazy("crm:order-list")