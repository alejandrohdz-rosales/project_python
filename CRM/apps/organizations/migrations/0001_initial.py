from django.db import migrations, models


def move_organization_table(apps, schema_editor):
    connection = schema_editor.connection
    tables = connection.introspection.table_names()
    if 'users_organization' in tables:
        schema_editor.execute(
            'ALTER TABLE users_organization RENAME TO organizations_organization'
        )
    elif 'organizations_organization' not in tables:
        Organization = apps.get_model('organizations', 'Organization')
        schema_editor.create_model(Organization)


def reverse_move(apps, schema_editor):
    connection = schema_editor.connection
    tables = connection.introspection.table_names()
    if 'organizations_organization' in tables and 'users_organization' not in tables:
        schema_editor.execute(
            'ALTER TABLE organizations_organization RENAME TO users_organization'
        )


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0005_user_organization_required'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Organization',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('created_at', models.DateTimeField(auto_now_add=True)),
                        ('updated_at', models.DateTimeField(auto_now=True)),
                        ('name', models.CharField(max_length=150)),
                        ('slug', models.SlugField(unique=True)),
                        ('is_active', models.BooleanField(default=True)),
                    ],
                    options={
                        'verbose_name': 'organization',
                        'verbose_name_plural': 'organizations',
                        'ordering': ['name'],
                    },
                ),
            ],
            database_operations=[
                migrations.RunPython(move_organization_table, reverse_move),
            ],
        ),
    ]
