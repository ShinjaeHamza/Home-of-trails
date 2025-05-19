from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from adoptions import views  # Import views from the adoptions app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='main_page'),  # Set the root URL to the main page
    path('', include('adoptions.urls')),
    path('adoptions/', include('adoptions.urls')),  # Include adoptions app URLs
    path('profile/update/', views.update_profile, name='update_profile'),  # Update profile without prefix
    path('login/', views.custom_login, name='login'),  # Custom login page
    path('logout/', views.custom_logout, name='logout'),  # Custom logout page
    path('register/', views.register, name='register'),  # Custom registration page
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)