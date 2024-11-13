# frequencia/urls.py

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from controle_frequencia import views as controle_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='controle_frequencia/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', controle_views.home, name='home'),
    path('home/', controle_views.home, name='home'),
    path('registro/', controle_views.registro, name='registro'),

    # URLs para redefinição de senha
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # URL para upload de turmas
    path('upload_turma/', controle_views.upload_turma, name='upload_turma'),

    # URL para visualização de turmas
    path('turmas/', controle_views.turmas, name='turmas'),
]
