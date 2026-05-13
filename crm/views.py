import datetime

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import (
    OrderSearchForm,
    OrderForm,
    ClientSearchForm,
    ClientCreationForm,
    WorkerSearchForm,
    WorkerCreationForm,
    ServiceCategorySearchForm,
    SpecialtySearchForm,
)
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


class ClientListView(LoginRequiredMixin, generic.ListView):
    model = Client
    context_object_name = "client_list"
    template_name = "crm/client_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        license_plate = self.request.GET.get("license_plate", "")

        context["search_form"] = ClientSearchForm(
            initial={"license_plate": license_plate}
        )
        return context

    def get_queryset(self):
        queryset = Client.objects.all().order_by("-id")
        form = ClientSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                license_plate__icontains=form.cleaned_data["license_plate"]
            )
        return queryset


class ClientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Client
    template_name = "crm/client_detail.html"


class ClientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Client
    template_name = "crm/client_delete_confirm.html"
    success_url = reverse_lazy("crm:client-list")


class ClientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Client
    form_class = ClientCreationForm
    template_name = "crm/client_form.html"
    success_url = reverse_lazy("crm:client-list")


class ClientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Client
    form_class = ClientCreationForm

    template_name = "crm/client_form.html"

    def get_success_url(self):

        next_page = self.request.GET.get("next")

        if next_page == "order":

            self.request.session["last_created_client_id"] = self.object.id
            return reverse_lazy("crm:order-create")

        return reverse_lazy("crm:client-list")

    def form_valid(self, form):
        response = super().form_valid(form)

        self.request.session["last_client_id"] = self.object.id
        return response


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = "worker_list"
    paginate_by = 5

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        last_name = self.request.GET.get("last_name", "")

        context["search_form"] = WorkerSearchForm(initial={"last_name": last_name})
        return context

    def get_queryset(self):
        queryset = Worker.objects.all().order_by("-is_active")
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                last_name__icontains=form.cleaned_data["last_name"]
            )
        status = self.request.GET.get("status")
        if status == "active":
            queryset = queryset.filter(is_active=True).order_by("-id")
        elif status == "inactive":
            queryset = queryset.filter(is_active=False).order_by("-id")
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = "crm/worker_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.object
        current_date = datetime.date.today()
        completed_orders = worker.orders.filter(is_completed=True).annotate(
            num_workers=Count("performers")
        )
        earn_all_time = 0
        earn_month = 0
        count_month = 0
        monthly_data = {}
        for order in completed_orders:
            share = order.total_price / order.num_workers
            earn_all_time += share
            month_key = order.date.strftime("%Y-%m")
            if month_key not in monthly_data:
                monthly_data[month_key] = {"earn": 0, "count": 0}
            monthly_data[month_key]["earn"] += share
            monthly_data[month_key]["count"] += 1
            if (
                order.date.month == current_date.month
                and order.date.year == current_date.year
            ):
                earn_month += share
                count_month += 1
        stats_by_month = [
            {
                "date": datetime.datetime.strptime(m, "%Y-%m"),
                "earn": round(v["earn"], 2),
                "count": v["count"],
            }
            for m, v in sorted(monthly_data.items(), reverse=True)
        ]
        context["earn_all_time"] = round(earn_all_time, 2)
        context["earn_month"] = round(earn_month, 2)
        context["count_all_time"] = completed_orders.count()
        context["count_month"] = count_month
        context["monthly_stats"] = stats_by_month
        total_months = (current_date.year - worker.date_joined.year) * 12 + (
            current_date.month - worker.date_joined.month
        )
        context["year"] = total_months // 12
        context["month"] = total_months % 12
        context["orders"] = worker.orders.all().order_by("-date")

        return context


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    fields = ["username", "first_name", "last_name", "specialty", "is_active"]
    template_name = "crm/worker_form.html"
    success_url = reverse_lazy("crm:worker-list")


class ServiceCategoryListView(LoginRequiredMixin, generic.ListView):
    model = ServiceCategory
    fields = "__all__"
    template_name = "crm/service_category_list.html"
    context_object_name = "category_list"
    paginate_by = 5

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["search_form"] = ServiceCategorySearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = ServiceCategory.objects.all()
        form = ServiceCategorySearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class ServiceCategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ServiceCategory
    template_name = "crm/service_category_delete_confirm.html"
    success_url = reverse_lazy("crm:service-category-list")


class ServiceCategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = ServiceCategory
    template_name = "crm/service_category_form.html"
    fields = "__all__"
    success_url = reverse_lazy("crm:service-category-list")


class ServiceCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ServiceCategory
    template_name = "crm/service_category_form.html"
    fields = "__all__"
    success_url = reverse_lazy("crm:service-category-list")


class SpecialtyListView(LoginRequiredMixin, generic.ListView):
    model = Specialty
    fields = "__all__"
    template_name = "crm/specialty_list.html"
    context_object_name = "specialty_list"
    paginate_by = 5

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["search_form"] = SpecialtySearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Specialty.objects.all()
        form = SpecialtySearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class SpecialtyDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Specialty
    template_name = "crm/specialty_delete_confirm.html"
    success_url = reverse_lazy("crm:specialty-list")


class SpecialtyCreateView(LoginRequiredMixin, generic.CreateView):
    model = Specialty
    template_name = "crm/specialty_form.html"
    fields = "__all__"
    success_url = reverse_lazy("crm:specialty-list")


class SpecialtyUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Specialty
    template_name = "crm/specialty_form.html"
    fields = "__all__"
    success_url = reverse_lazy("crm:specialty-list")


class SpecialtyDetailView(LoginRequiredMixin, generic.DetailView):
    model = Specialty
    template_name = "crm/specialty_detail.html"
