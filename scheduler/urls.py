from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('book/<int:service_id>/', views.book_appointment, name='book_appointment'),
    path('create_service/', views.create_service, name='create_service'),
    path('add-service/', views.add_service, name='add_service'),
]
