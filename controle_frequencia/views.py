@login_required
def upload_turma(request):
    if request.method == 'POST':
        form = UploadTurmaForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = request.FILES['arquivo']
            try:
                # Ler o arquivo enviado
                if arquivo.name.endswith('.csv'):
                    dados = pd.read_csv(arquivo, encoding='utf-8')
                elif arquivo.name.endswith('.xlsx'):
                    dados = pd.read_excel(arquivo)
                else:
                    messages.error(request, "Formato de arquivo não suportado. Use CSV ou XLSX.")
                    return redirect('upload_turma')

                # Verificar as colunas necessárias
                colunas_necessarias = [
                    'PROGRAMA', 'INSTITUIÇÃO DE ENSINO', 'UF', 'MUNICÍPIO',
                    'CÓDIGO DA UNIDADE DE ENSINO', 'NOME DA UNIDADE DE ENSINO',
                    'CÓDIGO DA UNIDADE DE ENSINO REMOTA', 'NOME DA UNIDADE DE ENSINO REMOTA',
                    'CÓDIGO DO CURSO', 'NOME DO CURSO', 'CÓDIGO DA TURMA', 'TURMA',
                    'DATA DE INÍCIO DA TURMA', 'DATA PREVISÃO DE TÉRMINO',
                    'MODALIDADE DE ENSINO', 'NOME DO ALUNO', 'CPF DO ALUNO'
                ]
                colunas_arquivo = list(dados.columns)

                for coluna in colunas_necessarias:
                    if coluna not in colunas_arquivo:
                        messages.error(request, f"Coluna esperada não encontrada: '{coluna}'")
                        return redirect('upload_turma')

                # Processar os dados do arquivo
                for _, linha in dados.iterrows():
                    try:
                        # Criar ou atualizar Instituição de Ensino
                        instituicao, _ = InstituicaoEnsino.objects.get_or_create(
                            nome=linha['INSTITUIÇÃO DE ENSINO'],
                            defaults={
                                'uf': linha['UF'],
                                'municipio': linha['MUNICÍPIO']
                            }
                        )

                        # Criar ou atualizar Unidade de Ensino
                        unidade, _ = UnidadeEnsino.objects.get_or_create(
                            codigo=linha['CÓDIGO DA UNIDADE DE ENSINO'],
                            defaults={
                                'nome': linha['NOME DA UNIDADE DE ENSINO'],
                                'instituicao': instituicao,
                                'codigo_remota': linha.get('CÓDIGO DA UNIDADE DE ENSINO REMOTA', None),
                                'nome_remota': linha.get('NOME DA UNIDADE DE ENSINO REMOTA', None)
                            }
                        )

                        # Criar ou atualizar Curso
                        curso, _ = Curso.objects.get_or_create(
                            codigo=linha['CÓDIGO DO CURSO'],
                            defaults={
                                'nome': linha['NOME DO CURSO']
                            }
                        )

                        # Criar ou atualizar Turma
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

                        # Criar ou atualizar Estudante
                        estudante, _ = Estudante.objects.get_or_create(
                            cpf=linha['CPF DO ALUNO'],
                            defaults={
                                'nome': linha['NOME DO ALUNO'],
                                'turma': turma
                            }
                        )
                    except KeyError as e:
                        messages.error(request, f"Erro ao processar o arquivo: coluna não encontrada ({e})")
                        return redirect('upload_turma')
                    except Exception as e:
                        messages.error(request, f"Erro ao processar o arquivo: {e}")
                        return redirect('upload_turma')

                messages.success(request, "Dados de turmas e estudantes importados com sucesso!")
                return redirect('upload_turma')
            except Exception as e:
                logger.error(f"Erro ao processar o arquivo: {e}")
                messages.error(request, f"Erro ao processar o arquivo: {e}")
                return redirect('upload_turma')
    else:
        form = UploadTurmaForm()
    return render(request, 'controle_frequencia/upload_turma.html', {'form': form})
