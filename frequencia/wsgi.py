import os
from django.core.wsgi import get_wsgi_application

# Defina a variável de ambiente DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frequencia.settings')

# Obtém a aplicação WSGI
application = get_wsgi_application()
