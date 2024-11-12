from django.contrib import admin
from .models import (
    Estudante, Turma, Professor, Frequencia, 
    Programa, InstituicaoEnsino, UnidadeEnsino,
    TipoCurso, EixoTecnologico, Curso,
    Matricula, SituacaoMatricula, PeriodoPactuacao
)

# Configurações de exibição personalizada no admin
class EstudanteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'turma', 'cpf', 'email')
    search_fields = ('usuario__username', 'cpf', 'email')

class TurmaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'curso', 'data_inicio', 'data_previsao_termino')
    list_filter = ('curso',)
    search_fields = ('codigo', 'nome')

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'disciplina', 'email', 'telefone')
    search_fields = ('nome', 'disciplina', 'email')

class FrequenciaAdmin(admin.ModelAdmin):
    list_display = ('data', 'turma', 'estudante', 'presente')
    list_filter = ('data', 'turma')
    search_fields = ('estudante__usuario__username',)

class ProgramaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

class InstituicaoEnsinoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'uf', 'municipio')
    list_filter = ('uf',)
    search_fields = ('nome', 'municipio')

class UnidadeEnsinoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'instituicao')
    search_fields = ('codigo', 'nome', 'instituicao__nome')

class TipoCursoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome')
    search_fields = ('codigo', 'nome')

class EixoTecnologicoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome')
    search_fields = ('codigo', 'nome')

class CursoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'eixo')
    search_fields = ('codigo', 'nome', 'eixo__nome')

class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('estudante', 'codigo_matricula', 'situacao')
    search_fields = ('codigo_matricula', 'estudante__usuario__username')
    list_filter = ('situacao',)

class SituacaoMatriculaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao')
    search_fields = ('codigo', 'descricao')

class PeriodoPactuacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'modalidade_demanda', 'modalidade_oferta')
    search_fields = ('nome', 'modalidade_demanda', 'modalidade_oferta')

# Registrando os modelos no admin
admin.site.register(Estudante, EstudanteAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Frequencia, FrequenciaAdmin)
admin.site.register(Programa, ProgramaAdmin)
admin.site.register(InstituicaoEnsino, InstituicaoEnsinoAdmin)
admin.site.register(UnidadeEnsino, UnidadeEnsinoAdmin)
admin.site.register(TipoCurso, TipoCursoAdmin)
admin.site.register(EixoTecnologico, EixoTecnologicoAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Matricula, MatriculaAdmin)
admin.site.register(SituacaoMatricula, SituacaoMatriculaAdmin)
admin.site.register(PeriodoPactuacao, PeriodoPactuacaoAdmin)
