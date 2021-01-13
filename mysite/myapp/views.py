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
                obj.save()
                Logs.objects.create(userS = request.user, action = Action.UPLOAD)
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
            email=request.POST['email']
            password=request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                Logs.objects.create(userS = request.user, action = Action.LOGIN)
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
                Logs.objects.create(userS = request.user, action = Action.DELETE)
            if req[0] == "DOWNLOAD":
                file= FileMod.objects.filter(id=int(req[1])).first()
                file_name= file.fileF.name
                f = open(file_name, 'rb')
                response =FileResponse(f)    
                response['Content-Disposition']='attachment;filename='+file.__str__()
                Logs.objects.create(userS = request.user, action = Action.DOWNLOAD)
                return response
            if req[0] == "SHARE":
                form=ShareForm(request.POST)
                form.save()
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
                    obj = form.save(commit=False)
                    opinion_exist = Opinion.objects.all().filter(fileS=file,userS=user)
                    if opinion_exist == None:
                        obj.fileS = file
                        obj.userS = user
                        obj.save()
                        Logs.objects.create(userS = request.user, action = Action.RATE)
                
        else:
            pass
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
            
                
        else:
            pass
        shared = SharedFile.objects.all().filter(userS = user)
        context['files']=FileMod.objects.all().filter(id__in =shared)
        return render(request, 'myapp/shared_files.html', context)
    else:
        return redirect('home', request)












