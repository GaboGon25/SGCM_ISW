from django.urls import path
from . import views



urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-home/', views.admin_home, name='admin_home'),
    path('medico-home/', views.medico_home, name='medico_home'),
    path('paciente-home/', views.paciente_home, name='paciente_home'),
]