# controle_frequencia/signals.py

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Turma, Estudante, Professor, Frequencia  # Certifique-se de que o modelo "Professor" está correto

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    # Criar o grupo Administrador
    admin_group, created = Group.objects.get_or_create(name='Administrador')
    if created:
        # Atribuir todas as permissões de cada modelo ao grupo Administrador
        for model in [Turma, Estudante, Professor, Frequencia]:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            admin_group.permissions.add(*permissions)

    # Criar o grupo Usuário Regular
    user_group, created = Group.objects.get_or_create(name='Usuário Regular')
    if created:
        # Atribuir apenas permissões de visualização para Usuário Regular
        for model in [Estudante, Frequencia]:
            content_type = ContentType.objects.get_for_model(model)
            view_permission = Permission.objects.filter(content_type=content_type, codename__startswith='view')
            user_group.permissions.add(*view_permission)
