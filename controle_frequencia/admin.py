from django.contrib import admin
from .models import (
    Estudante, Turma, Professor, Frequencia, 
    Programa, InstituicaoEnsino, UnidadeEnsino,
    TipoCurso, EixoTecnologico, Curso,
    Matricula, SituacaoMatricula, PeriodoPactuacao
)

# Registrando os modelos
admin.site.register(Estudante)
admin.site.register(Turma)
admin.site.register(Professor)
admin.site.register(Frequencia)
admin.site.register(Programa)
admin.site.register(InstituicaoEnsino)
admin.site.register(UnidadeEnsino)
admin.site.register(TipoCurso)
admin.site.register(EixoTecnologico)
admin.site.register(Curso)
admin.site.register(Matricula)
admin.site.register(SituacaoMatricula)
admin.site.register(PeriodoPactuacao)
