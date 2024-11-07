# Configuração de logging no settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '{asctime} {levelname} {name} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',  # Captura apenas erros e níveis superiores
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'error.log'),  # Caminho do arquivo de log
            'formatter': 'detailed',
        },
        'console': {
            'level': 'DEBUG',  # Exibe todas as mensagens no console
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG' if DEBUG else 'ERROR',  # DEBUG se DEBUG=True, ERROR caso contrário
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',  # Apenas erros de requisição HTTP
            'propagate': False,
        },
    },
}
