from django.utils.translation import gettext_lazy as _
from django import forms

from .models import CircuitImage


class CircuitImageForm(forms.ModelForm):
    class Meta:
        model = CircuitImage
        fields = ["title", "image"]
        labels = {
            "title": _("Titulli"),
            "image": _("Imazhi i qarkut"),
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": _("P.sh. Qark me porta AND/OR")}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
        }
