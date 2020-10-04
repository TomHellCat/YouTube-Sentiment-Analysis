"""twitter URL Configuration

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
from .import views
from django.urls import path

app_name = 'base'

urlpatterns = [
    path('', views.login_request,name='user_login'),
    path('register/', views.register, name='register'),
    path('howitworks/', views.how, name='howitworks'),
    path('home/', views.home, name='home'),
    path('header/', views.header, name='header'),
    path('logout/', views.logout_request, name='logout'),
    path('home/<str:pk>/', views.deleteTask, name="delete"),
    path('thing/<str:pk>',views.thing, name="thing"),
    path('project2/<str:pk>/', views.pro, name="pro"),
    path('createproject/', views.createProject, name="createproject"),
]
