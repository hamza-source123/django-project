from django import forms
from django.contrib.auth.models import User
from application1.models import User_profile_info

class Userform(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username','email','password')


class Userprofileinfo(forms.ModelForm):
    class Meta:
        model=User_profile_info
        fields=('portfolio_site','profile_pic')