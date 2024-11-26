from django.db import models

# Programa
class Programa(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

# Instituição de Ensino
class InstituicaoEnsino(models.Model):
    nome = models.CharField(max_length=255)
    uf = models.CharField(max_length=2)
    municipio = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

# Unidade de Ensino
class UnidadeEnsino(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=255)
    instituicao = models.ForeignKey(InstituicaoEnsino, on_delete=models.CASCADE)
    codigo_remota = models.CharField(max_length=50, blank=True, null=True)
    nome_remota = models.CharField(max_length=255, blank=True, null=True)
    nome_demandante = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome

# Tipo de Curso
class TipoCurso(models.Model):
    codigo = models.CharField(max_length=50)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

# Eixo Tecnológico
class EixoTecnologico(models.Model):
    codigo = models.CharField(max_length=50)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

# Curso
class Curso(models.Model):
    codigo = models.CharField(max_length=50)
    nome = models.CharField(max_length=255)
    eixo = models.ForeignKey(EixoTecnologico, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

# Turma
class Turma(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=255)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_previsao_termino = models.DateField()
    data_expiracao_primeira_chamada = models.DateField(blank=True, null=True)
    data_limite_confirmacao_matricula = models.DateField(blank=True, null=True)
    modalidade_ensino = models.CharField(max_length=255)
    carga_horaria_diaria = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nome} ({self.codigo})"

# Estudante
class Estudante(models.Model):
    nome = models.CharField(max_length=255)
    nome_social = models.CharField(max_length=255, blank=True, null=True)
    cpf = models.CharField(max_length=14, unique=True)
    nis_pis = models.CharField(max_length=20, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

# Matrícula
class Matricula(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    situacao = models.CharField(max_length=255)
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    def __str__(self):
        return self.codigo
