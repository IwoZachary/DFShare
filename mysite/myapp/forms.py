from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import  UserCreationForm
from django.forms import widgets
from django_enumfield.forms.fields import EnumChoiceField


from myapp.models import Account, FileMod, Logs, Rate, SharedFile, Opinion

class RegistrationForm(UserCreationForm):
    #email = forms.EmailField(max_length=60, help_text='Required valid email')

    class Meta:
        model=Account
        fields = ('email', 'username', 'password1', 'password2')
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control'}),
            
        }

class AccountAuthenticationForm(forms.ModelForm):

    #password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model=Account
        fields= ('email', 'password')
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'})
        }
    
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid login")


class FileForm(forms.ModelForm):
    class Meta:
        model = FileMod
        fields = ["is_public", "fileF"]

class ShareForm(forms.ModelForm):
    class Meta:
        model = SharedFile
        fields = ['userS']

    



class OpinionForm(forms.ModelForm):
    rate = EnumChoiceField(Rate)
    class Meta:
        model = Opinion
        fields = ["rate"]

class LogsForm(forms.ModelForm):
    class Meta:
        model= Logs
        fields = ['userS', 'action']
