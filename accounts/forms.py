from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Redactor


class RedactorCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )
    years_of_experience = forms.IntegerField(
        min_value=0,
        max_value=50,
        required=True,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Years of Experience"}
        ),
    )

    class Meta:
        model = Redactor
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Username"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirm Password"}
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.years_of_experience = self.cleaned_data["years_of_experience"]
        if commit:
            user.save()
        return user


class RedactorUpdateForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = ["first_name", "last_name", "email", "years_of_experience"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "years_of_experience": forms.NumberInput(
                attrs={"class": "form-control", "min": "0", "max": "50"}
            ),
        }
