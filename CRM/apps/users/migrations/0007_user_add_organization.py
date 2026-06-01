import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Actualiza el FK de User para apuntar al modelo en apps.organizations."""

    dependencies = [
        ('organizations', '0001_initial'),
        ('users', '0005_user_organization_required'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='organization',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='users',
                to='organizations.organization',
            ),
        ),
    ]
