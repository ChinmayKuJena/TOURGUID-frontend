from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('login/', views.login_view, name='login'),
    path('login_success/', views.login_success, name='login_success'),
    path('logout/', views.logout, name='logout'),  # Add the logout URL pattern
    path('user-details/', views.get_user_details, name='user_details'),


]
