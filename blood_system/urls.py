from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from bloodbank import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('donors/', views.donor_list, name='donor_list'),
    path('request-blood/', views.request_blood, name='request_blood'),
]