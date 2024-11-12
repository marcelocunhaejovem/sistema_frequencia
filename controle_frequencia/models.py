from django.db import models
from django.contrib.auth.models import User

# Modelo para Programa
class Programa(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

# Modelo para Instituição de Ensino
class InstituicaoEnsino(models.Model):
    nome = models.CharField(max_length=255)
    uf = models.CharField(max_length=2)
    municipio = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nome} - {self.uf}"

# Modelo para Unidade de Ensino
class UnidadeEnsino(models.Model):
    codigo = models.CharField(max_length=50)
    nome = models.CharField(max_length=255)
    instituicao = models.ForeignKey(InstituicaoEnsino, on_delete=models.CASCADE, related_name="unidades")
    codigo_remota = models.CharField(max_length=50, null=True, blank=True)
    nome_remota = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nome

# Modelo para Tipo de Curso
class TipoCurso(models.Model):
    codigo = models.CharField(max_length=50)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

# Modelo para Eixo Tecnológico
class EixoTecnologico(models.Model):
    codigo = models.CharField(max_length=50)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

# Modelo para Curso
class Curso(models.Model):
    codigo = models.CharField(max_length=50)
    nome = models.CharField(max_length=255)
    eixo = models.ForeignKey(EixoTecnologico, on_delete=models.CASCADE, related_name="cursos")

    def __str__(self):
        return self.nome

# Modelo para Turma
class Turma(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="turmas")
    data_inicio = models.DateField()
    data_previsao_termino = models.DateField()
    data_expiracao_primeira_chamada = models.DateField(null=True, blank=True)
    data_limite_confirmacao_matricula = models.DateField(null=True, blank=True)
    modalidade_ensino = models.CharField(max_length=255)
    carga_horaria_diaria = models.IntegerField(default=4)  # Horas por dia

    def __str__(self):
        return self.nome

# Modelo para Estudante
class Estudante(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True)
    nome_social = models.CharField(max_length=255, null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True)
    nis_pis = models.CharField(max_length=11, null=True, blank=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    celular = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField()
    data_cadastro_matricula = models.DateField()

    def __str__(self):
        return self.usuario.username

# Modelo para Professor
class Professor(models.Model):
    nome = models.CharField(max_length=100)
    disciplina = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"

    def __str__(self):
        return self.nome

# Modelo para Registro de Frequência
class Frequencia(models.Model):
    data = models.DateField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    presente = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.estudante.usuario.username} - {self.data}"

# Modelo para Situação da Matrícula
class SituacaoMatricula(models.Model):
    codigo = models.CharField(max_length=50)
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao

# Modelo para Matrícula
class Matricula(models.Model):
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    codigo_matricula = models.CharField(max_length=50)
    situacao = models.ForeignKey(SituacaoMatricula, on_delete=models.CASCADE)
    nome_periodo_pactuacao = models.CharField(max_length=255)
    modalidade_demanda = models.CharField(max_length=255)
    modalidade_oferta = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.estudante.usuario.username} - {self.codigo_matricula}"

# Modelo para Período de Pactuação
class PeriodoPactuacao(models.Model):
    nome = models.CharField(max_length=255)
    modalidade_demanda = models.CharField(max_length=255)
    modalidade_oferta = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
