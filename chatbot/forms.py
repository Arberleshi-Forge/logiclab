from django.utils.translation import gettext_lazy as _
from django import forms


class ChatbotForm(forms.Form):
    question = forms.CharField(
        label=_("Pyetja"),
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": _("Shkruaj pyetje për logjikë, algoritme, Big O, pseudokod ose kërko analizë për imazhin e qarkut..."),
            }
        ),
    )
    image = forms.ImageField(
        label=_("Imazh qarku"),
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control",
                "accept": "image/*",
            }
        ),
    )
