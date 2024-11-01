from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from controle_frequencia import views as controle_views  # Importa views do app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', controle_views.home, name='home'),  # URL para a página "home"
]
