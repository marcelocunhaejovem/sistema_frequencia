import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Programa, InstituicaoEnsino, UnidadeEnsino, TipoCurso, EixoTecnologico, Curso, Turma, Estudante, Matricula
from .forms import UploadTurmaForm

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
                    messages.error(request, "Formato de arquivo inválido. Use CSV ou XLSX.")
                    return redirect('upload_turma')

                for _, linha in dados.iterrows():
                    # Processar as informações de cada linha do arquivo
                    programa, _ = Programa.objects.get_or_create(nome=linha['PROGRAMA'])
                    instituicao, _ = InstituicaoEnsino.objects.get_or_create(
                        nome=linha['INSTITUIÇÃO DE ENSINO'],
                        defaults={'uf': linha['UF'], 'municipio': linha['MUNICÍPIO']}
                    )
                    unidade, _ = UnidadeEnsino.objects.get_or_create(
                        codigo=linha['CÓDIGO DA UNIDADE DE ENSINO'],
                        defaults={
                            'nome': linha['NOME DA UNIDADE DE ENSINO'],
                            'instituicao': instituicao,
                            'codigo_remota': linha['CÓDIGO DA UNIDADE DE ENSINO REMOTA'],
                            'nome_remota': linha['NOME DA UNIDADE DE ENSINO REMOTA'],
                            'nome_demandante': linha['NOME DA UNIDADE DEMANDANTE']
                        }
                    )
                    eixo, _ = EixoTecnologico.objects.get_or_create(
                        codigo=linha['CÓDIGO DO EIXO TECNOLÓGICO'],
                        defaults={'nome': linha['NOME DO EIXO TECNOLÓGICO']}
                    )
                    curso, _ = Curso.objects.get_or_create(
                        codigo=linha['CÓDIGO DO CURSO'],
                        defaults={'nome': linha['NOME DO CURSO'], 'eixo': eixo}
                    )
                    turma, _ = Turma.objects.get_or_create(
                        codigo=linha['CÓDIGO DA TURMA'],
                        defaults={
                            'nome': linha['TURMA'],
                            'curso': curso,
                            'data_inicio': linha['DATA DE INÍCIO DA TURMA'],
                            'data_previsao_termino': linha['DATA PREVISÃO DE TÉRMINO'],
                            'modalidade_ensino': linha['MODALIDADE DE ENSINO']
                        }
                    )
                    estudante, _ = Estudante.objects.get_or_create(
                        cpf=linha['CPF DO ALUNO'],
                        defaults={
                            'nome': linha['NOME DO ALUNO'],
                            'turma': turma,
                            'telefone': linha['TELEFONE DO ALUNO'],
                            'email': linha['E-MAIL DO ALUNO']
                        }
                    )

                messages.success(request, "Dados importados com sucesso!")
                return redirect('upload_turma')

            except Exception as e:
                messages.error(request, f"Erro ao processar o arquivo: {e}")
                return redirect('upload_turma')
    else:
        form = UploadTurmaForm()
    return render(request, 'controle_frequencia/upload_turma.html', {'form': form})
