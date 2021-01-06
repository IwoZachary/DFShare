from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .forms import FileForm
from django.contrib.auth import login, authenticate, logout
from myapp.forms import RegistrationForm
from myapp.forms import AccountAuthenticationForm, File

def home(request):
    return render(request, 'myapp/home.html')

def registration_view(request):
        context={}
        if request.POST:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                account = authenticate(email=email, password=raw_password)
                login(request, account)
                return redirect('home')
            else:
                context['registration_form'] = form
        else:
            form = RegistrationForm()
            context['registration_form'] = form
        return render(request, 'myapp/register.html', context)

def user_home_view(request):
    context = {}
    if request.user.is_authenticated:
        if request.POST:
            form = FileForm(request.POST, request.FILES)
            if form.is_valid():
                fs = FileSystemStorage()
                name = fs.save(request.FILES['file'])
                context['url'] = fs.url(name)
                return redirect(request,'myapp/user_home.html',)
        else:
            form = FileForm()
            context['file_form'] = form
            return render( request, 'myapp/user_home.html', context)
    else:
        return redirect('home')

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    context = {}
    user=request.user
    if user.is_authenticated:
        return redirect('user')
    if request.POST:
        form=AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email=request.POST['email']
            password=request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('user')
    else:
        form = AccountAuthenticationForm()
        context['login_form'] = form
    return render(request, "myapp/login.html", context)







