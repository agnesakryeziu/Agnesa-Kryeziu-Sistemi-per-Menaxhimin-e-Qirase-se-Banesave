from django import forms


class AbonimiForm(forms.Form):

    email = forms.EmailField(
        max_length=254,
        required=True
    )

    def clean_email(self):

        return self.cleaned_data["email"].strip().lower()