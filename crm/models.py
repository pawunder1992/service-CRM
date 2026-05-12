from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hour_cost = models.IntegerField()

    def __str__(self):
        return self.name


class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("crm:specialty-detail", kwargs={"pk": self.pk})


class Worker(AbstractUser):
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.SET_NULL,
        related_name="workers",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("crm:worker-detail", kwargs={"pk": self.pk})

    def active_orders_count(self):
        return self.orders.filter(is_completed=False).count()


class Order(models.Model):
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.CASCADE, related_name="orders"
    )
    client = models.ForeignKey(
        "Client", on_delete=models.CASCADE, related_name="orders"
    )
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    performers = models.ManyToManyField(Worker, related_name="orders")
    norm_hours = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return round(self.norm_hours * self.category.hour_cost, 2)

    def get_absolute_url(self):
        return reverse("crm:order-detail", kwargs={"pk": self.pk})


class Client(models.Model):
    model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse("crm:client-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.license_plate} {self.owner_name}"
