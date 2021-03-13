from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('login/', views.login_user, name='login'),
    path('login/submit', views.submit_login),
    path('logout/', views.logout_user, name='logout'),
    path('', views.home, name='home'),
    path('products/', views.produto_list, name='products'),
    path('products/<int:id>/', views.produto, name='produto'),
    path('products/register/', views.produto_register, name='produto_register'),
    path('products/register/submit', views.set_produto),
    path('products/delete/<slug:id>/', views.produto_delete),
    path('products/<int:pk>/json/', views.produto_json, name='produto_json'),
    path('estoque/entrada', views.EstoqueEntradaList.as_view(), name='estoque_entrada'),
    path('estoque/entrada/<int:id>/', views.estoque_entrada_detail, name='estoque_entrada_detail'),
    path('estoque/entrada/add/', views.estoque_entrada_add, name='estoque_entrada_add'),
    path('estoque/saida/', views.EstoqueSaidaList.as_view(), name='estoque_saida'),
    path('estoque/saida/<int:id>/', views.estoque_saida_detail, name='estoque_saida_detail'),
    path('estoque/saida/add/', views.estoque_saida_add, name='estoque_saida_add'),
]
