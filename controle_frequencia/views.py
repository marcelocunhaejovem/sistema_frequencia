# controle_frequencia/views.py

import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, UploadTurmaForm
from .models import Turma, Estudante
from django.http import HttpResponse
from django.contrib.auth.models import User  # Importação para criação de usuários
import logging

logger = logging.getLogger('django')

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
            
            # Verifica o tipo do arquivo e lê os dados
            try:
                if arquivo.name.endswith('.csv'):
                    dados = pd.read_csv(arquivo, encoding='utf-8')  # ajuste de encoding se necessário
                elif arquivo.name.endswith('.xlsx'):
                    dados = pd.read_excel(arquivo)
                else:
                    messages.error(request, "Formato de arquivo não suportado. Use CSV ou XLSX.")
                    return redirect('upload_turma')

                # Processar os dados do DataFrame e criar as turmas e estudantes
                for _, linha in dados.iterrows():
                    try:
                        nome_turma = linha['TURMA']  # Nome da turma
                        codigo_turma = linha['CÓDIGO DA TURMA']  # Código único da turma
                        nome_estudante = linha['NOME DO ALUNO']  # Nome do aluno
                        cpf_estudante = linha.get('CPF DO ALUNO')  # CPF do aluno, se disponível

                        # Crie ou atualize a turma no banco de dados com base no código único
                        turma, created = Turma.objects.get_or_create(
                            codigo=codigo_turma,
                            defaults={'nome': nome_turma, 'carga_horaria_diaria': 4}
                        )
                        
                        if not created:
                            # Atualiza o nome da turma se já existe o código
                            turma.nome = nome_turma
                            turma.save()

                        # Verifica se o estudante já existe pelo CPF
                        estudante = None
                        if cpf_estudante:
                            try:
                                estudante = Estudante.objects.get(cpf=cpf_estudante)
                                estudante.turma = turma  # Atualiza a turma do estudante, se necessário
                                estudante.save()
                            except Estudante.DoesNotExist:
                                pass

                        # Se o estudante com esse CPF não existir, cria um novo usuário e estudante
                        if not estudante:
                            user, user_created = User.objects.get_or_create(username=nome_estudante)
                            Estudante.objects.get_or_create(usuario=user, defaults={'turma': turma, 'cpf': cpf_estudante})

                    except KeyError as e:
                        messages.error(request, f"Coluna esperada não encontrada: {e}")
                        return redirect('upload_turma')
                    except Exception as e:
                        messages.error(request, f"Erro ao processar a linha: {e}")
                        return redirect('upload_turma')

                messages.success(request, "Turmas e estudantes importados com sucesso!")
                return redirect('upload_turma')
            except Exception as e:
                logger.error(f"Erro ao processar o arquivo: {e}")
                messages.error(request, f"Erro ao processar o arquivo: {e}")
                return redirect('upload_turma')
    else:
        form = UploadTurmaForm()
    
    return render(request, 'controle_frequencia/upload_turma.html', {'form': form})

# Teste de log para depuração
def test_logging(request):
    logger.debug('Teste de log - nível DEBUG')
    logger.error('Teste de log - nível ERROR')
    return HttpResponse("Log testado!")
