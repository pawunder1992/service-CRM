from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Worker, ServiceCategory, Client, Specialty, Order


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("specialty",)

    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("specialty",)}),)

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "specialty",
                )
            },
        ),
    )


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ("license_plate", "owner_name")
    list_display = ("license_plate", "model", "owner_name")


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "category", "is_completed", "date")
    list_filter = ("is_completed", "category", "date")
