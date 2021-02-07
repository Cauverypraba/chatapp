"""chatapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path
# from django.contrib.auth.views import LoginView
# from django.contrib.auth import views as auth_views
from . import views

app_name = 'real_chat'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('indexPage', views.indexPage, name = 'indexpage'),
    path('login',views.login,name='login'),
    #path('base', views.base, name = 'base'),
    #path('<str:room_name>/', views.room, name = 'room'),
    path('register', views.register, name = 'register'),
    path('homePage', views.homePage, name='home'),
    path('signupPage/', views.signupPage, name = 'signup'),
    path('password_reset', views.password_reset, name = 'reset_password')
    #path('logout', views.logout, name = 'logout'),
]
