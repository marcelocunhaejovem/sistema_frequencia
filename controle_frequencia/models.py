# controle_frequencia/models.py

from django.db import models
from django.contrib.auth.models import User

# Modelo para Turma
class Turma(models.Model):
    nome = models.CharField(max_length=100)
    carga_horaria_diaria = models.IntegerField(default=4)  # Horas por dia

    def __str__(self):
        return self.nome

# Modelo para Aluno (Estudante)
class Aluno(models.Model):
    nome = models.CharField(max_length=255)
    matricula = models.CharField(max_length=50)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="alunos")

    def __str__(self):
        return f"{self.nome} ({self.matricula})"

# Modelo para Professor
class Professor(models.Model):
    nome = models.CharField(max_length=100)
    # Outros campos para o professor podem ser definidos aqui...

    class Meta:
        verbose_name = "Professor"           # Nome singular
        verbose_name_plural = "Professores"  # Nome plural em português

    def __str__(self):
        return self.nome

# Modelo para Registro de Frequência
class Frequencia(models.Model):
    data = models.DateField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    presente = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.aluno.nome} - {self.data}"
