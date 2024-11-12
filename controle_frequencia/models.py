from django.db import models
from django.contrib.auth.models import User

# Modelo para Unidade de Ensino
class UnidadeEnsino(models.Model):
    codigo_unidade = models.CharField(max_length=50, unique=True)
    nome_unidade = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    codigo_unidade_remota = models.CharField(max_length=50, blank=True, null=True)
    nome_unidade_remota = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome_unidade

# Modelo para Curso
class Curso(models.Model):
    codigo_curso = models.CharField(max_length=50, unique=True)
    nome_curso = models.CharField(max_length=100)
    tipo_curso = models.CharField(max_length=50)
    codigo_eixo_tecnologico = models.CharField(max_length=50)
    nome_eixo_tecnologico = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_curso

# Modelo para Turma
class Turma(models.Model):
    codigo_turma = models.CharField(max_length=50, unique=True)
    nome_turma = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="turmas")
    data_inicio = models.DateField(null=True, blank=True)
    data_previsao_termino = models.DateField(null=True, blank=True)
    data_expiracao_primeira_chamada = models.DateField(null=True, blank=True)
    data_limite_confirmacao = models.DateField(null=True, blank=True)
    modalidade_ensino = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome_turma} ({self.codigo_turma})"

# Modelo para Instituição de Ensino
class InstituicaoEnsino(models.Model):
    nome_instituicao = models.CharField(max_length=100)
    programa = models.CharField(max_length=100)
    unidade_ensino = models.ForeignKey(UnidadeEnsino, on_delete=models.CASCADE, related_name="instituicoes")
    nome_demandante = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_instituicao

# Modelo para Estudante
class Estudante(models.Model):
    nome = models.CharField(max_length=255)
    nome_social = models.CharField(max_length=255, blank=True, null=True)
    cpf = models.CharField(max_length=11, unique=True)
    nis_pis = models.CharField(max_length=20, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    data_cadastro = models.DateField(null=True, blank=True)
    codigo_matricula = models.CharField(max_length=50)
    codigo_situacao_matricula = models.CharField(max_length=50)
    situacao_matricula = models.CharField(max_length=50)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="estudantes")

    def __str__(self):
        return f"{self.nome} ({self.cpf})"

# Modelo para Detalhes de Oferta
class Oferta(models.Model):
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name="ofertas")
    periodo_pactuacao = models.CharField(max_length=100)
    modalidade_demanda = models.CharField(max_length=100)
    modalidade_oferta = models.CharField(max_length=100)

    def __str__(self):
        return f"Oferta para {self.estudante.nome}"
