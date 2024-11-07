# controle_frequencia/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm

@login_required
def home(request):
    return render(request, 'controle_frequencia/home.html')

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

@login_required
def frequencia(request):
    # Exemplo de conteúdo para a página de frequência
    return render(request, 'controle_frequencia/frequencia.html')
