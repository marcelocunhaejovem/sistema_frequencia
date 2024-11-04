from django.contrib import admin
from .models import Estudante, Turma, Professor, Frequencia

# Registrando os modelos
admin.site.register(Estudante)
admin.site.register(Turma)
admin.site.register(Professor)
admin.site.register(Frequencia)
