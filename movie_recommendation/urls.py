

from django.contrib import admin
from django.urls import path, include
from recommend import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('home/', views.HomePage, name='home'),
    path('register/', views.LoginPage, name='login'),
    path('logout/', views.LogoutPage, name='logout'),
    
    
]


