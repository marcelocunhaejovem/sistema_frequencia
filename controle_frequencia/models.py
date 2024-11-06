# controle_frequencia/models.py

from django.db import models
from django.contrib.auth.models import User

# Modelo para Turma
class Turma(models.Model):
    nome = models.CharField(max_length=100)
    carga_horaria_diaria = models.IntegerField(default=4)  # Horas por dia

    def __str__(self):
        return self.nome

# Modelo para Estudante
class Estudante(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.usuario.username

# Modelo para Professor
class Professores(models.Model):  # Corrija o nome da classe para "Professores"
    # Defina aqui os campos do modelo
    
    nome = models.CharField(max_length=100)
    # outros campos...

    class Meta:
        verbose_name = "Professor"           # Nome singular
        verbose_name_plural = "Professores"  # Nome plural em português

# Modelo para Registro de Frequência
class Frequencia(models.Model):
    data = models.DateField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    presente = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.estudante.usuario.username} - {self.data}"
