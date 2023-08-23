from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Repeat password")
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        
    def clean_password2(self):
        cd = self.cleaned_data
        if not (cd['password'] == cd['password2']):
            raise ValidationError("The two passwords do not match.")
        return cd['password2']
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        # Check that the user does NOT already exist in our database, and is a valid e-mail address
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("this mail already exist")
        return email

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
    def clean_email(self):
        email = self.cleaned_data["email"]
        
        if email != "":
            qs = User.objects.filter(email=email).exclude(id=self.instance.id)
        
            if qs.exists():
                raise forms.ValidationError('This E-Mail Address Is Already Taken')
        return email
        
        
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']