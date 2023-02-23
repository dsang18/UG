"""Uttam_Glass URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from uttam_app import views
urlpatterns = [
    path('',views.LoginPage, name="Login"),
    path('<int:id>/home/', views.Home, name="Home"),
    path('<int:id>/delete-user/<int:id2>/', views.delete_user, name="confirm_delete_user"),
    path('<int:id>/delete-client/<int:id2>/', views.delete_client, name="confirm_delete_client"),
    path('<int:id>/add-user/', views.addUser, name="Add User"),
    path('<int:id>/authorize/', views.authorizeUsers, name="Authorize Users"),
    path('<int:id>/add-new-client/', views.add_new_client, name="Add New Client"),
    path('<int:id>/client-<int:id2>/', views.show_client_details, name="Show Client Details"),
    path('<int:id>/client-<int:id2>-summary/', views.show_summary, name="Show Client summary"),
    
]
