"""
Alinea la BD si Organization se creó antes en la app users.

Uso (desde la carpeta CRM):
  python manage.py sync_organization_table
  python manage.py migrate organizations
"""

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Renombra users_organization a organizations_organization si aplica.'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            tables = connection.introspection.table_names()
            if 'users_organization' in tables:
                cursor.execute(
                    'ALTER TABLE users_organization '
                    'RENAME TO organizations_organization'
                )
                self.stdout.write(self.style.SUCCESS(
                    'Tabla renombrada: users_organization → organizations_organization'
                ))
            elif 'organizations_organization' in tables:
                self.stdout.write('La tabla organizations_organization ya existe.')
            else:
                self.stdout.write(self.style.WARNING(
                    'No hay tabla de organizaciones. Ejecuta: python manage.py migrate organizations'
                ))
