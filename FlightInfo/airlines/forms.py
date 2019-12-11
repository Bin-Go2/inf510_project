from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "", 'autofocus': ''}))
    password = forms.CharField(label="Password", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ""}))


class RegisterForm(forms.Form):

    username = forms.CharField(label="Username", max_length=128,
                               widget=forms.TextInput(attrs={'class': 'form-control','placeholder': ""}))
    password1 = forms.CharField(label="Password", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': ""}))
    password2 = forms.CharField(label="Confirm Password", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': ""}))