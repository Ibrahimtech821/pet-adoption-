from django import forms
from django.forms import ModelForm 
from .models import adoptionform
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User

class AdoptionForm(ModelForm):
    class Meta:
        model=adoptionform
        fields=['age','why_you_wanna_adopt','do_you_have_any_experince_before_with_animals']

class customcreationform(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta:
        model=User
        fields=('username','email','password1','password2')
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

