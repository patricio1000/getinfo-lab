import re

from django import forms

from .models import Info


class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ["name", "email", "cell_phone", "comments"]

    def clean_cell_phone(self):
        phone = self.cleaned_data["cell_phone"]
        digits = re.sub(r"\D", "", phone)  # keep only the digits
        if len(digits) != 10:
            raise forms.ValidationError("Enter a 10-digit phone number, like 402-555-1234.")
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
