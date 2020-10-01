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
    
]
