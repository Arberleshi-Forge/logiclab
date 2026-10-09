from django.utils.translation import gettext_lazy as _
from django import forms


class BooleanExpressionForm(forms.Form):
    expression = forms.CharField(
        label=_("Shprehja Booleane"),
        max_length=300,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "(A & B) | (~A & C)",
                "autocomplete": "off",
            }
        ),
        help_text=_("Përdor &, |, ~, ^ ose AND, OR, NOT, XOR. Maksimumi 6 variabla."),
    )
