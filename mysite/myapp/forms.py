from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import  UserCreationForm
from django_enumfield.forms.fields import EnumChoiceField


from myapp.models import Account, FileMod, Logs, Rate, SharedFile, Opinion

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required valid email')

    class Meta:
        model=Account
        fields = ('email', 'username', 'password1', 'password2')

class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model=Account
        fields= ('email', 'password')
    
    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid login")


class FileForm(forms.ModelForm):
    class Meta:
        model = FileMod
        fields = ["is_public", "fileF","owner"]

class ShareForm(forms.ModelForm):
    class Meta:
        model = SharedFile
        fields = ['fileS', 'userS']


class OpinionForm(forms.ModelForm):
    rate = EnumChoiceField(Rate)
    class Meta:
        model = Opinion
        fields = ["fileS", "userS", "rate"]

class LogsForm(forms.ModelForm):
    class Meta:
        model= Logs
        fields = ['userS', 'action']
