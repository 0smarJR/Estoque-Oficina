from django.http import JsonResponse
from django.shortcuts import render, redirect, resolve_url
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .models import Produto, Estoque, EstoqueItens, EstoqueEntrada, EstoqueSaida
from .forms import ProdutoForm, EstoqueForm, EstoqueItensForm
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from django.views.generic import ListView, DetailView


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
    objects = Produto.objects.all()
    search = request.GET.get('search')
    if search:
        objects = objects.filter(nome__icontains=search)
    context = {'object_list': objects}
    return render (request, 'app/produto_list.html', context)

def logout_user(request):
    logout(request)
    return redirect('/login')

@login_required(login_url='/login')
def produto_list(request):
    objects = Produto.objects.all()
    search = request.GET.get('search')
    if search:
        objects = objects.filter(nome__icontains=search)
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

# @login_required(login_url='/login')
# def estoque_entrada_list(request):
#     template_name = 'app/estoque_entrada_list.html'
#     objects = EstoqueEntrada.objects.all()
#     context={'object_list': objects}
#     return render(request, template_name, context)

class EstoqueEntradaList(ListView):
    model = EstoqueEntrada
    template_name = 'app/estoque_entrada_list.html'

    def get_context_data(self, **kwargs):
        context = super(EstoqueEntradaList, self).get_context_data(**kwargs)
        context['titulo'] = 'Entrada'
        context['url_add'] = 'estoque_entrada_add'
        return context

@login_required(login_url='/login')
def estoque_entrada_detail(request, id):
    template_name = 'app/estoque_entrada_detail.html'
    obj = EstoqueEntrada.objects.get(id=id)
    context={'object': obj}
    return render(request, template_name, context)

class EstoqueEntradaDetail(DetailView):
    model = EstoqueEntrada
    template_name = 'app/estoque_entrada_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EstoqueEntradaDetail, self).get_context_data(**kwargs)
        context['url_list'] = 'estoque_entrada'
        return context

@login_required(login_url='/login')
def estoque_entrada_add(request):
    template_name = 'app/estoque_entrada_form.html'
    estoque_form = Estoque()
    item_estoque_formset = inlineformset_factory(
        Estoque,
        EstoqueItens,
        form=EstoqueItensForm,
        extra=0,
        can_delete=False,
        min_num=1,
        validate_min=True,
    )
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque_form, prefix='main')
        formset = item_estoque_formset(
            request.POST,
            instance=estoque_form,
            prefix='estoque'
        )
        if form.is_valid() and formset.is_valid():
            form = form.save()
            form.movimento='e'
            form.save()
            formset.save()
            dar_baixa_estoque(form)
            url = 'estoque_entrada_detail'
            return HttpResponseRedirect(resolve_url(url, form.pk))
    else:
        form = EstoqueForm(instance=estoque_form, prefix='main')
        formset = item_estoque_formset(instance=estoque_form, prefix='estoque')

    context = {'form': form, 'formset': formset}
    return render(request, template_name, context)

@login_required(login_url='/login')
def produto_json(request, pk):
    ''' Retorna o produto, id e estoque. '''
    produto = Produto.objects.filter(pk=pk)
    data = [item.to_dict_json() for item in produto]
    return JsonResponse({'data': data})

def dar_baixa_estoque(form):
    produtos=form.estoques.all()
    for item in produtos:
        produto = Produto.objects.get(pk=item.produto.pk)
        produto.quantidade = item.saldo
        produto.save()

# @login_required(login_url='/login')
# def estoque_saida_list(request):
#     template_name = 'app/estoque_saida_list.html'
#     objects = EstoqueSaida.objects.all()
#     context={'object_list': objects}
#     return render(request, template_name, context)

class EstoqueSaidaList(ListView):
    model = EstoqueSaida
    template_name = 'app/estoque_saida_list.html'

    def get_context_data(self, **kwargs):
        context = super(EstoqueSaidaList, self).get_context_data(**kwargs)
        context['titulo'] = 'Saida'
        context['url_add'] = 'estoque_saida_add'
        return context

@login_required(login_url='/login')
def estoque_saida_detail(request, id):
    template_name = 'app/estoque_saida_detail.html'
    obj = EstoqueSaida.objects.get(id=id)
    context={'object': obj}
    return render(request, template_name, context)

@login_required(login_url='/login')
def estoque_saida_add(request):
    template_name = 'app/estoque_saida_form.html'
    estoque_form = Estoque()
    item_estoque_formset = inlineformset_factory(
        EstoqueSaida,
        EstoqueItens,
        form=EstoqueItensForm,
        extra=0,
        can_delete=False,
        min_num=1,
        validate_min=True,
    )
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque_form, prefix='main')
        formset = item_estoque_formset(
            request.POST,
            instance=estoque_form,
            prefix='estoque'
        )
        if form.is_valid() and formset.is_valid():
            form = form.save()
            form.movimento='s'
            form.save()
            formset.save()
            dar_baixa_estoque(form)
            url = 'estoque_saida_detail'
            return HttpResponseRedirect(resolve_url(url, form.pk))
    else:
        form = EstoqueForm(instance=estoque_form, prefix='main')
        formset = item_estoque_formset(instance=estoque_form, prefix='estoque')

    context = {'form': form, 'formset': formset}
<<<<<<< HEAD
    return render(request, template_name, context)
=======
    return render(request, template_name, context)

class ProdutoList(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'app/produto_list.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            object_list = self.model.objects.filter(nome__icontains=query)
        else:
            object_list = self.model.objects.all()
        return object_list

class UsuarioCadastro(CreateView):
    template_name = 'app/cadastro_usuario.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('users')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Cadastrar Usuário"
        context['botao'] = "Cadastrar"
        return context

class UsuarioUpdate(UpdateView):
    template_name = 'app/cadastro_usuario.html'
    model = User
    fields = ['first_name', 'last_name', 'username', 'email', 'is_superuser']
    success_url = reverse_lazy('users')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Editar Usuário"
        context['botao'] = "Editar"
        return context

@login_required(login_url='/login')
def usuario_delete(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    return redirect('/usuarios')

class UsuariosList(LoginRequiredMixin, ListView):
    model = User
    template_name = 'app/users_list.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            object_list = self.model.objects.filter(username__icontains=query)

        else:
            object_list = self.model.objects.all()
        return object_list
>>>>>>> 8a160e2172e923d5b725aa7141db304c62b718a6
