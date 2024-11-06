# controle_frequencia/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Autentica o usuário automaticamente após o registro
            return redirect('dashboard')  # Redireciona para o dashboard
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})
