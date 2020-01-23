from django import forms



class Login_form(forms.Form):
    email =forms.EmailField()
    password = forms.PasswordInput()

class register_form(forms.Form):
    username = forms.CharField(unique=True)
    email = forms.EmailField()
    password = forms.CharField(max_length=100)
    repeat_password = forms.CharField(max_length=100)