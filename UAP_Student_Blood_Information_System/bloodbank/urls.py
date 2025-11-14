from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from UAP_Student_Blood_Information_System.bloodbank import views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    

    path('logout/', views.custom_logout, name='logout'),

    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/toggle-availability/', views.toggle_availability, name='toggle_availability'),
    path('donors/', views.donor_list, name='donor_list'),
    path('request-blood/', views.request_blood, name='request_blood'),
    path('request-history/', views.request_history, name='request_history'),
    path('accept-request/<int:request_id>/', views.accept_request, name='accept_request'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/count/', views.notification_count, name='notification_count'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
]
    
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)