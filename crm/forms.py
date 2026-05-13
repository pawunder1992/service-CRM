from django import forms

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