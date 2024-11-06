from django.apps import AppConfig

class ControleFrequenciaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'controle_frequencia'

    def ready(self):
        import controle_frequencia.signals  # Importa os sinais para registrar grupos e permissões

