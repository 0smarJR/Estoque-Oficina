from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .models import Produto
from .forms import ProdutoForm

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

@login_required(login_url='/login')
def produto_register(request):
    product_id = request.GET.get('id')
    if product_id:
        produto = Produto.objects.get(id=product_id)
        return render(request, 'app/produto_form.html', {'produto':produto})
    return render(request, 'app/produto_form.html')

@login_required(login_url='/login')
def produto_delete(request, id):
    produto = Produto.objects.get(id=id)
    produto.delete()
    return redirect('/products')

@login_required(login_url='/login')
def set_produto(request):
    nome = request.POST.get('nome')
    codigo = request.POST.get('codigo')
    marca = request.POST.get('marca')
    quantidade = request.POST.get('quantidade')
    preco = request.POST.get('preco')
    p_id= request.POST.get('produto_id')
    if(request.POST.get('status')=='true'):
        ativo=True
    else:
        ativo=False
    if p_id:
        produto = Produto.objects.get(id=p_id)
        produto.nome = nome
        produto.codigo = codigo
        produto.marca = marca
        produto.quantidade = quantidade
        produto.preco = preco
        produto.ativo = ativo
        produto.save()
    else:
        produto = Produto.objects.create(nome=nome, codigo=codigo, marca=marca, quantidade=quantidade, preco=preco, ativo=ativo)
    url = '/products/{}' .format(produto.id)
    return redirect(url)

