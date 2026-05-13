from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from crm.models import Worker, Order


class OrderSearchForm(forms.Form):
    license_plate = forms.CharField(
        required=False,
        max_length=255,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "search by license_plate"}
        ),
    )


class OrderForm(forms.ModelForm):

    performers = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        label="Performers",
        required=False,
    )

    class Meta:
        model = Order
        fields = "__all__"

class ClientSearchForm(forms.Form):
    license_plate = forms.CharField(
        required=False,
        max_length=255,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "search by license_plate"}
        ),
    )


class ClientCreationForm(forms.ModelForm):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "0X XXX XX XX"})
    )

    class Meta:
        model = Client
        fields = "__all__"

    def clean_license_plate(self):
        return validate_license_plate(self.cleaned_data["license_plate"])

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        validate_phone_number(data)
        return data


def validate_license_plate(license_plate):
    if len(license_plate) != 8:
        raise ValidationError("License plate should consist of 8 characters")
    elif not license_plate[:2].isupper() or not license_plate[:2].isalpha():
        raise ValidationError(
            "First 2 characters should be uppercase letters"
        )
    elif not license_plate[-2:].isupper() or not license_plate[-2:].isalpha():
        raise ValidationError("Last 2 characters should be uppercase letters")
    elif not license_plate[2:6].isdigit():
        raise ValidationError("Middle 4 characters should be digits")
    return license_plate


def validate_phone_number(phone_number):
    phone_number = phone_number.strip()
    if len(phone_number) != 10 or not phone_number.isdigit():
        raise ValidationError(
            "Enter the number in the format 096 123 45 67 (10 digits)"
        )
    return phone_number



class WorkerSearchForm(forms.Form):
    last_name = forms.CharField(
        required=False,
        max_length=255,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "search by last_name"}),
    )


class WorkerCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "specialty",
            "first_name",
            "last_name",
            "is_active",
        )


class ServiceCategorySearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        max_length=255,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "search by category"}),
    )



class SpecialtySearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        max_length=255,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "search by specialty"}),
    )