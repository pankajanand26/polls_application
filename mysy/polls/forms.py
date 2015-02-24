from django import forms 

class UserRegForm(forms.Form):
    first_name = forms.CharField(max_length=100,required=True)
    last_name = forms.CharField(max_length=100,required=True) 
    email = forms.EmailField(max_length=100,required=True) 
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
