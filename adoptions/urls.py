from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='home'),  # Home page (main_page.html)
    path('animals/', views.animal_list, name='animal_list'),  # List of animals
    path('<int:pk>/', views.animal_detail, name='animal_detail'),  # Animal details
    path('<int:pk>/apply/', views.apply_adoption, name='apply_adoption'),  # Apply for adoption
    path('login/', views.custom_login, name='login'),  # Login page
    path('logout/', views.custom_logout, name='logout'),  # Logout page
    path('register/', views.register, name='register'),  # Registration page
    path('profile/', views.profile, name='profile'),  # User profile
    path('applications/', views.application_list, name='application_list'),  # List of applications
    path('applications/<int:pk>/approve/', views.approve_application, name='approve_application'),  # Approve application
    path('applications/<int:pk>/reject/', views.reject_application, name='reject_application'),  # Reject application
    path('dashboard/', views.user_dashboard, name='user_dashboard'),  # User dashboard
    path('applications/<int:pk>/withdraw/', views.withdraw_application, name='withdraw_application'),  # Withdraw application
    path('profile/update/', views.update_profile, name='update_profile'),  # Update profile
]