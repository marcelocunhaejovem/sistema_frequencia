# controle_frequencia/views.py

import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, UploadTurmaForm
from .models import Turma

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
def upload_turma(request):
    if request.method == 'POST':
        form = UploadTurmaForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = request.FILES['arquivo']
            
            # Verifica o tipo do arquivo
            try:
                if arquivo.name.endswith('.csv'):
                    dados = pd.read_csv(arquivo)
                elif arquivo.name.endswith('.xls') or arquivo.name.endswith('.xlsx'):
                    dados = pd.read_excel(arquivo)
                else:
                    messages.error(request, "Formato de arquivo não suportado. Use CSV, XLS ou XLSX.")
                    return redirect('upload_turma')

                # Processar os dados do DataFrame e criar as turmas
                for _, linha in dados.iterrows():
                    # Exemplo de processamento (ajuste conforme as colunas do seu arquivo)
                    nome_turma = linha['nome_turma']
                    carga_horaria = linha['carga_horaria_diaria']

                    # Crie ou atualize a turma no banco de dados
                    turma, created = Turma.objects.get_or_create(
                        nome=nome_turma,
                        defaults={'carga_horaria_diaria': carga_horaria}
                    )
                    if not created:
                        turma.carga_horaria_diaria = carga_horaria
                        turma.save()

                messages.success(request, "Turmas importadas com sucesso!")
                return redirect('upload_turma')
            except Exception as e:
                messages.error(request, f"Erro ao processar o arquivo: {e}")
                return redirect('upload_turma')
    else:
        form = UploadTurmaForm()
    
    return render(request, 'controle_frequencia/upload_turma.html', {'form': form})




import logging
logger = logging.getLogger('django')

def test_logging(request):
    logger.debug('Teste de log - nível DEBUG')
    logger.error('Teste de log - nível ERROR')
    return HttpResponse("Log testado!")



