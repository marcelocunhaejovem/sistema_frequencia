"""
WSGI config for frequencia project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

#import os

#from django.core.wsgi import get_wsgi_application

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frequencia.settings")

#application = get_wsgi_application()

import os
import sys

# Adicione o caminho do seu projeto
path = '/home/seu_usuario/sistema_frequencia'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'frequencia.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

