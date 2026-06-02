from django.db import migrations


class Migration(migrations.Migration):
    """Quita Organization del estado de users; el modelo vive en apps.organizations."""

    dependencies = [
        ('organizations', '0001_initial'),
        ('users', '0007_user_add_organization'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(name='Organization'),
            ],
            database_operations=[],
        ),
    ]
