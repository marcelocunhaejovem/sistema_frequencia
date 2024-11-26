import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, UploadTurmaForm
from .models import (
    Turma,
    Estudante,
    UnidadeEnsino,
    Curso,
    InstituicaoEnsino,
    TipoCurso,
    EixoTecnologico,
    Programa,
    Matricula
)
from django.http import HttpResponse
from django.contrib.auth.models import User
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
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'controle_frequencia/registro.html', {'form': form})

@login_required
def upload_turma(request):
    if request.method == 'POST':
        form = UploadTurmaForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = request.FILES['arquivo']
            try:
                if arquivo.name.endswith('.csv'):
                    dados = pd.read_csv(arquivo, encoding='utf-8')
                elif arquivo.name.endswith('.xlsx'):
                    dados = pd.read_excel(arquivo)
                else:
                    messages.error(request, "Formato de arquivo não suportado. Use CSV ou XLSX.")
                    return redirect('upload_turma')

                for _, linha in dados.iterrows():
                    try:
                        programa, _ = Programa.objects.get_or_create(nome=linha['PROGRAMA'])
                        instituicao, _ = InstituicaoEnsino.objects.get_or_create(
                            nome=linha['INSTITUIÇÃO DE ENSINO'],
                            defaults={
                                'uf': linha['UF'],
                                'municipio': linha['MUNICÍPIO']
                            }
                        )
                        unidade, _ = UnidadeEnsino.objects.get_or_create(
                            codigo=linha['CÓDIGO DA UNIDADE DE ENSINO'],
                            defaults={
                                'nome': linha['NOME DA UNIDADE DE ENSINO'],
                                'instituicao': instituicao,
                                'codigo_remota': linha.get('CÓDIGO DA UNIDADE DE ENSINO REMOTA'),
                                'nome_remota': linha.get('NOME DA UNIDADE DE ENSINO REMOTA'),
                                'nome_demandante': linha.get('NOME DA UNIDADE DEMANDANTE'),
                            }
                        )
                        eixo, _ = EixoTecnologico.objects.get_or_create(
                            codigo=linha['CÓDIGO DO EIXO TECNOLÓGICO'],
                            defaults={'nome': linha['NOME DO EIXO TECNOLÓGICO']}
                        )
                        tipo_curso, _ = TipoCurso.objects.get_or_create(
                            codigo=linha['CÓDIGO DO TIPO DE CURSO'],
                            defaults={'nome': linha['TIPO DE CURSO']}
                        )
                        curso, _ = Curso.objects.get_or_create(
                            codigo=linha['CÓDIGO DO CURSO'],
                            defaults={
                                'nome': linha['NOME DO CURSO'],
                                'eixo': eixo
                            }
                        )
                        turma, _ = Turma.objects.get_or_create(
                            codigo=linha['CÓDIGO DA TURMA'],
                            defaults={
                                'nome': linha['TURMA'],
                                'curso': curso,
                                'data_inicio': linha['DATA DE INÍCIO DA TURMA'],
                                'data_previsao_termino': linha['DATA PREVISÃO DE TÉRMINO'],
                                'data_expiracao_primeira_chamada': linha.get('DATA EXPIRAÇÃO PRIMEIRA CHAMADA'),
                                'data_limite_confirmacao_matricula': linha.get('DATA LIMITE PARA CONFIRMAÇÃO DA MATRÍCULA'),
                                'modalidade_ensino': linha['MODALIDADE DE ENSINO'],
                                'carga_horaria_diaria': 4  # Ajuste conforme necessário
                            }
                        )
                        estudante, _ = Estudante.objects.get_or_create(
                            cpf=linha['CPF DO ALUNO'],
                            defaults={
                                'nome': linha['NOME DO ALUNO'],
                                'nome_social': linha.get('NOME SOCIAL'),
                                'nis_pis': linha.get('NÚMERO DO NIS/PIS'),
                                'telefone': linha.get('TELEFONE DO ALUNO'),
                                'celular': linha.get('CELULAR DO ALUNO'),
                                'email': linha.get('E-MAIL DO ALUNO'),
                                'turma': turma
                            }
                        )
                        Matricula.objects.get_or_create(
                            codigo=linha['CÓDIGO MATRÍCULA'],
                            defaults={
                                'situacao': linha['SITUAÇÃO DA MATRÍCULA'],
                                'estudante': estudante,
                                'turma': turma
                            }
                        )

                    except KeyError as e:
                        messages.error(request, f"Coluna esperada não encontrada: {e}")
                        return redirect('upload_turma')
                    except Exception as e:
                        logger.error(f"Erro ao processar a linha: {e}")
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

@login_required
def lista_turmas(request):
    turmas = Turma.objects.all()

    municipios = list(UnidadeEnsino.objects.values_list('instituicao__municipio', flat=True).distinct())
    unidades_ofertantes = list(UnidadeEnsino.objects.values_list('nome', flat=True).distinct())
    cursos = list(Curso.objects.values_list('nome', flat=True).distinct())

    municipio = request.GET.get('municipio')
    unidade_ofertante = request.GET.get('unidade_ofertante')
    unidade_remota = request.GET.get('unidade_remota')
    curso = request.GET.get('curso')
    turma_nome = request.GET.get('turma')
    codigo_turma = request.GET.get('codigo_turma')
    data_inicio = request.GET.get('data_inicio')

    if municipio and municipio != "Todos":
        turmas = turmas.filter(curso__unidadeensino__instituicao__municipio__icontains=municipio)
    if unidade_ofertante and unidade_ofertante != "Todas":
        turmas = turmas.filter(curso__unidadeensino__nome__icontains=unidade_ofertante)
    if unidade_remota:
        turmas = turmas.filter(curso__unidadeensino__nome_remota__icontains=unidade_remota)
    if curso and curso != "Todos":
        turmas = turmas.filter(curso__nome__icontains=curso)
    if turma_nome:
        turmas = turmas.filter(nome__icontains=turma_nome)
    if codigo_turma:
        turmas = turmas.filter(codigo=codigo_turma)
    if data_inicio:
        turmas = turmas.filter(data_inicio=data_inicio)

    context = {
        'turmas': turmas,
        'municipios': municipios,
        'unidades_ofertantes': unidades_ofertantes,
        'cursos': cursos,
        'municipio': municipio,
        'unidade_ofertante': unidade_ofertante,
        'unidade_remota': unidade_remota,
        'curso': curso,
        'turma_nome': turma_nome,
        'codigo_turma': codigo_turma,
        'data_inicio': data_inicio,
    }
    
    return render(request, 'controle_frequencia/lista_turmas.html', context)

# Teste de log para depuração
def test_logging(request):
    logger.debug('Teste de log - nível DEBUG')
    logger.error('Teste de log - nível ERROR')
    return HttpResponse("Log testado!")
