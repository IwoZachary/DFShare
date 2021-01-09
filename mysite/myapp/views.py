from myapp.models import Account, SharedFile
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .forms import FileForm, ShareForm
from django.contrib.auth import login, authenticate, logout
from myapp.forms import RegistrationForm
from myapp.forms import AccountAuthenticationForm, FileMod
from django.contrib import messages
from django.http import HttpResponse
import os
from django.http import FileResponse
from django.views.static import serve

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
            if form.is_valid() and request.FILES != None :
                obj = form.save(commit=False)
                obj.owner = request.user
                obj.save()
                messages.success(request, 'file added')
            else:
                form = FileForm()
                context['file_form'] = form
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

def my_files(request):
    context = {}
    user=request.user
    if user.is_authenticated:
        if request.POST:
            req=request.POST['action'].split("|")
            if req[0] =="DELETE":
                file= FileMod.objects.filter(id=int(req[1])).first()
                file_name= file.fileF.name
                FileMod.objects.filter(id=int(req[1])).delete()
                os.remove(file_name)
            if req[0] == "DOWNLOAD":
                file= FileMod.objects.filter(id=int(req[1])).first()
                file_name= file.fileF.name
                f = open(file_name, 'rb')
                response =FileResponse(f)    
                response['Content-Disposition']='attachment;filename='+file.__str__()
                return response
            if req[0] == "SHARE":
                form=ShareForm(request.POST)
                form.save()
                
        context['files']=FileMod.objects.all().filter(owner=user)
        context['share']=ShareForm

        return render(request, 'myapp/my_files.html', context)
    else:
        return redirect('home',request)










