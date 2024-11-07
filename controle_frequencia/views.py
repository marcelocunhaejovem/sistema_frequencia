# controle_frequencia/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm

@login_required
def home(request):
    return render(request, 'controle_frequencia/home.html')

@login_required
def turmas(request):
    # Lógica para exibir a lista de turmas (adicione a lógica conforme necessário)
    return render(request, 'controle_frequencia/turmas.html')

@login_required
def frequencia(request):
    # Lógica para exibir a frequência (adicione a lógica conforme necessário)
    return render(request, 'controle_frequencia/frequencia.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Autentica o usuário automaticamente após o registro
            return redirect('home')  # Redireciona para a página inicial após o registro
    else:
        form = RegistroForm()
    return render(request, 'controle_frequencia/registro.html', {'form': form})
