from enum import unique
from django.contrib.auth.models import AnonymousUser
from myapp.models import Account, Action, SharedFile, Logs
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .forms import FileForm, OpinionForm, ShareForm
from django.contrib.auth import login, authenticate, logout
from myapp.forms import RegistrationForm
from myapp.forms import AccountAuthenticationForm, FileMod, Opinion, LogsForm
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
                Logs.objects.create(userS = request.user, action = Action.LOGIN)
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
                obj.f_rate = 0
                obj.save()
                Logs.objects.create(userS = request.user, action = Action.UPLOAD)
                messages.success(request, 'File was added')
            else:
                form = FileForm()
                context['file_form'] = form
        
        form = FileForm()
        context['file_form'] = form
        return render( request, 'myapp/user_home.html', context)
    else:
        return redirect('home')

def logout_view(request):
    Logs.objects.create(userS = request.user, action = Action.LOGOUT)
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
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            userl = authenticate(email=email, password=password)

            if userl is not None:
                login(request, userl)
                Logs.objects.create(userS = request.user, action = Action.LOGIN)
                return redirect('user')

            else:
               messages.success(request, 'Email and password dont match')

    form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, "myapp/login.html", context)

def my_files(request):
    context = {}
    user=request.user
    if user.is_authenticated:
        if request.POST:
            req=request.POST['action'].split("|")
            file= FileMod.objects.filter(id=int(req[1])).first()
            file_name= file.fileF.name
            if req[0] =="DELETE":
                FileMod.objects.filter(id=int(req[1])).delete()
                os.remove(file_name)
                Logs.objects.create(userS = request.user, action = Action.DELETE)
            if req[0] == "DOWNLOAD":
                f = open(file_name, 'rb')
                response =FileResponse(f)    
                response['Content-Disposition']='attachment;filename='+file.__str__()
                Logs.objects.create(userS = request.user, action = Action.DOWNLOAD)
                return response
            if req[0] == "SHARE":

                form=ShareForm(request.POST)
                if form.is_valid():
                    share=form.save(commit=False)
                    is_uniq = SharedFile.objects.all().filter(userS=share.userS, fileS=file)
                    if len(is_uniq) ==0:
                        share.fileS=file
                        share.save()
                        Logs.objects.create(userS = request.user, action = Action.SHARE)
                
        context['files']=FileMod.objects.all().filter(owner=user)
        context['share']=ShareForm

        return render(request, 'myapp/my_files.html', context)
    else:
        return redirect('home',request)

    
def public_files(request):
    context = {}
    user=request.user
    if user.is_authenticated:
        if request.POST:
            req=request.POST['action'].split("|")
            file= FileMod.objects.filter(id=int(req[1])).first()
            if req[0] == "DOWNLOAD":                
                file_name= file.fileF.name
                f = open(file_name, 'rb')
                response =FileResponse(f)    
                response['Content-Disposition']='attachment;filename='+file.__str__()
                Logs.objects.create(userS = request.user, action = Action.DOWNLOAD)
                return response
            if req[0] == "RATE":
                form = OpinionForm(request.POST)
                if form.is_valid():
                    is_uniq = Opinion.objects.all().filter(userS=user, fileS=file)  
                    if len(is_uniq) == 0:              
                        obj = form.save(commit=False)
                        obj.fileS = file
                        obj.userS = user
                        obj.save()
                    else:
                        for el in is_uniq:
                            el.rate = form.cleaned_data.get('rate')
                            el.save()
                    rates_num = Opinion.objects.all().filter(fileS=file)
                    sum=0
                    for el in rates_num:
                        sum=sum+el.rate
                    avg = int(sum/len(rates_num))
                    file.f_rate = avg
                    file.save()
                    Logs.objects.create(userS = request.user, action = Action.RATE)
        context['files']=FileMod.objects.all().filter(is_public=True)
        context["opinion"]=OpinionForm
        return render(request, 'myapp/public_files.html', context)
    else:
        return redirect('home', request)


def shared_files(request):
    context = {}
    user=request.user
    if user.is_authenticated:
        if request.POST:
            req=request.POST['action'].split("|")
            file= FileMod.objects.filter(id=int(req[1])).first()
            if req[0] == "DOWNLOAD":                
                file_name= file.fileF.name
                f = open(file_name, 'rb')
                response =FileResponse(f)    
                response['Content-Disposition']='attachment;filename='+file.__str__()
                Logs.objects.create(userS = request.user, action = Action.DOWNLOAD)
                return response
        shared = SharedFile.objects.all().filter(userS = user)
        context['files']=FileMod.objects.all().filter(id__in =shared)
        return render(request, 'myapp/shared_files.html', context)
    else:
        return redirect('home', request)

def public(request):
    context = {}
    if request.POST:
            req=request.POST['action'].split("|")
            file= FileMod.objects.filter(id=int(req[1])).first()
            if req[0] == "DOWNLOAD":                
                file_name= file.fileF.name
                f = open(file_name, 'rb')
                response =FileResponse(f)    
                response['Content-Disposition']='attachment;filename='+file.__str__()
                return response
    context['files']=FileMod.objects.all().filter(is_public=True)
    return render(request, 'myapp/public.html', context)   














