from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Produto

# Create your views here.

def login_user(request):
    return render(request, 'app/login.html')

@csrf_protect
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Usuario e/ou senha errados')
    return redirect('/')

@login_required(login_url='/login')
def home(request):
    return render (request, 'app/index.html')

def logout_user(request):
    logout(request)
    return redirect('/login')

@login_required(login_url='/login')
def produto_list(request):
    objects = Produto.objects.all()
    context = {'object_list': objects}
    return render (request, 'app/produto_list.html', context)

@login_required(login_url='/login')
def produto(request, id):
    obj = Produto.objects.get(id=id)
    context = {'object': obj}
    return render (request, 'app/produto.html', context)