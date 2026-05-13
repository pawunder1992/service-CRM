from django import forms


class OrderSearchForm(forms.Form):
    license_plate = forms.CharField(
        required=False,
        max_length=255,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "search by license_plate"}
        ),
    )