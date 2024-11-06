from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from controle_frequencia import views as controle_views  # Importa views do app
from .views import registro

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='controle_frequencia/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', controle_views.home, name='home'),  # URL para a página inicial
    path('home/', controle_views.home, name='home'),  # URL para a página "home"
    path('registro/', registro, name='registro'),
]

