from django import forms

from .models import Rezervimi


class RezervimiForm(forms.ModelForm):

    mesazhi = forms.CharField(
        required=False,
        max_length=1000,
        label="Mesazhi për pronarin",
        widget=forms.Textarea(attrs={
            "placeholder": "Shkruani një mesazh për pronarin...",
            "rows": 5,
        })
    )

    class Meta:
        model = Rezervimi
        fields = ["mesazhi"]