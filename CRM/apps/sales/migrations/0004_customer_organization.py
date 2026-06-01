import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_refactor_models'),
        ('users', '0005_user_organization_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='organization',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='customers',
                to='users.organization',
            ),
        ),
    ]
