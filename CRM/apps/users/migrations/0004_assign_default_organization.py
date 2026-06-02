from django.db import migrations


def assign_default_organization(apps, schema_editor):
    Organization = apps.get_model('users', 'Organization')
    User = apps.get_model('users', 'User')

    org, _ = Organization.objects.get_or_create(
        slug='default',
        defaults={'name': 'Default Organization'},
    )
    User.objects.filter(organization__isnull=True).update(organization=org)


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_organization'),
    ]

    operations = [
        migrations.RunPython(assign_default_organization, migrations.RunPython.noop),
    ]
